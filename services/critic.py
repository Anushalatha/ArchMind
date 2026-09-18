"""Application service for structured architecture critiques."""

import json

from core.llm import generate_completion
from core.prompts import CRITIC_SYSTEM_PROMPT, build_critique_prompt
from core.schemas import Architecture, ArchitectureCritique


def critique_architecture(architecture: Architecture) -> ArchitectureCritique:
    """Analyze an architecture without changing the original model."""
    prompt = build_critique_prompt(architecture.model_dump())
    raw_response = generate_completion(CRITIC_SYSTEM_PROMPT, prompt).strip()

    if raw_response.startswith("```"):
        raw_response = raw_response.strip("`")
        if raw_response.startswith("json"):
            raw_response = raw_response[4:].lstrip()

    try:
        response_data = json.loads(raw_response)
        return ArchitectureCritique.model_validate(response_data)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError(
            "The critic returned invalid JSON. Please try the critique again."
        ) from error
    except ValueError as error:
        raise ValueError(
            "The critic response did not match the required structure. "
            "Please try again."
        ) from error