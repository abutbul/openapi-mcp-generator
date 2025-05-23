# OpenAPI to MCP Server Generator

A Python tool that automatically converts OpenAPI specifications into fully functional Model Context Protocol (MCP) servers. Generates Docker-ready implementations with support for SSE/IO communication protocols, authentication, and comprehensive error handling.

## Key features:

- 🔄 OpenAPI to MCP tools/resources conversion
- 🐳 Docker-ready with multi-stage builds
- 🔐 Multiple authentication methods
- ⚡ Async operations & rate limiting
- 📡 SSE/IO communication protocols
- 📦 Modular code structure with package support

## Modular Code Structure

The generator has been refactored into a proper Python package while maintaining backward compatibility:

1. **Original Entry Point**: The `generator.py` script still works exactly as before
2. **Modular Organization**: Code is now split into focused modules
3. **Package Installation**: Can be installed as a proper Python package
4. **Same Templates**: Uses the exact same templates in the `/templates` directory
5. **Docker Support**: Preserves all Docker functionality

You can use the tool in whatever way you prefer:
1. Run `generator.py` directly (original approach)
2. Install as a package and use `mcp-generator` command
3. Use the module programmatically in your own Python code

For more details on the modular code structure, see [MODULAR_REFACTORING.md](MODULAR_REFACTORING.md).

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
- pip or uv (Python package manager)

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/abutbul/openapi-mcp-generator.git
cd openapi-mcp-generator

# Install as a package (development mode)
pip install -e .

# Or using uv
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Using pip (once published)

```bash
pip install openapi-mcp-generator
```

## Usage

```bash
# Using the original script (still works the same way)
python generator.py openapi.yaml --output-dir ./output --api-url https://api.example.com

# Using the new modular CLI tool after installation
mcp-generator openapi.yaml --output-dir ./output --api-url https://api.example.com

# Using the python module directly
python -m openapi_mcp_generator.cli openapi.yaml --output-dir ./output
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
- `logs`: View container logs

## Project Structure

The modular generator has the following structure:

```
openapi-mcp-generator/
├── generator.py              # Original entry point (maintained for backward compatibility)
├── mcp_generator.py          # New entry point (uses the modular structure)
├── openapi_mcp_generator/    # Main package (new modular structure)
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── generator.py          # Main generator module
│   ├── generators.py         # Code generators for tools/resources
│   ├── http.py               # HTTP client utilities
│   ├── parser.py             # OpenAPI parser
│   └── project.py            # Project builder
├── templates/                # Original templates directory (used by the modular code)
│   ├── config/
│   ├── docker/
│   ├── server/
│   ├── pyproject.toml
│   └── requirements.txt
├── samples/                  # Sample implementations
├── tests/                    # Test cases
├── LICENSE                   # License file
├── README.md                 # This file
├── pyproject.toml            # Project metadata
└── setup.py                  # Package setup
```

The modular structure preserves all the existing functionality while making the code more maintainable:

1. The original entry point (`generator.py`) can still be used as before
2. The existing templates in `/templates` are used by the new modular code
3. All Docker-related functionality is preserved exactly as it was
4. The project can now be installed as a proper Python package

## Sample Implementations

Check out our sample implementations to see the generator in action:

- [Trilium Notes ETAPI Server](./samples/TriliumNext/README.md) - An MCP server for the Trilium Notes knowledge management system's ETAPI

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Usage Examples

### 1. Using the library without installing (direct from source)

To generate an MCP server from the Elasticsearch 6.1 spec folder:

```bash
# Run the original script directly
python generator.py samples/elasticsearch_6.1/api

# Or use the modular entry point
python mcp_generator.py samples/elasticsearch_6.1/api
```

### 2. Using the library after installing with pip

First, install the package (from the project root):

```bash
pip install .
```

Then use the CLI tool to convert the Trilium ETAPI spec:

```bash
mcp-generator samples/TriliumNext/etapi.openapi.yaml
```

Or use it programmatically in your own Python code:

```python
from openapi_mcp_generator import generator

generator.generate('samples/TriliumNext/etapi.openapi.yaml')
```
