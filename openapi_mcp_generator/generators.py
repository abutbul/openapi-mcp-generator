"""
Code Generator Module.

This module contains functions for generating MCP tool and resource definitions
from OpenAPI specifications.
"""

import yaml
from typing import Dict, Any, List, Tuple
from .parser import sanitize_description, sanitize_identifier, escape_string_literal, resolve_ref


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
    
    operation_id = sanitize_identifier(operation['operationId'])
    description = escape_string_literal(operation.get('description', f"{method.upper()} {path}"))
    
    # Get parameters separated by required vs optional
    required_params, optional_params = _get_parameter_definitions(spec, operation)
    
    # Combine parameters in correct order: required params, ctx, optional params
    parameters_definitions = required_params + ["ctx: Context"] + optional_params
    
    # Generate parameter processing code
    param_processing = _generate_parameter_processing(spec, operation, path)
    
    # Create tool function
    return f"""
@mcp.tool(description="{description}")
async def {operation_id}({', '.join(parameters_definitions)}) -> str:
    \"\"\"
    {description}
    \"\"\"
    async with await get_http_client() as client:
        try:
{param_processing}
            
            # Make the request
            response = await client.{method}(
                url,
                params=query_params,
                json=request_body if request_body else None
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


def _get_parameter_definitions(spec: Dict[str, Any], operation: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """
    Get parameter definitions for a tool function, separated by required vs optional.
    
    Args:
        spec: The parsed OpenAPI specification
        operation: The operation definition
        
    Returns:
        Tuple of (required_parameters, optional_parameters) definition strings
    """
    required_params = []
    optional_params = []
    seen_params = set()  # Track seen parameter names to avoid duplicates

    for param_obj in operation.get('parameters', []):
        actual_param = {}
        if '$ref' in param_obj:
            ref_path = param_obj['$ref']
            actual_param = resolve_ref(spec, ref_path)
        else:
            actual_param = param_obj

        if not actual_param or 'name' not in actual_param:
            print(f"Warning: Skipping parameter due to missing name or unresolved reference: {param_obj}")
            continue
            
        param_name = sanitize_identifier(actual_param['name'])
        
        # Handle duplicate parameter names
        original_param_name = param_name
        counter = 1
        while param_name in seen_params:
            param_name = f"{original_param_name}_{counter}"
            counter += 1
        
        seen_params.add(param_name)
        param_type = _get_param_type(actual_param)
        
        # Separate required and optional parameters
        if actual_param.get('required', False):
            required_params.append(f"{param_name}: {param_type}")
        else:
            # Add default value for optional parameters
            if param_type == 'bool':
                param_type = f"{param_type} = False"
            elif param_type == 'str':
                param_type = f"{param_type} = ''"
            elif param_type in ['int', 'float']:
                param_type = f"{param_type} = 0"
            else:
                param_type = f"Optional[{param_type}] = None"
            optional_params.append(f"{param_name}: {param_type}")
    
    return required_params, optional_params


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


def _generate_parameter_processing(spec: Dict[str, Any], operation: Dict[str, Any], path: str) -> str:
    """
    Generate parameter processing code for a tool function.
    
    Args:
        spec: The parsed OpenAPI specification
        operation: The operation definition
        path: The API path
        
    Returns:
        String containing parameter processing code
    """
    lines = []
    lines.append("            # Build the URL with path parameters")
    lines.append(f"            url = \"{path}\"")
    lines.append("")
    lines.append("            # Extract query parameters")
    lines.append("            query_params = {}")
    lines.append("            request_body = None")
    lines.append("")
    
    # Process parameters
    seen_params = set()
    for param_obj in operation.get('parameters', []):
        actual_param = {}
        if '$ref' in param_obj:
            ref_path = param_obj['$ref']
            actual_param = resolve_ref(spec, ref_path)
        else:
            actual_param = param_obj

        if not actual_param or 'name' not in actual_param:
            continue
            
        param_name = sanitize_identifier(actual_param['name'])
        original_param_name = param_name
        
        # Handle duplicate parameter names
        counter = 1
        while param_name in seen_params:
            param_name = f"{original_param_name}_{counter}"
            counter += 1
        seen_params.add(param_name)
        
        param_in = actual_param.get('in', 'query')
        original_name = actual_param['name']
        
        if param_in == 'path':
            # Replace path parameters in URL
            lines.append(f"            if {param_name} is not None:")
            lines.append(f"                url = url.replace('{{{original_name}}}', str({param_name}))")
        elif param_in == 'query':
            # Add to query parameters
            lines.append(f"            if {param_name} is not None:")
            lines.append(f"                query_params['{original_name}'] = {param_name}")
        elif param_in == 'header':
            # We'll handle headers separately if needed
            pass
    
    return "\n".join(lines)


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
    api_title = escape_string_literal(info.get('title', 'API'))
    api_version = escape_string_literal(info.get('version', '1.0.0'))
    api_description = escape_string_literal(info.get('description', 'API description'))
    
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
        safe_schema_name = sanitize_identifier(schema_name)
        escaped_schema_name = escape_string_literal(schema_name)
        schema_yaml = escape_string_literal(yaml.dump(schema, default_flow_style=False))
        
        resource_def = f"""
@mcp.resource("schema://{escaped_schema_name}")
def get_{safe_schema_name}_schema() -> str:
    \"\"\"
    Get the {escaped_schema_name} schema definition
    \"\"\"
    return \"\"\"
    {schema_yaml}
    \"\"\"
"""
        schema_resources.append(resource_def)
    
    return schema_resources
