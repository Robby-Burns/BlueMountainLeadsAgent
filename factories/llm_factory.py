from config import LLM_PROVIDER

def get_llm_provider() -> str:
    """
    Fetches the LLM provider connection string configured in the environment.
    This string is passed to the `llm` argument of CrewAI agents.
    """
    if LLM_PROVIDER == "anthropic":
        return "anthropic/claude-3-5-sonnet-20241022"
    elif LLM_PROVIDER == "gemini":
        return "gemini/gemini-1.5-pro"
    
    # Default to OpenAI
    return "gpt-4o"
