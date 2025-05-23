#!/usr/bin/env python3
"""
Compatibility example showing how to use both the original and modular approaches.

This script demonstrates that both the original and modular code can be used 
interchangeably with the same templates and functionality.
"""

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Example OpenAPI file path - use a sample from the samples directory
sample_openapi_file = os.path.join(project_root, "tests", "openapi.yaml")

# Create output directories
original_output_dir = os.path.join(project_root, "output", "original")
modular_output_dir = os.path.join(project_root, "output", "modular")

os.makedirs(original_output_dir, exist_ok=True)
os.makedirs(modular_output_dir, exist_ok=True)

# Method 1: Use the original generator.py directly
print("Method 1: Using the original generator.py directly")
print("=" * 60)
original_command = f"python {os.path.join(project_root, 'generator.py')} {sample_openapi_file} --output-dir={original_output_dir} --api-url=http://localhost:8000"
print(f"Running: {original_command}")
print("-" * 60)
os.system(original_command)
print("\n")

# Method 2: Import and use the modular generator
print("Method 2: Using the modular package programmatically")
print("=" * 60)
sys.path.insert(0, project_root)
from openapi_mcp_generator.generator import generate_mcp_server

print("Calling generate_mcp_server function from the modular package...")
project_dir = generate_mcp_server(
    sample_openapi_file,
    modular_output_dir,
    api_url="http://localhost:8000",
    auth_type="bearer",
    api_token="your-token"
)
print(f"MCP server generated successfully in: {project_dir}")
print(f"To build and run the Docker container:")
print(f"  cd {project_dir}")
print(f"  ./docker.sh build")
print(f"  ./docker.sh start --transport=sse")
print("\n")

# Method 3: Use the CLI script if installed
print("Method 3: Using the CLI tool (if installed with pip install -e .)")
print("=" * 60)
print("This would normally be run as:")
print(f"mcp-generator {sample_openapi_file} --output-dir={modular_output_dir} --api-url=http://localhost:8000")
print("Or as:")
print(f"python -m openapi_mcp_generator.cli {sample_openapi_file} --output-dir={modular_output_dir} --api-url=http://localhost:8000")
print("\n")

print("Summary")
print("=" * 60)
print("All methods use the exact same templates in the /templates directory")
print("All methods generate Docker-ready MCP servers with identical functionality")
print("All the core features remain the same regardless of which approach you use")
