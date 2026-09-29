from functools import cache

from jsonschema.exceptions import ValidationError  # noqa: F401
from jsonschema.exceptions import best_match
from jsonschema.protocols import Validator
from jsonschema.validators import Draft202012Validator

from ._types import JSONType
from .load_schemas import build_registry
from .load_schemas import get_ome_schema


def get_ome_property(data: dict[str, JSONType]) -> dict[str, JSONType]:
    """
    Get the `ome` property from a JSON document.

    This supports both an arbitrary JSON file with a top-level `ome` property and a
    Zarr-group `zarr.json` file with the `ome` property nested within the `attributes`
    property. See https://ngff.openmicroscopy.org/rfc/8/index.html#metadata-storage.

    Arguments:
        data: The original JSON document.

    Returns:
        ome_data: The `ome` property value, if any.

    Raises:
        ValueError: When `data` does not fit with one of the two supported cases.
    """
    if isinstance(data, dict) and "ome" in data.keys() and isinstance(data["ome"], dict):
        return data["ome"]
    elif (
        isinstance(data, dict)
        and "attributes" in data.keys()
        and isinstance(data["attributes"], dict)
        and "ome" in data["attributes"].keys()
        and isinstance(data["attributes"]["ome"], dict)
    ):
        return data["attributes"]["ome"]
    else:
        error = (
            "The document must include a 'ome' object property, "
            "either at the document root or within an 'attributes' object. "
            "See https://ngff.openmicroscopy.org/rfc/8/index.html#metadata-storage"
        )
        raise ValueError(error)


@cache
def get_ome_validator() -> Validator:
    """
    Get a draft-2020-12 JSON Schema validator for `ome` data.

    Returns:
        validator: The validator object.
    """
    validator = Draft202012Validator(
        schema=get_ome_schema(),
        registry=build_registry(),
    )
    return validator


def validate_collection(
    data: dict[str, JSONType],
    ignore_nodes: bool = False,
) -> None:
    """
    Validate a JSON document against the `ome` JSON Schema.

    Arguments:
        data: JSON document to validate.
        ignore_nodes:
            If `True`, set the `nodes` property to an empty array (`[]`).

    Raises:
        ValidationError: If the instance is invalid.
    """
    ome_property = get_ome_property(data)

    if ignore_nodes and "nodes" in ome_property.keys():
        ome_property["nodes"] = []

    validator = get_ome_validator()
    error = best_match(validator.iter_errors({"ome": ome_property}))
    if error is not None:
        raise error
