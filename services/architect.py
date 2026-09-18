"""Application service for generating validated system architectures."""

import json

from collections.abc import Mapping

from core.llm import generate_completion
from core.prompts import SYSTEM_PROMPT, build_architecture_prompt
from core.schemas import Architecture


def generate_architecture(
    product_idea: str, settings: Mapping[str, str]
) -> Architecture:
    """Generate an architecture proposal for a product idea."""
    if not product_idea.strip():
        raise ValueError("Describe your product idea before generating an architecture.")

    prompt = build_architecture_prompt(product_idea, settings)
    last_error: Exception | None = None

    for _ in range(2):
        raw_response = generate_completion(SYSTEM_PROMPT, prompt).strip()
        raw_response = _extract_json_object(raw_response)
        try:
            response_data = json.loads(raw_response)
            return Architecture.model_validate(response_data)
        except (json.JSONDecodeError, TypeError, ValueError) as error:
            last_error = error

    detail = str(last_error).splitlines()[0] if last_error else "Unknown validation error"
    raise ValueError(
        "The model response did not match the required architecture structure. "
        f"Please try again. Detail: {detail}"
    ) from last_error


def _extract_json_object(raw_response: str) -> str:
    """Remove optional Markdown wrapping and isolate the first JSON object."""
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned[3:].lstrip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].lstrip()
    if "```" in cleaned:
        cleaned = cleaned.split("```", 1)[0].rstrip()

    object_start = cleaned.find("{")
    if object_start > 0:
        cleaned = cleaned[object_start:]
    return cleaned
