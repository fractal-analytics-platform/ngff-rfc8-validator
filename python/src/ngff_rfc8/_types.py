from typing import TypeAlias

JSONType: TypeAlias = (  # noqa: UP040
    dict[str, "JSONType"] | list["JSONType"] | str | int | float | bool | None
)
"""Type of a JSON document."""

JSONSchemaType = dict[str, JSONType]
"""Type of a JSON Schema."""
