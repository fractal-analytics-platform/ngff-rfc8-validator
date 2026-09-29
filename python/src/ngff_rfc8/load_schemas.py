import json
from pathlib import Path

from referencing import Registry
from referencing import Resource

from ngff_rfc8._types import Schema


def _get_schema_dir() -> Path:
    return Path(__file__).parent / "schemas"


def _get_schema(name: str) -> Schema:
    schema = json.loads((_get_schema_dir() / f"{name}.json").read_text())
    return schema


def _get_list_schema_files() -> list[Path]:
    return list(sorted(_get_schema_dir().glob("*.json")))


def get_ome_schema() -> Schema:
    return _get_schema("ome")


def get_node_schema() -> Schema:
    return _get_schema("node")


def build_registry() -> Registry:
    registry = Registry()
    for path in _get_list_schema_files():
        schema = json.loads(path.read_text())
        registry = registry.with_resource(
            schema["$id"],
            Resource.from_contents(schema),
        )
    return registry
