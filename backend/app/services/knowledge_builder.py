from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from ..profile_knowledge import PROFILE_KNOWLEDGE
from ..project_knowledge import PROJECT_KNOWLEDGE


@dataclass(frozen=True)
class KnowledgeChunkInput:
    source_type: str
    source_key: str
    section: str
    chunk_index: int
    title: str
    content: str
    content_hash: str


def _humanize(value: str) -> str:
    return value.replace("_", " ").strip().title()


def _render(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()

    if isinstance(value, (int, float, bool)):
        return str(value)

    if isinstance(value, dict):
        lines: list[str] = []

        for key, nested in value.items():
            rendered = _render(nested)

            if not rendered:
                continue

            lines.append(
                f"{_humanize(str(key))}: {rendered}"
            )

        return "\n".join(lines)

    if isinstance(value, (list, tuple)):
        items = [
            _render(item)
            for item in value
        ]

        return "\n".join(
            f"- {item}"
            for item in items
            if item
        )

    return ""


def _make_chunk(
    *,
    source_type: str,
    source_key: str,
    section: str,
    chunk_index: int,
    title: str,
    value: Any,
) -> KnowledgeChunkInput:
    content = _render(value).strip()

    if not content:
        raise ValueError(
            f"Empty knowledge chunk: "
            f"{source_type}/{source_key}/"
            f"{section}/{chunk_index}"
        )

    digest_source = (
        f"{title}\0{content}"
    ).encode("utf-8")

    return KnowledgeChunkInput(
        source_type=source_type,
        source_key=source_key,
        section=section,
        chunk_index=chunk_index,
        title=title.strip(),
        content=content,
        content_hash=sha256(
            digest_source
        ).hexdigest(),
    )


def build_profile_chunks() -> list[KnowledgeChunkInput]:
    chunks: list[KnowledgeChunkInput] = []

    overview = PROFILE_KNOWLEDGE.get("overview")

    if overview:
        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="overview",
                chunk_index=0,
                title="Saleh Rezaei — Professional Overview",
                value=overview,
            )
        )

    for index, experience in enumerate(
        PROFILE_KNOWLEDGE.get(
            "experience",
            [],
        )
    ):
        company = experience.get(
            "company",
            "Experience",
        )
        role = experience.get(
            "role",
            "",
        )

        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="experience",
                chunk_index=index,
                title=(
                    f"Experience — {company}"
                    + (
                        f" — {role}"
                        if role
                        else ""
                    )
                ),
                value=experience,
            )
        )

    for index, education in enumerate(
        PROFILE_KNOWLEDGE.get(
            "education",
            [],
        )
    ):
        institution = education.get(
            "institution",
            "Education",
        )

        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="education",
                chunk_index=index,
                title=f"Education — {institution}",
                value=education,
            )
        )

    skills = PROFILE_KNOWLEDGE.get(
        "skills",
        {},
    )

    for index, (
        category,
        category_skills,
    ) in enumerate(skills.items()):
        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="skills",
                chunk_index=index,
                title=(
                    "Skills — "
                    f"{_humanize(category)}"
                ),
                value=category_skills,
            )
        )

    for index, interest in enumerate(
        PROFILE_KNOWLEDGE.get(
            "professional_interests",
            [],
        )
    ):
        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="professional_interests",
                chunk_index=index,
                title=(
                    "Professional Interest — "
                    f"{interest.get('topic', 'AI')}"
                ),
                value=interest,
            )
        )

    availability = PROFILE_KNOWLEDGE.get(
        "availability"
    )

    if availability:
        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="availability",
                chunk_index=0,
                title="Availability and Target Roles",
                value=availability,
            )
        )

    work_authorization = (
        PROFILE_KNOWLEDGE.get(
            "work_authorization",
            {},
        )
    )

    for index, (
        country,
        authorization,
    ) in enumerate(
        work_authorization.items()
    ):
        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="work_authorization",
                chunk_index=index,
                title=(
                    "Work Authorization — "
                    f"{_humanize(country)}"
                ),
                value={
                    "country": _humanize(
                        country
                    ),
                    **authorization,
                },
            )
        )

    for index, interest in enumerate(
        PROFILE_KNOWLEDGE.get(
            "personal_interests",
            [],
        )
    ):
        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="personal_interests",
                chunk_index=index,
                title=(
                    "Personal Interest — "
                    f"{interest.get('topic', 'Interest')}"
                ),
                value=interest,
            )
        )

    public_links = PROFILE_KNOWLEDGE.get(
        "public_links"
    )

    if public_links:
        chunks.append(
            _make_chunk(
                source_type="profile",
                source_key="profile",
                section="public_links",
                chunk_index=0,
                title="Public Contact and Links",
                value=public_links,
            )
        )

    return chunks


