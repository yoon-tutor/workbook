"""Public tool registration: a thin adapter over ``service`` (STANDARD.md 6.1)."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Annotated, Any, Literal

from fastmcp import FastMCP
from pydantic import Field

from . import service

READ = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
WRITE = {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True}
RELEASE_ID = Annotated[str, Field(pattern=r"^[0-9a-f]{32}$", description="Release ID returned by workbook_prepare_release.")]
IMAGE_NAME = Annotated[str, Field(min_length=1, max_length=200, description="Exact name from data.reviewImages of workbook_prepare_release.")]
PUBLIC_NAME = Literal["문제.html", "문제.pdf", "해설.html", "해설.pdf"]
CANONICAL = Annotated[dict[str, Any], Field(description="Canonical workbook object (workbooks/<name>/content.json).")]
PACKET = Annotated[dict[str, Any], Field(description="Semantic authoring packet object (.build/authoring/<name>/authoring.json).")]
UPDATE = Annotated[dict[str, Any], Field(description="Update definition object whose id/scope match canonical.updateState.")]
Result = dict[str, Any]


def register_tools(mcp: FastMCP, owner_provider: Callable[[], str]) -> None:
    @mcp.tool(annotations=READ)
    async def workbook_get_guidance() -> Result:
        """Get authoring rules, schemas, workflow and review policy in data. Call first; then workbook_authoring_verify."""
        return await asyncio.to_thread(service.guidance)

    @mcp.tool(annotations=READ)
    async def workbook_validate_canonical(canonical: CANONICAL) -> Result:
        """Validate a canonical workbook without storing anything. Returns ok or invalid_input with field violations."""
        return await asyncio.to_thread(service.validate_canonical, canonical)

    @mcp.tool(annotations=READ)
    async def workbook_authoring_verify(packet: PACKET) -> Result:
        """Verify a new semantic authoring packet. Returns ok with workbookId and sentence count, or invalid_input."""
        return await asyncio.to_thread(service.authoring_verify, packet)

    @mcp.tool(annotations=READ)
    async def workbook_authoring_expand(packet: PACKET) -> Result:
        """Verify and expand a packet; the canonical arrives as artifact content.json (save it with --into workbooks/<name>)."""
        return await asyncio.to_thread(service.authoring_expand, packet)

    @mcp.tool(annotations=READ)
    async def workbook_compile(canonical: CANONICAL, edition: Literal["student", "answer"]) -> Result:
        """Compile intermediate page IR for one edition (inspection only; never a release)."""
        return await asyncio.to_thread(service.compile_edition, canonical, edition)

    @mcp.tool(annotations=WRITE)
    async def workbook_prepare_release(
        canonical: CANONICAL, update: UPDATE,
        output_base: Annotated[str | None, Field(max_length=200, pattern=r"^[0-9A-Za-z가-힣_-]+$",
                                                 description="Optional public output folder base name.")] = None,
    ) -> Result:
        """Run browser/PDF QA and store a private release. Returns needs_review with reviewImages; review every image next."""
        owner = owner_provider()
        return await asyncio.to_thread(service.prepare_release, canonical, update, output_base, owner_id=owner)

    @mcp.tool(annotations={**WRITE, "idempotentHint": True})
    async def workbook_review_image(release_id: RELEASE_ID, image_name: IMAGE_NAME) -> Result:
        """Deliver one review PNG as an artifact bundle and record it as opened. Save with --into and open the file."""
        owner = owner_provider()
        return await asyncio.to_thread(service.review_image, release_id=release_id, image_name=image_name, owner_id=owner)

    @mcp.tool(annotations={**WRITE, "idempotentHint": True})
    async def workbook_publish_release(
        release_id: RELEASE_ID,
        reviewer: Annotated[str, Field(min_length=1, max_length=200, description="Name of the reviewer who inspected all images.")],
        notes: Annotated[str, Field(min_length=1, max_length=8000, description="Actual visual review findings.")],
    ) -> Result:
        """Publish after every review image was opened. Returns done with the four public files as an artifact bundle."""
        owner = owner_provider()
        return await asyncio.to_thread(service.publish_release, release_id=release_id, reviewer=reviewer,
                                       notes=notes, owner_id=owner)

    @mcp.tool(annotations=READ)
    async def workbook_get_artifacts(release_id: RELEASE_ID) -> Result:
        """Return the four published files of an owned release as a bundle with fresh one-day links."""
        owner = owner_provider()
        return await asyncio.to_thread(service.get_artifacts, release_id=release_id, owner_id=owner)

    @mcp.tool(annotations=READ)
    async def workbook_read_artifact(release_id: RELEASE_ID, name: PUBLIC_NAME) -> Result:
        """Return one published file of an owned release inline (base64/utf-8) as an artifact bundle."""
        owner = owner_provider()
        return await asyncio.to_thread(service.read_artifact, release_id=release_id, name=name, owner_id=owner)
