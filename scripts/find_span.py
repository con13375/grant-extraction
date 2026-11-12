#!/usr/bin/env python3
"""Find the character span of a quote in a processed document.

Usage:
    python scripts/find_span.py data/processed/894743.json "the quote"
"""
import json
import sys
import re

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    path, quote = sys.argv[1], sys.argv[2]

    doc = json.load(open(path))
    text = doc["text"]

    # Try exact match first
    start = text.find(quote)
    if start != -1:
        end = start + len(quote)
        print(f"exact: span_start = {start} span_end = {end}")
        print(f"       {text[start:end]!r}")
        return

    # Try normalized whitespace
    norm_quote = re.sub(r"\s+", " ", quote).strip()
    for m in re.finditer(re.escape(norm_quote.split(" ")[0]), text):
        # crude: try to match the whole normalized quote starting here
        snippet = text[m.start():m.start() + len(quote) * 3]
        norm_snippet = re.sub(r"\s+", " ", snippet)
        if norm_snippet.startswith(norm_quote):
            # map end: walk forward in original until we've consumed len(norm_quote) non-space chars
            end = m.start()
            need = len(norm_quote)
            got = 0
            while end < len(text) and got < need:
                if not text[end].isspace() or (end > m.start() and not text[end-1].isspace()):
                    got += 1
                end += 1
            print(f"normalized: span_start = {m.start()} span_end = {end}")
            print(f"            {text[m.start():end]!r}")
            return

    print("NOT FOUND")
    # Show a hint: closest prefix
    prefix = quote[:30]
    idx = text.find(prefix)
    if idx != -1:
        print(f"closest prefix found at {idx}: {text[idx:idx+100]!r}")
    sys.exit(2)

if __name__ == "__main__":
    main()