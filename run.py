import sys
from pathlib import Path

# Add the 'src' directory to the Python path so it can find 'iac_sec'
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path.resolve()))

# Import our Typer CLI app
from iac_sec.cli import app

if __name__ == "__main__":
    app()