"""
Main Generator Module.

This module ties together the parsing, code generation, and project creation
to generate a complete MCP server implementation.
"""

import os
from typing import Dict, Any
from .parser import parse_openapi_spec
from .generators import generate_tool_definitions, generate_resource_definitions
from .project import ProjectBuilder
from .http import generate_http_client_template

# Get the path to the templates directory
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")


def generate_mcp_server(
    openapi_file: str, 
    output_dir: str, 
    api_url: str = "", 
    auth_type: str = "bearer",  # Default to bearer auth
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
    spec = parse_openapi_spec(openapi_file)
    
    # Get API info
    api_name = spec.get('info', {}).get('title', 'API')
    
    # Initialize project builder
    project_builder = ProjectBuilder(TEMPLATE_DIR)
    
    # Create project directory
    project_dir = project_builder.create_project_directory(output_dir, api_name)
    
    # Generate MCP tool and resource definitions
    tool_defs = generate_tool_definitions(spec)
    resource_defs = generate_resource_definitions(spec)
    
    # Get server URL from spec if not provided
    if not api_url and 'servers' in spec and spec['servers']:
        api_url = spec['servers'][0].get('url', '')
    
    # Set up template context
    template_context = _create_template_context(
        api_name=api_name,
        api_url=api_url,
        auth_type=auth_type,
        api_token=api_token,
        project_dir=project_dir,
        tool_defs=tool_defs,
        resource_defs=resource_defs
    )
    
    # Generate project files
    project_builder.generate_project_files(project_dir, template_context)
    
    return project_dir


def _create_template_context(
    api_name: str,
    api_url: str,
    auth_type: str,
    api_token: str,
    project_dir: str,
    tool_defs: str,
    resource_defs: str
) -> Dict[str, Any]:
    """
    Create the template context for rendering templates.
    
    Args:
        api_name: Name of the API
        api_url: Base URL for the API
        auth_type: Authentication type
        api_token: API token for authentication
        project_dir: Path to the project directory
        tool_defs: Generated tool definitions
        resource_defs: Generated resource definitions
        
    Returns:
        Template context dictionary
    """
    container_name = os.path.basename(project_dir)
    image_name = container_name.lower()
    project_name = container_name.lower().replace('-', '_')
    
    # Generate HTTP client code
    http_client_code = generate_http_client_template(
        api_url=api_url,
        auth_type=auth_type,
        api_token=api_token
    )
    
    return {
        'api_name': api_name,
        'api_url': api_url,
        'auth_type': 'bearer',  # Always use bearer auth
        'api_token': api_token,  # Pass through directly
        'api_username': '',
        'api_password': '',
        'container_name': container_name,
        'image_name': image_name,
        'project_name': project_name,
        'mcp_server_name': f"{api_name} MCP Server",
        'tool_definitions': tool_defs,
        'resource_definitions': resource_defs,
        'http_client_code': http_client_code
    }
