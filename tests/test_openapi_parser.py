import unittest
import os
import sys
from unittest.mock import patch # Removed mock_open as it's not used

# Add project root to sys.path to allow importing from openapi_parser
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from openapi_parser import OpenAPISpecParser, TypeScriptOpenAPIParser, BaseOpenAPISpecParser

INVALID_YAML_CONTENT = "openapi: 3.0.0\ninfo: title: Sample API\n  version: 1.0.0" # Indentation error
DUMMY_TS_CONTENT_MISSING_KEYWORDS = "const variable = 'some value';"

class TestOpenAPISpecParser(unittest.TestCase):

    def setUp(self):
        self.parser = OpenAPISpecParser()
        self.ts_parser = TypeScriptOpenAPIParser()
        self.invalid_test_file_path = "invalid_test_spec.yaml"
        self.existing_valid_spec_path = os.path.join(project_root, "tests", "openapi.yaml")
        self.sample_ts_spec_path = os.path.join(project_root, "tests", "sample_openapi.ts")
        self.dummy_ts_file_path = "dummy.ts"

    def tearDown(self):
        if os.path.exists(self.invalid_test_file_path):
            os.remove(self.invalid_test_file_path)
        if os.path.exists(self.dummy_ts_file_path):
            os.remove(self.dummy_ts_file_path)

    def test_successful_parsing_existing_file(self):
        """Test parsing an existing valid OpenAPI YAML file (tests/openapi.yaml)."""
        self.assertTrue(os.path.exists(self.existing_valid_spec_path), f"Test file {self.existing_valid_spec_path} not found.")
        parsed_spec = self.parser.parse(self.existing_valid_spec_path)
        self.assertIsNotNone(parsed_spec)
        self.assertEqual(parsed_spec['info']['title'], "Reference Test API")
        self.assertIn('/items', parsed_spec['paths'])
        self.assertIn('IdRequired', parsed_spec['components']['parameters'])

    @patch('sys.exit')
    def test_parse_file_not_found(self, mock_sys_exit):
        """Test parsing a non-existent file with OpenAPISpecParser."""
        self.parser.parse("non_existent_file.yaml")
        mock_sys_exit.assert_called_once_with(1)

    @patch('sys.exit')
    def test_parse_invalid_yaml(self, mock_sys_exit):
        """Test parsing a file with invalid YAML content with OpenAPISpecParser."""
        with open(self.invalid_test_file_path, 'w') as f:
            f.write(INVALID_YAML_CONTENT)
        self.parser.parse(self.invalid_test_file_path)
        mock_sys_exit.assert_called_once_with(1)
        
    # Tests for TypeScriptOpenAPIParser
    def test_typescript_parser_successful_stub_parsing(self):
        """Test successful stub parsing of a .ts file."""
        self.assertTrue(os.path.exists(self.sample_ts_spec_path), f"Test file {self.sample_ts_spec_path} not found.")
        parsed_spec = self.ts_parser.parse(self.sample_ts_spec_path)
        self.assertIsNotNone(parsed_spec)
        self.assertEqual(parsed_spec['openapi'], '3.0.0')
        self.assertEqual(parsed_spec['info']['title'], 'Sample TS API') # From tests/sample_openapi.ts
        self.assertEqual(parsed_spec['info']['version'], '1.0.0-ts-stub')
        self.assertEqual(parsed_spec['paths'], {})

    @patch('sys.exit')
    def test_typescript_parser_file_not_found(self, mock_sys_exit):
        """Test TypeScriptOpenAPIParser with a non-existent file."""
        self.ts_parser.parse("non_existent_file.ts")
        mock_sys_exit.assert_called_once_with(1)

    @patch('sys.exit')
    def test_typescript_parser_missing_keywords(self, mock_sys_exit):
        """Test TypeScriptOpenAPIParser with a file missing essential keywords."""
        with open(self.dummy_ts_file_path, 'w') as f:
            f.write(DUMMY_TS_CONTENT_MISSING_KEYWORDS)
        
        self.ts_parser.parse(self.dummy_ts_file_path)
        mock_sys_exit.assert_called_once_with(1)

    def test_is_instance_of_base_class(self):
        """Test that parsers are instances of BaseOpenAPISpecParser."""
        self.assertIsInstance(self.parser, BaseOpenAPISpecParser)
        self.assertIsInstance(self.ts_parser, BaseOpenAPISpecParser)

if __name__ == '__main__':
    unittest.main()
