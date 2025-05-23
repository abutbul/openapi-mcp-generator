"""
OpenAPI Specification Parser Module.

This module handles the parsing and validation of OpenAPI specification files.
"""

import os
import sys
import yaml
from typing import Dict, Any


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


def resolve_reference(spec: Dict[str, Any], ref_path: str) -> Dict[str, Any]:
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
