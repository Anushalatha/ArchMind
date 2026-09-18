"""Prompts used by the architecture generation service."""

from collections.abc import Mapping

import json


SYSTEM_PROMPT = """You are ArchMind, a pragmatic AI system architect.
Create clear, technically realistic architecture proposals for software products.
Explain important decisions and trade-offs. Prefer simple designs unless the
requirements justify additional complexity. Do not invent requirements that are
not supported by the user's idea; label assumptions clearly.
Return only valid JSON matching the requested architecture schema. Do not wrap
the JSON in Markdown fences and do not add commentary before or after it.
"""

CRITIC_SYSTEM_PROMPT = """You are ArchMind's architecture critic.
Review the supplied architecture carefully and identify concrete, actionable
problems. Consider security, scalability, missing components, unnecessary
complexity, bottlenecks, and important trade-offs. Do not rewrite or modify the
architecture. Return only valid JSON with no Markdown fences or commentary.
"""


def build_architecture_prompt(
    product_idea: str, settings: Mapping[str, str]
) -> str:
    """Build the user prompt from the idea and selected architecture settings."""
    return f"""Design a technical system architecture for this product idea:

{product_idea.strip()}

Architecture preferences:
- Application type: {settings['application_type']}
- Expected scale: {settings['expected_scale']}
- AI components required: {settings['ai_components']}
- Architecture preference: {settings['architecture_preference']}

Include:
1. A concise system overview
2. Recommended architecture style and why
3. Core components and each responsibility
4. Main data flow
5. Suggested API surface
6. Storage and database choices
7. Security considerations
8. Scalability considerations
9. Risks, assumptions, and trade-offs

Return this exact JSON shape:
{{
    "project_name": "string",
    "system_overview": "string",
    "architecture_style": "string",
    "functional_requirements": ["string"],
    "non_functional_requirements": ["string"],
    "components": [{{
        "name": "string",
        "responsibility": "string",
        "api_endpoints": [{{"method": "string", "endpoint": "string", "purpose": "string"}}],
        "database_entities": [{{"name": "string", "purpose": "string"}}],
        "ai_components": [{{"name": "string", "purpose": "string", "technology": "string"}}]
    }}],
    "security_considerations": ["string"],
    "scalability_considerations": ["string"],
    "risks_and_tradeoffs": ["string"]
}}
"""


def build_critique_prompt(architecture: Mapping[str, object]) -> str:
        """Build a JSON critique request from a validated architecture."""
        architecture_json = json.dumps(architecture, indent=2)
        return f"""Analyze this architecture:

{architecture_json}

Return this exact JSON shape:
{{
    "summary": "short overall assessment",
    "findings": [
        {{
            "category": "security | scalability | missing component | complexity | bottleneck | trade-off",
            "severity": "low | medium | high | critical",
            "finding": "specific problem",
            "impact": "why it matters",
            "recommendation": "practical improvement"
        }}
    ]
}}
"""
