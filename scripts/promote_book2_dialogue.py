#!/usr/bin/env python3
"""Book II wrapper for canonical DOCX promotion through hundred-series headings."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import promote_book1_polish as impl
except ModuleNotFoundError:
    from scripts import promote_book1_polish as impl


_original_number_from_heading = impl._number_from_heading


def _number_from_heading(text: str) -> int | None:
    original = _original_number_from_heading(text)
    if original is not None:
        return original
    match = impl.HEADING_RE.match(text.strip())
    if not match:
        return None
    raw = match.group(1).strip().upper()
    numeric = re.match(r"^(\d+)\b", raw)
    if numeric:
        return int(numeric.group(1))
    token = raw.replace("-", " ")
    parts = token.split()
    if len(parts) < 2 or parts[0] != "ONE" or parts[1] != "HUNDRED":
        return None
    if len(parts) == 2:
        return 100
    tail = parts[2:]
    if len(tail) == 1:
        if tail[0] in impl.ONES:
            return 100 + impl.ONES[tail[0]]
        if tail[0] in impl.TENS:
            return 100 + impl.TENS[tail[0]]
        return None
    if len(tail) == 2 and tail[0] in impl.TENS and tail[1] in impl.ONES:
        return 100 + impl.TENS[tail[0]] + impl.ONES[tail[1]]
    return None


impl._number_from_heading = _number_from_heading


def _print_heading_diagnostic() -> None:
    try:
        index = sys.argv.index("--docx")
        path = Path(sys.argv[index + 1])
    except (ValueError, IndexError):
        return
    from docx import Document
    doc = Document(path)
    parsed = impl._heading_map(doc)
    print("Parsed heading keys 95-105:", [n for n in sorted(parsed) if 95 <= n <= 105])
    for p in doc.paragraphs:
        if "CHAPTER 100" in p.text.upper() or "CHAPTER 99" in p.text.upper() or "CHAPTER 101" in p.text.upper():
            print("Seam heading:", repr(p.text), "=>", _number_from_heading(p.text))


if __name__ == "__main__":
    _print_heading_diagnostic()
    raise SystemExit(impl.main())
