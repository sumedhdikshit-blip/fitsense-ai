import os
from groq import Groq

def get_groq_client() -> Groq:
    """
    Initializes and returns the Groq client.
    Raises ValueError if GROQ_API_KEY is not set.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing.")
    return Groq(api_key=api_key)
