import os
import uuid
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from jinja2 import Environment

class MCPGenerator:
    """
    Generates MCP server files from a parsed OpenAPI specification.
    """

    def __init__(self, parsed_spec: Dict[str, Any], template_env: Environment):
        """
        Initializes the MCPGenerator.

        Args:
            parsed_spec: Dictionary containing the parsed OpenAPI specification.
            template_env: Jinja2 Environment for loading templates.
        """
        self.parsed_spec = parsed_spec
        self.template_env = template_env

    def sanitize_description(self, desc: str) -> str:
        """Remove newlines and escape quotes to prevent unterminated strings."""
        return desc.replace("\n", " ").replace('"', '\\"')

    def generate_tool_definitions(self) -> str:
        """
        Generate MCP tool definitions from OpenAPI paths.
        
        Returns:
            String containing the generated tool definitions
        """
        tools = []
        
        for path, path_item in self.parsed_spec.get('paths', {}).items():
            for method, operation in path_item.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    if 'operationId' not in operation:
                        continue
                    
                    operation_id = operation['operationId']
                    description = self.sanitize_description(operation.get('description', f"{method.upper()} {path}"))
                    
                    parameters_definitions = []
                    for param_obj in operation.get('parameters', []):
                        actual_param = {}
                        if '$ref' in param_obj:
                            ref_path = param_obj['$ref']
                            try:
                                parts = ref_path.strip('#/').split('/')
                                resolved_obj = self.parsed_spec
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
                        param_type = "str"
                        
                        if 'schema' in actual_param:
                            schema_type = actual_param['schema'].get('type', 'string')
                            if schema_type == 'integer':
                                param_type = "int"
                            elif schema_type == 'number':
                                param_type = "float"
                            elif schema_type == 'boolean':
                                param_type = "bool"
                        
                        parameters_definitions.append(f"{param_name}: {param_type}")
                    
                    parameters_definitions.append("ctx: Context")
                    
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
            
            response.raise_for_status()
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {{e.response.status_code}} - {{e.response.text}}"
        except Exception as e:
            return f"Error: {{str(e)}}"
"""
                    tools.append(tool_def)
        
        return '\n'.join(tools)

    def generate_resource_definitions(self) -> str:
        """
        Generate MCP resource definitions from OpenAPI components.
        
        Returns:
            String containing the generated resource definitions
        """
        resources = []
        
        info = self.parsed_spec.get('info', {})
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
        
        for schema_name, schema in self.parsed_spec.get('components', {}).get('schemas', {}).items():
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

    def create_project_directory(self, output_dir: str, api_name: str) -> str:
        """
        Create a new project directory with a unique ID.
        
        Args:
            output_dir: The base output directory
            api_name: The name of the API
            
        Returns:
            The path to the created directory
        """
        sanitized_name = ''.join(c if c.isalnum() else '-' for c in api_name.lower())
        unique_id = str(uuid.uuid4())[:8]
        dir_name = f"openapi-mcp-{sanitized_name}-{unique_id}"
        full_path = os.path.join(output_dir, dir_name)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def render_template(self, template_path: str, output_path: str, context: Dict[str, Any]) -> None:
        """
        Render a Jinja2 template to a file.
        
        Args:
            template_path: Path to the template file (relative to templates dir)
            output_path: Path where the rendered file will be saved
            context: Dictionary with template variables
        """
        template = self.template_env.get_template(template_path)
        rendered = template.render(**context)
        
        with open(output_path, 'w') as f:
            f.write(rendered)

    def generate_project_files(
        self, 
        project_dir: str, 
        api_name: str, 
        api_url: str, 
        auth_type: str, 
        api_token: str, 
        api_username: str, 
        api_password: str
    ) -> None:
        """
        Generates all project files (Dockerfile, mcp_server.py, etc.).

        Args:
            project_dir: Path to the project directory.
            api_name: Name of the API.
            api_url: Base URL for the API.
            auth_type: Authentication type.
            api_token: API token for authentication.
            api_username: Username for basic authentication.
            api_password: Password for basic authentication.
        """
        tool_defs = self.generate_tool_definitions()
        resource_defs = self.generate_resource_definitions()

        if not api_url and 'servers' in self.parsed_spec and self.parsed_spec['servers']:
            api_url = self.parsed_spec['servers'][0].get('url', '')

        container_name = os.path.basename(project_dir)
        image_name = container_name.lower()
        project_name = container_name.lower().replace('-', '_')

        template_context = {
            'api_name': api_name,
            'api_url': api_url,
            'auth_type': auth_type, # Ensure this is 'bearer' for MCP
            'api_token': api_token,
            'api_username': api_username,
            'api_password': api_password,
            'container_name': container_name,
            'image_name': image_name,
            'project_name': project_name,
            'mcp_server_name': f"{api_name} MCP Server",
            'tool_definitions': tool_defs,
            'resource_definitions': resource_defs
        }

        self.render_template('docker/Dockerfile', os.path.join(project_dir, 'Dockerfile'), template_context)
        self.render_template('docker/docker.sh', os.path.join(project_dir, 'docker.sh'), template_context)
        self.render_template('config/.env.sh', os.path.join(project_dir, '.env.sh'), template_context)
        self.render_template('server/mcp_server.py', os.path.join(project_dir, 'mcp_server.py'), template_context)
        self.render_template('requirements.txt', os.path.join(project_dir, 'requirements.txt'), template_context)
        self.render_template('pyproject.toml', os.path.join(project_dir, 'pyproject.toml'), template_context)

        os.chmod(os.path.join(project_dir, 'docker.sh'), 0o755)
        os.chmod(os.path.join(project_dir, '.env.sh'), 0o755)
        os.chmod(os.path.join(project_dir, 'mcp_server.py'), 0o755)
