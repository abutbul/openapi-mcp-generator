import importlib.util
import os
import sys
import types
import pytest
import json

# Dynamically import the generated mcp_server.py as a module
def import_generated_server(path):
    spec = importlib.util.spec_from_file_location("mcp_server", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mcp_server"] = module
    spec.loader.exec_module(module)
    return module

generated_dir = os.path.join(os.path.dirname(__file__), "out")
# Find all generated subdirs (should start with openapi-mcp-reference-test-api- or openapi-mcp-generated-api-)
generated_subdirs = []
for d in os.listdir(generated_dir):
    if d.startswith("openapi-mcp-reference-test-api-") or d.startswith("openapi-mcp-generated-api-"):
        generated_subdirs.append(d)

if not generated_subdirs:
    raise FileNotFoundError("No generated MCP server directory found in tests/out/")

# Import all available generated servers
generated_servers = []
for subdir in generated_subdirs:
    generated_path = os.path.join(generated_dir, subdir, "mcp_server.py")
    # Create a unique module name for each server
    module_name = f"mcp_server_{subdir.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, generated_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    generated_servers.append((subdir, module))

# For backwards compatibility, set mcp_server to the first one found
mcp_server = generated_servers[0][1]

# Path to test fixtures
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "test_fixtures")

def load_fixture(fixture_name):
    """Load a JSON fixture from the test_fixtures directory"""
    fixture_path = os.path.join(FIXTURES_DIR, fixture_name)
    with open(fixture_path, 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("server_info", generated_servers, ids=[s[0] for s in generated_servers])
def test_get_api_info(server_info):
    subdir, mcp_server = server_info
    info = mcp_server.get_api_info()
    
    # Check if this is the Reference Test API (from openapi.yaml) or Generated API (from JSON)
    if "Reference Test API" in info:
        # Testing openapi.yaml generated server
        expected = load_fixture("api_info.json")
        assert expected["title"] in info
        assert f"Version: {expected['version']}" in info
        assert "API to test $ref in parameters and oneOf in schemas." in info
    elif "Generated API from JSON Specifications" in info:
        # Testing JSON specifications generated server
        assert "Generated API from JSON Specifications" in info
        assert "Version: 1.0.0" in info
        assert "API generated from 4 JSON specification files" in info
    else:
        pytest.fail(f"Unknown API type in info: {info}")

@pytest.mark.parametrize("server_info", generated_servers, ids=[s[0] for s in generated_servers])
def test_get_BadRequestDetails_schema(server_info):
    subdir, mcp_server = server_info
    # Only test if the function exists (for openapi.yaml generated servers)
    if hasattr(mcp_server, 'get_BadRequestDetails_schema'):
        schema_str = mcp_server.get_BadRequestDetails_schema()
        assert "oneOf" in schema_str
        assert "error_type" in schema_str
        
        # Verify the actual oneOf structure exists
        assert "details:" in schema_str
        assert "Simple error message as a string" in schema_str
    else:
        pytest.skip("BadRequestDetails schema not available in this generated server")

@pytest.mark.parametrize("server_info", generated_servers, ids=[s[0] for s in generated_servers])
def test_get_ErrorModel_schema(server_info):
    subdir, mcp_server = server_info
    # Only test if the function exists (for openapi.yaml generated servers)
    if hasattr(mcp_server, 'get_ErrorModel_schema'):
        schema_str = mcp_server.get_ErrorModel_schema()
        assert "code" in schema_str
        assert "message" in schema_str
    else:
        pytest.skip("ErrorModel schema not available in this generated server")

@pytest.mark.parametrize("server_info", generated_servers, ids=[s[0] for s in generated_servers])
def test_get_DataReturned_schema(server_info):
    subdir, mcp_server = server_info
    # Only test if the function exists (for openapi.yaml generated servers)
    if hasattr(mcp_server, 'get_DataReturned_schema'):
        schema_str = mcp_server.get_DataReturned_schema()
        assert "data" in schema_str
        assert "type: object" in schema_str
        assert "message" in schema_str
    else:
        pytest.skip("DataReturned schema not available in this generated server")

@pytest.mark.parametrize("server_info", generated_servers, ids=[s[0] for s in generated_servers])
def test_server_has_tools(server_info):
    """Test that the server has at least one tool defined"""
    subdir, mcp_server = server_info
    # Get all callable attributes that might be tools
    tools = [attr for attr in dir(mcp_server) if callable(getattr(mcp_server, attr)) and not attr.startswith('_')]
    
    # Filter out known non-tool functions
    non_tool_functions = ['get_api_info', 'get_BadRequestDetails_schema', 'get_ErrorModel_schema', 'get_DataReturned_schema', 'parse_args']
    actual_tools = [tool for tool in tools if tool not in non_tool_functions]
    
    assert len(actual_tools) > 0, f"No tools found in generated server {subdir}. Available functions: {tools}"
