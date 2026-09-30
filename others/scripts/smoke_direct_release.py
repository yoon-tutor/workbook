"""Run the approved chocolate example against a tagged direct-MCP candidate.

The API token is read only from the package-local .env by scripts.run.configuration.
This utility never prints the token or signed artifact URLs.
"""

from __future__ import annotations

import argparse
import base64
from hashlib import sha256
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run import Client, configuration


def tool(client: Client, name: str, arguments: dict) -> dict:
    result = client.rpc("tools/call", {"name": name, "arguments": arguments}, 2)
    if result.get("isError"):
        message = "\n".join(item.get("text", "") for item in result.get("content", []) if item.get("type") == "text")
        raise RuntimeError(f"{name} failed: {message[:2000]}")
    if "structuredContent" in result:
        return result["structuredContent"]
    return json.loads(next(item["text"] for item in result["content"] if item["type"] == "text"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "review", "publish", "verify"))
    parser.add_argument("--url", required=True)
    parser.add_argument("--state", type=Path, required=True)
    args = parser.parse_args()
    _, token = configuration()
    client = Client(args.url, token)
    original_open = client.opener.open
    client.opener.open = lambda request, timeout=60: original_open(request, timeout=900)
    state_path = args.state.resolve()
    state_path.parent.mkdir(parents=True, exist_ok=True)

    if args.phase == "prepare":
        canonical = json.loads((ROOT / "workbooks/chocolate/content.json").read_text(encoding="utf-8"))
        update = json.loads((ROOT / "updates/U-20260710-001.json").read_text(encoding="utf-8"))
        result = tool(client, "workbook_prepare_release", {
            "canonical": canonical, "update": update, "output_base": "chocolate-smoke",
        })
        if result.get("status") != "awaiting-visual-review":
            raise RuntimeError("Prepare did not reach visual review")
        state_path.write_text(json.dumps({
            "releaseId": result["releaseId"], "reviewImages": result["reviewImages"],
            "pageCount": result["pageCount"], "qa": result["qa"],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"phase": "prepared", "releaseId": result["releaseId"],
                          "pageCount": result["pageCount"],
                          "reviewImageCount": len(result["reviewImages"])}, ensure_ascii=False))
        return

    state = json.loads(state_path.read_text(encoding="utf-8"))
    release_id = state["releaseId"]
    if args.phase == "verify":
        guidance = tool(client, "workbook_get_guidance", {})
        lock = json.loads((ROOT / "runtime.lock.json").read_text(encoding="utf-8"))
        if guidance.get("runtimeId") != lock["runtimeId"] or guidance.get("directApiVersion") != 2:
            raise RuntimeError("Operating MCP runtime or direct API version mismatch")
        published = tool(client, "workbook_get_artifacts", {"release_id": release_id})
        for name, details in published["files"].items():
            with urlopen(published["downloadUrls"][name], timeout=120) as response:
                data = response.read()
            if sha256(data).hexdigest() != details["sha256"] or len(data) != details["size"]:
                raise RuntimeError("Operating artifact mismatch: " + name)
        print(json.dumps({"phase": "operating-verified", "runtimeId": lock["runtimeId"],
                          "directApiVersion": 2, "fileCount": len(published["files"])}, ensure_ascii=False))
        return
    if args.phase == "review":
        image_dir = state_path.parent / (state_path.stem + "-images")
        image_dir.mkdir(exist_ok=True)
        for image_name in state["reviewImages"]:
            response = client.rpc("tools/call", {"name": "workbook_review_image", "arguments": {
                "release_id": release_id, "image_name": image_name}}, 3)
            if response.get("isError"):
                raise RuntimeError("Review image retrieval failed")
            images = [item for item in response["content"] if item.get("type") == "image"]
            if len(images) != 1:
                raise RuntimeError("Expected one review image")
            (image_dir / image_name).write_bytes(base64.b64decode(images[0]["data"], validate=True))
        print(json.dumps({"phase": "review-images-downloaded", "count": len(state["reviewImages"]),
                          "directory": str(image_dir)}, ensure_ascii=False))
        return

    published = tool(client, "workbook_publish_release", {
        "release_id": release_id, "reviewer": "Codex",
        "notes": "학생용·해설용 전체 contact sheet와 대표 전체 페이지에서 잘림, 겹침, 정답 노출을 확인함",
    })
    if published.get("status") != "published":
        raise RuntimeError("Publish did not complete")
    output_dir = state_path.parent / (state_path.stem + "-artifacts")
    output_dir.mkdir(exist_ok=True)
    candidate_origin = urlsplit(args.url.removesuffix("/mcp"))
    for name, details in published["files"].items():
        signed = urlsplit(published["downloadUrls"][name])
        candidate_url = urlunsplit((candidate_origin.scheme, candidate_origin.netloc,
                                    signed.path, signed.query, signed.fragment))
        with urlopen(candidate_url, timeout=120) as response:
            data = response.read()
        if sha256(data).hexdigest() != details["sha256"] or len(data) != details["size"]:
            raise RuntimeError("Published artifact hash or size mismatch: " + name)
        (output_dir / name).write_bytes(data)
    print(json.dumps({"phase": "published-and-downloaded", "releaseId": release_id,
                      "fileCount": len(published["files"]), "directory": str(output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
