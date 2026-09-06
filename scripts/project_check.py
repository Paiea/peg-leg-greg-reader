#!/usr/bin/env python3
"""Run focused, machine-readable Peg-Leg Greg project checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from project_audit import (
    CHAPTER_HEADING,
    chapter_art_coverage,
    inventory_images,
    normalize_reference,
)


ACTIVE_MARKDOWN_MANUSCRIPTS = {
    "Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md",
    "Peg_Leg_Greg_Running_Manuscript.md",
}


def manuscript_check(root: Path) -> tuple[dict, bool]:
    manuscript_root = root / "state/manuscript"
    files = (
        sorted(
            path
            for path in manuscript_root.glob("*.md")
            if path.name in ACTIVE_MARKDOWN_MANUSCRIPTS
        )
        if manuscript_root.exists()
        else []
    )
    chapter_counts: Counter[int] = Counter()
    em_dash_count = 0
    stale_lysa = []
    checked = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        chapters = [int(value) for value in CHAPTER_HEADING.findall(text)]
        chapter_counts.update(chapters)
        first_chapter = CHAPTER_HEADING.search(text)
        prose = text[first_chapter.start():] if first_chapter else text
        em_dash_count += prose.count("—")
        if re.search(r"\bLysa\b", text):
            stale_lysa.append(path.relative_to(root).as_posix())
        checked.append(path.relative_to(root).as_posix())
    duplicates = sorted(number for number, count in chapter_counts.items() if count > 1)
    errors = {
        "duplicate_chapters": duplicates,
        "em_dash_count": em_dash_count,
        "stale_lysa_files": stale_lysa,
    }
    payload = {
        "check": "manuscript",
        "checked_files": checked,
        "chapter_count": len(chapter_counts),
        "errors": errors,
    }
    return payload, not any([duplicates, em_dash_count, stale_lysa])


def reader_check(root: Path) -> tuple[dict, bool]:
    images = inventory_images(root)
    coverage = chapter_art_coverage(root, images)
    chapter_numbers = sorted(int(number) for number in coverage["chapters"])
    illustrated = [number for number in chapter_numbers if 1 <= number <= 155]
    preview = [number for number in chapter_numbers if number >= 220]
    expected_illustrated = list(range(1, 156))
    errors = {
        "broken_image_references": coverage["broken_references"],
        "missing_illustrated_chapters": sorted(set(expected_illustrated) - set(illustrated)),
        "duplicate_chapter_files": [],
    }
    payload = {
        "check": "reader",
        "illustrated_chapters": illustrated,
        "preview_chapters": preview,
        "errors": errors,
    }
    return payload, not any(errors.values())


def assets_check(root: Path) -> tuple[dict, bool]:
    images = inventory_images(root)
    duplicate_groups = {
        row["duplicate_group"] for row in images if row["duplicate_group"] is not None
    }
    errors = {"unreadable_dimensions": sum(
        "DIMENSIONS_UNREADABLE" in row["quality_flags"] for row in images
    )}
    warnings = {
        "unused_assets": sum(row["status"] == "UNUSED_REVIEW" for row in images),
        "low_resolution_assets": sum(
            "LOW_RESOLUTION" in row["quality_flags"] for row in images
        ),
        "oversized_assets": sum(
            "OVERSIZED_FILE" in row["quality_flags"] for row in images
        ),
        "duplicate_hash_groups": len(duplicate_groups),
    }
    payload = {
        "check": "assets",
        "image_count": len(images),
        "errors": errors,
        "warnings": warnings,
    }
    return payload, not any(errors.values())


CHECKS = {
    "manuscript": manuscript_check,
    "reader": reader_check,
    "assets": assets_check,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=[*CHECKS, "all"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    names = list(CHECKS) if args.command == "all" else [args.command]
    results = {}
    success = True
    for name in names:
        payload, passed = CHECKS[name](root)
        results[name] = payload
        success = success and passed
    output = results[names[0]] if len(names) == 1 else {"checks": results}
    print(json.dumps(output, indent=2, sort_keys=True))
    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
