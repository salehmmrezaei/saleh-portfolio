import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache

from sqlalchemy import create_engine, func, select
from sqlalchemy.engine import Engine

from ..config import get_database_url
from ..models import KnowledgeChunk
from ..project_knowledge import PROJECT_KNOWLEDGE
from .knowledge_embeddings import embed_texts


DEFAULT_RESULT_LIMIT = 6
CANDIDATE_LIMIT = 16

RRF_K = 60
LEXICAL_WEIGHT = 1.25
VECTOR_WEIGHT = 1.0

FUZZY_PROJECT_THRESHOLD = 0.84


@dataclass(frozen=True)
class RetrievalCandidate:
    id: int
    source_type: str
    source_key: str
    section: str
    chunk_index: int
    title: str
    content: str


@dataclass(frozen=True)
class RetrievedKnowledge:
    candidate: RetrievalCandidate
    score: float
    matched_by: tuple[str, ...]


@lru_cache
def _get_engine() -> Engine:
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )


def _normalize(value: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        " ",
        value.lower(),
    ).strip()


def _contains_phrase(
    text: str,
    phrase: str,
) -> bool:
    if not text or not phrase:
        return False

    return (
        f" {phrase} "
        in f" {text} "
    )


def _fuzzy_phrase_score(
    query: str,
    phrase: str,
) -> float:
    query_tokens = query.split()
    phrase_tokens = phrase.split()

    if not query_tokens or not phrase_tokens:
        return 0.0

    if len(phrase_tokens) > len(query_tokens):
        return 0.0

    # Short technical aliases such as AI, RL and RAG
    # should only be matched exactly.
    if (
        len(phrase_tokens) == 1
        and len(phrase_tokens[0]) < 5
    ):
        return 0.0

    size = len(phrase_tokens)

    scores = []

    for start in range(
        0,
        len(query_tokens) - size + 1,
    ):
        window = " ".join(
            query_tokens[
                start : start + size
            ]
        )

        scores.append(
            SequenceMatcher(
                None,
                window,
                phrase,
            ).ratio()
        )

    return max(scores, default=0.0)


def match_project_keys(
    query: str,
) -> tuple[str, ...]:
    normalized_query = _normalize(query)

    if not normalized_query:
        return ()

    matched: list[str] = []

    for project_key, project in (
        PROJECT_KNOWLEDGE.items()
    ):
        raw_terms = [
            project.get(
                "title",
                project_key,
            ),
            *project.get(
                "aliases",
                [],
            ),
        ]

        terms = {
            _normalize(str(term))
            for term in raw_terms
            if term
        }

        exact_match = any(
            _contains_phrase(
                normalized_query,
                term,
            )
            for term in terms
        )

        if exact_match:
            matched.append(project_key)
            continue

        best_score = max(
            (
                _fuzzy_phrase_score(
                    normalized_query,
                    term,
                )
                for term in terms
            ),
            default=0.0,
        )

        if best_score >= FUZZY_PROJECT_THRESHOLD:
            matched.append(project_key)

    return tuple(matched)


def is_project_query(
    query: str,
) -> bool:
    normalized = _normalize(query)

    if match_project_keys(query):
        return True

    return bool(
        re.search(
            r"\bprojects?\b",
            normalized,
        )
    )


def is_project_catalog_query(
    query: str,
) -> bool:
    normalized = _normalize(query)

    patterns = (
        r"^what projects has\b",
        r"^what projects have\b",
        r"^what are saleh s projects\b",
        r"^what are his projects\b",
        r"^list saleh s projects\b",
        r"^list his projects\b",
        r"^show me saleh s projects\b",
        r"^show me his projects\b",
        r"^tell me about saleh s projects\b",
        r"^tell me about his projects\b",
    )

    return any(
        re.search(
            pattern,
            normalized,
        )
        for pattern in patterns
    )


def _row_to_candidate(
    row,
) -> RetrievalCandidate:
    return RetrievalCandidate(
        id=row["id"],
        source_type=row["source_type"],
        source_key=row["source_key"],
        section=row["section"],
        chunk_index=row["chunk_index"],
        title=row["title"],
        content=row["content"],
    )


def _apply_scope(
    statement,
    *,
    source_type: str | None,
    source_keys: tuple[str, ...],
):
    if source_type:
        statement = statement.where(
            KnowledgeChunk.source_type
            == source_type
        )

    if source_keys:
        statement = statement.where(
            KnowledgeChunk.source_key.in_(
                source_keys
            )
        )

    return statement


def lexical_search(
    query: str,
    *,
    limit: int = CANDIDATE_LIMIT,
    source_type: str | None = None,
    source_keys: tuple[str, ...] = (),
) -> list[RetrievalCandidate]:
    query = query.strip()

    if not query:
        return []

    tsquery = func.websearch_to_tsquery(
        "english",
        query,
    )

    rank = func.ts_rank_cd(
        KnowledgeChunk.search_document,
        tsquery,
    )

    statement = select(
        KnowledgeChunk.id,
        KnowledgeChunk.source_type,
        KnowledgeChunk.source_key,
        KnowledgeChunk.section,
        KnowledgeChunk.chunk_index,
        KnowledgeChunk.title,
        KnowledgeChunk.content,
    ).where(
        KnowledgeChunk.search_document.op(
            "@@"
        )(tsquery)
    )

    statement = _apply_scope(
        statement,
        source_type=source_type,
        source_keys=source_keys,
    )

    statement = (
        statement
        .order_by(
            rank.desc(),
            KnowledgeChunk.id.asc(),
        )
        .limit(limit)
    )

    with _get_engine().connect() as connection:
        rows = connection.execute(
            statement
        ).mappings().all()

    return [
        _row_to_candidate(row)
        for row in rows
    ]


