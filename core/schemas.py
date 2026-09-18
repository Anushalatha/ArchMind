"""Validated data models for generated system architectures."""

from pydantic import BaseModel, Field


class APIEndpoint(BaseModel):
    """An API endpoint exposed by a system component."""

    method: str
    endpoint: str
    purpose: str


class DatabaseEntity(BaseModel):
    """A database entity required by the architecture."""

    name: str
    purpose: str


class AIComponent(BaseModel):
    """An AI capability used by the architecture."""

    name: str
    purpose: str
    technology: str


class SystemComponent(BaseModel):
    """A deployable or logical component in the architecture."""

    name: str
    responsibility: str
    api_endpoints: list[APIEndpoint] = Field(default_factory=list)
    database_entities: list[DatabaseEntity] = Field(default_factory=list)
    ai_components: list[AIComponent] = Field(default_factory=list)


class Architecture(BaseModel):
    """The complete validated architecture returned by the LLM."""

    project_name: str
    system_overview: str
    architecture_style: str
    functional_requirements: list[str]
    non_functional_requirements: list[str]
    components: list[SystemComponent]
    security_considerations: list[str]
    scalability_considerations: list[str]
    risks_and_tradeoffs: list[str]


class CritiqueFinding(BaseModel):
    """One actionable issue identified in an architecture."""

    category: str
    severity: str
    finding: str
    impact: str
    recommendation: str


class ArchitectureCritique(BaseModel):
    """Validated critique returned for an architecture."""

    summary: str
    findings: list[CritiqueFinding]
