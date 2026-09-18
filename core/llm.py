"""Small wrapper around the OpenAI Python SDK."""

import os

from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAIError
from openai import RateLimitError

load_dotenv()


def generate_completion(system_prompt: str, user_prompt: str) -> str:
    """Send prompts to the configured LLM provider and return generated text."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        base_url = "https://api.groq.com/openai/v1"
        key_name = "GROQ_API_KEY"
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        base_url = None
        key_name = "OPENAI_API_KEY"
    else:
        raise RuntimeError(
            f"Unsupported LLM_PROVIDER '{provider}'. Use 'openai' or 'groq'."
        )

    if not api_key:
        raise RuntimeError(
            f"{key_name} is missing. Add it to the local .env file and try again."
        )

    client_options = {"api_key": api_key}
    if base_url:
        client_options["base_url"] = base_url
    client = OpenAI(**client_options)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
    except RateLimitError as error:
        error_code = getattr(error, "code", None)
        if error_code == "insufficient_quota" or "credit_balance_exhausted" in str(
            error
        ):
            raise RuntimeError(
                f"The {provider} account has no API credits remaining. Add credits or use "
                "an API key from an account with available usage, then try again."
            ) from error
        raise RuntimeError(
            f"The {provider} rate limit was reached. Wait briefly and try again."
        ) from error
    except OpenAIError as error:
        raise RuntimeError(
            "The architecture request failed. Check the API key, model, and network connection."
        ) from error

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty architecture response.")

    return content
