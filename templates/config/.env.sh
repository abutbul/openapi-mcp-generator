#!/bin/bash

# API configuration
export API_URL="{{ api_url }}"
export API_TOKEN="{{ api_token }}"

# Force bearer authentication for MCP server
export API_AUTH_TYPE="bearer"

# MCP server configuration
export MCP_SERVER_NAME="{{ mcp_server_name }}"