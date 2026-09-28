from typing import Any

from jsonschema import validate

from .load_schemas import build_registry
from .load_schemas import get_ome_schema


def get_ome_property(data: dict[str, Any]) -> dict[str, Any]:
    if "ome" in data.keys():
        return data["ome"]
    elif "attributes" in data.keys() and "ome" in data["attributes"].keys():
        return data["attributes"]["ome"]
    else:
        error = (
            "The document must include a 'ome' property, "
            "either at the document root or within an 'attributes' object. "
            "See https://ngff.openmicroscopy.org/rfc/8/index.html#metadata-storage"
        )
        raise ValueError(error)


def validate_collection(
    data: dict[str, Any],
    ignore_nodes: bool = False,
) -> None:
    ome_property = get_ome_property(data)

    if ignore_nodes and "nodes" in ome_property.keys():
        ome_property["nodes"] = []

    validate(
        instance={"ome": ome_property},
        schema=get_ome_schema(),
        registry=build_registry(),
    )
