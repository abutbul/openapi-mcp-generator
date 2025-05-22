#!/usr/bin/env python3
"""
OpenAPI to MCP Server Generator

This script generates a fully functional MCP server implementation based on an OpenAPI specification.
The generated server is Docker-ready and exposes API operations as MCP tools and resources.
"""

import argparse
import os
import sys
# import uuid # No longer directly used by generator.py
# import yaml # No longer directly used by generator.py
# import shutil # No longer directly used by generator.py
# from pathlib import Path # No longer directly used by generator.py
# from typing import Dict, List, Any, Optional, Tuple # No longer directly used by generator.py
from typing import Dict, Any # Still needed for type hints in generate_mcp_server

from jinja2 import Environment, FileSystemLoader

from openapi_parser import OpenAPISpecParser
from mcp_generator import MCPGenerator

# Setup Jinja2 environment for templates
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_mcp_server(
    openapi_file: str, 
    output_dir: str, 
    api_url: str = "", 
    auth_type: str = "bearer",
    api_token: str = "",
    api_username: str = "",
    api_password: str = ""
) -> str:
    """
    Generate an MCP server implementation from an OpenAPI specification.
    
    Args:
        openapi_file: Path to the OpenAPI specification file
        output_dir: Directory where the project will be created
        api_url: Base URL for the API
        auth_type: Authentication type (always bearer for MCP servers)
        api_token: API token for authentication
        api_username: Username for basic authentication (unused)
        api_password: Password for basic authentication (unused)
        
    Returns:
        Path to the generated project directory
    """
    # Parse the OpenAPI specification
    parser = OpenAPISpecParser()
    spec = parser.parse(openapi_file)
    
    # Get API info
    api_name = spec.get('info', {}).get('title', 'API')
    
    # Initialize MCPGenerator
    mcp_gen = MCPGenerator(parsed_spec=spec, template_env=env)
    
    # Create project directory
    project_dir = mcp_gen.create_project_directory(output_dir, api_name)
    
    # Generate project files
    mcp_gen.generate_project_files(
        project_dir=project_dir,
        api_name=api_name,
        api_url=api_url,
        auth_type=auth_type, # This should always be 'bearer' for MCP
        api_token=api_token,
        api_username=api_username,
        api_password=api_password
    )
        
    return project_dir


def main():
    """Main function to parse arguments and generate the MCP server."""
    parser = argparse.ArgumentParser(description='Generate an MCP server from an OpenAPI specification.')
    parser.add_argument('openapi_file', help='Path to the OpenAPI YAML file')
    parser.add_argument('--output-dir', default='.', help='Output directory for the generated project')
    parser.add_argument('--api-url', default='', help='Base URL for the API')
    parser.add_argument('--auth-type', default='bearer', choices=['bearer', 'token', 'basic'], help='Authentication type')
    parser.add_argument('--api-token', default='', help='API token for authentication')
    parser.add_argument('--api-username', default='', help='Username for basic authentication')
    parser.add_argument('--api-password', default='', help='Password for basic authentication')
    
    args = parser.parse_args()
    
    # Generate the MCP server
    project_dir = generate_mcp_server(
        args.openapi_file,
        args.output_dir,
        args.api_url,
        args.auth_type,
        args.api_token,
        args.api_username,
        args.api_password
    )
    
    print(f"MCP server generated successfully in: {project_dir}")
    print(f"To build and run the Docker container:")
    print(f"  cd {project_dir}")
    print(f"  ./docker.sh build")
    print(f"  ./docker.sh start --transport=sse")


if __name__ == "__main__":
    main()
