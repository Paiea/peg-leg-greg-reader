#!/usr/bin/env python3
"""Build one stable chapter identity registry for manuscript, reader, and art state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manuscript_authority import discover_manuscript_chapters, parse_reader_page


def stable_id(number: int) -> str:
    """Initial immutable ID assignment before any renumber migration has begun."""
    return f"plg-ch-{number:06d}"


def _book_and_act(number: int) -> tuple[str, str]:
    # Transitional publication placement. These boundaries remain current presentation
    # metadata until a structural migration explicitly replaces them.
    if number <= 82:
        book = "book-i"
        act = "act-i" if number <= 20 else "act-ii" if number <= 63 else "act-iii"
    elif number <= 180:
        book = "book-ii"
        act = "act-i" if number <= 99 else "act-ii" if number <= 137 else "act-iii"
    else:
        book = "book-iii"
        act = "act-i" if number <= 219 else "act-ii"
    return book, act


def _load_coverage_art(root: Path) -> dict[int, list[str]]:
    path = root / "publishing/chapter_art_coverage.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {
        int(key): list(value.get("assets", []))
        for key, value in data.get("chapters", {}).items()
        if str(key).isdigit()
    }


def _art_for_chapter(root: Path, number: int, coverage: dict[int, list[str]]) -> list[str]:
    assets = set(coverage.get(number, []))
    directory = root / f"visual/chapter_art/{number:03d}"
    if directory.exists():
        assets.update(
            path.relative_to(root).as_posix()
            for path in directory.iterdir()
            if path.is_file()
        )
    return sorted(assets)


def _reader_pages(root: Path) -> dict[int, list[str]]:
    pages: dict[int, list[str]] = {}
    for dirname in ("chapters", "light"):
        directory = root / dirname
        if not directory.exists():
            continue
        for page in sorted(directory.glob("[0-9][0-9][0-9].html")):
            number = int(page.stem)
            pages.setdefault(number, []).append(page.relative_to(root).as_posix())
    return pages


def _reader_title(root: Path, pages: list[str]) -> str | None:
    for relative in pages:
        parsed = parse_reader_page(root / relative)
        if parsed and parsed[1]:
            return parsed[1]
    return None


def _load_existing_ids(root: Path) -> dict[int, str]:
    """Preserve already-issued IDs if a durable registry has previously been written."""
    path = root / "publishing/chapter_identity_registry.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    result: dict[int, str] = {}
    for row in data.get("chapters", []):
        origin = row.get("origin_chapter_number")
        chapter_id = row.get("chapter_id")
        if isinstance(origin, int) and isinstance(chapter_id, str):
            result[origin] = chapter_id
    return result


def build_registry(root: Path) -> dict:
    root = root.resolve()
    authority = discover_manuscript_chapters(root)
    coverage = _load_coverage_art(root)
    pages_by_number = _reader_pages(root)
    existing_ids = _load_existing_ids(root)

    records = []
    for source in authority.get("chapters", []):
        number = int(source["chapter_number"])
        pages = pages_by_number.get(number, [])
        title = source.get("title") or _reader_title(root, pages) or f"CHAPTER {number}"
        book, act = _book_and_act(number)
        public_slug = next((page for page in pages if page.startswith("chapters/")), None)
        if public_slug is None:
            public_slug = next((page for page in pages if page.startswith("light/")), None)
        chapter_id = existing_ids.get(number, stable_id(number))
        records.append({
            "chapter_id": chapter_id,
            "origin_chapter_number": number,
            "current_display_number": number,
            "current_title": title,
            "book": book,
            "act": act,
            "status": "active",
            "merged_into": None,
            "source_chapter_ids": [chapter_id],
            "source_path": source["path"],
            "manuscript_path": source["path"],
            "manuscript_source_kind": source["source_kind"],
            "manuscript_source_priority": source["source_priority"],
            "reader_pages": pages,
            "public_slug": public_slug,
            "legacy_slugs": list(pages),
            "illustration_refs": _art_for_chapter(root, number, coverage),
            "notes": "",
        })

    ids = [row["chapter_id"] for row in records]
    numbers = [row["current_display_number"] for row in records]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate stable chapter ids")
    if len(numbers) != len(set(numbers)):
        raise ValueError("duplicate active display numbers")

    manuscript_numbers = set(numbers)
    reader_numbers = set(pages_by_number)
    diagnostics = {
        "manuscript_endpoint": authority.get("endpoint", 0),
        "manuscript_chapter_count": authority.get("chapter_count", 0),
        "manuscript_gaps": authority.get("gaps", []),
        "authority_conflicts": authority.get("authority_conflicts", []),
        "chapter_index_endpoint": authority.get("chapter_index_endpoint"),
        "chapter_index_stale_by": authority.get("chapter_index_stale_by"),
        "chapter_index_title_mismatches": authority.get("chapter_index_title_mismatches", []),
        "reader_only_chapters": sorted(reader_numbers - manuscript_numbers),
        "manuscript_only_chapters": sorted(manuscript_numbers - reader_numbers),
        "reader_chapter_count": len(reader_numbers),
    }
    return {
        "schema_version": 2,
        "source": "whole_book_authority",
        "chapters": records,
        "diagnostics": diagnostics,
        "authority_source_files": authority.get("source_files", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("publishing/chapter_identity_registry.json"))
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    payload = build_registry(args.root)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.stdout:
        print(rendered, end="")
    else:
        output = args.output if args.output.is_absolute() else args.root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f'wrote {len(payload["chapters"])} chapter identities to {output}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
