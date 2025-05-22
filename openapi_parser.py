import os
import sys
import yaml
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
    extensions or considerations in the future.
    """

    def __init__(self):
        """
        Initializes the TypeScriptOpenAPIParser.
        """
        super().__init__()

    def parse(self, filepath: str) -> Dict[str, Any]:
        """
        Parse an OpenAPI specification file (intended for TypeScript projects).
        
        Args:
            filepath: Path to the OpenAPI file
            
        Returns:
            Dictionary containing the parsed OpenAPI specification
            
        Raises:
            NotImplementedError: This parser is not yet implemented.
        """
        raise NotImplementedError("TypeScript OpenAPI parsing is not yet implemented.")
