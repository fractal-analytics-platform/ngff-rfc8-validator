from typing import Any

from jsonschema import Draft202012Validator
from jsonschema import ValidationError
from jsonschema import validate
from jsonschema.exceptions import best_match

from .load_schemas import build_registry
from .load_schemas import get_ome_schema

VALIDATOR = Draft202012Validator(
    schema=get_ome_schema(),
    registry=build_registry(),
)


class CustomError(ValidationError):
    def __str__(self):
        return f"{self.json_path}: {self.message}"

    def __repr__(self):
        return f"{self.json_path}: {self.message}"


def get_ome_property(data: dict[str, Any]) -> dict[str, Any]:
    if "ome" in data.keys() and isinstance(data["ome"], dict):
        return data["ome"]
    elif (
        "attributes" in data.keys()
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


_COLLECTION = "collection"
_SINGLESCALE = "singlescale"
_MULTISCALE = "multiscale"
_TYPES = {_COLLECTION, _SINGLESCALE, _MULTISCALE}
_SCHEMA_PATH_PREFIX = [
    "properties",
    "ome",
    "allOf",
    1,  # FIXME: Re-compute?
    "oneOf",
]

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


def validate_collection(
    data: dict[str, Any],
    ignore_nodes: bool = False,
) -> None:
    ome_data = get_ome_property(data)
    instance_type = ome_data.get("type", None)

    if ignore_nodes and "nodes" in ome_data.keys():
        ome_data["nodes"] = []

    top_level_errors = list(VALIDATOR.iter_errors({"ome": ome_data}))
    match len(top_level_errors):
        case 0:
            return
        case 1:
            top_level_error = top_level_errors[0]
            suberrors = [
                suberror
                for suberror in top_level_error.context
                if _include_error(suberror, ome_type=instance_type)
            ]
            match len(suberrors):
                case 0:
                    raise top_level_error
                case _:
                    raise best_match(suberrors)
        case _:
            raise NotImplementedError("More than one top-level error.")

    try:
        validate(
            instance={"ome": ome_data},
            schema=get_ome_schema(),
            registry=build_registry(),
        )
    except ValidationError as e:
        print(e.context)
    except Exception as generic_exception:
        raise generic_exception
