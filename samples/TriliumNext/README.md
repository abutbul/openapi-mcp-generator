# Trilium Notes ETAPI MCP Server Example

This example demonstrates how to generate an MCP server for the Trilium Notes ETAPI, allowing integration with the Trilium Notes knowledge management system.

## Setup Instructions

1. First, obtain the ETAPI OpenAPI specification:
```bash
wget https://github.com/TriliumNext/Notes/blob/master/src/etapi/etapi.openapi.yaml
```

2. Generate the MCP server:
```bash
python ../../generator.py \
  --output-dir=./trilnext \
  --api-url=http://localhost:8021 \
  --auth-type bearer \
  --api-token "your-token" \
  etapi.openapi.yaml
```

The server will be generated at: `./trilnext/openapi-mcp-etapi-uuid`

3. Build and run the Docker container:
```bash
cd ./trilnext/openapi-mcp-etapi-uuid
./docker.sh build
./docker.sh start --transport=sse
```

## Configuration

- Default API URL: `http://localhost:8021` (standard Trilium Notes ETAPI port)
- Authentication: Bearer token (obtained from Trilium Notes settings)
- Transport: SSE (Server-Sent Events)

## Available ETAPI Operations

The generated MCP server provides tools for all Trilium Notes ETAPI operations, including:

- Note management (create, read, update, delete)
- Attachment handling
- Branch operations
- Attribute management
- Day/Week/Month/Year note operations
- Backup creation
- Authentication

## Testing

You can test the connection to your Trilium Notes instance by accessing the `/api/app-info` endpoint through the MCP server.