#!/usr/bin/env python3
"""
MCP Server Implementation for {{ api_name }}

This MCP server exposes the API operations defined in the OpenAPI specification
as MCP tools and resources.
"""

import os
import argparse
import logging
import httpx
from typing import Dict, List, Any, Optional, Union
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP(name=os.environ.get("MCP_SERVER_NAME", "{{ api_name }} API"))

# API configuration
API_URL = os.environ.get("API_URL", "{{ api_url }}")
API_TOKEN = os.environ.get("API_TOKEN", "")
API_AUTH_TYPE = os.environ.get("API_AUTH_TYPE", "bearer")
API_USERNAME = os.environ.get("API_USERNAME", "")
API_PASSWORD = os.environ.get("API_PASSWORD", "")

# Async HTTP client for API calls
async def get_http_client():
    """Create and configure the HTTP client with appropriate authentication."""
    headers = {}
    
    if API_AUTH_TYPE == "bearer":
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    elif API_AUTH_TYPE == "token":
        headers["Authorization"] = API_TOKEN
    
    return httpx.AsyncClient(
        base_url=API_URL,
        headers=headers,
        auth=(API_USERNAME, API_PASSWORD) if API_AUTH_TYPE == "basic" else None
    )

# MCP tools for API operations
{{ tool_definitions }}

# MCP resources
{{ resource_definitions }}

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Server for {{ api_name }}")
    parser.add_argument(
        "--transport", 
        choices=["sse", "io"], 
        default="sse",
        help="Transport type (sse or io)"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    logger.info(f"Starting MCP server with {args.transport} transport")
    
    if args.transport == "sse":
        # Run with SSE transport (default host and port)
        mcp.run(transport="sse")
    else:
        # Run with stdio transport
        mcp.run(transport="stdio")