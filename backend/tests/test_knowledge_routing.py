import pytest

from app.services.knowledge_retrieval import (
    is_project_catalog_query,
    is_project_demo_catalog_query,
    is_project_query,
    match_project_keys,
)


def test_repopilot_typo_matches_project() -> None:
    assert match_project_keys(
        "Tell me about Repopliot."
    ) == ("repopilot-ai",)


def test_forecasting_typo_matches_project() -> None:
    assert match_project_keys(
        "How did the forcasting project perform?"
    ) == ("time-series-forecasting",)


def test_named_comparison_matches_both_projects() -> None:
    assert match_project_keys(
        "Compare RepoPilot AI and Voice Notes AI."
    ) == (
        "repopilot-ai",
        "voice-notes-ai",
    )


def test_generic_project_question_has_project_scope() -> None:
    query = (
        "Which project shows "
        "background job experience?"
    )

    assert match_project_keys(query) == ()
    assert is_project_query(query)


def test_project_catalog_question_is_detected() -> None:
    assert is_project_catalog_query(
        "What projects has Saleh built?"
    )


def test_specific_project_question_is_not_catalog() -> None:
    assert not is_project_catalog_query(
        "Which project shows "
        "background job experience?"
    )


@pytest.mark.parametrize("name", ["MediFlow AI", "mediflowai", "Medi Flow"])
def test_mediflow_aliases_scope_project(name: str) -> None:
    assert match_project_keys(f"How does {name} work?") == ("mediflow-ai",)


@pytest.mark.parametrize("name", ["AI Rental Agent", "Casa", "ai-rental-agent"])
def test_rental_aliases_scope_project(name: str) -> None:
    assert match_project_keys(f"Can I visit {name}'s demo?") == ("ai-rental-agent",)


def test_comparison_matches_both_new_projects() -> None:
    assert set(match_project_keys("Compare MediFlow AI and Casa.")) == {
        "mediflow-ai", "ai-rental-agent",
    }


@pytest.mark.parametrize("query", [
    "Which projects have live demos?",
    "Show available demos.",
    "List Saleh's projects with demos.",
])
def test_demo_catalog_question(query: str) -> None:
    assert is_project_demo_catalog_query(query)


def test_named_demo_question_is_not_demo_catalog() -> None:
    assert not is_project_demo_catalog_query("Which features are in Casa's demo?")


def test_generic_catalog_wording() -> None:
    assert is_project_catalog_query("List all projects.")
    assert is_project_catalog_query("What projects did Saleh build?")
