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

## Status (as of November 2026)

- [x] Repository skeleton and packaging (`pyproject.toml`, `src/` layout)
- [x] Pydantic schema for requirements and evidence spans
- [x] PDF ingestion CLI (`grant-extract ingest`)
- [x] Verified citation spans on a real BDNS document (51 pages)
- [x] Source manifests for 4 BDNS documents (`data/manifests/`)
- [x] Annotation guide and train/dev/test split (`docs/annotation_guide.md`, `data/splits/split.json`)
- [ ] Gold annotations — 10 items from one train/dev document (in progress)
- [ ] Automated extraction (LLM) — blocked on HTCondor accounting group
- [ ] Retrieval baseline (RAG)
- [ ] Fine-tuning (LoRA/QLoRA)
- [ ] Rule engine

## Data

Corpus: 4 BDNS grant calls, documented in `data/manifests/`. Each manifest
records the BDNS identifier, source URL, retrieval date, SHA-256, page count,
and licence terms. Raw PDFs and extracted text are gitignored; only the
manifests are tracked.

Split (`data/splits/split.json`): 1 document frozen as test, 3 as
train/dev. Gold annotations live in `data/gold/` (in progress).

Ingestion notes: `docs/ingestion_notes.md` (in progress) records
extraction failures — notably that bilingual Castellano/Valencian PDFs
require `fonttools` for correct text extraction.

## How to run

```bash
# install (editable)
pip install -e .

# smoke test
grant-extract hello

# ingest a PDF
grant-extract ingest data/raw/894743.pdf --out data/processed/894743.json
