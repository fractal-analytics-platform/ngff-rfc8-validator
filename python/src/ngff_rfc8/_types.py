from typing import TypeAlias

JSONType: TypeAlias = (  # noqa: UP040
    dict[str, "JSONType"] | list["JSONType"] | str | int | float | bool | None
)

JSONSchemaType = dict[str, JSONType]
