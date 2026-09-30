"""Authenticated stateless MCP; execution packages contain no workspace data."""
import os
from fastmcp import FastMCP
from fastmcp.server.auth import StaticTokenVerifier
from .bundle import ROOT, runtime_bundle
from . import direct_release


def create_server(token=None):
    token = token or os.environ.get('WORKBOOK_MCP_API_TOKEN', '').strip()
    if not token:
        raise RuntimeError('WORKBOOK_MCP_API_TOKEN is required')
    mcp = FastMCP('Workbook Runtime', auth=StaticTokenVerifier(tokens={
        token: {'client_id': 'workbook-local', 'scopes': []}}))
    bundle = runtime_bundle()

    @mcp.tool
    def workbook_get_guidance() -> dict:
        """Get authoritative rules and the current immutable runtime identity."""
        return {'runtimeId': bundle['runtimeId'], 'directApiVersion': 2,
                'execution': 'direct-mcp-authoring-and-release',
                'publicFiles': ['문제.html', '문제.pdf', '해설.html', '해설.pdf'],
                'workflow': ['authoring-verify', 'authoring-expand', 'validate',
                             'prepare-release', 'review-every-image', 'publish-release', 'download-artifacts'],
                'rules': {name: (ROOT / name).read_text(encoding='utf-8') for name in (
                    'docs/authoring-pipeline.md', 'docs/semantic-rubric.md',
                    'config/workbook-spec.json', 'schemas/canonical-workbook.schema.json')},
                'stage9Authoring': {
                    'choiceLabels': '선택지 표시는 위에서부터 A, B, C 순서다. 섞을 내용은 blocks에 그 순서로 넣는다.',
                    'coverage': '매 문항의 지문 전체 문장을 이동 가능한 blocks에 빠짐없이 한 번씩 넣는다.',
                    'answerKey': 'answerOrder는 원문을 복원하는 선택지 순서다. 이미 A-B-C로 놓인 무의미한 배열 문제를 만들지 않는다.',
                    'questionSet': '여러 문항은 가능한 범위에서 정답 순열이 서로 다르게 되도록 설계한다.',
                    'verification': '새 packet의 authoring verify와 expand에서 위반을 거부하며 기존 공개본은 변경하지 않는다.',
                },
                'note': 'PDF prepare runs automated QA; inspect every review image before publish.'}

    @mcp.tool
    def workbook_get_runtime(runtime_id: str) -> dict:
        """Return an exact pinned script package, never silently upgrade a client."""
        if runtime_id != bundle['runtimeId']:
            raise ValueError('Requested runtime is unavailable; review a new lock explicitly')
        return bundle

    @mcp.tool
    def workbook_validate_canonical(canonical: dict) -> dict:
        """Validate an explicitly supplied canonical using unchanged server rules."""
        import json
        from workbook_engine.schema_gate import validate_schema
        from workbook_engine.validator import load_spec, validate_canonical
        issues = validate_schema(canonical, json.loads(
            (ROOT / 'schemas/canonical-workbook.schema.json').read_text(encoding='utf-8')))
        if issues:
            return {'status': 'invalid_input', 'issues': [i.format() for i in issues]}
        issues = validate_canonical(canonical, load_spec())
        return {'status': 'invalid_input' if any(i.severity == 'error' for i in issues) else 'passed',
                'issues': [i.format() for i in issues]}

    @mcp.tool
    def workbook_authoring_verify(packet: dict) -> dict:
        """Verify a new semantic authoring packet with the server's current policy."""
        from workbook_authoring import expand_packet, verify_new_packet_policy
        verify_new_packet_policy(packet)
        canonical = expand_packet(packet)
        return {'status': 'passed', 'workbookId': canonical['workbookId'],
                'sentences': len(canonical['sentences']), 'runtimeId': bundle['runtimeId']}

    @mcp.tool
    def workbook_authoring_expand(packet: dict) -> dict:
        """Verify a new packet and return its canonical, without writing any workspace file."""
        from workbook_authoring import expand_packet, verify_new_packet_policy
        verify_new_packet_policy(packet)
        return {'status': 'passed', 'runtimeId': bundle['runtimeId'],
                'canonical': expand_packet(packet)}

    @mcp.tool
    def workbook_compile(canonical: dict, edition: str) -> dict:
        """Compile page IR using the original engine; this is not a reviewed release."""
        from workbook_engine.compiler import compile_workbook
        return compile_workbook(canonical, edition)

    @mcp.tool
    def workbook_prepare_release(canonical: dict, update: dict, output_base: str | None = None) -> dict:
        """Run the original browser/PDF QA and persist a private release for visual review."""
        return direct_release.prepare(canonical, update, output_base)

    @mcp.tool
    def workbook_review_image(release_id: str, image_name: str):
        """Show one student or answer PDF review image before publication."""
        return direct_release.review_image(release_id, image_name)

    @mcp.tool
    def workbook_publish_release(release_id: str, reviewer: str, notes: str) -> dict:
        """Publish only after every generated review image was opened and inspected."""
        return direct_release.publish(release_id, reviewer, notes)

    @mcp.tool
    def workbook_get_artifacts(release_id: str) -> dict:
        """Refresh private, one-day download links for a published four-file release."""
        return direct_release.artifacts(release_id)

    @mcp.tool
    def workbook_read_artifact(release_id: str, name: str):
        """Return a published student or answer PDF as an MCP file resource."""
        return direct_release.read_artifact(release_id, name)

    mcp.custom_route('/artifact/{release_id}/{name}', methods=['GET'])(direct_release.artifact_route)

    return mcp


if __name__ == '__main__':
    create_server().run(transport='http', host=os.environ.get('HOST', '127.0.0.1'),
                        port=int(os.environ.get('PORT', '8080')),
                        stateless_http=True, json_response=True, show_banner=False)
