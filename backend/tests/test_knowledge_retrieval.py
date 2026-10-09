from app.services.knowledge_retrieval import (
    RetrievalCandidate,
    fuse_ranked_results,
)


def candidate(
    candidate_id: int,
    title: str,
) -> RetrievalCandidate:
    return RetrievalCandidate(
        id=candidate_id,
        source_type="project",
        source_key=f"project-{candidate_id}",
        section="overview",
        chunk_index=0,
        title=title,
        content=f"Content for {title}",
    )


def test_result_found_by_both_ranks_first() -> None:
    shared = candidate(
        1,
        "Shared result",
    )

    lexical_only = candidate(
        2,
        "Lexical result",
    )

    vector_only = candidate(
        3,
        "Vector result",
    )

    results = fuse_ranked_results(
        lexical=[
            lexical_only,
            shared,
        ],
        vector=[
            vector_only,
            shared,
        ],
        limit=3,
    )

    assert results[0].candidate.id == 1

    assert results[0].matched_by == (
        "lexical",
        "vector",
    )


def test_lexical_result_gets_weight() -> None:
    lexical = candidate(
        1,
        "Exact lexical result",
    )

    vector = candidate(
        2,
        "Vector result",
    )

    results = fuse_ranked_results(
        lexical=[lexical],
        vector=[vector],
        limit=2,
    )

    assert results[0].candidate.id == 1


def test_duplicates_are_removed() -> None:
    shared = candidate(
        1,
        "Shared result",
    )

    results = fuse_ranked_results(
        lexical=[shared],
        vector=[shared],
        limit=6,
    )

    assert len(results) == 1


def test_limit_is_respected() -> None:
    results = fuse_ranked_results(
        lexical=[
            candidate(
                index,
                f"Result {index}",
            )
            for index in range(1, 10)
        ],
        vector=[],
        limit=3,
    )

    assert len(results) == 3


def test_zero_limit_returns_empty() -> None:
    results = fuse_ranked_results(
        lexical=[
            candidate(
                1,
                "Result",
            )
        ],
        vector=[],
        limit=0,
    )

    assert results == []
