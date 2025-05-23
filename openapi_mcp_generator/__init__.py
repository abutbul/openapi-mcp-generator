"""
OpenAPI to MCP Server Generator package.

This package provides tools for generating Model Context Protocol (MCP) servers from OpenAPI specifications.
"""

from .generator import generate_mcp_server
from .parser import parse_openapi_spec, sanitize_description, sanitize_identifier, escape_string_literal
from .generators import generate_tool_definitions, generate_resource_definitions

__all__ = [
    'generate_mcp_server',
    'parse_openapi_spec',
    'sanitize_description',
    'sanitize_identifier', 
    'escape_string_literal',
    'generate_tool_definitions',
    'generate_resource_definitions',
]
