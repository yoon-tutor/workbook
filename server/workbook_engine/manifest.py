"""Deterministic snapshot helpers for workbook change reporting.

The change reporter deliberately accepts plain JSON mappings.  This module adds a
small, stable envelope around those mappings so the compiler, renderer and CLI do
not need to agree on Python classes or third-party packages.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


COMPONENTS = ("canonical", "spec", "template", "build")


def canonical_json(value: Any, *, pretty: bool = False) -> str:
    """Return a deterministic UTF-8-safe JSON representation."""

    if pretty:
        return json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def json_digest(value: Any) -> str:
    """Hash a JSON-compatible value independently of mapping insertion order."""

    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, value: Any) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(canonical_json(value, pretty=True), encoding="utf-8")


def file_record(path: str | Path, *, root: str | Path | None = None) -> dict[str, Any]:
    """Create a portable file record suitable for a component ``files`` array."""

    source = Path(path)
    data = source.read_bytes()
    if root is None:
        display_path = source.as_posix()
    else:
        try:
            display_path = source.resolve().relative_to(Path(root).resolve()).as_posix()
        except ValueError:
            display_path = source.resolve().as_posix()
    return {
        "path": display_path,
        "sha256": sha256(data).hexdigest(),
        "size": len(data),
    }


def file_manifest(
    paths: Iterable[str | Path], *, root: str | Path | None = None
) -> dict[str, Any]:
    """Build a deterministic ``files`` manifest from existing files."""

    records = (file_record(path, root=root) for path in paths)
    return {"files": sorted(records, key=lambda record: record["path"])}


def _coerce_component(name: str, value: Any) -> Mapping[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} manifest must be a JSON object")
    return dict(value)


@dataclass(frozen=True)
class ManifestBundle:
    """The four snapshots compared for every workbook update."""

    canonical: Mapping[str, Any]
    spec: Mapping[str, Any]
    template: Mapping[str, Any]
    build: Mapping[str, Any]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ManifestBundle":
        if not isinstance(value, Mapping):
            raise ValueError("manifest bundle must be a JSON object")
        unknown = sorted(set(value) - set(COMPONENTS) - {"bundleVersion"})
        if unknown:
            names = ", ".join(unknown)
            raise ValueError(f"unknown manifest bundle component(s): {names}")
        return cls(
            canonical=_coerce_component("canonical", value.get("canonical")),
            spec=_coerce_component("spec", value.get("spec")),
            template=_coerce_component("template", value.get("template")),
            build=_coerce_component("build", value.get("build")),
        )

    @classmethod
    def empty(cls) -> "ManifestBundle":
        return cls(canonical={}, spec={}, template={}, build={})

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundleVersion": 1,
            "canonical": dict(self.canonical),
            "spec": dict(self.spec),
            "template": dict(self.template),
            "build": dict(self.build),
        }

    def component(self, name: str) -> Mapping[str, Any]:
        if name not in COMPONENTS:
            raise KeyError(name)
        return getattr(self, name)

    def digests(self) -> dict[str, str]:
        return {name: json_digest(self.component(name)) for name in COMPONENTS}

    def versions(self) -> dict[str, str | None]:
        return {
            name: component_version(self.component(name), component_name=name)
            for name in COMPONENTS
        }


def component_version(
    component: Mapping[str, Any], *, component_name: str | None = None
) -> str | None:
    """Read a conventional component version without imposing a schema."""

    preferred = (f"{component_name}Version",) if component_name else ()
    for key in preferred + (
        "version",
        "contentVersion",
        "specVersion",
        "schemaVersion",
        "templateVersion",
        "compilerVersion",
        "buildVersion",
    ):
        value = component.get(key)
        if isinstance(value, (str, int, float)) and not isinstance(value, bool):
            return str(value)
    manifest = component.get("manifest")
    if isinstance(manifest, Mapping):
        value = manifest.get("version")
        if isinstance(value, (str, int, float)) and not isinstance(value, bool):
            return str(value)
    versions = component.get("versions")
    if isinstance(versions, Mapping) and component_name:
        value = versions.get(component_name)
        if isinstance(value, (str, int, float)) and not isinstance(value, bool):
            return str(value)
    return None


def load_bundle(path: str | Path) -> ManifestBundle:
    value = read_json(path)
    if not isinstance(value, Mapping):
        raise ValueError("manifest bundle must be a JSON object")
    return ManifestBundle.from_dict(value)


def write_bundle(path: str | Path, bundle: ManifestBundle) -> None:
    write_json(path, bundle.to_dict())


def bundle_from_paths(
    *,
    canonical: str | Path | None = None,
    spec: str | Path | None = None,
    template: str | Path | None = None,
    build: str | Path | None = None,
) -> ManifestBundle:
    """Load individual JSON snapshots into a reportable bundle."""

    values: dict[str, Mapping[str, Any]] = {}
    for name, path in {
        "canonical": canonical,
        "spec": spec,
        "template": template,
        "build": build,
    }.items():
        if path is None:
            values[name] = {}
            continue
        loaded = read_json(path)
        values[name] = _coerce_component(name, loaded)
    return ManifestBundle(**values)
