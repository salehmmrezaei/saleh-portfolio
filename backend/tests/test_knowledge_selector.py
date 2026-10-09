import json

from app.schemas import ChatRequest, ChatTurn
from app.services.knowledge_selector import (
    build_knowledge_context,
    select_profile_fields,
    select_project_keys,
)


def test_selects_repopilot_from_project_name() -> None:
    payload = ChatRequest(
        message="How does RepoPilot perform retrieval?"
    )

    assert select_project_keys(payload) == [
        "repopilot-ai"
    ]


def test_selects_two_named_projects_for_comparison() -> None:
    payload = ChatRequest(
        message=(
            "Compare RepoPilot AI with Voice Notes AI."
        )
    )

    selected = select_project_keys(payload)

    assert set(selected) == {
        "repopilot-ai",
        "voice-notes-ai",
    }


def test_follow_up_uses_recent_project_context() -> None:
    payload = ChatRequest(
        message="What was the hardest part?",
        history=[
            ChatTurn(
                role="user",
                content="Tell me about RepoPilot AI.",
            ),
            ChatTurn(
                role="assistant",
                content=(
                    "RepoPilot AI is a repository "
                    "intelligence platform."
                ),
            ),
        ],
    )

    assert select_project_keys(payload) == [
        "repopilot-ai"
    ]


def test_unrelated_profile_question_does_not_reuse_project() -> None:
    payload = ChatRequest(
        message="Where did Saleh study?",
        history=[
            ChatTurn(
                role="user",
                content="Tell me about RepoPilot AI.",
            ),
            ChatTurn(
                role="assistant",
                content=(
                    "RepoPilot AI is a repository "
                    "intelligence platform."
                ),
            ),
        ],
    )

    assert select_project_keys(payload) == []


def test_availability_question_selects_availability() -> None:
    payload = ChatRequest(
        message="When is Saleh available to start work?"
    )

    fields = select_profile_fields(payload)

    assert "overview" in fields
    assert "availability" in fields


def test_work_permit_question_selects_authorization() -> None:
    payload = ChatRequest(
        message="Can Saleh work in Italy?"
    )

    fields = select_profile_fields(payload)

    assert "work_authorization" in fields


def test_education_question_selects_education() -> None:
    payload = ChatRequest(
        message="Where did Saleh study?"
    )

    fields = select_profile_fields(payload)

    assert "education" in fields


def test_skill_question_selects_skills() -> None:
    payload = ChatRequest(
        message="Does Saleh have FastAPI experience?"
    )

    fields = select_profile_fields(payload)

    assert "skills" in fields


def test_generic_python_question_does_not_force_project() -> None:
    payload = ChatRequest(
        message="Does Saleh know Python?"
    )

    assert select_project_keys(payload) == []


def test_context_contains_only_selected_project() -> None:
    payload = ChatRequest(
        message="Explain RepoPilot's hybrid retrieval."
    )

    context = json.loads(
        build_knowledge_context(payload)
    )

    assert "overview" in context["profile"]
    assert set(context["projects"]) == {
        "repopilot-ai"
    }



def test_outside_work_selects_personal_interests() -> None:
    payload = ChatRequest(
        message="What does Saleh enjoy outside of work?"
    )

    fields = select_profile_fields(payload)

    assert "personal_interests" in fields


def test_forecasting_project_selects_time_series() -> None:
    payload = ChatRequest(
        message="How did the forecasting project perform?"
    )

    assert select_project_keys(payload) == [
        "time-series-forecasting"
    ]
