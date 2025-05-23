#!/usr/bin/env python3
"""
OpenAPI to MCP Server Generator

This is the new modular entry point for generating a fully functional MCP server
implementation based on an OpenAPI specification. It uses the same functionality
as the original generator.py but packaged in a more modular way.

You can also use the original generator.py which will continue to work exactly as before.
"""

import sys
from openapi_mcp_generator.cli import main

if __name__ == "__main__":
    sys.exit(main())
