#!/usr/bin/env python3
"""Discover current chapter authority across the whole Peg-Leg Greg manuscript.

This module is intentionally read-only. It reconciles heterogeneous manuscript sources
without trusting the stale chapter index as authority. Exact checkpoint files outrank the
running manuscript, recovered exact blocks, book DOCX files, and reader fallbacks.
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree


NUMERIC_HEADING = re.compile(
    r"(?im)^#{1,6}\s+CHAPTER\s+(\d+)\s*(?:[—:-]\s*(.+?))?\s*$"
)
INDEX_ENTRY = re.compile(r"(?m)^(\d+)\.\s+\*\*(.+?)\*\*\s*$")
HTML_TITLE = re.compile(r"<title>\s*Chapter\s+(\d+)\s*:\s*(.+?)\s+[—-]\s+Peg-Leg Greg\s*</title>", re.I | re.S)
HTML_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")
CHECKPOINT_NAME = re.compile(r"Peg_Leg_Greg_Chapter_(\d+)_EXACT_WIP\.md$", re.I)

ONES = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
TEENS = {
    10: "TEN", 11: "ELEVEN", 12: "TWELVE", 13: "THIRTEEN", 14: "FOURTEEN",
    15: "FIFTEEN", 16: "SIXTEEN", 17: "SEVENTEEN", 18: "EIGHTEEN", 19: "NINETEEN",
}
TENS = {
    20: "TWENTY", 30: "THIRTY", 40: "FORTY", 50: "FIFTY",
    60: "SIXTY", 70: "SEVENTY", 80: "EIGHTY", 90: "NINETY",
}


def number_words(number: int) -> str:
    if number < 10:
        return ONES[number]
    if number < 20:
        return TEENS[number]
    if number < 100:
        tens, remainder = divmod(number, 10)
        return TENS[tens * 10] + (f"-{ONES[remainder]}" if remainder else "")
    if number < 1000:
        hundreds, remainder = divmod(number, 100)
        prefix = f"{ONES[hundreds]} HUNDRED"
        return prefix + (f" {number_words(remainder)}" if remainder else "")
    return str(number)


NUMBER_WORD_PREFIXES = sorted(
    ((number_words(number), number) for number in range(1, 1000)),
    key=lambda item: len(item[0]),
    reverse=True,
)


def clean_title(value: str | None) -> str | None:
    if value is None:
        return None
    value = TAG.sub("", value)
    value = re.sub(r"[*_`]+", "", value).strip()
    return value or None


def parse_markdown_chapters(path: Path) -> list[tuple[int, str | None]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return [
        (int(match.group(1)), clean_title(match.group(2)))
        for match in NUMERIC_HEADING.finditer(text)
    ]


def docx_paragraphs(path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(path) as archive:
            document = ElementTree.fromstring(archive.read("word/document.xml"))
    except (KeyError, zipfile.BadZipFile, ElementTree.ParseError):
        return []
    paragraphs: list[str] = []
    for paragraph in (node for node in document.iter() if node.tag.endswith("}p")):
        text = "".join(
            node.text or "" for node in paragraph.iter() if node.tag.endswith("}t")
        ).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def parse_docx_chapters(path: Path) -> list[tuple[int, str | None]]:
    paragraphs = docx_paragraphs(path)
    chapters: list[tuple[int, str | None]] = []
    for index, paragraph in enumerate(paragraphs):
        text = paragraph.strip()
        upper = text.upper()
        if not upper.startswith("CHAPTER "):
            continue
        tail = upper[len("CHAPTER "):].strip()
        number: int | None = None
        title: str | None = None
        numeric = re.match(r"(\d+)\b\s*(?:[—:-]\s*(.*))?$", text[len("CHAPTER "):].strip(), re.I)
        if numeric:
            number = int(numeric.group(1))
            title = clean_title(numeric.group(2))
        else:
            for words, candidate in NUMBER_WORD_PREFIXES:
                if tail == words or tail.startswith(words + " ") or tail.startswith(words + " —") or tail.startswith(words + " -") or tail.startswith(words + ":"):
                    number = candidate
                    remainder = text[len("CHAPTER ") + len(words):].strip()
                    remainder = re.sub(r"^[—:-]+\s*", "", remainder)
                    title = clean_title(remainder)
                    break
        if number is None:
            continue
        if title is None and index + 1 < len(paragraphs):
            next_text = paragraphs[index + 1].strip()
            if not next_text.upper().startswith("CHAPTER "):
                title = clean_title(next_text)
        chapters.append((number, title))
    return chapters


def parse_reader_page(path: Path) -> tuple[int, str | None] | None:
    if not path.stem.isdigit():
        return None
    number = int(path.stem)
    text = path.read_text(encoding="utf-8", errors="replace")
    title_match = HTML_TITLE.search(text)
    if title_match:
        return number, clean_title(title_match.group(2))
    h1 = HTML_H1.search(text)
    return number, clean_title(h1.group(1) if h1 else None)


def source_kind(path: Path, root: Path) -> tuple[str, int] | None:
    relative = path.relative_to(root).as_posix()
    name = path.name
    if CHECKPOINT_NAME.fullmatch(name):
        return "exact_checkpoint", 100
    if name == "Peg_Leg_Greg_Running_Manuscript.md":
        return "running_manuscript", 90
    if "Recovered" in name and "EXACT" in name and path.suffix.lower() == ".md":
        return "recovered_exact", 80
    if name == "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx":
        return "authoritative_docx", 75
    if path.suffix.lower() == ".docx" and path.parent.name == "manuscript":
        return "book_docx", 70
    if relative.startswith("light/") and path.suffix.lower() == ".html":
        return "light_reader_fallback", 40
    if relative.startswith("chapters/") and path.suffix.lower() == ".html":
        return "illustrated_reader_fallback", 35
    return None


def candidate_rows(root: Path) -> list[dict]:
    candidates: list[dict] = []
    manuscript_root = root / "state/manuscript"
    source_paths: list[Path] = []
    if manuscript_root.exists():
        source_paths.extend(
            path for path in manuscript_root.iterdir()
            if path.is_file() and path.suffix.lower() in {".md", ".docx"}
        )
    for reader_dir in (root / "light", root / "chapters"):
        if reader_dir.exists():
            source_paths.extend(reader_dir.glob("[0-9][0-9][0-9].html"))

    for path in sorted(set(source_paths)):
        classification = source_kind(path, root)
        if classification is None:
            continue
        kind, priority = classification
        if path.suffix.lower() == ".docx":
            parsed = parse_docx_chapters(path)
        elif path.suffix.lower() == ".md":
            parsed = parse_markdown_chapters(path)
        else:
            one = parse_reader_page(path)
            parsed = [one] if one else []
        for number, title in parsed:
            candidates.append({
                "chapter_number": number,
                "title": title,
                "path": path.relative_to(root).as_posix(),
                "source_kind": kind,
                "source_priority": priority,
            })
    return candidates


def parse_chapter_index(root: Path) -> tuple[int | None, dict[int, str]]:
    path = root / "state/MANUSCRIPT_CHAPTER_INDEX.md"
    if not path.exists():
        return None, {}
    text = path.read_text(encoding="utf-8", errors="replace")
    entries = {int(match.group(1)): clean_title(match.group(2)) or "" for match in INDEX_ENTRY.finditer(text)}
    return (max(entries) if entries else None), entries


def discover_manuscript_chapters(root: Path) -> dict:
    root = root.resolve()
    candidates = candidate_rows(root)
    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in candidates:
        grouped[row["chapter_number"]].append(row)

    chapters: list[dict] = []
    authority_conflicts: list[dict] = []
    for number in sorted(grouped):
        rows = sorted(grouped[number], key=lambda row: (-row["source_priority"], row["path"]))
        top_priority = rows[0]["source_priority"]
        top = [row for row in rows if row["source_priority"] == top_priority]
        top_signatures = {(row["path"], row.get("title")) for row in top}
        if len(top_signatures) > 1:
            authority_conflicts.append({
                "chapter_number": number,
                "top_priority": top_priority,
                "candidates": top,
            })
        canonical = rows[0].copy()
        canonical["alternate_sources"] = [
            {key: row[key] for key in ("path", "source_kind", "source_priority", "title")}
            for row in rows[1:]
        ]
        chapters.append(canonical)

    endpoint = max(grouped, default=0)
    discovered = set(grouped)
    gaps = sorted(set(range(1, endpoint + 1)) - discovered) if endpoint else []
    index_endpoint, index_titles = parse_chapter_index(root)
    stale_by = max(0, endpoint - index_endpoint) if endpoint and index_endpoint is not None else None
    index_title_mismatches = []
    canonical_by_number = {row["chapter_number"]: row for row in chapters}
    for number, title in index_titles.items():
        canonical = canonical_by_number.get(number)
        if canonical and canonical.get("title") and title and canonical["title"] != title:
            index_title_mismatches.append({
                "chapter_number": number,
                "index_title": title,
                "authority_title": canonical["title"],
            })

    return {
        "schema_version": 1,
        "source": "whole_book_current_checkout",
        "endpoint": endpoint,
        "chapter_count": len(chapters),
        "chapters": chapters,
        "gaps": gaps,
        "authority_conflicts": authority_conflicts,
        "chapter_index_endpoint": index_endpoint,
        "chapter_index_stale_by": stale_by,
        "chapter_index_title_mismatches": index_title_mismatches,
        "source_files": sorted({row["path"] for row in candidates}),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = discover_manuscript_chapters(args.root)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else args.root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
