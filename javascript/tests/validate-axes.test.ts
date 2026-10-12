import { describe, it, expect } from 'vitest';

import { validate } from '../src/main';

describe('Validate axes', () => {
  function validateAxes(axes: any[]) {
    validate({
      ome: {
        type: 'multiscale',
        name: 'foo',
        version: '0.x',
        nodes: [],
        attributes: {
          labels: {},
          coordinateSystems: [
            {
              id: 'x',
              axes
            }
          ]
        }
      }
    });
  }

  it('invalid axes: type space maxContains 3', () => {
    expect(() =>
      validateAxes(
        [...Array(4).keys()].map((i) => ({
          name: `k${i}`,
          type: 'space',
          unit: 'micrometer'
        }))
      )
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateSystems/0/axes',
            schemaPath: '#/allOf/0/then/contains',
            keyword: 'contains',
            params: { minContains: 2, maxContains: 3 },
            message: 'must contain at least 2 and no more than 3 valid item(s)'
          }
        ])
      })
    );
  });

  it('invalid axes: type space minContains 2', () => {
    expect(() =>
      validateAxes([
        {
          name: 'x',
          type: 'space',
          unit: 'micrometer'
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateSystems/0/axes',
            schemaPath: '#/allOf/0/then/contains',
            keyword: 'contains',
            params: { minContains: 2, maxContains: 3 },
            message: 'must contain at least 2 and no more than 3 valid item(s)'
          }
        ])
      })
    );
  });

  it('invalid axes: type array minContains 2', () => {
    expect(() =>
      validateAxes([
        {
          name: 'x',
          type: 'array',
          unit: 'micrometer'
        }
      ])
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateSystems/0/axes',
            schemaPath: '#/allOf/1/then/contains',
            keyword: 'contains',
            params: { minContains: 2 },
            message: 'must contain at least 2 valid item(s)'
          }
        ])
      })
    );
  });

  it('valid axes: type array maxItems 5', () => {
    expect(() =>
      validateAxes(
        [...Array(5).keys()].map((i) => ({
          name: `k${i}`,
          type: 'array'
        }))
      )
    ).not.toThrow();
  });

  it('invalid axes: maxItems 5', () => {
    expect(() =>
      validateAxes(
        [...Array(6).keys()].map((i) => ({
          name: `k${i}`,
          type: 'array'
        }))
      )
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateSystems/0/axes',
            schemaPath: '#/maxItems',
            keyword: 'maxItems',
            params: { limit: 5 },
            message: 'must NOT have more than 5 items'
          }
        ])
      })
    );
  });

  it('invalid axes: minItems 1', () => {
    expect(() => validateAxes([])).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes/coordinateSystems/0/axes',
            schemaPath: '#/minItems',
            keyword: 'minItems',
            params: { limit: 1 },
            message: 'must NOT have fewer than 1 items'
          }
        ])
      })
    );
  });

  it('valid axes with custom type', () => {
    expect(() =>
      validateAxes([
        {
          name: 'x',
          type: 'custom-type'
        }
      ])
    ).not.toThrow();
  });

  it('valid axes without type', () => {
    expect(() => validateAxes([{ name: 'a' }])).not.toThrow();
  });
});
