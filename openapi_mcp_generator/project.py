"""
Project Generator Module.

This module handles the creation of project directories and files from templates.
"""

import os
import uuid
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader


class ProjectBuilder:
    """Class for managing project creation and template rendering."""
    
    def __init__(self, template_dir: str):
        """
        Initialize the project builder.
        
        Args:
            template_dir: Path to the directory containing templates
        """
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def create_project_directory(self, output_dir: str, api_name: str) -> str:
        """
        Create a new project directory with a unique ID.
        
        Args:
            output_dir: The base output directory
            api_name: The name of the API
            
        Returns:
            The path to the created directory
        """
        # Create a sanitized version of the API name
        sanitized_name = ''.join(c if c.isalnum() else '-' for c in api_name.lower())
        
        # Create a unique directory name
        unique_id = str(uuid.uuid4())[:8]
        dir_name = f"openapi-mcp-{sanitized_name}-{unique_id}"
        full_path = os.path.join(output_dir, dir_name)
        
        # Create the directory
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
        template = self.env.get_template(template_path)
        rendered = template.render(**context)
        
        with open(output_path, 'w') as f:
            f.write(rendered)
    
    def generate_project_files(self, project_dir: str, template_context: Dict[str, Any]) -> None:
        """
        Generate project files from templates.
        
        Args:
            project_dir: Path to the project directory
            template_context: Context dictionary for template rendering
        """
        # Render and write templates
        self.render_template('docker/Dockerfile', os.path.join(project_dir, 'Dockerfile'), template_context)
        self.render_template('docker/docker.sh', os.path.join(project_dir, 'docker.sh'), template_context)
        self.render_template('config/.env.sh', os.path.join(project_dir, '.env.sh'), template_context)
        self.render_template('server/mcp_server.py', os.path.join(project_dir, 'mcp_server.py'), template_context)
        self.render_template('requirements.txt', os.path.join(project_dir, 'requirements.txt'), template_context)
        self.render_template('pyproject.toml', os.path.join(project_dir, 'pyproject.toml'), template_context)
        
        # Set executable permissions
        os.chmod(os.path.join(project_dir, 'docker.sh'), 0o755)
        os.chmod(os.path.join(project_dir, '.env.sh'), 0o755)
        os.chmod(os.path.join(project_dir, 'mcp_server.py'), 0o755)
