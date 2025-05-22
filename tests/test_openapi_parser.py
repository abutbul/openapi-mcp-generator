import unittest
import os
import sys
from unittest.mock import patch, mock_open # mock_open is not used after this change

# Add project root to sys.path to allow importing from openapi_parser
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from openapi_parser import OpenAPISpecParser, TypeScriptOpenAPIParser, BaseOpenAPISpecParser

INVALID_YAML_CONTENT = "openapi: 3.0.0\ninfo: title: Sample API\n  version: 1.0.0" # Indentation error

class TestOpenAPISpecParser(unittest.TestCase):

    def setUp(self):
        self.parser = OpenAPISpecParser()
        self.ts_parser = TypeScriptOpenAPIParser()
        # self.test_file_path = "test_spec.yaml" # No longer creating this temp file
        self.invalid_test_file_path = "invalid_test_spec.yaml"
        self.existing_valid_spec_path = os.path.join(project_root, "tests", "openapi.yaml")


    def tearDown(self):
        # if os.path.exists(self.test_file_path): # No longer creating this temp file
        #     os.remove(self.test_file_path)
        if os.path.exists(self.invalid_test_file_path):
            os.remove(self.invalid_test_file_path)

    def test_successful_parsing_existing_file(self):
        """Test parsing an existing valid OpenAPI YAML file (tests/openapi.yaml)."""
        self.assertTrue(os.path.exists(self.existing_valid_spec_path), f"Test file {self.existing_valid_spec_path} not found.")
        parsed_spec = self.parser.parse(self.existing_valid_spec_path)
        self.assertIsNotNone(parsed_spec)
        self.assertEqual(parsed_spec['info']['title'], "Reference Test API")
        self.assertIn('/items', parsed_spec['paths'])
        self.assertIn('IdRequired', parsed_spec['components']['parameters'])

    def test_parse_file_not_found(self):
        """Test parsing a non-existent file."""
        # Note: The current implementation uses sys.exit(1).
        # A more testable approach would be to raise FileNotFoundError.
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse("non_existent_file.yaml")
        self.assertEqual(cm.exception.code, 1)

    def test_parse_invalid_yaml(self):
        """Test parsing a file with invalid YAML content."""
        with open(self.invalid_test_file_path, 'w') as f:
            f.write(INVALID_YAML_CONTENT)
        
        # Note: The current implementation uses sys.exit(1).
        # A more testable approach would be to raise a specific parsing error.
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse(self.invalid_test_file_path)
        self.assertEqual(cm.exception.code, 1)

    def test_typescript_parser_not_implemented(self):
        """Test that TypeScriptOpenAPIParser.parse raises NotImplementedError."""
        with self.assertRaises(NotImplementedError) as context:
            self.ts_parser.parse("any_file.yaml")
        self.assertEqual(str(context.exception), "TypeScript OpenAPI parsing is not yet implemented.")

    def test_is_instance_of_base_class(self):
        """Test that parsers are instances of BaseOpenAPISpecParser."""
        self.assertIsInstance(self.parser, BaseOpenAPISpecParser)
        self.assertIsInstance(self.ts_parser, BaseOpenAPISpecParser)

if __name__ == '__main__':
    # This allows running the tests directly from this file
    # For a larger project, you'd typically use a test runner like `python -m unittest discover`
    unittest.main()
