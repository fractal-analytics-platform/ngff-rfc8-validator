from enum import StrEnum
from functools import cache
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema import ValidationError
from jsonschema.exceptions import best_match

from ngff_rfc8._types import JSONType
from ngff_rfc8.load_schemas import build_registry
from ngff_rfc8.load_schemas import get_node_schema
from ngff_rfc8.load_schemas import get_ome_schema

_OME = "ome"


class RFC8NodeType(StrEnum):
    COLLECTION = "collection"
    SINGLESCALE = "singlescale"
    MULTISCALE = "multiscale"
    UNKNOWN = "__unknown_node_type__"


@cache
def _get_version_ok_path() -> list[str | int]:
    """
    The `ome` JSON schema has an `allOf` array which covers two options, depending on
    whether a valid `version` is present.
    This function returns the common part of an error path shared by all cases where the
    version is valid, which is then used below when filtering out some spurious error
    branches.
    """
    allOf_array: list[JSONType] = get_ome_schema()["properties"][_OME]["allOf"]
    version_ok_index = allOf_array.index({"$ref": "node.schema"})
    return [
        "properties",
        _OME,
        "allOf",
        version_ok_index,
        "oneOf",
    ]


@cache
def _get_oneOf_indices_dict() -> dict[RFC8NodeType, int]:
    """
    The `node` JSON schema has a top-level `oneOf`, which covers four possible `type`
    values: collection, multiscale, singlescale, a different type. This function finds
    their indices in the array, which are then used below when filtering out some spurious
    `oneOf`-related error branches.

    NOTE: The usage of OpenAPI `discriminator` keyword (see e.g.
    https://swagger.io/specification/v3.2/#discriminator-object) would make this logic
    redundant, as we would only attempt validation with the schema corresponding to the
    `type` value.
    """
    node_schema = get_node_schema()
    oneOf_array: list[JSONType] = node_schema["oneOf"]
    if len(oneOf_array) != 4:
        raise RuntimeError(
            "Unexpected length for the `oneOf` array of the `node` schema: "
            f"{len(oneOf_array)}"
        )
    node_indices: dict[RFC8NodeType, int] = {
        node_type: oneOf_array.index({"$ref": f"{node_type}.schema"})
        for node_type in (
            RFC8NodeType.COLLECTION,
            RFC8NodeType.MULTISCALE,
            RFC8NodeType.SINGLESCALE,
        )
    }
    node_indices[RFC8NodeType.UNKNOWN] = (set(range(4)) - set(node_indices.keys())).pop()
    return node_indices


def _is_spurious_error(
    *,
    error: ValidationError,
    ome_type: RFC8NodeType,
    verbose: bool,
) -> bool:
    """
    Determine whether this is a spurious error, based on the OME type and on the path of
    the error branch.
    """
    absolute_schema_path = list(error.absolute_schema_path)
    if (
        absolute_schema_path[:5] == _get_version_ok_path()
        and absolute_schema_path[5] != _get_oneOf_indices_dict()[ome_type]
    ):
        if verbose:
            print(f"[_is_spurious_error] Spurious error branch {error=}, {ome_type=}")
        return True
    else:
        if verbose:
            print(f"[_is_spurious_error] Valid error branch {error=}, {ome_type=}")
        return False


VALIDATOR = Draft202012Validator(
    schema=get_ome_schema(),
    registry=build_registry(),
)


def get_ome_property(data: dict[str, Any]) -> dict[str, Any]:
    if _OME in data.keys() and isinstance(data[_OME], dict):
        return data[_OME]
    elif (
        "attributes" in data.keys()
        and _OME in data["attributes"].keys()
        and isinstance(data["attributes"][_OME], dict)
    ):
        return data["attributes"][_OME]
    else:
        error = (
            "The document must include a 'ome' object property, "
            "either at the document root or within an 'attributes' object. "
            "See https://ngff.openmicroscopy.org/rfc/8/index.html#metadata-storage"
        )
        raise ValueError(error)


def validate_collection(
    data: dict[str, Any],
    *,
    ignore_nodes: bool = False,
    verbose: bool = False,
) -> None:
    ome_data = get_ome_property(data)
    if ignore_nodes and "nodes" in ome_data.keys():
        ome_data["nodes"] = []
    ome_type = ome_data.get("type", RFC8NodeType.UNKNOWN)

    if verbose:
        print(f"[validate_collection] {ome_data=}")
        print(f"[validate_collection] {ome_type=}")

    top_level_errors = list(VALIDATOR.iter_errors({_OME: ome_data}))
    if verbose:
        print(f"[validate_collection] {len(top_level_errors)=}")
    match len(top_level_errors):
        case 0:
            if verbose:
                print("[validate_collection] No errors.")
            return
        case 1:
            top_level_error = top_level_errors[0]
            if verbose:
                print(f"[validate_collection] Single top-level error: {top_level_error}.")
            suberrors = [
                suberror
                for suberror in top_level_error.context
                if not _is_spurious_error(
                    error=suberror,
                    ome_type=ome_type,
                    verbose=verbose,
                )
            ]
            if verbose:
                print(f"[validate_collection] {len(suberrors)=}")
                for ind, suberror in enumerate(suberrors):
                    print(f"[validate_collection] {ind}, {suberror}")
            match len(suberrors):
                case 0:
                    raise top_level_error
                case _:
                    best_exception = best_match(suberrors)
                    if verbose:
                        print(f"[validate_collection] best match: {best_exception}")
                    raise best_exception
        case _:
            # Fall-back on the standard validate, to avoid handling this specific case
            if verbose:
                print(
                    "[validate_collection] More than one top-level error, fall-back on "
                    "upstream validation."
                )
            VALIDATOR.validate({_OME: ome_data})
