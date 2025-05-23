"""
OpenAPI Specification Parser Module.

This module handles the parsing and validation of OpenAPI specification files,
including support for directories containing multiple JSON API specification files.
"""

import os
import sys
import yaml
import json
import re
import keyword
from typing import Dict, Any, List, Optional


def parse_openapi_spec(filepath: str) -> Dict[str, Any]:
    """
    Parse an OpenAPI specification file or directory containing JSON API files.
    
    Args:
        filepath: Path to the OpenAPI YAML file or directory containing JSON API files
        
    Returns:
        Dictionary containing the parsed OpenAPI specification
        
    Raises:
        SystemExit: If the file/directory cannot be read or parsed
    """
    if not os.path.exists(filepath):
        print(f"Error: OpenAPI specification file or directory not found: {filepath}")
        sys.exit(1)
    
    # Check if it's a directory containing JSON API files
    if os.path.isdir(filepath):
        print(f"Processing API specification directory: {filepath}")
        return merge_json_api_specs(filepath)
    
    # Handle single file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Try parsing as YAML first (supports JSON too)
            try:
                spec = yaml.safe_load(content)
                if not isinstance(spec, dict):
                    print(f"Error: OpenAPI specification must be a document containing an object, got {type(spec)}")
                    sys.exit(1)
                return spec
            except yaml.YAMLError as e:
                print(f"Error parsing YAML/JSON in OpenAPI specification: {e}")
                sys.exit(1)
    except IOError as e:
        print(f"Error reading OpenAPI specification file: {e}")
        sys.exit(1)


def sanitize_description(desc: str) -> str:
    """
    Remove newlines and escape quotes to prevent unterminated strings.
    
    Args:
        desc: The description string to sanitize
        
    Returns:
        Sanitized description string
    """
    if not desc:
        return ""
    return desc.replace("\n", " ").replace('"', '\\"')


def sanitize_identifier(name: str) -> str:
    """
    Sanitize an identifier to ensure it's safe for Python code generation and MCP framework.
    
    Args:
        name: The identifier name to sanitize
        
    Returns:
        A safe Python identifier that doesn't start with underscore (MCP requirement)
    """
    if not name:
        return "unnamed"
    
    # Replace non-alphanumeric characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    
    # Ensure it starts with a letter (MCP framework doesn't allow leading underscores)
    if sanitized and (sanitized[0].isdigit() or sanitized[0] == '_'):
        sanitized = f"param_{sanitized.lstrip('_')}"
    
    # Handle Python keywords and builtins
    if keyword.iskeyword(sanitized) or sanitized in dir(__builtins__):
        sanitized = f"{sanitized}_"
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed"
    
    return sanitized


def escape_string_literal(value: str) -> str:
    """
    Escape a string literal for safe inclusion in generated Python code.
    
    Args:
        value: The string value to escape
        
    Returns:
        Escaped string safe for Python code
    """
    if not isinstance(value, str):
        return str(value)
    
    # Escape backslashes first, then quotes
    escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    return escaped


