#!/usr/bin/env python3
"""
OpenAPI to MCP Server Generator

This script generates a fully functional MCP server implementation based on an OpenAPI specification.
The generated server is Docker-ready and exposes API operations as MCP tools and resources.
"""

import argparse
import os
import sys
import uuid
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from jinja2 import Environment, FileSystemLoader

# Setup Jinja2 environment for templates
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Try to import from the modular version - if it fails, we'll use the original implementation
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from openapi_mcp_generator.generator import generate_mcp_server as modular_generate
    USE_MODULAR = True
except ImportError:
    USE_MODULAR = False


def parse_openapi_spec(filepath: str) -> Dict[str, Any]:
    """
    Parse an OpenAPI specification file.
    
    Args:
        filepath: Path to the OpenAPI YAML file
        
    Returns:
        Dictionary containing the parsed OpenAPI specification
        
    Raises:
        SystemExit: If the file cannot be read or parsed
    """
    if not os.path.exists(filepath):
        print(f"Error: OpenAPI specification file not found: {filepath}")
        sys.exit(1)
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                spec = yaml.safe_load(content)
                if not isinstance(spec, dict):
                    print(f"Error: OpenAPI specification must be a YAML document containing an object, got {type(spec)}")
                    sys.exit(1)
                return spec
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in OpenAPI specification: {e}")
                sys.exit(1)
    except IOError as e:
        print(f"Error reading OpenAPI specification file: {e}")
        sys.exit(1)


def sanitize_description(desc: str) -> str:
    """Remove newlines and escape quotes to prevent unterminated strings."""
    return desc.replace("\n", " ").replace('"', '\\"')


def generate_tool_definitions(spec: Dict[str, Any]) -> str:
    """
    Generate MCP tool definitions from OpenAPI paths.
    
    Args:
        spec: The parsed OpenAPI specification
        
    Returns:
        String containing the generated tool definitions
    """
    tools = []
    
    for path, path_item in spec.get('paths', {}).items():
        for method, operation in path_item.items():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                # Skip operations that don't have an operationId
                if 'operationId' not in operation:
                    continue
                
                operation_id = operation['operationId']
                description = sanitize_description(operation.get('description', f"{method.upper()} {path}"))
                
                # Get parameters
                parameters_definitions = []
                for param_obj in operation.get('parameters', []):
                    actual_param = {}
                    if '$ref' in param_obj:
                        ref_path = param_obj['$ref']
                        # Resolve the reference, e.g., #/components/parameters/IdRequired
                        try:
                            parts = ref_path.strip('#/').split('/')
                            resolved_obj = spec
                            for part in parts:
                                resolved_obj = resolved_obj[part]
                            actual_param = resolved_obj
                        except KeyError:
                            print(f"Warning: Could not resolve parameter reference: {ref_path}")
                            continue
                    else:
                        actual_param = param_obj

                    if not actual_param or 'name' not in actual_param:
                        print(f"Warning: Skipping parameter due to missing name or unresolved reference: {param_obj}")
                        continue
                        
                    param_name = actual_param['name']
                    param_type = "str"  # Default to string
                    
                    # Try to determine appropriate Python type
                    if 'schema' in actual_param:
                        schema_type = actual_param['schema'].get('type', 'string')
                        if schema_type == 'integer':
                            param_type = "int"
                        elif schema_type == 'number':
                            param_type = "float"
                        elif schema_type == 'boolean':
                            param_type = "bool"
                    
                    parameters_definitions.append(f"{param_name}: {param_type}")
                
                # Add ctx parameter
                parameters_definitions.append("ctx: Context")
                
                # Create tool function
                tool_def = f"""
@mcp.tool(description="{description}")
async def {operation_id}({', '.join(parameters_definitions)}) -> str:
    \"\"\"
    {description}
    \"\"\"
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "{path}"
            
            # Extract query parameters
            query_params = {{}}
            # ... build query params from function args
            
            # Make the request
            response = await client.{method}(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {{e.response.status_code}} - {{e.response.text}}"
        except Exception as e:
            return f"Error: {{str(e)}}"
"""
                tools.append(tool_def)
    
    return '\n'.join(tools)


