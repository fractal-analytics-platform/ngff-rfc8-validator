import json
from pathlib import Path
from typing import TypeAlias

from referencing import Registry
from referencing import Resource

JSONValue: TypeAlias = (  # noqa: UP040
    dict[str, "JSONValue"] | list["JSONValue"] | str | int | float | bool | None
)


def get_schema_dir() -> Path:
    """
    Get root directory of JSON Schemas.
    """
    return Path(__file__).parent / "schemas"


def get_schema(name: str) -> JSONValue:
    """
    Get JSON Schema named `name`.

    Arguments:
        name: Name of the schema (e.g. `node`, `collection`, `multiscale`, ...).
    """
    schema = json.loads((get_schema_dir() / f"{name}.json").read_text())
    return schema


def _get_list_schema_files() -> list[Path]:
    return list(sorted(get_schema_dir().glob("*.json")))


def get_ome_schema() -> JSONValue:
    return get_schema("ome")


def build_registry() -> Registry:
    registry = Registry()
    for path in _get_list_schema_files():
        schema = json.loads(path.read_text())
        registry = registry.with_resource(
            schema["$id"],
            Resource.from_contents(schema),
        )
    return registry
