import unittest
import os
import sys
from unittest.mock import MagicMock, patch, call

# Add project root to sys.path to allow importing from mcp_generator
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from mcp_generator import MCPGenerator
from jinja2 import Environment

class TestMCPGenerator(unittest.TestCase):

    def setUp(self):
        self.mock_parsed_spec = {
            "info": {
                "title": "Test API",
                "version": "1.0",
                "description": "A test API."
            },
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "getItems",
                        "description": "Get all items.",
                        "parameters": [
                            {
                                "name": "limit",
                                "in": "query",
                                "schema": {"type": "integer"}
                            }
                        ]
                    },
                    "post": {
                        "operationId": "createItem",
                        "description": "Create an item."
                        # No parameters for simplicity in this test
                    }
                },
                 "/items/{item_id}": {
                    "get": {
                        "operationId": "getItemById",
                        "description": "Get an item by its ID.",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "string"}
                            }
                        ]
                    }
                }
            },
            "components": {
                "schemas": {
                    "Item": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"}
                        }
                    }
                }
            },
            "servers": [{"url": "http://localhost:8000/api"}]
        }
        self.mock_template_env = MagicMock(spec=Environment)
        self.generator = MCPGenerator(self.mock_parsed_spec, self.mock_template_env)

    def test_sanitize_description(self):
        self.assertEqual(self.generator.sanitize_description("Test\ndescription"), "Test description")
        self.assertEqual(self.generator.sanitize_description('Test "quotes"'), 'Test \\"quotes\\"')
        self.assertEqual(self.generator.sanitize_description(""), "")

    def test_generate_tool_definitions(self):
        tool_defs = self.generator.generate_tool_definitions()
        self.assertIn("@mcp.tool(description=\"Get all items.\")", tool_defs)
        self.assertIn("async def getItems(limit: int, ctx: Context)", tool_defs)
        self.assertIn("@mcp.tool(description=\"Create an item.\")", tool_defs)
        self.assertIn("async def createItem(ctx: Context)", tool_defs)
        self.assertIn('url = "/items"', tool_defs) # Check path is used
        self.assertIn('url = "/items/{item_id}"', tool_defs)


    def test_generate_tool_definitions_no_operation_id(self):
        spec_no_op_id = {
            "paths": {
                "/test": {
                    "get": {"description": "Missing operationId"}
                }
            }
        }
        generator_no_op_id = MCPGenerator(spec_no_op_id, self.mock_template_env)
        tool_defs = generator_no_op_id.generate_tool_definitions()
        self.assertEqual(tool_defs, "")


    def test_generate_resource_definitions(self):
        resource_defs = self.generator.generate_resource_definitions()
        self.assertIn('@mcp.resource("api://info")', resource_defs)
        self.assertIn("Title: Test API", resource_defs)
        self.assertIn('@mcp.resource("schema://Item")', resource_defs)
        self.assertIn("Get the Item schema definition", resource_defs)
        self.assertIn("type: object", resource_defs) # Part of YAML dump of schema

    @patch('mcp_generator.os.makedirs')
    @patch('mcp_generator.uuid.uuid4')
    def test_create_project_directory(self, mock_uuid, mock_makedirs):
        mock_uuid.return_value = MagicMock(hex="testuuid") # uuid4() returns an object, so hex is not needed.
        # Corrected: uuid4() returns an object that can be converted to a string.
        # We only need the first 8 characters of the string representation.
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__.return_value = "testuuid12345678"

        output_dir = "test_output"
        api_name = "My Test API"
        
        expected_sanitized_name = "my-test-api"
        # expected_dir_name = f"openapi-mcp-{expected_sanitized_name}-testuuid" # Original
        expected_dir_name = f"openapi-mcp-{expected_sanitized_name}-testuuid" # Corrected based on [:8]
        expected_full_path = os.path.join(output_dir, expected_dir_name)

        created_path = self.generator.create_project_directory(output_dir, api_name)
        
        self.assertEqual(created_path, expected_full_path)
        mock_makedirs.assert_called_once_with(expected_full_path, exist_ok=True)


    @patch('mcp_generator.os.chmod')
    def test_generate_project_files(self, mock_chmod):
        # Mock the methods that generate content to simplify this test
        self.generator.generate_tool_definitions = MagicMock(return_value="mocked_tool_defs")
        self.generator.generate_resource_definitions = MagicMock(return_value="mocked_resource_defs")
        self.generator.render_template = MagicMock() # Mock render_template directly

        project_dir = "fake_project_dir"
        api_name = "MyAPI"
        api_url = "http://fakeapi.com"
        auth_type = "bearer"
        api_token = "test_token"
        
        self.generator.generate_project_files(
            project_dir, api_name, api_url, auth_type, api_token, "", ""
        )

        # Check that render_template was called for all expected files
        expected_template_calls = [
            call('docker/Dockerfile', os.path.join(project_dir, 'Dockerfile'), unittest.mock.ANY),
            call('docker/docker.sh', os.path.join(project_dir, 'docker.sh'), unittest.mock.ANY),
            call('config/.env.sh', os.path.join(project_dir, '.env.sh'), unittest.mock.ANY),
            call('server/mcp_server.py', os.path.join(project_dir, 'mcp_server.py'), unittest.mock.ANY),
            call('requirements.txt', os.path.join(project_dir, 'requirements.txt'), unittest.mock.ANY),
            call('pyproject.toml', os.path.join(project_dir, 'pyproject.toml'), unittest.mock.ANY),
        ]
        self.generator.render_template.assert_has_calls(expected_template_calls, any_order=False)
        
        # Check context for one of the calls (e.g., mcp_server.py)
        # This is a bit more involved as we need to reconstruct the expected context
        context_for_mcp_server = self.generator.render_template.call_args_list[3][0][2] # 4th call, 3rd argument
        self.assertEqual(context_for_mcp_server['api_name'], api_name)
        self.assertEqual(context_for_mcp_server['api_url'], api_url)
        self.assertEqual(context_for_mcp_server['api_token'], api_token)
        self.assertEqual(context_for_mcp_server['tool_definitions'], "mocked_tool_defs")
        self.assertEqual(context_for_mcp_server['resource_definitions'], "mocked_resource_defs")

        # Check that os.chmod was called for the correct files
        expected_chmod_calls = [
            call(os.path.join(project_dir, 'docker.sh'), 0o755),
            call(os.path.join(project_dir, '.env.sh'), 0o755),
            call(os.path.join(project_dir, 'mcp_server.py'), 0o755),
        ]
        mock_chmod.assert_has_calls(expected_chmod_calls, any_order=True)


    def test_render_template_integration(self):
        # This is a more focused test for render_template itself, using a real Environment
        # but with a MagicMock for get_template to avoid file system dependency for the template itself.
        
        mock_template_obj = MagicMock()
        mock_template_obj.render.return_value = "Rendered Content"
        
        # Create a real Environment but mock out get_template
        real_env_with_mocked_loader = MagicMock(spec=Environment)
        real_env_with_mocked_loader.get_template.return_value = mock_template_obj
        
        generator_with_real_env = MCPGenerator(self.mock_parsed_spec, real_env_with_mocked_loader)
        
        template_path = "some/template.txt"
        output_path = "output_file.txt"
        context = {"key": "value"}

        # Use mock_open to simulate file writing
        with patch('builtins.open', new_callable=unittest.mock.mock_open) as mock_file:
            generator_with_real_env.render_template(template_path, output_path, context)
        
        real_env_with_mocked_loader.get_template.assert_called_once_with(template_path)
        mock_template_obj.render.assert_called_once_with(**context)
        mock_file.assert_called_once_with(output_path, 'w')
        mock_file().write.assert_called_once_with("Rendered Content")


if __name__ == '__main__':
    unittest.main()
