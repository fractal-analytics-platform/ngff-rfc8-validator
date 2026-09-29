import json
from functools import cache
from pathlib import Path

from referencing import Registry
from referencing import Resource

from ._types import JSONSchemaType

_SCHEMA_DIR = Path(__file__).parent / "schemas"
"""
Root directory of JSON Schemas.
"""


@cache
def get_schema(name: str) -> JSONSchemaType:
    """
    Get JSON Schema named `name`.

    Arguments:
        name: Name of the schema (e.g. `node`, `collection`, `multiscale`, ...).

    Returns:
        The JSON Schema named `name`.
    """
    schema = json.loads((_SCHEMA_DIR / f"{name}.json").read_text())
    return schema


@cache
def get_list_schema_files() -> list[Path]:
    """
    Get list of JSON Schema files.

    Returns:
        List of JSON Schema paths.
    """
    return list(sorted(_SCHEMA_DIR.glob("*.json")))


@cache
def get_ome_schema() -> JSONSchemaType:
    """
    Get `ome` JSON Schema.

    Returns:
        JSON Schema for `ome` data.
    """
    return get_schema("ome")


@cache
def build_registry() -> Registry:
    """
    Build a JSON-referencing registry including all schemas from this package.

    Returns:
        The complete registry.
    """
    registry = Registry()
    for path in get_list_schema_files():
        schema = json.loads(path.read_text())
        registry = registry.with_resource(
            schema["$id"],
            Resource.from_contents(schema),
        )
    return registry