def _project_overview(
    project: dict[str, Any],
) -> dict[str, Any]:
    overview: dict[str, Any] = {}

    for field in (
        "title",
        "aliases",
        "role",
        "year",
        "type",
        "overview",
        "keywords",
    ):
        value = project.get(field)

        if value:
            overview[field] = value

    return overview


def build_project_chunks() -> list[KnowledgeChunkInput]:
    chunks: list[KnowledgeChunkInput] = []

    for project_key, project in (
        PROJECT_KNOWLEDGE.items()
    ):
        project_title = project.get(
            "title",
            project_key,
        )

        chunks.append(
            _make_chunk(
                source_type="project",
                source_key=project_key,
                section="overview",
                chunk_index=0,
                title=f"{project_title} — Overview",
                value=_project_overview(
                    project
                ),
            )
        )

        for section in (
            "problem",
            "architecture",
        ):
            value = project.get(section)

            if value:
                chunks.append(
                    _make_chunk(
                        source_type="project",
                        source_key=project_key,
                        section=section,
                        chunk_index=0,
                        title=(
                            f"{project_title} — "
                            f"{_humanize(section)}"
                        ),
                        value=value,
                    )
                )

        for index, stage in enumerate(
            project.get("pipeline", [])
        ):
            stage_title = (
                stage.get("title")
                if isinstance(stage, dict)
                else None
            )

            chunks.append(
                _make_chunk(
                    source_type="project",
                    source_key=project_key,
                    section="pipeline",
                    chunk_index=index,
                    title=(
                        f"{project_title} — Pipeline"
                        + (
                            f" — {stage_title}"
                            if stage_title
                            else ""
                        )
                    ),
                    value=stage,
                )
            )

        stack = project.get(
            "stack",
            {},
        )

        for index, (
            stack_name,
            stack_details,
        ) in enumerate(stack.items()):
            chunks.append(
                _make_chunk(
                    source_type="project",
                    source_key=project_key,
                    section="stack",
                    chunk_index=index,
                    title=(
                        f"{project_title} — Stack — "
                        f"{stack_name}"
                    ),
                    value={
                        "group": stack_name,
                        **stack_details,
                    },
                )
            )

        engineering_details = project.get(
            "engineering_details"
        )

        if engineering_details:
            chunks.append(
                _make_chunk(
                    source_type="project",
                    source_key=project_key,
                    section="engineering_details",
                    chunk_index=0,
                    title=(
                        f"{project_title} — "
                        "Engineering Details"
                    ),
                    value=engineering_details,
                )
            )

        for index, challenge in enumerate(
            project.get("challenges", [])
        ):
            challenge_title = (
                challenge.get("title")
                if isinstance(
                    challenge,
                    dict,
                )
                else None
            )

            chunks.append(
                _make_chunk(
                    source_type="project",
                    source_key=project_key,
                    section="challenges",
                    chunk_index=index,
                    title=(
                        f"{project_title} — Challenge"
                        + (
                            f" — {challenge_title}"
                            if challenge_title
                            else ""
                        )
                    ),
                    value=challenge,
                )
            )

        for section in (
            "security_and_reliability",
            "testing_and_quality",
            "outcomes",
            "verified_metrics",
            "limitations",
        ):
            value = project.get(section)

            if value:
                chunks.append(
                    _make_chunk(
                        source_type="project",
                        source_key=project_key,
                        section=section,
                        chunk_index=0,
                        title=(
                            f"{project_title} — "
                            f"{_humanize(section)}"
                        ),
                        value=value,
                    )
                )

    return chunks


def build_knowledge_chunks() -> list[KnowledgeChunkInput]:
    chunks = [
        *build_profile_chunks(),
        *build_project_chunks(),
    ]

    identities = [
        (
            chunk.source_type,
            chunk.source_key,
            chunk.section,
            chunk.chunk_index,
        )
        for chunk in chunks
    ]

    if len(identities) != len(
        set(identities)
    ):
        raise ValueError(
            "Duplicate knowledge chunk identity."
        )

    return chunks
