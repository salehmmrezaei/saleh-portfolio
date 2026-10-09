import json
import re
from collections import Counter
from collections.abc import Iterator
from typing import Any

from ..profile_knowledge import PROFILE_KNOWLEDGE
from ..project_knowledge import PROJECT_KNOWLEDGE
from ..schemas import ChatRequest


MAX_SELECTED_PROJECTS = 2
MIN_PROJECT_SCORE = 4

SHORT_PROJECT_TERMS = {
    "ai",
    "cp",
    "dqn",
    "llm",
    "llms",
    "mip",
    "nlp",
    "ppo",
    "qmix",
    "rag",
    "rl",
    "sat",
    "vdn",
}

PROFILE_HINTS = {
    "experience": (
        "experience",
        "work experience",
        "employment",
        "work history",
        "career",
        "worked at",
        "employer",
        "company",
    ),
    "education": (
        "education",
        "degree",
        "university",
        "studied",
        "study",
        "study at",
        "graduate",
        "graduated",
        "graduation",
        "master",
        "masters",
        "msc",
        "bachelor",
        "bsc",
    ),
    "skills": (
        "skill",
        "skills",
        "technology",
        "technologies",
        "tech stack",
        "technical background",
        "know how to",
        "experience with",
    ),
    "professional_interests": (
        "professional interest",
        "professional interests",
        "career interest",
        "career interests",
        "interested in",
        "looking for",
        "target field",
        "type of work",
        "kind of work",
    ),
    "availability": (
        "available",
        "availability",
        "start immediately",
        "start working",
        "start work",
        "when can saleh start",
        "notice period",
        "open to work",
        "job search",
        "looking for a job",
        "looking for jobs",
    ),
    "work_authorization": (
        "work permit",
        "work authorization",
        "work authorisation",
        "right to work",
        "visa",
        "sponsorship",
        "legally work",
        "work in italy",
        "work in the netherlands",
        "work in netherlands",
    ),
    "personal_interests": (
        "hobby",
        "hobbies",
        "outside work",
        "outside of work",
        "free time",
        "personal interest",
        "personal interests",
        "enjoy algorithms",
        "likes algorithms",
        "algorithm hobby",
        "problem solving hobby",
    ),
    "public_links": (
        "contact",
        "contact saleh",
        "email",
        "linkedin",
        "github",
        "portfolio",
        "reach saleh",
        "reach him",
    ),
}

FOLLOW_UP_HINTS = (
    "it",
    "that",
    "this",
    "those",
    "the project",
    "that project",
    "this project",
    "what about",
    "how does it",
    "how did it",
    "why did",
    "hardest part",
    "biggest challenge",
    "what was difficult",
    "what was the challenge",
)


def _normalize(value: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        " ",
        value.casefold(),
    ).strip()


def _contains_term(text: str, term: str) -> bool:
    normalized_term = _normalize(term)

    if not normalized_term:
        return False

    return f" {normalized_term} " in f" {text} "


def _iter_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
        return

    if isinstance(value, dict):
        for nested in value.values():
            yield from _iter_strings(nested)
        return

    if isinstance(value, (list, tuple)):
        for nested in value:
            yield from _iter_strings(nested)


def _looks_like_follow_up(message: str) -> bool:
    normalized = _normalize(message)

    return any(
        _contains_term(normalized, hint)
        for hint in FOLLOW_UP_HINTS
    )


def _selection_text(payload: ChatRequest) -> str:
    current = _normalize(payload.message)

    if not _looks_like_follow_up(payload.message):
        return current

    recent_history = " ".join(
        turn.content
        for turn in payload.history[-4:]
    )

    return _normalize(
        f"{recent_history} {payload.message}"
    )


def _profile_skill_terms() -> tuple[str, ...]:
    skills = PROFILE_KNOWLEDGE.get("skills", {})

    return tuple(_iter_strings(skills))


def _experience_terms() -> tuple[str, ...]:
    terms: list[str] = []

    for item in PROFILE_KNOWLEDGE.get("experience", []):
        company = item.get("company")
        role = item.get("role")

        if isinstance(company, str):
            terms.append(company)

        if isinstance(role, str):
            terms.append(role)

    return tuple(terms)


def _education_terms() -> tuple[str, ...]:
    terms: list[str] = []

    for item in PROFILE_KNOWLEDGE.get("education", []):
        institution = item.get("institution")
        degree = item.get("degree")

        if isinstance(institution, str):
            terms.append(institution)

        if isinstance(degree, str):
            terms.append(degree)

    return tuple(terms)


