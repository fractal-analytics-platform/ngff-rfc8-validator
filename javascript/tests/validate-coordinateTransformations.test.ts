import { describe, it, expect } from 'vitest';

import { validate } from '../src/main';

describe('Validate nodes with coordinateTransformations', () => {
  function validateCoordinateTransformations(coordinateTransformations: any[]) {
    validate({
      ome: {
        version: '0.x',
        type: 'singlescale',
        name: 'single',
        attributes: {
          coordinateTransformations
        },
        path: { type: 'json', path: './foo.json' }
      }
    });
  }

  it('missing type', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          translation: [0, 0, 100],
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0',
            keyword: 'required',
            message: "must have required property 'type'",
            params: {
              missingProperty: 'type'
            },
            schemaPath: '#/allOf/0/required'
          }
        ])
      })
    );
  });

  it('missing output id', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'translation',
          translation: [0, 0, 100],
          input: { id: 'physical' },
          output: {}
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/output',
            keyword: 'required',
            message: "must have required property 'id'",
            params: {
              missingProperty: 'id'
            },
            schemaPath: '#/required'
          }
        ])
      })
    );
  });

  it('valid identity', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'identity',
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).not.toThrow();
  });

  it('invalid projectAxis', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'projectAxis',
          droppedInputs: [0, 0],
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/droppedInputs',
            schemaPath: '#/$defs/projectAxis/allOf/0/properties/droppedInputs/uniqueItems',
            keyword: 'uniqueItems',
            params: { i: 0, j: 1 },
            message: 'must NOT have duplicate items (items ## 1 and 0 are identical)'
          }
        ])
      })
    );
  });

  it('invalid scale', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'scale',
          scale: [-1],
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/scale/0',
            schemaPath: '#/$defs/scale/properties/scale/items/exclusiveMinimum',
            keyword: 'exclusiveMinimum',
            params: { comparison: '>', limit: 0 },
            message: 'must be > 0'
          }
        ])
      })
    );
  });

  it('invalid translation', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'translation',
          translation: ['x'],
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/translation/0',
            schemaPath: '#/$defs/translation/properties/translation/items/type',
            keyword: 'type',
            params: { type: 'number' },
            message: 'must be number'
          }
        ])
      })
    );
  });

  it('invalid affine', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'affine',
          affine: ['x'],
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/affine/0',
            schemaPath: '#/$defs/affine/oneOf/1/properties/affine/items/type',
            keyword: 'type',
            params: { type: 'array' },
            message: 'must be array'
          }
        ])
      })
    );
  });

  it('invalid rotation', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'rotation',
          rotation: [0],
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/rotation',
            schemaPath: '#/$defs/rotation/oneOf/1/properties/rotation/oneOf/0/minItems',
            keyword: 'minItems',
            params: { limit: 2 },
            message: 'must NOT have fewer than 2 items'
          }
        ])
      })
    );
  });

  it('invalid bijection', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'bijection',
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0',
            schemaPath: '#/required',
            keyword: 'required',
            params: { missingProperty: 'forward' },
            message: "must have required property 'forward'"
          },
          {
            instancePath: '/ome/attributes/coordinateTransformations/0',
            schemaPath: '#/required',
            keyword: 'required',
            params: { missingProperty: 'inverse' },
            message: "must have required property 'inverse'"
          }
        ])
      })
    );
  });

  it('invalid sequence', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'sequence',
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0',
            schemaPath: '#/required',
            keyword: 'required',
            params: { missingProperty: 'transformations' },
            message: "must have required property 'transformations'"
          }
        ])
      })
    );
  });

  it('invalid byDimension', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'byDimension',
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0',
            schemaPath: '#/required',
            keyword: 'required',
            params: { missingProperty: 'transformations' },
            message: "must have required property 'transformations'"
          }
        ])
      })
    );
  });

  it('invalid displacements', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'displacements',
          path: '/foo',
          interpolation: 'foo',
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/interpolation',
            schemaPath: '#/$defs/displacements/properties/interpolation/enum',
            keyword: 'enum',
            params: { allowedValues: ['nearest', 'linear', 'cubic'] },
            message: 'must be equal to one of the allowed values'
          }
        ])
      })
    );
  });

  it('invalid coordinates', () => {
    expect(() =>
      validateCoordinateTransformations([
        {
          type: 'coordinates',
          path: '/foo',
          interpolation: 'foo',
          input: { id: 'physical' },
          output: { id: 'world' }
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateTransformations/0/interpolation',
            schemaPath: '#/$defs/coordinates/properties/interpolation/enum',
            keyword: 'enum',
            params: { allowedValues: ['nearest', 'linear', 'cubic'] },
            message: 'must be equal to one of the allowed values'
          }
        ])
      })
    );
  });
});
