import { describe, it, expect } from 'vitest';

import { validate } from '../src/main';

describe('Validate', () => {
  const validOmeProperty = {
    version: '0.x',
    type: 'collection',
    name: 'My Dataset',
    id: 'dataset',
    attributes: { 'fractal:dataset': { user: 'lorenzo', project: 'base-dataset' } },
    nodes: [
      {
        type: 'collection',
        name: 'My Plate',
        id: 'plate',
        path: { type: 'json', path: './plate/plate.json' }
      }
    ]
  };

  it('valid inline collection', () => {
    expect(() => validate({ ome: validOmeProperty })).not.toThrow();
  });

  it('zarr valid inline collection', () => {
    expect(() =>
      validate({
        zarr_format: 3,
        node_type: 'group',
        attributes: { ome: validOmeProperty }
      })
    ).not.toThrow();
  });

  it('missing ome', () => {
    expect(() => validate({})).toThrow('Missing ome field');
  });

  it('missing version', () => {
    expect(() => validate({ ome: { type: 'collection', name: 'foo' } })).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome',
            keyword: 'required',
            message: "must have required property 'version'",
            params: {
              missingProperty: 'version'
            },
            schemaPath: '#/properties/ome/allOf/0/required'
          }
        ])
      })
    );
  });

  it('missing name', () => {
    expect(() => validate({ ome: { version: '0.x', type: 'collection' } })).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome',
            schemaPath: '#/required',
            keyword: 'required',
            params: { missingProperty: 'name' },
            message: "must have required property 'name'"
          }
        ])
      })
    );
  });

  it('invalid id', () => {
    expect(() =>
      validate({ ome: { version: '0.x', type: 'collection', name: 'foo', id: '' } })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/id',
            schemaPath: '#/properties/id/pattern',
            keyword: 'pattern',
            params: { pattern: '^[a-zA-Z0-9-_.]+$' },
            message: 'must match pattern "^[a-zA-Z0-9-_.]+$"'
          }
        ])
      })
    );
  });

  it('invalid attributes type', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          type: 'collection',
          name: 'foo',
          attributes: []
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/attributes',
            schemaPath: '#/properties/attributes/type',
            keyword: 'type',
            params: { type: 'object' },
            message: 'must be object'
          }
        ])
      })
    );
  });

  it('valid empty labels', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'multiscale',
              name: 'foo',
              attributes: {
                labels: {},
                coordinateSystems: [
                  {
                    id: 'x',
                    axes: [
                      {
                        name: 'x',
                        type: 'space',
                        unit: 'micrometer'
                      },
                      {
                        name: 'y',
                        type: 'space',
                        unit: 'micrometer'
                      }
                    ]
                  }
                ]
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).not.toThrow();
  });

  it('labels attribute missing label value', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'multiscale',
              name: 'foo',
              attributes: {
                labels: { labelAttributes: [{}] },
                coordinateSystems: [
                  {
                    id: 'x',
                    axes: [
                      {
                        name: 'x',
                        type: 'space',
                        unit: 'micrometer'
                      },
                      {
                        name: 'y',
                        type: 'space',
                        unit: 'micrometer'
                      }
                    ]
                  }
                ]
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0/attributes/labels/labelAttributes/0',
            keyword: 'required',
            message: "must have required property 'labelValue'",
            params: {
              missingProperty: 'labelValue'
            },
            schemaPath: '#/properties/labelAttributes/items/required'
          }
        ])
      })
    );
  });

  it('valid label attributes', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'multiscale',
              name: 'foo',
              attributes: {
                labels: {
                  labelAttributes: [{ labelValue: 1, color: [0, 255, 100, 255] }]
                },
                coordinateSystems: [
                  {
                    id: 'x',
                    axes: [
                      {
                        name: 'x',
                        type: 'space',
                        unit: 'micrometer'
                      },
                      {
                        name: 'y',
                        type: 'space',
                        unit: 'micrometer'
                      }
                    ]
                  }
                ]
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).not.toThrow();
  });

  it('invalid label colors', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'multiscale',
              name: 'foo',
              attributes: {
                labels: {
                  labelAttributes: [{ labelValue: 1, color: [0] }]
                },
                coordinateSystems: [
                  {
                    id: 'x',
                    axes: [
                      {
                        name: 'x',
                        type: 'space',
                        unit: 'micrometer'
                      },
                      {
                        name: 'y',
                        type: 'space',
                        unit: 'micrometer'
                      }
                    ]
                  }
                ]
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0/attributes/labels/labelAttributes/0/color',
            keyword: 'minItems',
            message: 'must NOT have fewer than 4 items',
            params: {
              limit: 4
            },
            schemaPath: '#/properties/labelAttributes/items/properties/color/minItems'
          }
        ])
      })
    );
  });

  it('valid singlescale', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'singlescale',
              name: 'single',
              attributes: {
                coordinateTransformations: [
                  {
                    type: 'translation',
                    translation: [0, 0, 100],
                    input: {
                      id: 'physical',
                      path: { type: 'json', path: './foo.json' }
                    },
                    output: { id: 'world' }
                  }
                ]
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).not.toThrow();
  });

  it('missing attributes in multiscale', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'multiscale',
              name: 'foo',
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0',
            keyword: 'required',
            message: "must have required property 'attributes'",
            params: {
              missingProperty: 'attributes'
            },
            schemaPath: '#/required'
          }
        ])
      })
    );
  });

  it('invalid coordinateTransformations: missing type', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'singlescale',
              name: 'single',
              attributes: {
                coordinateTransformations: [
                  {
                    translation: [0, 0, 100],
                    input: {
                      id: 'physical',
                      path: {
                        type: 'json',
                        path: './foo.json'
                      }
                    },
                    output: { id: 'world' }
                  }
                ]
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0/attributes/coordinateTransformations/0',
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

  it('invalid coordinateTransformations: missing output id', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'singlescale',
              name: 'single',
              attributes: {
                coordinateTransformations: [
                  {
                    type: 'translation',
                    translation: [0, 0, 100],
                    input: {
                      id: 'physical',
                      path: {
                        type: 'json',
                        path: './foo.json'
                      }
                    },
                    output: {}
                  }
                ]
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0/attributes/coordinateTransformations/0/output',
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

  it('valid scene', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'collection',
              name: 'name',
              attributes: {
                scene: {
                  coordinateTransformations: [
                    {
                      type: 'translation',
                      translation: [0, 0, 100],
                      input: { id: 'physical' },
                      output: { id: 'world' }
                    }
                  ],
                  coordinateSystems: [
                    {
                      id: 'physical',
                      name: 'The physical coordinate system',
                      axes: [
                        {
                          name: 'x',
                          type: 'space',
                          unit: 'micrometer'
                        },
                        {
                          name: 'y',
                          type: 'space',
                          unit: 'micrometer'
                        }
                      ]
                    }
                  ]
                }
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).not.toThrow();
  });

  it('invalid scene: missing coordinateTransformations', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'collection',
              name: 'name',
              attributes: {
                scene: {
                  coordinateSystems: [
                    {
                      id: 'physical',
                      name: 'The physical coordinate system',
                      axes: [
                        {
                          name: 'x',
                          type: 'space',
                          unit: 'micrometer'
                        },
                        {
                          name: 'y',
                          type: 'space',
                          unit: 'micrometer'
                        }
                      ]
                    }
                  ]
                }
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0/attributes/scene',
            keyword: 'required',
            message: "must have required property 'coordinateTransformations'",
            params: {
              missingProperty: 'coordinateTransformations'
            },
            schemaPath: '#/required'
          }
        ])
      })
    );
  });

  it('invalid scene: missing coordinateSystem id', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'collection',
              name: 'name',
              attributes: {
                scene: {
                  coordinateTransformations: [
                    {
                      type: 'translation',
                      translation: [0, 0, 100],
                      input: { id: 'physical' },
                      output: { id: 'world' }
                    }
                  ],
                  coordinateSystems: [
                    {
                      name: 'The physical coordinate system',
                      axes: [
                        {
                          name: 'x',
                          type: 'space',
                          unit: 'micrometer'
                        },
                        {
                          name: 'y',
                          type: 'space',
                          unit: 'micrometer'
                        }
                      ]
                    }
                  ]
                }
              },
              path: { type: 'json', path: './foo.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0/attributes/scene/coordinateSystems/0',
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

  it('invalid multiscale: missing nodes or path', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'multiscale',
              name: 'multi',
              attributes: {
                coordinateSystems: [
                  {
                    id: 'coord',
                    axes: [
                      {
                        name: 'x',
                        type: 'space',
                        unit: 'micrometer'
                      },
                      {
                        name: 'y',
                        type: 'space',
                        unit: 'micrometer'
                      }
                    ]
                  }
                ]
              }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0',
            schemaPath: '#/allOf/2/oneOf/0/required',
            keyword: 'required',
            params: { missingProperty: 'nodes' },
            message: "must have required property 'nodes'"
          },
          {
            instancePath: '/ome/nodes/0',
            schemaPath: '#/allOf/2/oneOf/1/required',
            keyword: 'required',
            params: { missingProperty: 'path' },
            message: "must have required property 'path'"
          }
        ])
      })
    );
  });

  it('invalid multiscale: both nodes and path', () => {
    expect(() =>
      validate({
        ome: {
          version: '0.x',
          name: 'root',
          type: 'collection',
          nodes: [
            {
              type: 'multiscale',
              name: 'multi',
              attributes: {
                coordinateSystems: [
                  {
                    id: 'coord',
                    axes: [
                      {
                        name: 'x',
                        type: 'space',
                        unit: 'micrometer'
                      },
                      {
                        name: 'y',
                        type: 'space',
                        unit: 'micrometer'
                      }
                    ]
                  }
                ]
              },
              nodes: [],
              path: { type: 'json', path: './invalid.json' }
            }
          ]
        }
      })
    ).toThrow(
      expect.objectContaining({
        message: 'JSON schema validation failed',
        schemaErrors: expect.arrayContaining([
          {
            instancePath: '/ome/nodes/0',
            schemaPath: '#/allOf/1/not',
            keyword: 'not',
            params: {},
            message: 'must NOT be valid'
          }
        ])
      })
    );
  });
});
