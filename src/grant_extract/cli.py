import json
from pathlib import Path

import typer
from pypdf import PdfReader

app = typer.Typer()


@app.command("hello")
def hello():
    """Smoke test: confirms the CLI is installed correctly."""
    typer.echo("grant-extract is alive")


@app.command("ingest")
def ingest(
    pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out", "-o", help="Output JSON path"),
):
    """Extract text + page offsets from a PDF and write them to JSON."""
    reader = PdfReader(str(pdf))
    text = ""
    page_offsets = []
    for page in reader.pages:
        page_offsets.append(len(text))
        text += page.extract_text() or ""

    payload = {
        "document_id": pdf.stem,
        "source_path": str(pdf),
        "num_pages": len(reader.pages),
        "num_chars": len(text),
        "page_offsets": page_offsets,
        "text": text,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"Wrote {out} ({len(text)} chars, {len(reader.pages)} pages)")


@app.command("noop")
def noop():
    """Placeholder to prevent Typer from flattening a single-command app."""
    pass


if __name__ == "__main__":
    app()
