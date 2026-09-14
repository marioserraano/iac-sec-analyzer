import pytest
from pathlib import Path
from iac_sec.parser.hcl_parser import TerraformParser, HclParsingError

def test_parse_valid_tf_file(tmp_path: Path):
    """Tests that a correctly formatted .tf file is parsed into a dictionary."""
    # 1. Setup: Create a temporary file
    tf_file = tmp_path / "valid.tf"
    tf_content = 'resource "aws_s3_bucket" "test" { bucket = "my-bucket" }'
    tf_file.write_text(tf_content)
    
    # 2. Act: Parse the file
    parsed_data = TerraformParser.parse_file(str(tf_file))
    
    # 3. Assert: Verify the output
    assert "resource" in parsed_data
    assert parsed_data["resource"][0]["aws_s3_bucket"]["test"]["bucket"] == "my-bucket"

def test_parse_invalid_extension(tmp_path: Path):
    """Tests that the parser rejects non-.tf files."""
    bad_file = tmp_path / "config.json"
    bad_file.write_text('{"key": "value"}')
    
    with pytest.raises(ValueError, match="not a valid Terraform"):
        TerraformParser.parse_file(str(bad_file))

def test_parse_non_existent_file():
    """Tests that the parser handles missing files correctly."""
    with pytest.raises(FileNotFoundError):
        TerraformParser.parse_file("ghost_file.tf")