import json
import re

from ..profile_knowledge import PROFILE_KNOWLEDGE
from ..schemas import ChatRequest
from .knowledge_retrieval import retrieve_knowledge
from .knowledge_selector import select_profile_fields


RAG_RESULT_LIMIT = 6
MAX_CHUNK_CONTEXT_CHARS = 2200

FOLLOW_UP_PATTERNS = (
    r"^what about\b",
    r"^how about\b",
    r"^and\b",
    r"^also\b",
    r"^what was\b",
    r"^what were\b",
    r"^why\b",
    r"^how does it\b",
    r"^how did it\b",
    r"^does it\b",
    r"^did it\b",
    r"^its\b",
    r"^that\b",
    r"^this\b",
)


def _normalize(value: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        value.strip().lower(),
    )


def _looks_like_follow_up(
    message: str,
) -> bool:
    normalized = _normalize(message)

    return any(
        re.search(
            pattern,
            normalized,
        )
        for pattern in FOLLOW_UP_PATTERNS
    )


def build_retrieval_query(
    payload: ChatRequest,
) -> str:
    if not _looks_like_follow_up(
        payload.message
    ):
        return payload.message

    previous_user_messages = [
        turn.content
        for turn in payload.history
        if turn.role == "user"
    ][-2:]

    if not previous_user_messages:
        return payload.message

    return "\n".join(
        [
            *previous_user_messages,
            payload.message,
        ]
    )


def _profile_context(
    payload: ChatRequest,
) -> dict:
    fields = select_profile_fields(
        payload
    )

    return {
        field: PROFILE_KNOWLEDGE[field]
        for field in fields
        if field in PROFILE_KNOWLEDGE
    }


def build_chat_knowledge_context(
    payload: ChatRequest,
) -> str:
    retrieval_query = build_retrieval_query(
        payload
    )

    results = retrieve_knowledge(
        retrieval_query,
        limit=RAG_RESULT_LIMIT,
    )

    chunks = []

    for rank, result in enumerate(
        results,
        start=1,
    ):
        candidate = result.candidate

        chunks.append(
            {
                "rank": rank,
                "source_type": (
                    candidate.source_type
                ),
                "source_key": (
                    candidate.source_key
                ),
                "section": candidate.section,
                "title": candidate.title,
                "content": (
                    candidate.content[
                        :MAX_CHUNK_CONTEXT_CHARS
                    ]
                ),
            }
        )

    context = {
        "profile_facts": _profile_context(
            payload
        ),
        "retrieved_chunks": chunks,
    }

    return json.dumps(
        context,
        ensure_ascii=False,
        separators=(",", ":"),
    )
