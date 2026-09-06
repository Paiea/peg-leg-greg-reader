#!/usr/bin/env python3
"""Find chapter-number-coupled references that structural compression could break."""

from __future__ import annotations

import argparse
import bisect
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

TEXT_SUFFIXES = {".html", ".md", ".json", ".py", ".txt", ".yaml", ".yml", ".js", ".css", ".sh"}
SCAN_ROOTS = (
    "chapters",
    "light",
    "visual",
    "state",
    "prompts",
    "scripts",
    "tests",
    ".github",
    "publishing",
    "docs",
)
PATTERNS = (
    ("reader_slug", re.compile(r"(?:chapters|light)/(\d{1,4})\.html", re.I), "hard"),
    ("reader_query", re.compile(r"light\.html\?chapter=(\d{1,4})", re.I), "hard"),
    ("chapter_art_path", re.compile(r"(?:visual/)?chapter_art/(\d{1,4})/", re.I), "hard"),
    ("checkpoint_name", re.compile(r"Peg_Leg_Greg_Chapter_(\d{1,4})_EXACT", re.I), "hard"),
    (
        "chapter_field",
        re.compile(
            r"[\"']?(?:chapter_number|display_number|current_display_number|origin_chapter_number|chapter)[\"']?\s*[:=]\s*[\"']?(\d{1,4})\b",
            re.I,
        ),
        "hard",
    ),
    ("chapter_text", re.compile(r"\bChapter\s+(\d{1,4})\b", re.I), "soft"),
    ("asset_name", re.compile(r"\bCh(\d{3,4})(?!\d)", re.I), "soft"),
)
GENERATED_OUTPUTS = {
    "publishing/chapter_dependency_report.json",
    "publishing/chapter_number_dependencies.json",
    "publishing/compression_readiness.json",
    "publishing/chapter_identity_registry.json",
}


def file_category(relative: str, suffix: str) -> str:
    if relative.startswith("visual/"):
        return "art"
    if relative.startswith("state/"):
        return "state"
    if relative.startswith("prompts/"):
        return "prompt"
    if relative.startswith(("scripts/", "tests/", ".github/")):
        return "script"
    if relative.startswith(("chapters/", "light/")) or relative in {"index.html", "light.html", "latest.html", "art.html"}:
        return "reader"
    if relative.startswith("publishing/") or suffix in {".json", ".yaml", ".yml"}:
        return "metadata"
    if relative.startswith("docs/"):
        return "docs"
    return "other"


def newline_offsets(text: str) -> list[int]:
    """Return newline offsets once so match-to-line lookup stays logarithmic."""
    return [index for index, char in enumerate(text) if char == "\n"]


def line_number(offsets: list[int], character_offset: int) -> int:
    return bisect.bisect_left(offsets, character_offset) + 1


def iter_scan_paths(root: Path):
    """Yield migration-relevant text files without traversing generated export trees."""
    seen: set[Path] = set()

    for path in sorted(root.iterdir()):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            seen.add(path)
            yield path

    for directory_name in SCAN_ROOTS:
        directory = root / directory_name
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if path in seen or not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            seen.add(path)
            yield path


def scan_dependencies(root: Path) -> dict:
    root = root.resolve()
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    seen_items: set[tuple[str, str, int, str, str]] = set()
    scanned = 0
    counts_by_kind: Counter[str] = Counter()
    counts_by_file_category: Counter[str] = Counter()
    counts_by_risk: Counter[str] = Counter()

    for path in iter_scan_paths(root):
        relative = path.relative_to(root).as_posix()
        if "__pycache__" in path.parts or relative in GENERATED_OUTPUTS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        category = file_category(relative, path.suffix.lower())
        offsets = newline_offsets(text)
        for kind, pattern, risk in PATTERNS:
            for match in pattern.finditer(text):
                number = str(int(match.group(1)))
                line = line_number(offsets, match.start())
                key = (number, relative, line, kind, match.group(0))
                if key in seen_items:
                    continue
                seen_items.add(key)
                item = {
                    "kind": kind,
                    "risk": risk,
                    "file_category": category,
                    "path": relative,
                    "line": line,
                    "match": match.group(0),
                }
                by_chapter[number].append(item)
                counts_by_kind[kind] += 1
                counts_by_file_category[category] += 1
                counts_by_risk[risk] += 1

    for refs in by_chapter.values():
        refs.sort(key=lambda row: (row["path"], row["line"], row["kind"]))

    return {
        "schema_version": 2,
        "scan_roots": list(SCAN_ROOTS),
        "scanned_files": scanned,
        "chapters_with_dependencies": len(by_chapter),
        "reference_count": sum(len(rows) for rows in by_chapter.values()),
        "counts_by_kind": dict(sorted(counts_by_kind.items())),
        "counts_by_file_category": dict(sorted(counts_by_file_category.items())),
        "counts_by_risk": dict(sorted(counts_by_risk.items())),
        "by_chapter": dict(sorted(by_chapter.items(), key=lambda item: int(item[0]))),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("publishing/chapter_dependency_report.json"))
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    payload = scan_dependencies(args.root)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.stdout:
        print(rendered, end="")
    else:
        output = args.output if args.output.is_absolute() else args.root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f'wrote {payload["reference_count"]} chapter-coupled references to {output}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
