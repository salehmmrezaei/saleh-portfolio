import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from app.services import knowledge_sync
from app.services.knowledge_builder import (
    KnowledgeChunkInput,
)
from app.services.knowledge_sync import (
    ExistingChunkState,
    needs_embedding,
)


def make_chunk() -> KnowledgeChunkInput:
    return KnowledgeChunkInput(
        source_type="project",
        source_key="repopilot-ai",
        section="architecture",
        chunk_index=0,
        title="RepoPilot AI — Architecture",
        content="Hybrid retrieval architecture.",
        content_hash="a" * 64,
    )


def make_existing(
    *,
    content_hash: str = "a" * 64,
    embedding_model: str | None = (
        "text-embedding-3-small"
    ),
    has_embedding: bool = True,
) -> ExistingChunkState:
    return ExistingChunkState(
        id=1,
        source_type="project",
        source_key="repopilot-ai",
        section="architecture",
        chunk_index=0,
        content_hash=content_hash,
        embedding_model=embedding_model,
        has_embedding=has_embedding,
    )


def test_new_chunk_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=None,
        embedding_model="text-embedding-3-small",
    )


def test_unchanged_chunk_skips_embedding() -> None:
    assert not needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(),
        embedding_model="text-embedding-3-small",
    )


def test_changed_content_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(
            content_hash="b" * 64
        ),
        embedding_model="text-embedding-3-small",
    )


def test_changed_model_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(
            embedding_model="old-model"
        ),
        embedding_model="text-embedding-3-small",
    )


def test_missing_embedding_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(
            has_embedding=False
        ),
        embedding_model="text-embedding-3-small",
    )


def test_check_command_validates_without_database_or_ai(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbidden(*args, **kwargs):
        pytest.fail("Source validation must not access the database or AI")

    monkeypatch.setattr(knowledge_sync, "create_engine", forbidden)
    monkeypatch.setattr(knowledge_sync, "embed_chunks", forbidden)
    monkeypatch.setattr(knowledge_sync, "sync_knowledge", forbidden)

    knowledge_sync.main(["--check"])

    summary = json.loads(capsys.readouterr().out)
    assert summary["sources"]["project/mediflow-ai"] > 0
    assert summary["sources"]["project/ai-rental-agent"] > 0
    assert summary["total"] == sum(summary["sources"].values())


def test_check_module_runs_without_credentials() -> None:
    environment = {
        key: value for key, value in os.environ.items()
        if key not in {"DATABASE_URL", "MIGRATION_DATABASE_URL", "OPENAI_API_KEY"}
    }
    environment["PYTHON_DOTENV_DISABLED"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "app.services.knowledge_sync", "--check"],
        cwd=Path(__file__).resolve().parents[1],
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )

    summary = json.loads(completed.stdout)
    assert summary["sources"]["project/mediflow-ai"] > 0
    assert summary["sources"]["project/ai-rental-agent"] > 0


def test_sync_command_reports_result(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls = []

    def sync():
        calls.append(True)
        return knowledge_sync.KnowledgeSyncResult(
            total=200, embedded=12, upserted=12, deleted=0,
        )

    monkeypatch.setattr(knowledge_sync, "sync_knowledge", sync)
    knowledge_sync.main(["--sync"])

    assert calls == [True]
    assert json.loads(capsys.readouterr().out) == {
        "total": 200, "embedded": 12, "upserted": 12, "deleted": 0,
    }


def test_command_requires_explicit_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden():
        pytest.fail("No mode must not synchronize knowledge")

    monkeypatch.setattr(knowledge_sync, "sync_knowledge", forbidden)

    with pytest.raises(SystemExit) as error:
        knowledge_sync.main([])

    assert error.value.code == 2
