import instructor
from openai import AsyncOpenAI
from iac_sec.core.config import settings

def get_llm_client() -> instructor.AsyncInstructor:
    """
    Initializes an asynchronous client pointing to the local Ollama instance.
    Patches it with Instructor to enforce JSON schema responses.
    """
    # Point the OpenAI client to the local Ollama server
    base_client = AsyncOpenAI(
        base_url=settings.OLLAMA_BASE_URL,
        api_key=settings.API_KEY,
    )
    
    # Patch with Instructor using JSON mode for optimal local model compatibility
    patched_client = instructor.from_openai(
        base_client, 
        mode=instructor.Mode.JSON
    )
    
    return patched_client