def vector_search(
    query: str,
    *,
    limit: int = CANDIDATE_LIMIT,
    source_type: str | None = None,
    source_keys: tuple[str, ...] = (),
) -> list[RetrievalCandidate]:
    query = query.strip()

    if not query:
        return []

    query_vector = embed_texts(
        [query]
    )[0]

    distance = (
        KnowledgeChunk.embedding.cosine_distance(
            query_vector
        )
    )

    statement = select(
        KnowledgeChunk.id,
        KnowledgeChunk.source_type,
        KnowledgeChunk.source_key,
        KnowledgeChunk.section,
        KnowledgeChunk.chunk_index,
        KnowledgeChunk.title,
        KnowledgeChunk.content,
    ).where(
        KnowledgeChunk.embedding.is_not(None)
    )

    statement = _apply_scope(
        statement,
        source_type=source_type,
        source_keys=source_keys,
    )

    statement = (
        statement
        .order_by(
            distance.asc(),
            KnowledgeChunk.id.asc(),
        )
        .limit(limit)
    )

    with _get_engine().connect() as connection:
        rows = connection.execute(
            statement
        ).mappings().all()

    return [
        _row_to_candidate(row)
        for row in rows
    ]


def project_catalog() -> list[
    RetrievedKnowledge
]:
    statement = (
        select(
            KnowledgeChunk.id,
            KnowledgeChunk.source_type,
            KnowledgeChunk.source_key,
            KnowledgeChunk.section,
            KnowledgeChunk.chunk_index,
            KnowledgeChunk.title,
            KnowledgeChunk.content,
        )
        .where(
            KnowledgeChunk.source_type
            == "project",
            KnowledgeChunk.section
            == "overview",
        )
    )

    with _get_engine().connect() as connection:
        rows = connection.execute(
            statement
        ).mappings().all()

    candidates = {
        row["source_key"]: _row_to_candidate(
            row
        )
        for row in rows
    }

    results: list[RetrievedKnowledge] = []

    for project_key in PROJECT_KNOWLEDGE:
        candidate = candidates.get(
            project_key
        )

        if candidate is None:
            continue

        results.append(
            RetrievedKnowledge(
                candidate=candidate,
                score=1.0,
                matched_by=("catalog",),
            )
        )

    return results


def fuse_ranked_results(
    *,
    lexical: list[RetrievalCandidate],
    vector: list[RetrievalCandidate],
    limit: int = DEFAULT_RESULT_LIMIT,
) -> list[RetrievedKnowledge]:
    if limit < 1:
        return []

    scores: dict[int, float] = {}
    candidates: dict[
        int,
        RetrievalCandidate,
    ] = {}
    modes: dict[int, set[str]] = {}

    for rank, candidate in enumerate(
        lexical,
        start=1,
    ):
        candidates[candidate.id] = candidate

        scores[candidate.id] = (
            scores.get(candidate.id, 0.0)
            + LEXICAL_WEIGHT
            / (RRF_K + rank)
        )

        modes.setdefault(
            candidate.id,
            set(),
        ).add("lexical")

    for rank, candidate in enumerate(
        vector,
        start=1,
    ):
        candidates[candidate.id] = candidate

        scores[candidate.id] = (
            scores.get(candidate.id, 0.0)
            + VECTOR_WEIGHT
            / (RRF_K + rank)
        )

        modes.setdefault(
            candidate.id,
            set(),
        ).add("vector")

    ordered_ids = sorted(
        scores,
        key=lambda candidate_id: (
            -scores[candidate_id],
            candidate_id,
        ),
    )

    return [
        RetrievedKnowledge(
            candidate=candidates[
                candidate_id
            ],
            score=scores[candidate_id],
            matched_by=tuple(
                sorted(
                    modes[candidate_id]
                )
            ),
        )
        for candidate_id
        in ordered_ids[:limit]
    ]


def retrieve_knowledge(
    query: str,
    *,
    limit: int = DEFAULT_RESULT_LIMIT,
) -> list[RetrievedKnowledge]:
    query = query.strip()

    if not query:
        return []

    if is_project_catalog_query(query):
        return project_catalog()

    project_keys = match_project_keys(
        query
    )

    if project_keys:
        source_type = "project"
        source_keys = project_keys
    elif is_project_query(query):
        source_type = "project"
        source_keys = ()
    else:
        source_type = None
        source_keys = ()

    lexical = lexical_search(
        query,
        limit=CANDIDATE_LIMIT,
        source_type=source_type,
        source_keys=source_keys,
    )

    vector = vector_search(
        query,
        limit=CANDIDATE_LIMIT,
        source_type=source_type,
        source_keys=source_keys,
    )

    return fuse_ranked_results(
        lexical=lexical,
        vector=vector,
        limit=limit,
    )
