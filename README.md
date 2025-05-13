# OpenAPI to MCP Server Generator

A Python tool that automatically converts OpenAPI specifications into fully functional Model Context Protocol (MCP) servers. Generates Docker-ready implementations with support for SSE/IO communication protocols, authentication, and comprehensive error handling.

## Key features:

🔄 OpenAPI to MCP tools/resources conversion
🐳 Docker-ready with multi-stage builds
🔐 Multiple authentication methods
⚡ Async operations & rate limiting
📡 SSE/IO communication protocols

## Overview

This generator creates a fully functional MCP server implementation that exposes API operations defined in an OpenAPI specification as MCP tools and resources. The generated server is packaged with Docker for easy deployment and supports both SSE and IO communication protocols.

## Features

- Convert OpenAPI specifications to MCP servers
- Docker-ready implementation with multi-stage builds
- Support for multiple authentication methods
- Choice of SSE or IO communication protocols
- Comprehensive error handling and logging
- Built-in rate limiting and security features
- Async operations for optimal performance
- Extensive test suite with coverage reporting

## Prerequisites

- Python 3.10+
- Docker (for running the generated server)
- uv (Python package manager)

## Installation

```bash
# Clone the repository
git clone https://github.com/abutbul/openapi-mcp-generator.git
cd openapi-mcp-generator

# Install dependencies using uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

```bash
python generator.py openapi.yaml --output-dir ./output --api-url https://api.example.com
```

### Command Line Options

- `openapi_file`: Path to the OpenAPI YAML file (required)
- `--output-dir`: Output directory for the generated project (default: '.')
- `--api-url`: Base URL for the API
- `--auth-type`: Authentication type (bearer, token, basic)
- `--api-token`: API token for authentication
- `--api-username`: Username for basic authentication
- `--api-password`: Password for basic authentication

## Running the Generated Server

After generating the server, you can build and run it using Docker:

```bash
cd output/openapi-mcp-*
./docker.sh build
./docker.sh start --transport=sse --port=8000
```

### Docker Script Options

The generated `docker.sh` script supports the following commands:

- `build`: Build the Docker image
- `start`: Start the container
  - `--port=PORT`: Set the port (default: 8000)
  - `--transport=TYPE`: Set transport type: 'sse' or 'io' (default: sse)
  - `--log-level=LEVEL`: Set logging level (default: info)
- `stop`: Stop the container
- `clean`: Remove the container and image
- `test`: Run the test suite (TBD)
- `logs`: View container logs

## Documentation

For more detailed information, see:

TBD

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request


## License

This project is licensed under the MIT License - see the (./LICENSE) file for details.
