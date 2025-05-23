"""
HTTP Client Utilities Module.

This module provides HTTP client configuration and utility functions.
"""

import httpx
from typing import Dict, Any


def create_http_client_config(
    api_url: str, 
    auth_type: str = "bearer", 
    api_token: str = "", 
    api_username: str = "", 
    api_password: str = ""
) -> Dict[str, Any]:
    """
    Create HTTP client configuration for the API.
    
    Args:
        api_url: Base URL for the API
        auth_type: Authentication type (bearer, token, or basic)
        api_token: API token for authentication
        api_username: Username for basic authentication
        api_password: Password for basic authentication
        
    Returns:
        Dictionary with HTTP client configuration
    """
    config = {
        'base_url': api_url,
        'headers': {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        'timeout': 30.0,
    }
    
    # Configure authentication
    if auth_type == "bearer" and api_token:
        config['headers']['Authorization'] = f"Bearer {api_token}"
    elif auth_type == "token" and api_token:
        config['headers']['X-API-Key'] = api_token
    elif auth_type == "basic" and api_username and api_password:
        auth = httpx.BasicAuth(username=api_username, password=api_password)
        config['auth'] = auth
    
    return config


def generate_http_client_template(
    api_url: str,
    auth_type: str = "bearer",
    api_token: str = "",
    api_username: str = "",
    api_password: str = ""
) -> str:
    """
    Generate template code for HTTP client setup.
    
    Args:
        api_url: Base URL for the API
        auth_type: Authentication type (bearer, token, or basic)
        api_token: API token for authentication
        api_username: Username for basic authentication
        api_password: Password for basic authentication
        
    Returns:
        String containing template code for HTTP client setup
    """
    # Header configuration
    headers_code = "    'headers': {\n        'Accept': 'application/json',\n        'Content-Type': 'application/json',"
    
    # Authentication configuration
    auth_code = ""
    if auth_type == "bearer" and api_token:
        auth_var = "${API_TOKEN}"
        headers_code += f"\n        'Authorization': f'Bearer {auth_var}',"
    elif auth_type == "token" and api_token:
        auth_var = "${API_TOKEN}"
        headers_code += f"\n        'X-API-Key': f'{auth_var}',"
    elif auth_type == "basic" and api_username and api_password:
        auth_code = f"""
    # Basic Authentication
    auth = httpx.BasicAuth(
        username="${{API_USERNAME}}",
        password="${{API_PASSWORD}}"
    )"""
    
    headers_code += "\n    },"
    
    # Generate final template
    http_client_code = f"""
async def get_http_client() -> httpx.AsyncClient:
    \"\"\"
    Get configured HTTP client for API requests.
    
    Returns:
        Configured AsyncClient instance
    \"\"\"
    # API base URL
    base_url = "{api_url}"
    
    # Configure client{auth_code}
    
    # Create client
    client = httpx.AsyncClient(
        base_url=base_url,{headers_code}
        timeout=30.0,{f'auth=auth,' if auth_code else ''}
    )
    
    return client
"""
    
    return http_client_code
