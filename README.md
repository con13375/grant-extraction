# Grant Extraction

A research prototype for extracting structured requirements from Spanish
public-grant documents (BDNS/BOE) with exact source citations.

## What this is

This project compares several approaches — prompt-only, RAG, supervised
fine-tuning (LoRA/QLoRA), and a neuro-symbolic rule engine — for turning
administrative grant documents into structured, machine-checkable
requirements.

The core design principle: **every extracted fact must carry a verifiable
citation back to the source text.** The schema enforces this — a
`Requirement` cannot be constructed without an `Evidence` object that
points at a character span in the original document.

## Status (as of October 2026)

- [x] Repository skeleton and packaging (`pyproject.toml`, `src/` layout)
- [x] Pydantic schema for requirements and evidence spans
- [x] PDF ingestion CLI (`grant-extract ingest`)
- [x] Verified citation spans on a real BDNS document (51 pages)
- [ ] Automated extraction (LLM) — in progress
- [ ] Retrieval baseline (RAG)
- [ ] Fine-tuning (LoRA/QLoRA)
- [ ] Rule engine

## How to run

```bash
# install (editable)
pip install -e .

# smoke test
grant-extract hello

# ingest a PDF
grant-extract ingest data/raw/894743.pdf --out data/processed/894743.json