def select_profile_fields(
    payload: ChatRequest,
) -> list[str]:
    text = _selection_text(payload)

    selected = ["overview"]

    for field, hints in PROFILE_HINTS.items():
        if any(
            _contains_term(text, hint)
            for hint in hints
        ):
            selected.append(field)

    if any(
        _contains_term(text, term)
        for term in _profile_skill_terms()
    ):
        selected.append("skills")

    if any(
        _contains_term(text, term)
        for term in _experience_terms()
    ):
        selected.append("experience")

    if any(
        _contains_term(text, term)
        for term in _education_terms()
    ):
        selected.append("education")

    return list(dict.fromkeys(selected))


def _project_terms(
    project: dict[str, Any],
) -> dict[str, int]:
    weighted_terms: dict[str, int] = {}

    title = project.get("title")

    if isinstance(title, str):
        weighted_terms[_normalize(title)] = 20

    for alias in project.get("aliases", []):
        normalized = _normalize(alias)

        if normalized:
            weighted_terms[normalized] = max(
                weighted_terms.get(normalized, 0),
                20,
            )

    for term in project.get("retrieval_terms", []):
        normalized = _normalize(term)

        if normalized:
            weighted_terms[normalized] = max(
                weighted_terms.get(normalized, 0),
                3,
            )

    for term in project.get("keywords", []):
        normalized = _normalize(term)

        if normalized:
            weighted_terms[normalized] = max(
                weighted_terms.get(normalized, 0),
                2,
            )

    return weighted_terms


PROJECT_TERM_MAP = {
    key: _project_terms(project)
    for key, project in PROJECT_KNOWLEDGE.items()
}

PROJECT_TERM_FREQUENCY: Counter[str] = Counter()

for terms in PROJECT_TERM_MAP.values():
    PROJECT_TERM_FREQUENCY.update(terms.keys())


def _is_usable_project_term(term: str) -> bool:
    if term in SHORT_PROJECT_TERMS:
        return True

    return len(term) >= 4


def _project_score(
    text: str,
    project_key: str,
) -> int:
    score = 0

    for term, base_weight in PROJECT_TERM_MAP[
        project_key
    ].items():
        if not _is_usable_project_term(term):
            continue

        if not _contains_term(text, term):
            continue

        if base_weight >= 20:
            score += base_weight
            continue

        frequency = PROJECT_TERM_FREQUENCY[term]

        if frequency == 1:
            specificity = 3
        elif frequency == 2:
            specificity = 2
        else:
            specificity = 1

        score += base_weight * specificity

    return score


def _rank_projects(
    text: str,
) -> list[tuple[str, int]]:
    ranked = [
        (
            project_key,
            _project_score(text, project_key),
        )
        for project_key in PROJECT_KNOWLEDGE
    ]

    ranked.sort(
        key=lambda item: (-item[1], item[0]),
    )

    return ranked


def _qualified_projects(
    ranked: list[tuple[str, int]],
) -> list[str]:
    qualified = [
        item
        for item in ranked
        if item[1] >= MIN_PROJECT_SCORE
    ]

    if not qualified:
        return []

    top_score = qualified[0][1]
    minimum_secondary_score = max(
        MIN_PROJECT_SCORE,
        int(top_score * 0.6),
    )

    selected = [qualified[0][0]]

    for project_key, score in qualified[1:]:
        if len(selected) >= MAX_SELECTED_PROJECTS:
            break

        if score >= minimum_secondary_score:
            selected.append(project_key)

    return selected


def select_project_keys(
    payload: ChatRequest,
) -> list[str]:
    current_text = _normalize(payload.message)

    selected = _qualified_projects(
        _rank_projects(current_text)
    )

    if selected:
        return selected

    if not _looks_like_follow_up(payload.message):
        return []

    history_text = _normalize(
        " ".join(
            turn.content
            for turn in payload.history[-4:]
        )
    )

    return _qualified_projects(
        _rank_projects(history_text)
    )


def build_knowledge_context(
    payload: ChatRequest,
) -> str:
    profile_fields = select_profile_fields(payload)
    project_keys = select_project_keys(payload)

    profile = {
        field: PROFILE_KNOWLEDGE[field]
        for field in profile_fields
        if field in PROFILE_KNOWLEDGE
    }

    projects = {
        key: PROJECT_KNOWLEDGE[key]
        for key in project_keys
    }

    context = {
        "profile": profile,
        "projects": projects,
    }

    return json.dumps(
        context,
        ensure_ascii=False,
        separators=(",", ":"),
    )
