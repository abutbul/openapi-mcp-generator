"""
Command Line Interface Module.

This module provides the command-line interface for the OpenAPI to MCP generator.
"""

import argparse
import sys
import os
from .generator import generate_mcp_server


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
    
    try:
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
        return 0
    except Exception as e:
        print(f"Error generating MCP server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
