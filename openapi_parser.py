import os
import sys
import yaml
import re # Added for TypeScriptOpenAPIParser
from typing import Dict, Any
from abc import ABC, abstractmethod

class BaseOpenAPISpecParser(ABC):
    """
    Abstract base class for OpenAPI specification parsers.
    """

    def __init__(self):
        """
        Initializes the BaseOpenAPISpecParser.
        """
        super().__init__()

    @abstractmethod
    def parse(self, filepath: str) -> Dict[str, Any]:
        """
        Parse an OpenAPI specification file.
        
        Args:
            filepath: Path to the OpenAPI file
            
        Returns:
            Dictionary containing the parsed OpenAPI specification
        
        Raises:
            NotImplementedError: If the parser is not implemented.
        """
        pass

class OpenAPISpecParser(BaseOpenAPISpecParser):
    """
    Parses an OpenAPI specification file (YAML or JSON).
    This is the original parser, typically for Python-based OpenAPI specs.
    """

    def __init__(self):
        """
        Initializes the OpenAPISpecParser.
        """
        super().__init__()

    def parse(self, filepath: str) -> Dict[str, Any]:
        """
        Parse an OpenAPI specification file.
        
        Args:
            filepath: Path to the OpenAPI YAML file
            
        Returns:
            Dictionary containing the parsed OpenAPI specification
            
        Raises:
            SystemExit: If the file cannot be read or parsed
        """
        if not os.path.exists(filepath):
            print(f"Error: OpenAPI specification file not found: {filepath}")
            sys.exit(1)
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    # Attempt to parse as YAML first
                    spec = yaml.safe_load(content)
                    if not isinstance(spec, dict):
                        # If not a dict, it might be an invalid YAML or structure
                        print(f"Error: OpenAPI specification must be a YAML/JSON document containing an object, got {type(spec)}")
                        sys.exit(1)
                    return spec
                except yaml.YAMLError as e:
                    # Potentially add JSON parsing fallback here if needed,
                    # but for now, we assume YAML as per original logic.
                    print(f"Error parsing YAML/JSON in OpenAPI specification: {e}")
                    sys.exit(1)
        except IOError as e:
            print(f"Error reading OpenAPI specification file: {e}")
            sys.exit(1)

class TypeScriptOpenAPIParser(BaseOpenAPISpecParser):
    """
    Parses an OpenAPI specification file, potentially with TypeScript-specific
    extensions or considerations in the future. This is a stub implementation.
    """

    def __init__(self):
        """
        Initializes the TypeScriptOpenAPIParser.
        """
        super().__init__()

    def parse(self, filepath: str) -> Dict[str, Any]:
        """
        Parse an OpenAPI specification file (intended for TypeScript projects).
        This is a basic stub implementation that checks for keywords and extracts a title.
        
        Args:
            filepath: Path to the OpenAPI file (e.g., a .ts file)
            
        Returns:
            A dictionary structure resembling a parsed OpenAPI spec.
            
        Raises:
            SystemExit: If the file cannot be read or basic keywords are not found.
        """
        if not os.path.exists(filepath):
            print(f"Error: TypeScript OpenAPI file not found: {filepath}")
            sys.exit(1)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except IOError as e:
            print(f"Error reading TypeScript OpenAPI file: {e}")
            sys.exit(1)

        # Basic keyword check
        if not all(keyword in content for keyword in ["openapi:", "info:", "title:"]):
            print(f"Error: Essential OpenAPI keywords not found in {filepath}. This does not appear to be a valid OpenAPI-like TS file.")
            sys.exit(1)
            
        # Extract title using regex
        title = "Sample TS API" # Default title
        match = re.search(r"title:\s*['\"](.*?)['\"]", content)
        if match and match.group(1):
            title = match.group(1)

        # Return a stubbed OpenAPI-like dictionary
        return {
            "openapi": "3.0.0",
            "info": {
                "title": title,
                "version": "1.0.0-ts-stub"
            },
            "paths": {}
        }
