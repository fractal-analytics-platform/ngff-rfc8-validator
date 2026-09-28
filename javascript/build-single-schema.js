import fs from 'fs';
import path from 'path';

const __dirname = import.meta.dirname;

const schemaFolder = path.resolve(__dirname, '..', 'schemas');
const targetFile = path.resolve(__dirname, 'ngff-rfc8-schema.json');

function replaceRefs(obj) {
  for (const [key, value] of Object.entries(obj)) {
    if (key === '$ref' && typeof value === 'string' && !value.startsWith('#')) {
      const id = value.replace('.schema', '');
      obj[key] = `#/$defs/${id}`;
    } else if (value !== null && typeof value === 'object') {
      if (Array.isArray(value)) {
        for (const v of value) {
          if (v !== null && typeof v === 'object') {
            replaceRefs(v);
          }
        }
      } else {
        replaceRefs(value);
      }
    }
  }
}

export function buildSingleSchema() {
  const schemas = {};
  let rootSchema = null;
  const defs = {};

  const files = fs
    .readdirSync(schemaFolder, { withFileTypes: true })
    .filter((item) => !item.isDirectory())
    .map((item) => path.resolve(schemaFolder, item.name));

  for (const filePath of files) {
    const schema = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    if (schema['$id'] === 'ome.schema') {
      rootSchema = schema;
    } else {
      if ('$defs' in schema) {
        const d = schema['$defs'];
        replaceRefs(d);
        Object.assign(defs, d);
        delete schema['$defs'];
      }
      schemas[schema['$id']] = schema;
    }
    delete schema['$id'];
  }

  replaceRefs(rootSchema);

  for (const [id, schema] of Object.entries(schemas)) {
    const cleanId = id.replace('.schema', '');
    replaceRefs(schema);
    defs[cleanId] = schema;
  }

  rootSchema['$defs'] = defs;

  fs.writeFileSync(targetFile, JSON.stringify(rootSchema, null, 2));
}