def generate_resource_definitions(spec: Dict[str, Any]) -> str:
    """
    Generate MCP resource definitions from OpenAPI components.
    
    Args:
        spec: The parsed OpenAPI specification
        
    Returns:
        String containing the generated resource definitions
    """
    resources = []
    
    # Create a resource for API info
    info = spec.get('info', {})
    api_title = info.get('title', 'API')
    api_version = info.get('version', '1.0.0')
    api_description = info.get('description', 'API description')
    
    info_resource = f"""
@mcp.resource("api://info")
def get_api_info() -> str:
    \"\"\"
    Get API information
    \"\"\"
    return f\"\"\"
    Title: {api_title}
    Version: {api_version}
    Description: {api_description}
    \"\"\"
"""
    resources.append(info_resource)
    
    # Create resources for schemas
    for schema_name, schema in spec.get('components', {}).get('schemas', {}).items():
        resource_def = f"""
@mcp.resource("schema://{schema_name}")
def get_{schema_name}_schema() -> str:
    \"\"\"
    Get the {schema_name} schema definition
    \"\"\"
    return \"\"\"
    {yaml.dump(schema, default_flow_style=False)}
    \"\"\"
"""
        resources.append(resource_def)
    
    return '\n'.join(resources)


def create_project_directory(output_dir: str, api_name: str) -> str:
    """
    Create a new project directory with a unique ID.
    
    Args:
        output_dir: The base output directory
        api_name: The name of the API
        
    Returns:
        The path to the created directory
    """
    # Create a sanitized version of the API name
    sanitized_name = ''.join(c if c.isalnum() else '-' for c in api_name.lower())
    
    # Create a unique directory name
    unique_id = str(uuid.uuid4())[:8]
    dir_name = f"openapi-mcp-{sanitized_name}-{unique_id}"
    full_path = os.path.join(output_dir, dir_name)
    
    # Create the directory
    os.makedirs(full_path, exist_ok=True)
    
    return full_path


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
    # Use the modular implementation if available
    if USE_MODULAR:
        try:
            return modular_generate(
                openapi_file,
                output_dir,
                api_url,
                auth_type,
                api_token,
                api_username,
                api_password
            )
        except Exception as e:
            print(f"Warning: Error using modular implementation: {e}")
            print("Falling back to original implementation...")
    
    # Original implementation
    # Parse the OpenAPI specification
    spec = parse_openapi_spec(openapi_file)
    
    # Get API info
    api_name = spec.get('info', {}).get('title', 'API')
    
    # Create project directory
    project_dir = create_project_directory(output_dir, api_name)
    
    # Generate MCP tool and resource definitions
    tool_defs = generate_tool_definitions(spec)
    resource_defs = generate_resource_definitions(spec)
    
    # Get server URL from spec if not provided
    if not api_url and 'servers' in spec and spec['servers']:
        api_url = spec['servers'][0].get('url', '')
    
    # Set up template context
    container_name = os.path.basename(project_dir)
    image_name = container_name.lower()
    project_name = container_name.lower().replace('-', '_')
    
    # Pass api_token through directly instead of environment variable placeholder
    template_context = {
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
        'resource_definitions': resource_defs
    }
    
    # Render and write templates
    render_template('docker/Dockerfile', os.path.join(project_dir, 'Dockerfile'), template_context)
    render_template('docker/docker.sh', os.path.join(project_dir, 'docker.sh'), template_context)
    render_template('config/.env.sh', os.path.join(project_dir, '.env.sh'), template_context)
    render_template('server/mcp_server.py', os.path.join(project_dir, 'mcp_server.py'), template_context)
    render_template('requirements.txt', os.path.join(project_dir, 'requirements.txt'), template_context)
    render_template('pyproject.toml', os.path.join(project_dir, 'pyproject.toml'), template_context)
    
    # Set executable permissions
    os.chmod(os.path.join(project_dir, 'docker.sh'), 0o755)
    os.chmod(os.path.join(project_dir, '.env.sh'), 0o755)
    os.chmod(os.path.join(project_dir, 'mcp_server.py'), 0o755)
    
    return project_dir


def render_template(template_path: str, output_path: str, context: Dict[str, Any]) -> None:
    """
    Render a Jinja2 template to a file.
    
    Args:
        template_path: Path to the template file (relative to templates dir)
        output_path: Path where the rendered file will be saved
        context: Dictionary with template variables
    """
    template = env.get_template(template_path)
    rendered = template.render(**context)
    
    with open(output_path, 'w') as f:
        f.write(rendered)


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
