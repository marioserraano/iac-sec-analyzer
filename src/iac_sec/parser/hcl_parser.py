import hcl2
import json
from pathlib import Path
from typing import Any, Dict

class HclParsingError(Exception):
    """Custom exception raised when HCL parsing fails."""
    pass

class TerraformParser:
    """
    Handles the ingestion and parsing of Terraform (.tf) configuration files.
    """
    
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        """
        Reads a Terraform file and parses its HCL content into a Python dictionary.
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Terraform file not found at: {file_path}")
            
        if path.suffix != '.tf':
            raise ValueError(f"File {file_path} is not a valid Terraform (.tf) file.")

        try:
            with open(path, 'r', encoding='utf-8') as file:
                parsed_hcl = hcl2.load(file)
                return parsed_hcl
        except Exception as e:
            # We catch broad exceptions from hcl2 and wrap them in our domain exception
            raise HclParsingError(f"Failed to parse HCL file {file_path}. Details: {str(e)}")

    @staticmethod
    def to_json_string(parsed_data: Dict[str, Any]) -> str:
        """
        Converts the parsed HCL dictionary into a formatted JSON string.
        """
        return json.dumps(parsed_data, indent=2)