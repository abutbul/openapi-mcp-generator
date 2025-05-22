// tests/sample_openapi.ts

export const openApiSpec = {
  openapi: '3.0.0',
  info: {
    title: 'Sample TS API',
    version: '1.0.0',
    description: 'A sample API defined in TypeScript',
  },
  paths: {
    '/items': {
      get: {
        summary: 'Get all items',
        operationId: 'getItems',
        responses: {
          '200': {
            description: 'A list of items',
            content: {
              'application/json': {
                schema: {
                  type: 'array',
                  items: {
                    type: 'string',
                  },
                },
              },
            },
          },
        },
      },
    },
  },
};
