#!/usr/bin/env python3
"""Apply dialogue ownership boundaries to active Peg-Leg Greg canon sources."""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.dialogue_ownership_engine import has_dialogue, quoted_spans, split_paragraph


CHAPTERS_DIR = ROOT / "chapters"
MANUSCRIPT_DIR = ROOT / "state" / "manuscript"
RECOVERED = MANUSCRIPT_DIR / "Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md"
RUNNING = MANUSCRIPT_DIR / "Peg_Leg_Greg_Running_Manuscript.md"
CHECKPOINT_GLOB = "Peg_Leg_Greg_Chapter_*_EXACT_WIP.md"

BOUNDARY_RE = re.compile(
    r"^(?:# CHAPTER (?P<standard_num>\d+)[ \t]*|"
    r"## Chapter (?P<combined_num>\d+)[ \t]*[—–-][ \t]*(?P<combined_title>[^\n]+?)[ \t]*)$",
    re.MULTILINE,
)
P_RE = re.compile(r"<p>(.*?)</p>", re.S)
ARTICLE_RE = re.compile(
    r"(?P<open><article\b[^>]*class=[\"'][^\"']*\bprose\b[^\"']*[\"'][^>]*>)"
    r"(?P<body>.*?)"
    r"(?P<close></article>)",
    re.I | re.S,
)


def markdown_chapter_numbers(path: Path) -> list[int]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    return [
        int(match.group("standard_num") or match.group("combined_num"))
        for match in BOUNDARY_RE.finditer(text)
    ]


def active_source_map() -> dict[int, Path]:
    """Mirror scripts/generate_light.py source precedence with exact file paths."""
    sources: dict[int, Path] = {}

    for path in sorted(CHAPTERS_DIR.glob("[0-9][0-9][0-9].html")):
        number = int(path.stem)
        if number <= 155:
            sources[number] = path

    for number in markdown_chapter_numbers(RECOVERED):
        sources[number] = RECOVERED

    running_numbers = markdown_chapter_numbers(RUNNING)
    for number in running_numbers:
        sources[number] = RUNNING
    running_edge = max(running_numbers, default=0)

    for path in sorted(MANUSCRIPT_DIR.glob(CHECKPOINT_GLOB)):
        for number in markdown_chapter_numbers(path):
            if number > running_edge:
                sources[number] = path

    return sources


def _flat_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _html_prose_text(article_body: str) -> str:
    parts: list[str] = []
    for match in P_RE.finditer(article_body):
        plain = re.sub(r"<[^>]+>", "", match.group(1))
        parts.append(plain)
    return _flat_space(" ".join(parts))


def transform_html(path: Path) -> tuple[bool, int]:
    before = path.read_text(encoding="utf-8")
    article = ARTICLE_RE.search(before)
    if not article:
        raise ValueError(f"no article.prose in {path}")
    body_before = article.group("body")
    quote_before = quoted_spans(_html_prose_text(body_before))
    split_count = 0

    def replace_paragraph(match: re.Match[str]) -> str:
        nonlocal split_count
        content = match.group(1)
        if "<" in content or not has_dialogue(content):
            return match.group(0)
        pieces = split_paragraph(content)
        if len(pieces) <= 1:
            return match.group(0)

        reconstructed = " ".join(pieces)
        if _flat_space(reconstructed) != _flat_space(content):
            raise ValueError(
                "paragraph text changed while splitting "
                f"{path}: before={content!r} after_parts={pieces!r}"
            )
        if quoted_spans(reconstructed) != quoted_spans(content):
            raise ValueError(
                "paragraph dialogue changed while splitting "
                f"{path}: before={content!r} after_parts={pieces!r}"
            )

        split_count += len(pieces) - 1
        return "".join(f"<p>{piece}</p>" for piece in pieces)

    body_after = P_RE.sub(replace_paragraph, body_before)
    after = before[: article.start("body")] + body_after + before[article.end("body") :]

    if _html_prose_text(body_after) != _html_prose_text(body_before):
        raise ValueError(f"prose text changed while splitting {path}")
    if quoted_spans(_html_prose_text(body_after)) != quote_before:
        raise ValueError(f"dialogue changed while splitting {path}")

    if after != before:
        path.write_text(after, encoding="utf-8")
        return True, split_count
    return False, 0


