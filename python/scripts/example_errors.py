from typing import Any

from jsonschema import Draft202012Validator
from jsonschema import ValidationError
from jsonschema.exceptions import best_match
from ngff_rfc8.load_schemas import build_registry
from ngff_rfc8.load_schemas import get_ome_schema
from ngff_rfc8.validate import get_ome_property

_TYPES = {"collection", "singlescale", "multiscale"}
_SCHEMA_PATH_PREFIX = [
    "properties",
    "ome",
    "allOf",
    1,  # FIXME: Re-compute?
    "oneOf",
]

_COLLECTION = "collection"
_SINGLESCALE = "singlescale"
_MULTISCALE = "multiscale"
_VALIDATOR = Draft202012Validator(
    schema=get_ome_schema(),
    registry=build_registry(),
)

# FIXME: Re-compute these indices (based on the actual schema)?
_INDEX_TYPE_OTHER = 0
_INDEX_TYPE_COLLECTION = 1
_INDEX_TYPE_SINGLESCALE = 2
_INDEX_TYPE_MULTISCALE = 3


def _include_error(error: ValidationError, ome_type: str) -> bool:
    absolute_schema_path = list(error.absolute_schema_path)
    if absolute_schema_path[:5] == _SCHEMA_PATH_PREFIX:
        oneOf_option = absolute_schema_path[5]
        if (
            (ome_type not in _TYPES and oneOf_option != _INDEX_TYPE_OTHER)
            or (ome_type == _COLLECTION and oneOf_option != _INDEX_TYPE_COLLECTION)
            or (ome_type == _SINGLESCALE and oneOf_option != _INDEX_TYPE_SINGLESCALE)
            or (ome_type == _MULTISCALE and oneOf_option != _INDEX_TYPE_MULTISCALE)
        ):
            return False
    else:
        print("THIS WAS DIFFERENT", absolute_schema_path)
    return True


def find_best_error(instance: dict[str, Any]) -> ValidationError | None:
    ome_data = get_ome_property(instance)
    instance_type = ome_data.get("type")
    root_errors = list(_VALIDATOR.iter_errors({"ome": ome_data}))
    if len(root_errors) == 0:
        return None
    elif len(root_errors) > 1:
        raise NotImplementedError()
    root_error = root_errors[0]
    suberrors = [
        suberror
        for suberror in root_error.context
        if _include_error(suberror, ome_type=instance_type)
    ]
    if len(suberrors) == 0:
        return root_error
    else:
        return best_match(suberrors)


_CASES = [
    (
        {
            "ome": {
                "version": "0.x",
                "type": "collection",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'name' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'name' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'coordinateSystems' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {"coordinateSystems": {}},
                "nodes": [],
            }
        },
        r"{} is not of type 'array'",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {"coordinateSystems": []},
                "nodes": [],
            }
        },
        "[] should be non-empty",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {"coordinateSystems": [{"id": "my-id", "axes": []}]},
                "nodes": [],
            }
        },
        "[] should be non-empty",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "singlescale",
                "name": "name",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'coordinateTransformations' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "collection",
                "name": "name",
                "id": "??",
                "attributes": {},
                "nodes": [],
            }
        },
        "'??' does not match '^[a-zA-Z0-9-_.]+$'",
    ),
    (
        {
            "ome": {
                "type": "collection",
                "name": "name",
                "id": "id",
                "attributes": {},
                "nodes": [],
            }
        },
        "'version' is a required property",
    ),
    (
        {
            "ome": {
                "version": 1234,
                "type": "collection",
                "name": "name",
                "id": "id",
                "attributes": {},
                "nodes": [],
            }
        },
        "1234 is not of type 'string'",
    ),
]

for data, msg in _CASES:
    error = find_best_error(data)
    print(f"Data:    {data}")
    print(f"Path:    {error.json_path}")
    print(f"Message: {error.message}")
    assert error.message == msg
    print()
