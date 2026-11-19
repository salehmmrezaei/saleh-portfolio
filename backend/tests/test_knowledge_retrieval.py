from app.project_knowledge import PROJECT_KNOWLEDGE
from app.services import knowledge_retrieval
from app.services.knowledge_builder import build_knowledge_chunks
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


def test_named_project_questions_scope_both_search_channels(monkeypatch) -> None:
    calls = []

    def search(query, **kwargs):
        calls.append(kwargs)
        return []

    monkeypatch.setattr(knowledge_retrieval, "lexical_search", search)
    monkeypatch.setattr(knowledge_retrieval, "vector_search", search)

    for query, keys in (
        ("What AWS skills does MediFlow AI demonstrate?", {"mediflow-ai"}),
        ("How is Casa deployed?", {"ai-rental-agent"}),
        ("Compare MediFlow AI and Casa.", {"mediflow-ai", "ai-rental-agent"}),
    ):
        calls.clear()
        knowledge_retrieval.retrieve_knowledge(query)
        assert len(calls) == 2
        assert all(call["source_type"] == "project" for call in calls)
        assert all(set(call["source_keys"]) == keys for call in calls)


def test_catalogs_return_all_matching_projects_without_top_six_limit(monkeypatch) -> None:
    chunks = build_knowledge_chunks()
    sections = []

    def catalog(*, section="overview"):
        sections.append(section)
        return [
            knowledge_retrieval.RetrievedKnowledge(
                candidate=knowledge_retrieval.RetrievalCandidate(
                    id=index, source_type="project", source_key=chunk.source_key,
                    section=chunk.section, chunk_index=chunk.chunk_index,
                    title=chunk.title, content=chunk.content,
                ),
                score=1.0, matched_by=("catalog",),
            )
            for index, chunk in enumerate(chunks)
            if chunk.source_type == "project" and chunk.section == section
        ]

    def unexpected_search(*args, **kwargs):
        raise AssertionError("Catalog queries should not use top-k search")

    monkeypatch.setattr(knowledge_retrieval, "project_catalog", catalog)
    monkeypatch.setattr(knowledge_retrieval, "lexical_search", unexpected_search)
    monkeypatch.setattr(knowledge_retrieval, "vector_search", unexpected_search)

    projects = knowledge_retrieval.retrieve_knowledge("List all projects.", limit=6)
    assert {result.candidate.source_key for result in projects} == set(PROJECT_KNOWLEDGE)
    assert len(projects) > 6

    demos = knowledge_retrieval.retrieve_knowledge("Which projects have live demos?", limit=1)
    assert {result.candidate.source_key for result in demos} == {"mediflow-ai", "ai-rental-agent"}
    assert sections == ["overview", "public_demo"]


def test_named_comparison_keeps_evidence_from_both_projects(monkeypatch) -> None:
    from dataclasses import replace

    mediflow = [
        replace(candidate(index, "MediFlow"), source_key="mediflow-ai")
        for index in range(1, 9)
    ]
    rental = [
        replace(candidate(index, "Casa"), source_key="ai-rental-agent")
        for index in range(9, 12)
    ]
    monkeypatch.setattr(
        knowledge_retrieval, "lexical_search",
        lambda *args, **kwargs: mediflow + rental,
    )
    monkeypatch.setattr(
        knowledge_retrieval, "vector_search",
        lambda *args, **kwargs: mediflow + rental,
    )

    results = knowledge_retrieval.retrieve_knowledge("Compare MediFlow AI and Casa.", limit=6)

    assert [result.candidate.id for result in results] == [1, 9, 2, 10, 3, 11]


def test_named_demo_access_keeps_exact_url_even_when_hybrid_ranks_architecture(monkeypatch) -> None:
    from dataclasses import replace

    chunk = next(
        chunk for chunk in build_knowledge_chunks()
        if chunk.source_key == "mediflow-ai" and chunk.section == "public_demo"
    )
    demo = knowledge_retrieval.RetrievedKnowledge(
        candidate=RetrievalCandidate(
            id=100, source_type="project", source_key=chunk.source_key,
            section=chunk.section, chunk_index=chunk.chunk_index,
            title=chunk.title, content=chunk.content,
        ),
        score=1.0, matched_by=("catalog",),
    )
    architecture = replace(candidate(1, "MediFlow architecture"), source_key="mediflow-ai")
    monkeypatch.setattr(knowledge_retrieval, "project_catalog", lambda **kwargs: [demo])
    monkeypatch.setattr(knowledge_retrieval, "lexical_search", lambda *args, **kwargs: [architecture])
    monkeypatch.setattr(knowledge_retrieval, "vector_search", lambda *args, **kwargs: [architecture])

    results = knowledge_retrieval.retrieve_knowledge("Where can I try MediFlowAI?", limit=1)

    assert len(results) == 1
    assert results[0].candidate.section == "public_demo"
    assert "https://mediflow.salehmmrezaei.com/demo" in results[0].candidate.content
    assert "simulat" in results[0].candidate.content.lower()