def parse_json_api_file(filepath: str) -> Dict[str, Any]:
    """
    Parse a single JSON API specification file.
    
    Args:
        filepath: Path to the JSON API file
        
    Returns:
        Dictionary containing the parsed API specification
        
    Raises:
        Exception: If the file cannot be read or parsed
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                spec = json.loads(content)
                if not isinstance(spec, dict):
                    raise ValueError(f"JSON API specification must be an object, got {type(spec)}")
                return spec
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON in API specification: {e}")
    except IOError as e:
        raise IOError(f"Error reading API specification file: {e}")


def merge_json_api_specs(api_dir: str) -> Dict[str, Any]:
    """
    Parse and merge multiple JSON API specification files from a directory.
    
    Args:
        api_dir: Path to directory containing JSON API files
        
    Returns:
        Dictionary containing merged OpenAPI specification
        
    Raises:
        SystemExit: If the directory cannot be read or contains no valid files
    """
    if not os.path.isdir(api_dir):
        print(f"Error: API specification directory not found: {api_dir}")
        sys.exit(1)
    
    # Find all JSON files in the directory
    json_files = []
    try:
        for file in os.listdir(api_dir):
            if file.endswith('.json'):
                json_files.append(os.path.join(api_dir, file))
    except OSError as e:
        print(f"Error reading API specification directory: {e}")
        sys.exit(1)
    
    if not json_files:
        print(f"Error: No JSON files found in directory: {api_dir}")
        sys.exit(1)
    
    print(f"Found {len(json_files)} JSON API specification files")
    
    # Parse common parameters if _common.json exists
    common_params = {}
    common_file = os.path.join(api_dir, '_common.json')
    if os.path.exists(common_file):
        try:
            common_spec = parse_json_api_file(common_file)
            common_params = common_spec.get('params', {})
            print(f"Loaded common parameters from _common.json")
        except Exception as e:
            print(f"Warning: Could not parse _common.json: {e}")
    
    # Build OpenAPI specification
    openapi_spec = {
        'openapi': '3.0.0',
        'info': {
            'title': 'Generated API from JSON Specifications',
            'version': '1.0.0',
            'description': f'API generated from {len(json_files)} JSON specification files'
        },
        'paths': {},
        'components': {
            'parameters': {},
            'schemas': {}
        }
    }
    
    # Process each JSON file
    for json_file in sorted(json_files):
        filename = os.path.basename(json_file)
        
        # Skip _common.json as it's already processed
        if filename == '_common.json':
            continue
            
        try:
            api_spec = parse_json_api_file(json_file)
            
            # Each JSON file contains one API endpoint
            for api_name, api_def in api_spec.items():
                if not isinstance(api_def, dict):
                    continue
                    
                _convert_json_api_to_openapi_path(
                    openapi_spec, api_name, api_def, common_params, filename
                )
                
        except Exception as e:
            print(f"Warning: Could not parse {filename}: {e}")
            continue
    
    if not openapi_spec['paths']:
        print(f"Error: No valid API endpoints found in directory: {api_dir}")
        sys.exit(1)
    
    print(f"Successfully merged {len(openapi_spec['paths'])} API endpoints")
    return openapi_spec


def _convert_json_api_to_openapi_path(
    openapi_spec: Dict[str, Any], 
    api_name: str, 
    api_def: Dict[str, Any], 
    common_params: Dict[str, Any],
    filename: str
) -> None:
    """
    Convert a single JSON API definition to OpenAPI path specification.
    
    Args:
        openapi_spec: The OpenAPI specification being built
        api_name: Name of the API endpoint
        api_def: The API definition from JSON
        common_params: Common parameters to include
        filename: Source filename for debugging
    """
    url_def = api_def.get('url', {})
    methods = api_def.get('methods', ['GET'])
    
    # Get paths - use the first path as primary, others as alternatives
    paths = url_def.get('paths', [url_def.get('path', '/')])
    if not paths:
        paths = ['/']
    
    primary_path = paths[0]
    
    # Sanitize the path for OpenAPI
    openapi_path = _convert_elasticsearch_path_to_openapi(primary_path)
    
    # Initialize path in OpenAPI spec
    if openapi_path not in openapi_spec['paths']:
        openapi_spec['paths'][openapi_path] = {}
    
    # Process each HTTP method
    for method in methods:
        method_lower = method.lower()
        operation_id = sanitize_identifier(f"{api_name}_{method_lower}")
        
        # Build parameters list
        parameters = []
        
        # Add path parameters
        path_parts = url_def.get('parts', {})
        for param_name, param_def in path_parts.items():
            param = _convert_json_param_to_openapi(param_name, param_def, 'path')
            parameters.append(param)
        
        # Add query parameters from API definition
        api_params = url_def.get('params', {})
        for param_name, param_def in api_params.items():
            param = _convert_json_param_to_openapi(param_name, param_def, 'query')
            parameters.append(param)
        
        # Add common parameters
        for param_name, param_def in common_params.items():
            param = _convert_json_param_to_openapi(param_name, param_def, 'query')
            parameters.append(param)
        
        # Build operation definition
        operation = {
            'operationId': operation_id,
            'summary': f'{api_name} operation',
            'description': api_def.get('documentation', f'{api_name} API endpoint from {filename}'),
            'parameters': parameters,
            'responses': {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': {'type': 'object'}
                        }
                    }
                },
                'default': {
                    'description': 'Error response',
                    'content': {
                        'application/json': {
                            'schema': {'type': 'object'}
                        }
                    }
                }
            }
        }
        
        # Add request body for POST/PUT methods
        if method_lower in ['post', 'put', 'patch'] and api_def.get('body') is not None:
            operation['requestBody'] = {
                'content': {
                    'application/json': {
                        'schema': {'type': 'object'}
                    },
                    'application/x-ndjson': {
                        'schema': {'type': 'string'}
                    }
                }
            }
        
        openapi_spec['paths'][openapi_path][method_lower] = operation


def _convert_elasticsearch_path_to_openapi(es_path: str) -> str:
    """
    Convert Elasticsearch-style path to OpenAPI path format.
    
    Args:
        es_path: Elasticsearch path like "/{index}/_bulk"
        
    Returns:
        OpenAPI path like "/{index}/_bulk"
    """
    # Elasticsearch paths are already close to OpenAPI format
    # Just ensure proper parameter syntax
    path = es_path
    
    # Convert {param} to {param} if needed (already correct format)
    # Handle any edge cases
    if not path.startswith('/'):
        path = '/' + path
    
    return path


def _convert_json_param_to_openapi(param_name: str, param_def: Dict[str, Any], param_in: str) -> Dict[str, Any]:
    """
    Convert JSON API parameter definition to OpenAPI parameter.
    
    Args:
        param_name: Parameter name
        param_def: Parameter definition from JSON
        param_in: Parameter location ('path', 'query', 'header')
        
    Returns:
        OpenAPI parameter definition
    """
    param_type = param_def.get('type', 'string')
    
    # Map parameter types
    schema = {'type': 'string'}  # Default
    if param_type == 'boolean':
        schema = {'type': 'boolean'}
    elif param_type == 'number':
        schema = {'type': 'number'}
    elif param_type == 'integer':
        schema = {'type': 'integer'}
    elif param_type == 'list':
        schema = {
            'type': 'array',
            'items': {'type': 'string'}
        }
    elif param_type == 'enum':
        options = param_def.get('options', [])
        schema = {
            'type': 'string',
            'enum': options
        }
    elif param_type == 'time':
        schema = {
            'type': 'string',
            'description': 'Time duration (e.g., "1s", "1m", "1h")'
        }
    
    param = {
        'name': param_name,
        'in': param_in,
        'required': param_in == 'path',  # Path parameters are always required
        'schema': schema
    }
    
    # Add description
    description = param_def.get('description', f'{param_name} parameter')
    param['description'] = sanitize_description(description)
    
    # Add default value if specified
    if 'default' in param_def:
        param['schema']['default'] = param_def['default']
    
    return param


def resolve_ref(spec: Dict[str, Any], ref_path: str) -> Dict[str, Any]:
    """
    Resolve a reference in the OpenAPI spec.
    
    Args:
        spec: The OpenAPI specification dictionary
        ref_path: The reference path, e.g., #/components/parameters/IdRequired
        
    Returns:
        The resolved object or an empty dict if resolution fails
        
    Notes:
        This function strips the leading '#/' from the reference path and splits it by '/'
        to navigate through the spec dictionary.
    """
    try:
        parts = ref_path.strip('#/').split('/')
        resolved_obj = spec
        for part in parts:
            resolved_obj = resolved_obj[part]
        return resolved_obj
    except KeyError:
        print(f"Warning: Could not resolve reference: {ref_path}")
        return {}
