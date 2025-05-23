"""
Code Generator Module.

This module contains functions for generating MCP tool and resource definitions
from OpenAPI specifications.
"""

import yaml
from typing import Dict, Any, List
from .parser import sanitize_description, resolve_reference


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
                tool_def = _generate_tool(spec, path, method, operation)
                if tool_def:
                    tools.append(tool_def)
    
    return '\n'.join(tools)


def _generate_tool(spec: Dict[str, Any], path: str, method: str, operation: Dict[str, Any]) -> str:
    """
    Generate a single MCP tool definition from an OpenAPI operation.
    
    Args:
        spec: The parsed OpenAPI specification
        path: The path for the operation
        method: The HTTP method (get, post, etc.)
        operation: The operation definition
        
    Returns:
        String containing the generated tool definition or empty string if skipped
    """
    # Skip operations that don't have an operationId
    if 'operationId' not in operation:
        return ""
    
    operation_id = operation['operationId']
    description = sanitize_description(operation.get('description', f"{method.upper()} {path}"))
    
    # Get parameters
    parameters_definitions = _get_parameter_definitions(spec, operation)
    
    # Add ctx parameter
    parameters_definitions.append("ctx: Context")
    
    # Create tool function
    return f"""
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


def _get_parameter_definitions(spec: Dict[str, Any], operation: Dict[str, Any]) -> List[str]:
    """
    Get parameter definitions for a tool function.
    
    Args:
        spec: The parsed OpenAPI specification
        operation: The operation definition
        
    Returns:
        List of parameter definition strings
    """
    parameters_definitions = []
    for param_obj in operation.get('parameters', []):
        actual_param = {}
        if '$ref' in param_obj:
            ref_path = param_obj['$ref']
            actual_param = resolve_reference(spec, ref_path)
        else:
            actual_param = param_obj

        if not actual_param or 'name' not in actual_param:
            print(f"Warning: Skipping parameter due to missing name or unresolved reference: {param_obj}")
            continue
            
        param_name = actual_param['name']
        param_type = _get_param_type(actual_param)
        
        parameters_definitions.append(f"{param_name}: {param_type}")
    
    return parameters_definitions


def _get_param_type(param: Dict[str, Any]) -> str:
    """
    Determine the Python type for a parameter.
    
    Args:
        param: The parameter definition
        
    Returns:
        Python type as a string
    """
    param_type = "str"  # Default to string
    
    # Try to determine appropriate Python type
    if 'schema' in param:
        schema_type = param['schema'].get('type', 'string')
        if schema_type == 'integer':
            param_type = "int"
        elif schema_type == 'number':
            param_type = "float"
        elif schema_type == 'boolean':
            param_type = "bool"
    
    return param_type


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
    info_resource = _generate_api_info_resource(spec)
    resources.append(info_resource)
    
    # Create resources for schemas
    schema_resources = _generate_schema_resources(spec)
    resources.extend(schema_resources)
    
    return '\n'.join(resources)


def _generate_api_info_resource(spec: Dict[str, Any]) -> str:
    """
    Generate a resource for API information.
    
    Args:
        spec: The parsed OpenAPI specification
        
    Returns:
        String containing the generated resource definition
    """
    info = spec.get('info', {})
    api_title = info.get('title', 'API')
    api_version = info.get('version', '1.0.0')
    api_description = sanitize_description(info.get('description', 'API description'))
    
    return f"""
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


def _generate_schema_resources(spec: Dict[str, Any]) -> List[str]:
    """
    Generate resources for API schema components.
    
    Args:
        spec: The parsed OpenAPI specification
        
    Returns:
        List of resource definition strings
    """
    schema_resources = []
    
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
        schema_resources.append(resource_def)
    
    return schema_resources
