"""Streamlit entry point for ArchMind."""

import streamlit as st

from core.schemas import Architecture, ArchitectureCritique
from services.critic import critique_architecture
from services.architect import generate_architecture


def render_sidebar() -> dict[str, str]:
    """Render architecture preferences and return the selected values."""
    with st.sidebar:
        st.header("Architecture settings")
        return {
            "application_type": st.selectbox(
                "Application Type",
                [
                    "Web Application",
                    "Mobile Application",
                    "AI Application",
                    "SaaS Platform",
                    "Data Platform",
                    "API Service",
                ],
            ),
            "expected_scale": st.selectbox(
                "Expected Scale", ["Small", "Medium", "Large", "Enterprise"]
            ),
            "ai_components": st.selectbox(
                "AI Components Required", ["Yes", "No", "Not Sure"]
            ),
            "architecture_preference": st.selectbox(
                "Architecture Preference",
                ["Recommended", "Monolith", "Modular Monolith", "Microservices"],
            ),
        }


def render_architecture(architecture: Architecture) -> None:
    """Render a validated architecture across focused tabs."""
    tabs = st.tabs(
        [
            "Overview",
            "Requirements",
            "Components",
            "APIs",
            "Database",
            "AI Components",
            "Security",
            "Scalability",
            "Risks & Trade-offs",
            "Raw JSON",
        ]
    )

    with tabs[0]:
        st.header(architecture.project_name)
        st.info(architecture.system_overview)
        st.metric("Architecture style", architecture.architecture_style)

    with tabs[1]:
        st.subheader("Functional requirements")
        for requirement in architecture.functional_requirements:
            st.markdown(f"- {requirement}")
        st.subheader("Non-functional requirements")
        for requirement in architecture.non_functional_requirements:
            st.markdown(f"- {requirement}")

    with tabs[2]:
        for component in architecture.components:
            with st.expander(component.name, expanded=True):
                st.write(component.responsibility)

    with tabs[3]:
        endpoints = [
            endpoint
            for component in architecture.components
            for endpoint in component.api_endpoints
        ]
        if endpoints:
            for endpoint in endpoints:
                st.markdown(f"**{endpoint.method}** `{endpoint.endpoint}`")
                st.caption(endpoint.purpose)
        else:
            st.info("No API endpoints were identified.")

    with tabs[4]:
        entities = [
            entity
            for component in architecture.components
            for entity in component.database_entities
        ]
        if entities:
            for entity in entities:
                st.markdown(f"**{entity.name}**")
                st.caption(entity.purpose)
        else:
            st.info("No database entities were identified.")

    with tabs[5]:
        ai_components = [
            ai_component
            for component in architecture.components
            for ai_component in component.ai_components
        ]
        if ai_components:
            for ai_component in ai_components:
                with st.expander(ai_component.name):
                    st.write(ai_component.purpose)
                    st.caption(f"Technology: {ai_component.technology}")
        else:
            st.info("No AI components were identified.")

    with tabs[6]:
        for item in architecture.security_considerations:
            st.markdown(f"- {item}")

    with tabs[7]:
        for item in architecture.scalability_considerations:
            st.markdown(f"- {item}")

    with tabs[8]:
        for item in architecture.risks_and_tradeoffs:
            st.warning(item)

    with tabs[9]:
        st.json(architecture.model_dump())


def render_critique(critique: ArchitectureCritique) -> None:
    """Render a validated critique separately from the architecture."""
    st.subheader("Architecture Critique")
    st.info(critique.summary)
    for finding in critique.findings:
        with st.expander(f"{finding.severity.upper()} - {finding.category}"):
            st.write(finding.finding)
            st.markdown(f"**Impact:** {finding.impact}")
            st.markdown(f"**Recommendation:** {finding.recommendation}")


def main() -> None:
    """Render the architecture generation application."""
    st.set_page_config(page_title="ArchMind", page_icon="A", layout="wide")
    st.title("ArchMind")
    st.subheader("Transform product ideas into technical architectures")

    settings = render_sidebar()
    product_idea = st.text_area(
        "Describe the system you want to build",
        height=260,
        placeholder="Example: A team collaboration platform for remote engineering teams...",
    )

    if st.button("Generate Architecture", type="primary"):
        if not product_idea.strip():
            st.warning("Describe your product idea before generating an architecture.")
        else:
            with st.spinner("Designing your architecture..."):
                try:
                    st.session_state["architecture"] = generate_architecture(product_idea, settings)
                except ValueError as error:
                    st.warning(str(error))
                except RuntimeError as error:
                    st.error(str(error))

    architecture = st.session_state.get("architecture")
    if isinstance(architecture, Architecture):
        st.divider()
        st.subheader("Generated Architecture")
        render_architecture(architecture)
        with st.expander("Selected settings"):
            st.json(settings)

        if st.button("Critique Architecture"):
            with st.spinner("Reviewing the architecture..."):
                try:
                    st.session_state["critique"] = critique_architecture(architecture)
                except ValueError as error:
                    st.warning(str(error))
                except RuntimeError as error:
                    st.error(str(error))

    critique = st.session_state.get("critique")
    if isinstance(critique, ArchitectureCritique):
        st.divider()
        render_critique(critique)


if __name__ == "__main__":
    main()
