import json

from ngff_rfc8.load_schemas import get_list_schema_files


def _replace_refs(obj):
    for key, value in obj.items():
        if key == "$ref" and not value.startswith("#"):
            id = value[: -len(".schema")]
            obj[key] = f"#/$defs/{id}"
        elif type(value) is dict:
            _replace_refs(value)
        elif type(value) is list:
            for v in value:
                if type(v) is dict:
                    _replace_refs(v)


def main():
    schemas = {}
    root_schema = None
    defs = {}
    for path in get_list_schema_files():
        schema = json.loads(path.read_text())
        if schema["$id"] == "ome.schema":
            root_schema = schema
        else:
            if "$defs" in schema:
                d = schema["$defs"]
                _replace_refs(d)
                defs.update(d)
                del schema["$defs"]
            schemas[schema["$id"]] = schema
        del schema["$id"]

    _replace_refs(root_schema)

    for id, schema in schemas.items():
        id = id[: -len(".schema")]
        _replace_refs(schema)
        defs[id] = schema

    root_schema["$defs"] = defs

    print(json.dumps(root_schema, indent=2))


if __name__ == "__main__":
    main()
