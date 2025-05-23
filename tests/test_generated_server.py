import importlib.util
import os
import sys
import types
import pytest

# Dynamically import the generated mcp_server.py as a module
def import_generated_server(path):
    spec = importlib.util.spec_from_file_location("mcp_server", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mcp_server"] = module
    spec.loader.exec_module(module)
    return module

generated_dir = os.path.join(os.path.dirname(__file__), "out")
# Find the generated subdir (should start with openapi-mcp-reference-test-api-)
generated_subdir = next(
    d for d in os.listdir(generated_dir)
    if d.startswith("openapi-mcp-reference-test-api-")
)
generated_path = os.path.join(generated_dir, generated_subdir, "mcp_server.py")

mcp_server = import_generated_server(generated_path)

def test_get_api_info():
    info = mcp_server.get_api_info()
    assert "Reference Test API" in info
    assert "Version: 1.0.0" in info

def test_get_BadRequestDetails_schema():
    schema = mcp_server.get_BadRequestDetails_schema()
    assert "oneOf" in schema
    assert "error_type" in schema

def test_get_ErrorModel_schema():
    schema = mcp_server.get_ErrorModel_schema()
    assert "code" in schema
    assert "message" in schema

def test_get_DataReturned_schema():
    schema = mcp_server.get_DataReturned_schema()
    assert "data" in schema
    assert "type: object" in schema