def _transform_markdown_body(body: str) -> tuple[str, int]:
    pieces = re.split(r"(\n\s*\n+)", body)
    split_count = 0
    for index in range(0, len(pieces), 2):
        block = pieces[index]
        stripped = block.strip()
        if not stripped or not has_dialogue(stripped):
            continue
        # Formatted Markdown needs a markup-aware transformer. Leave it intact
        # and surface it through audit rather than moving emphasis/link/code
        # delimiters across newly inserted paragraph boundaries.
        has_markdown_markup = (
            "**" in stripped
            or "__" in stripped
            or "`" in stripped
            or "](" in stripped
        )
        if stripped.startswith("#") or "\n" in stripped or "<" in stripped or has_markdown_markup:
            continue
        ownership = split_paragraph(stripped)
        if len(ownership) <= 1:
            continue
        leading = block[: len(block) - len(block.lstrip())]
        trailing = block[len(block.rstrip()) :]
        pieces[index] = leading + "\n\n".join(ownership) + trailing
        split_count += len(ownership) - 1
    return "".join(pieces), split_count


def transform_markdown(path: Path, target_chapters: set[int]) -> tuple[set[int], int]:
    before = path.read_text(encoding="utf-8")
    matches = list(BOUNDARY_RE.finditer(before))
    replacements: list[tuple[int, int, str, int]] = []
    changed_chapters: set[int] = set()
    total_splits = 0

    for index, match in enumerate(matches):
        number = int(match.group("standard_num") or match.group("combined_num"))
        if number not in target_chapters:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(before)
        body = before[start:end]
        transformed, splits = _transform_markdown_body(body)
        if transformed != body:
            replacements.append((start, end, transformed, splits))
            changed_chapters.add(number)
            total_splits += splits

    after = before
    for start, end, transformed, _ in reversed(replacements):
        after = after[:start] + transformed + after[end:]

    if _flat_space(after) != _flat_space(before):
        raise ValueError(f"text changed beyond paragraph whitespace in {path}")
    if quoted_spans(after) != quoted_spans(before):
        raise ValueError(f"dialogue changed while splitting {path}")

    if after != before:
        path.write_text(after, encoding="utf-8")
    return changed_chapters, total_splits


def apply_range(start: int, end: int) -> tuple[set[int], int, int]:
    sources = active_source_map()
    if not sources:
        raise SystemExit("no canon sources found")
    frontier = max(sources)
    end = min(end, frontier)
    targets = [number for number in range(start, end + 1) if number in sources]
    missing = [number for number in range(start, end + 1) if number not in sources]
    if missing:
        preview = ", ".join(str(n) for n in missing[:20])
        raise SystemExit(f"missing active canon source(s): {preview}")

    by_source: dict[Path, set[int]] = defaultdict(set)
    for number in targets:
        by_source[sources[number]].add(number)

    changed: set[int] = set()
    total_splits = 0
    for path, numbers in sorted(by_source.items(), key=lambda item: str(item[0])):
        if path.suffix.lower() == ".html":
            for number in sorted(numbers):
                did_change, splits = transform_html(path)
                if did_change:
                    changed.add(number)
                    total_splits += splits
        else:
            path_changed, splits = transform_markdown(path, numbers)
            changed.update(path_changed)
            total_splits += splits

    return changed, total_splits, frontier


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", required=True, help="inclusive chapter number or current")
    args = parser.parse_args()

    sources = active_source_map()
    frontier = max(sources, default=0)
    if frontier == 0:
        raise SystemExit("no canon frontier found")
    end = frontier if args.end == "current" else int(args.end)
    changed, splits, frontier = apply_range(args.start, end)
    if changed:
        preview = ", ".join(str(n) for n in sorted(changed)[:30])
        suffix = "..." if len(changed) > 30 else ""
        print(
            f"dialogue ownership {args.start}-{min(end, frontier)}: "
            f"changed {len(changed)} chapters, inserted {splits} paragraph boundaries: {preview}{suffix}"
        )
    else:
        print(f"dialogue ownership {args.start}-{min(end, frontier)}: no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
