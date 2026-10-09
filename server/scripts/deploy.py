#!/usr/bin/env python3
"""Cloud Run 배포 (모든 서비스 공통). 서비스별 값은 server/service.json에서 읽는다.

  python server/scripts/deploy.py setup            # Artifact Registry·정리 정책·서비스 계정·Secret 권한·버킷
  python server/scripts/deploy.py build [--tag T]  # allowlist context로 Cloud Build, digest 기록
  python server/scripts/deploy.py deploy           # 기록된 digest로 배포, Host/URL 환경값 확정
  python server/scripts/deploy.py smoke            # /health, /ready 확인
  python server/scripts/deploy.py status

결과(image, digest, url, revision)는 server/deploy-state.json에 기록한다(비밀값 없음).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standard_tools import REPO_ROOT, SERVER, gcloud, load_service, version  # noqa: E402

STATE = SERVER / "deploy-state.json"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".env", ".env.*", ".DS_Store", "tests", "*.log")
CLEANUP_POLICY = [
    {"name": "keep-recent", "action": {"type": "Keep"}, "mostRecentVersions": {"keepCount": 3}},
    {"name": "delete-rest", "action": {"type": "Delete"}, "condition": {"tagState": "ANY"}},
]


def load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.is_file() else {}


def save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def project_args(config: dict) -> list[str]:
    return ["--project", config["gcp"]["project"]]


def image_base(config: dict) -> str:
    gcp = config["gcp"]
    return f"{gcp['region']}-docker.pkg.dev/{gcp['project']}/{gcp['repository']}/server"


def setup(config: dict) -> None:
    gcp, project = config["gcp"], project_args(config)
    if gcloud("artifacts", "repositories", "describe", gcp["repository"], "--location", gcp["region"],
              *project, "--format=value(name)", check=False) is None:
        gcloud("artifacts", "repositories", "create", gcp["repository"], "--location", gcp["region"],
               "--repository-format=docker", *project)
    with tempfile.TemporaryDirectory() as directory:
        policy = Path(directory) / "policy.json"
        policy.write_text(json.dumps(CLEANUP_POLICY), encoding="utf-8")
        gcloud("artifacts", "repositories", "set-cleanup-policies", gcp["repository"], "--location", gcp["region"],
               f"--policy={policy}", "--no-dry-run", *project)
    account = gcp["service_account"]
    for bucket in gcp.get("buckets", []):
        setup_bucket(config, bucket, account)
    if gcloud("iam", "service-accounts", "describe", account, *project, "--format=value(email)", check=False) is None:
        gcloud("iam", "service-accounts", "create", account.split("@")[0], f"--display-name={config['service']} runtime", *project)
    for reference in config["run"].get("secrets", {}).values():
        secret = reference.split(":")[0]
        gcloud("secrets", "add-iam-policy-binding", secret, f"--member=serviceAccount:{account}",
               "--role=roles/secretmanager.secretAccessor", *project, "--format=none")
    print(json.dumps({"status": "ok", "repository": gcp["repository"], "region": gcp["region"]}))


def setup_bucket(config: dict, bucket: dict, account: str) -> None:
    """Private regional bucket with optional lifecycle and a role for the runtime account."""
    gcp, project = config["gcp"], project_args(config)
    url = f"gs://{bucket['name']}"
    if gcloud("storage", "buckets", "describe", url, *project, "--format=value(name)", check=False) is None:
        gcloud("storage", "buckets", "create", url, "--location", gcp["region"], "--uniform-bucket-level-access",
               "--public-access-prevention", *project, "--format=none")
    if bucket.get("lifecycle"):
        gcloud("storage", "buckets", "update", url, f"--lifecycle-file={REPO_ROOT / bucket['lifecycle']}", *project, "--format=none")
    gcloud("storage", "buckets", "add-iam-policy-binding", url, f"--member=serviceAccount:{account}",
           f"--role={bucket.get('role', 'roles/storage.objectUser')}", *project, "--format=none")


def build(config: dict, tag: str | None) -> None:
    tag = tag or f"{version()}-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"
    image = f"{image_base(config)}:{tag}"
    with tempfile.TemporaryDirectory(prefix="build-") as directory:
        stage = Path(directory)
        for relative in config["build"]["context"]:
            source = REPO_ROOT / relative
            target = stage / relative
            if source.is_dir():
                shutil.copytree(source, target, ignore=IGNORE)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
        shutil.copyfile(REPO_ROOT / config["build"]["dockerfile"], stage / "Dockerfile")
        (stage / "VERSION").write_text(version() + "\n", encoding="utf-8")
        gcloud("builds", "submit", str(stage), "--tag", image, *project_args(config), "--format=none")
    digest = gcloud("artifacts", "docker", "images", "describe", image, *project_args(config),
                    "--format=value(image_summary.digest)")
    state = load_state()
    state.update(version=version(), image=image, digest=digest, built_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    save_state(state)
    print(json.dumps({"status": "built", "image": image, "digest": digest}))


def describe(config: dict) -> dict | None:
    raw = gcloud("run", "services", "describe", config["service"], "--region", config["gcp"]["region"],
                 *project_args(config), "--format=json", check=False)
    return json.loads(raw) if raw else None


def service_urls(service: dict) -> list[str]:
    urls = [service["status"]["url"]]
    extra = service["metadata"].get("annotations", {}).get("run.googleapis.com/urls")
    if extra:
        urls += [url for url in json.loads(extra) if url not in urls]
    return urls


def environment(config: dict, urls: list[str]) -> dict[str, str]:
    run = config["run"]
    hosts = ",".join(urlsplit(url).hostname for url in urls) if urls else "localhost"
    values = {"MCP_ALLOWED_HOSTS": hosts, "MCP_ALLOWED_ORIGINS": run.get("allowed_origins", ""),
              "SERVICE_VERSION": version()}
    for key, value in run.get("env", {}).items():
        values[key] = str(value).replace("{service_url}", urls[0] if urls else "")
    return values


def env_file(directory: str, values: dict[str, str]) -> str:
    """Pass env vars through a file: gcloud on Windows runs via cmd.exe, which mangles | ^ & in arguments."""
    path = Path(directory) / "env.json"
    path.write_text(json.dumps(values, ensure_ascii=False), encoding="utf-8")
    return f"--env-vars-file={path}"


def deploy(config: dict) -> None:
    state = load_state()
    if not state.get("digest"):
        raise SystemExit("먼저 build를 실행한다.")
    run, gcp = config["run"], config["gcp"]
    current = describe(config)
    urls = service_urls(current) if current else []
    secrets = ",".join(f"{key}={value}" for key, value in run.get("secrets", {}).items())
    image = state["image"].rsplit(":", 1)[0] + "@" + state["digest"]
    with tempfile.TemporaryDirectory() as directory:
        args = ["run", "deploy", config["service"], "--image", image, "--region", gcp["region"],
                "--service-account", gcp["service_account"], "--allow-unauthenticated", "--port=8080",
                f"--memory={run['memory']}", f"--cpu={run['cpu']}", "--min-instances=0",
                f"--max-instances={run['max_instances']}", f"--concurrency={run['concurrency']}",
                f"--timeout={run['timeout']}", "--cpu-throttling", env_file(directory, environment(config, urls)),
                *project_args(config), "--format=none"]
        if run.get("startup_cpu_boost", True):
            args.append("--cpu-boost")
        if secrets:
            args.append(f"--set-secrets={secrets}")
        gcloud(*args)
        service = describe(config)
        final_urls = service_urls(service)
        if final_urls != urls:
            gcloud("run", "services", "update", config["service"], "--region", gcp["region"],
                   env_file(directory, environment(config, final_urls)), *project_args(config), "--format=none")
            service = describe(config)
    state.update(service=config["service"], region=gcp["region"], service_version=version(), url=service["status"]["url"], urls=final_urls,
                 revision=service["status"]["latestReadyRevisionName"],
                 deployed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    save_state(state)
    print(json.dumps({"status": "deployed", "url": state["url"], "revision": state["revision"]}))


def smoke(config: dict) -> int:
    state = load_state()
    results = {}
    for path in ("/health", "/ready"):
        try:
            with urllib.request.urlopen(state["url"].rstrip("/") + path, timeout=60) as response:
                results[path] = response.status
        except Exception as exc:  # report every endpoint
            results[path] = getattr(exc, "code", str(exc))
    print(json.dumps({"url": state["url"], "results": results}))
    return 0 if all(value == 200 for value in results.values()) else 1


def main() -> int:
    config = load_service()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=["setup", "build", "deploy", "smoke", "status"])
    parser.add_argument("--tag")
    args = parser.parse_args()
    if args.action == "setup":
        setup(config)
    elif args.action == "build":
        build(config, args.tag)
    elif args.action == "deploy":
        deploy(config)
    elif args.action == "smoke":
        return smoke(config)
    else:
        service = describe(config)
        print(json.dumps({"state": load_state(), "deployed": bool(service),
                          "revision": service and service["status"].get("latestReadyRevisionName")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
