# Portfolio chatbot knowledge

The chatbot retrieves project context from PostgreSQL/pgvector and adds selected
profile facts directly from Python. Editing knowledge source files alone does
not refresh an existing database index.

## Source files

- `app/project_knowledge.py`: project capabilities, architecture, stack,
  challenges, limitations, public links and public demo behavior.
- `app/profile_knowledge.py`: professional profile and skills supported by work
  experience and projects.
- `app/services/knowledge_builder.py`: deterministic chunks and content hashes.
- `../docs/chatbot/`: source evidence and review notes.

MediFlow AI and AI Rental Agent (Casa) include separate public-demo records.
Both public demos use fictional data and simulated responses. Casa's public
demo reads authorized PostgreSQL records but disables rental mutations and live
model calls. MediFlow's public demo runs in browser memory without AWS/OpenAI
calls; its authenticated Doctor Workspace uses the full serverless workflow.

## Validate locally

From `backend/`, with `requirements-dev.txt` installed in your Python environment:

```sh
python -m app.services.knowledge_sync --check
python -m pytest
```

`--check` builds every chunk, validates nonempty content and unique identities,
and prints counts by source. It needs no credentials, database or model calls.
Tests mock external services; they do not measure live answer quality.

## Refresh the chatbot index

Run from the updated backend checkout in the environment for the intended
portfolio database. Configure privately through its existing environment or
ignored `backend/.env`:

- `DATABASE_URL`: existing backend runtime connection, also required when
  loading the shared database models. It can remain read-only when a separate
  writer connection is supplied below.
- `MIGRATION_DATABASE_URL`: writer connection for the existing `knowledge_chunks`
  table. The sync falls back to `DATABASE_URL` if this is absent. The runtime
  database role can remain read-only.
- `OPENAI_API_KEY`: server-side credential for embeddings.
- `OPENAI_EMBEDDING_MODEL`: optional; retain the configured compatible model and
  1536 dimensions used by the existing index.

```sh
python -m app.services.knowledge_sync --check
python -m app.services.knowledge_sync --sync
```

`--sync` makes embedding requests for new/changed chunks or chunks missing the
configured embedding, then upserts them and removes obsolete chunk identities
in one database transaction. Unchanged chunks with current embeddings are
skipped. It prints total, embedded, upserted and deleted counts. The command
requires an explicit `--check` or `--sync` mode. It does not modify project,
experience or contact records. Existing knowledge schema migrations must
already be applied; this update adds no migration.

Deploy the updated backend as well as refreshing its index so the new aliases,
demo retrieval and follow-up handling are active. Knowledge synchronization is
an operator command, not an application-startup or request hook. Credentials
are never needed in the frontend.

## Acceptance questions

After deployment and index refresh, try these in a fresh chat and then as
follow-ups:

- What is MediFlowAI, and how are discharge letters reviewed?
- Can a doctor reopen a previous discharge job?
- Where can I try it? Does its public demo use real AI?
- Tell me about Casa and how booking conflicts are handled.
- Can Casa's public demo make a booking or send a message?
- Compare MediFlow AI and AI Rental Agent.
- Which projects have live demos?
- What AWS and backend skills has Saleh demonstrated in these projects?

Check correct demo/source URLs, the distinction between demo and normal mode,
evidence from both projects in comparisons, and no invented clinical outcomes,
certifications, production adoption or real tenancies.
