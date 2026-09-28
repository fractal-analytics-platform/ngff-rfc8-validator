import Ajv, { type ErrorObject } from 'ajv/dist/2020';
import schema from 'ngff-rfc8-schema';

export class NGFFValidationError extends Error {
  schemaErrors: ErrorObject[];

  constructor(message: string, errors: ErrorObject[] = []) {
    super(message);
    this.schemaErrors = errors;
  }
}

export function validate(data: any) {
  validateSchema({
    ome: getOme(data)
  });
}

function getOme(data: any) {
  if ('ome' in data) {
    return data.ome;
  }
  if ('attributes' in data && 'ome' in data.attributes) {
    return data.attributes.ome;
  }
  throw new NGFFValidationError('Missing ome field');
}

function validateSchema(data: any) {
  const ajv = new Ajv({ allErrors: true, strict: false });
  const validate = ajv.compile(schema);
  const valid = validate(data);
  if (!valid) {
    throw new NGFFValidationError('JSON schema validation failed', validate.errors || []);
  }
}
