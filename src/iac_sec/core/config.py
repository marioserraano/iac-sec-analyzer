import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file if present
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    """
    Centralized configuration management for Local LLM (Ollama).
    """
    # Base URL for the Ollama API, defaulting to localhost if not set in environment variables 
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.1")
    
    # API key for authenticating with the Ollama API, defaulting to "ollama-local" if not set in environment variables
    API_KEY: str = os.getenv("API_KEY", "ollama-local")

# Instantiate a singleton settings object
settings = Settings()