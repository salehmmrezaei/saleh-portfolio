from app.services.knowledge_retrieval import (
    is_project_catalog_query,
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
