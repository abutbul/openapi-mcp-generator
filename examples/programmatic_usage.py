#!/usr/bin/env python3
"""
Example of using the openapi_mcp_generator package programmatically.

This script shows how to use the modular package in your own Python code.
"""

from openapi_mcp_generator import generate_mcp_server, parse_openapi_spec

def main():
    """Example of using the generator programmatically."""
    # Generate an MCP server for an OpenAPI spec
    project_dir = generate_mcp_server(
        openapi_file="path/to/openapi.yaml",
        output_dir="./output",
        api_url="https://api.example.com",
        auth_type="bearer",
        api_token="your-token"
    )
    
    print(f"Server generated at: {project_dir}")
    
    # Example of parsing an OpenAPI spec
    spec = parse_openapi_spec("path/to/openapi.yaml")
    print(f"API title: {spec.get('info', {}).get('title', 'Unknown')}")

if __name__ == "__main__":
    main()
