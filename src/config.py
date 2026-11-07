"""Configuration loader and LLM factory."""

import os
import sys
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env if present
PROJECT_ROOT = Path(__file__).resolve().parent.parent
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv(override=True)


def get_llm(provider: Optional[str] = None, model_name: Optional[str] = None) -> Any:
    """Instantiates and returns the configured LLM client.

    Supports:
        - 'gemini' via langchain-google-genai
        - 'openai' via langchain-openai or openai client
        - 'groq' via ChatOpenAI with Groq base URL
        - 'mock' for testing without an active API key
    """
    provider = (provider or os.getenv("LLM_PROVIDER") or "").lower()

    # Auto-detect provider if not explicitly given
    if not provider:
        if os.getenv("GEMINI_API_KEY"):
            provider = "gemini"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("GROQ_API_KEY"):
            provider = "groq"
        else:
            provider = "gemini"

    if provider == "mock":
        from tests.test_agent_flow import DeterministicReActMockLLM
        return DeterministicReActMockLLM()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please add it to your .env file or environment variables."
            )
        from langchain_google_genai import ChatGoogleGenerativeAI

        model = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.1,
            max_retries=2,
        )

    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please add it to your .env file or environment variables."
            )
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            # Fallback if langchain-openai is not installed
            os.system(f"{sys.executable} -m pip install langchain-openai")
            from langchain_openai import ChatOpenAI

        model = model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0.1,
        )

    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set.")
        from langchain_openai import ChatOpenAI

        model = model_name or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            temperature=0.1,
        )

    elif provider == "mock":
        from tests.test_agent_flow import DeterministicReActMockLLM
        return DeterministicReActMockLLM()

    else:
        raise ValueError(
            f"Unsupported LLM provider '{provider}'. Supported options: gemini, openai, groq."
        )
