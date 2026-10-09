"""Small dependency-free validator for the JSON Schema features used here."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


@dataclass(frozen=True)
class SchemaIssue:
    path: str
    message: str

    def format(self) -> str:
        return f"[SCHEMA] {self.path}: {self.message}"


def _pointer(root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"only local schema references are supported: {reference}")
    node: Any = root
    for raw in reference[2:].split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        node = node[key]
    if not isinstance(node, dict):
        raise ValueError(f"schema reference is not an object: {reference}")
    return node


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _format_valid(value: str, expected: str) -> bool:
    try:
        if expected == "date-time":
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        elif expected == "date":
            date.fromisoformat(value)
        elif expected == "uri-reference":
            if any(character.isspace() for character in value):
                return False
            urlparse(value)
    except ValueError:
        return False
    return True


def validate_schema(data: Any, schema: dict[str, Any]) -> list[SchemaIssue]:
    issues: list[SchemaIssue] = []

    def visit(value: Any, rule: dict[str, Any], path: str) -> None:
        if "$ref" in rule:
            visit(value, _pointer(schema, str(rule["$ref"])), path)
            rule = {key: child for key, child in rule.items() if key != "$ref"}
            if not rule:
                return

        alternatives = rule.get("anyOf")
        if isinstance(alternatives, list):
            if not any(not _trial(value, alternative, path) for alternative in alternatives):
                issues.append(SchemaIssue(path, "value does not match any allowed schema"))
                return
        alternatives = rule.get("oneOf")
        if isinstance(alternatives, list):
            matches = sum(not _trial(value, alternative, path) for alternative in alternatives)
            if matches != 1:
                issues.append(SchemaIssue(path, f"value must match exactly one schema, matched {matches}"))
                return
        combined = rule.get("allOf")
        if isinstance(combined, list):
            for child in combined:
                if isinstance(child, dict):
                    visit(value, child, path)
        condition = rule.get("if")
        if isinstance(condition, dict):
            branch = rule.get("then") if not _trial(value, condition, path) else rule.get("else")
            if isinstance(branch, dict):
                visit(value, branch, path)

        expected_type = rule.get("type")
        if isinstance(expected_type, str) and not _type_matches(value, expected_type):
            issues.append(SchemaIssue(path, f"expected {expected_type}, found {type(value).__name__}"))
            return
        if isinstance(expected_type, list) and not any(_type_matches(value, item) for item in expected_type):
            issues.append(SchemaIssue(path, f"expected one of {expected_type}"))
            return
        if "const" in rule and value != rule["const"]:
            issues.append(SchemaIssue(path, f"expected constant {rule['const']!r}"))
        if "enum" in rule and value not in rule["enum"]:
            issues.append(SchemaIssue(path, f"value is not in {rule['enum']!r}"))

        if isinstance(value, dict):
            required = rule.get("required", [])
            for key in required if isinstance(required, list) else []:
                if key not in value:
                    issues.append(SchemaIssue(f"{path}.{key}", "required field is missing"))
            properties = rule.get("properties", {})
            if isinstance(properties, dict):
                for key, child in properties.items():
                    if key in value and isinstance(child, dict):
                        visit(value[key], child, f"{path}.{key}")
                if rule.get("additionalProperties") is False:
                    for key in sorted(set(value) - set(properties)):
                        issues.append(SchemaIssue(f"{path}.{key}", "additional property is not allowed"))
        elif isinstance(value, list):
            minimum = rule.get("minItems")
            maximum = rule.get("maxItems")
            if isinstance(minimum, int) and len(value) < minimum:
                issues.append(SchemaIssue(path, f"needs at least {minimum} items"))
            if isinstance(maximum, int) and len(value) > maximum:
                issues.append(SchemaIssue(path, f"allows at most {maximum} items"))
            if rule.get("uniqueItems"):
                rendered = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
                if len(rendered) != len(set(rendered)):
                    issues.append(SchemaIssue(path, "array items must be unique"))
            child = rule.get("items")
            if isinstance(child, dict):
                for index, item in enumerate(value):
                    visit(item, child, f"{path}[{index}]")
        elif isinstance(value, str):
            minimum = rule.get("minLength")
            if isinstance(minimum, int) and len(value) < minimum:
                issues.append(SchemaIssue(path, f"needs at least {minimum} characters"))
            pattern = rule.get("pattern")
            if isinstance(pattern, str) and re.search(pattern, value) is None:
                issues.append(SchemaIssue(path, f"does not match pattern {pattern}"))
            expected_format = rule.get("format")
            if isinstance(expected_format, str) and not _format_valid(value, expected_format):
                issues.append(SchemaIssue(path, f"invalid {expected_format} format"))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            minimum = rule.get("minimum")
            maximum = rule.get("maximum")
            if isinstance(minimum, (int, float)) and value < minimum:
                issues.append(SchemaIssue(path, f"must be at least {minimum}"))
            if isinstance(maximum, (int, float)) and value > maximum:
                issues.append(SchemaIssue(path, f"must be at most {maximum}"))

    def _trial(value: Any, rule: Any, path: str) -> list[SchemaIssue]:
        before = len(issues)
        if isinstance(rule, dict):
            visit(value, rule, path)
        result = issues[before:]
        del issues[before:]
        return result

    visit(data, schema, "$")
    return issues


def validate_schema_files(data_path: Path, schema_path: Path) -> list[SchemaIssue]:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return validate_schema(data, schema)
