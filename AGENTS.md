# AGENTS.md — grant-extraction

## Objective

Build a reproducible pipeline that extracts structured requirements from
Spanish public-grant documents (BDNS/BOE) with exact source citations, plus
a benchmark runner comparing prompt-only, RAG, SFT, SFT+RAG, and
neuro-symbolic variants.

## Repository map

- `src/grant_extract/cli.py` — Typer CLI. This is the entry point agents
  should use for any file operation or test run.
- `src/grant_extract/schema/` — Pydantic models. Changing these breaks
  everything downstream.
- `src/grant_extract/ingestion/` — PDF/HTML → normalized text. Never mutate
  `data/raw/`.
- `data/manifests/` — one JSON per source document: URL, retrieval date,
  SHA-256, licence.
- `data/raw/`, `data/processed/` — gitignored. Do not commit anything here.
- `docs/agent_log.md` — log each agent session: what was asked, what came
  back, what was kept.

## Fixed constraints (do not violate)

- Every extracted field must carry `evidence.span_start` and
  `evidence.span_end`. A field without a verifiable span is a bug.
- Never edit `data/splits/test.jsonl` (when it exists). The test split is
  frozen until the final hold-out evaluation.
- No network calls in tests. Use `tests/fixtures/` recorded responses.
- Do not add dependencies silently. Justify new packages in the commit
  message or in `docs/decisions/`.
- Python 3.11. Dependencies pinned in `pyproject.toml`.
- Do not commit anything under `data/raw/`, `data/processed/`,
  `data/interim/`, `.venv/`, or `__pycache__/`.

## Commands

    pip install -e .                        # editable install
    grant-extract hello                     # smoke test
    grant-extract ingest <pdf> --out <json> # ingest a PDF
    pytest                                  # once tests/ exists

## Style

- Pydantic v2 for all schemas. No dataclasses across module boundaries.
- Type hints on every public function.
- Log via typer.echo for CLI output.
- Fail loudly on schema violations; never silently coerce.

## Completion criteria for an agent-produced change

1. `python -c "import grant_extract"` succeeds.
2. If it touches the CLI: `grant-extract --help` shows the command.
3. If it touches the schema: existing fixtures still validate.
4. Commit message says what and why.
5. No new dependencies unless noted.

## What not to do

- Do not invent file paths or module names. If unsure, `ls` first.
- Do not modify `.gitignore` to allow tracking `data/raw/` or `.venv/`.
- Do not rewrite large sections of the codebase in one shot.
- Do not guess the BDNS document schema. Read `schema/requirement.py`.
