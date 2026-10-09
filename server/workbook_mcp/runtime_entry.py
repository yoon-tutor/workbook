"""Bind unmodified remote engine code to a local workspace in a fresh process.

Source constants stay in the verified runtime; mutable paths stay in workspace.
Portable manifest paths remain identical to the legacy engine's paths.
"""
import argparse
import os
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace

RUNTIME = Path(__file__).resolve().parents[1]


def windows_browser_support(qa):
    if os.name != 'nt':
        return
    qa.CHROME_CANDIDATES += tuple(Path(path) for path in (
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
        'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'))

    # Only the process started by the engine is terminated. Do not change QA.
    def kill_group(pid, sig):
        result = subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode:
            raise ProcessLookupError(pid)
    qa.os = SimpleNamespace(**{name: getattr(os, name) for name in dir(os)})
    qa.os.killpg = kill_group
    qa.signal = SimpleNamespace(**{name: getattr(qa.signal, name) for name in dir(qa.signal)})
    qa.signal.SIGKILL = 9


def bind_workspace(workspace):
    import workbook_engine.release as release
    import workbook_engine.qa as qa
    from workbook_engine.manifest import file_record
    workspace = workspace.resolve()
    release.ROOT = workspace
    import workbook_engine.migrate_legacy as migration
    migration.ROOT = workspace
    migration.DEFAULT_LEGACY = workspace / 'tmp/build_chocolate_reading_json.py'
    migration.DEFAULT_OUTPUT = workspace / 'workbooks/chocolate/content.json'

    def portable_record(path, *, root=None):
        path = Path(path).resolve()
        if root is not None and Path(root).resolve() == workspace and path.is_relative_to(RUNTIME):
            root = RUNTIME
        return file_record(path, root=root)

    def portable_manifest(paths, *, root=None):
        return {'files': sorted((portable_record(path, root=root) for path in paths),
                                key=lambda record: record['path'])}

    original_digests = release._input_digests

    def input_digests(canonical_path, update_path):
        values = original_digests(canonical_path, update_path)
        prefixes = [RUNTIME.resolve().as_posix() + '/']
        if RUNTIME.resolve().is_relative_to(workspace) and RUNTIME.resolve() != workspace:
            prefixes.append(RUNTIME.resolve().relative_to(workspace).as_posix() + '/')
        def portable(key):
            for prefix in prefixes:
                if key.startswith(prefix):
                    return key[len(prefix):]
            return key
        return {portable(key): value for key, value in values.items()}

    release.file_record = portable_record
    release.file_manifest = portable_manifest
    release._input_digests = input_digests
    windows_browser_support(qa)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('mode', choices=['engine', 'authoring', 'render'])
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    sys.path.insert(0, str(RUNTIME))
    os.chdir(args.workspace)
    bind_workspace(args.workspace)
    if args.mode == 'engine':
        from workbook_engine.__main__ import main as engine_main
        return engine_main(args.arguments)
    if args.mode == 'authoring':
        sys.argv = ['authoring_packet.py', *args.arguments]
        runpy.run_path(str(RUNTIME / 'scripts/authoring_packet.py'), run_name='__main__')
        return 0
    # Deterministic, unmeasured HTML for parity checks, never a public release.
    import json
    from workbook_engine.compiler import compile_workbook
    from workbook_engine.render import write_html
    render = argparse.ArgumentParser()
    render.add_argument('canonical', type=Path)
    render.add_argument('--edition', choices=['student', 'answer'], required=True)
    render.add_argument('--output', type=Path, required=True)
    parsed = render.parse_args(args.arguments)
    canonical = json.loads(parsed.canonical.read_text(encoding='utf-8'))
    write_html(compile_workbook(canonical, parsed.edition), parsed.output)
    print(parsed.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
