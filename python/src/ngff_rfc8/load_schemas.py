import json
from pathlib import Path
from typing import TypeAlias

from referencing import Registry
from referencing import Resource

JSONValue: TypeAlias = (  # noqa: UP040
    dict[str, "JSONValue"] | list["JSONValue"] | str | int | float | bool | None
)


def _get_schema_dir() -> Path:
    return Path(__file__).parent / "schemas"


def _get_schema(name: str) -> JSONValue:
    schema = json.loads((_get_schema_dir() / f"{name}.json").read_text())
    return schema


def _get_list_schema_files() -> list[Path]:
    return list(sorted(_get_schema_dir().glob("*.json")))


def get_ome_schema() -> JSONValue:
    return _get_schema("ome")


def get_node_schema() -> JSONValue:
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
