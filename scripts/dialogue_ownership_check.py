#!/usr/bin/env python3
"""Read-only dialogue ownership checks for Peg-Leg Greg manuscript prose.

This checker is deliberately conservative. It reports clear dramatic-owner
collisions as errors and uncertain attribution/quotation structures as review
items. It never rewrites manuscript prose.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import html
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Iterator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_light import Chapter, load_all_sources


P_RE = re.compile(r"<p\b[^>]*>(.*?)</p>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")

SPEECH_VERBS = {
    "said", "asked", "answered", "replied", "told", "called", "shouted",
    "yelled", "whispered", "muttered", "murmured", "continued", "added",
    "offered", "warned", "insisted", "snapped", "growled", "sighed",
    "admitted", "agreed", "argued", "explained", "demanded", "ordered",
    "promised", "suggested", "announced", "observed", "remarked",
}

ACTION_VERBS = {
    "accepted", "adjusted", "answered", "asked", "blinked", "bowed",
    "breathed", "called", "checked", "closed", "continued", "counted",
    "crossed", "denied", "drummed", "exhaled", "flinched", "folded",
    "froze", "glanced", "glared", "grinned", "groaned", "laughed",
    "leaned", "left", "looked", "moved", "nodded", "opened", "paused",
    "picked", "pointed", "pulled", "pushed", "raised", "reached", "sat",
    "shook", "shrugged", "sighed", "smiled", "stared", "stood", "stopped",
    "swore", "tapped", "turned", "waited", "walked", "watched", "waved",
    "winced", "wrote", "took", "gave", "held", "set", "slid", "put",
    "ran", "stepped", "returned", "followed", "tilted", "rubbed",
    "scratched", "lifted", "dropped", "caught", "kicked", "flattened",
    "tightened", "changed", "softened", "knew", "thought", "remembered",
    "noticed", "decided", "considered", "wondered", "realized", "felt",
    "heard", "saw", "named", "smelled", "wanted", "hated", "liked",
}

ACTOR_PATTERN = (
    r"I|My|Greg|He|She|They|His|Her|Their"
    r"|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?"
    r"|[A-Z][a-z]+'s"
    r"|The\s+[a-z]+(?:\s+[a-z]+){0,4}"
    r"(?:\s+(?:with|in|at|by|from|near|behind|beside|under|over)"
    r"\s+(?:the\s+)?[a-z]+(?:\s+[a-z]+){0,4})?"
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    chapter: int
    paragraph: int
    excerpt: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _excerpt(text: str, limit: int = 240) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact if len(compact) <= limit else compact[: limit - 1].rstrip() + "…"


def _has_quote_char(text: str) -> bool:
    return '"' in text or '“' in text or '”' in text


def _quote_structure_safe(text: str) -> bool:
    mode: str | None = None
    escaped = False
    for char in text:
        if mode == "straight":
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                mode = None
            continue
        if mode == "smart":
            if char == '“':
                return False
            if char == '”':
                mode = None
            continue
        if char == '"':
            mode = "straight"
        elif char == '“':
            mode = "smart"
        elif char == '”':
            return False
    return mode is None


def _quoted_spans(text: str) -> list[str]:
    if not _quote_structure_safe(text):
        return []
    spans: list[str] = []
    mode: str | None = None
    start: int | None = None
    escaped = False
    for index, char in enumerate(text):
        if mode == "straight":
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                assert start is not None
                spans.append(text[start : index + 1])
                start = None
                mode = None
            continue
        if mode == "smart":
            if char == '”':
                assert start is not None
                spans.append(text[start : index + 1])
                start = None
                mode = None
            continue
        if char == '"':
            start = index
            mode = "straight"
        elif char == '“':
            start = index
            mode = "smart"
    return spans


def _is_attribution_tail(text: str) -> bool:
    actor = rf"(?:{ACTOR_PATTERN})"
    verbs = "|".join(sorted(SPEECH_VERBS, key=len, reverse=True))
    return re.match(rf"^\s*{actor}\s+(?:[a-z]+ly\s+){{0,2}}(?:{verbs})\b", text) is not None


def _beat_ranges(text: str) -> list[tuple[int, int]]:
    """Return sentence-like ranges while keeping dialogue attribution attached."""
    boundaries: list[int] = []
    mode: str | None = None
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
        if mode == "straight":
            if escaped:
                escaped = False
                index += 1
                continue
            if char == "\\":
                escaped = True
                index += 1
                continue
            if char == '"':
                mode = None
                if index > 0 and text[index - 1] in ".!?" and not _is_attribution_tail(text[index + 1 :]):
                    boundaries.append(index + 1)
            index += 1
            continue
        if mode == "smart":
            if char == '”':
                mode = None
                if index > 0 and text[index - 1] in ".!?" and not _is_attribution_tail(text[index + 1 :]):
                    boundaries.append(index + 1)
            index += 1
            continue
        if char == '"':
            mode = "straight"
        elif char == '“':
            mode = "smart"
        elif char in ".!?":
            # Collapse an ellipsis into one punctuation event.
            if char == "." and index + 1 < len(text) and text[index + 1] == ".":
                while index + 1 < len(text) and text[index + 1] == ".":
                    index += 1
            boundaries.append(index + 1)
        index += 1

    ranges: list[tuple[int, int]] = []
    start = 0
    for end in sorted(set(boundaries)):
        if end <= start:
            continue
        if text[start:end].strip():
            ranges.append((start, end))
        start = end
    if text[start:].strip():
        ranges.append((start, len(text)))
    return ranges


def _normalize_actor(actor: str) -> str:
    raw = actor.strip()
    if raw in {"I", "My", "Greg"}:
        return "GREG"
    if raw in {"He", "His"}:
        return "PRONOUN:he"
    if raw in {"She", "Her"}:
        return "PRONOUN:she"
    if raw in {"They", "Their"}:
        return "PRONOUN:they"
    if raw.endswith("'s") and raw[:-2]:
        raw = raw[:-2]
    if raw.startswith("The "):
        return "DESC:" + re.sub(r"\s+", " ", raw.lower())
    return "NAME:" + raw.split()[0]


def _speech_owner(beat: str) -> str | None:
    if not _quoted_spans(beat):
        return None
    verbs = "|".join(sorted(SPEECH_VERBS, key=len, reverse=True))
    actor = rf"(?P<actor>{ACTOR_PATTERN})"
    adverbs = r"(?:[a-z]+ly\s+){0,2}"
    after = re.search(rf'["”]\s*{actor}\s+{adverbs}(?:{verbs})\b', beat)
    if after:
        return _normalize_actor(after.group("actor"))
    before = re.search(rf'\b{actor}\s+{adverbs}(?:{verbs})\b[^"“\n]*["“]', beat)
    if before:
        return _normalize_actor(before.group("actor"))
    return None


def _outside_quotes(text: str) -> str:
    return re.sub(r'"(?:[^"\\]|\\.)*"|“[^”]*”', '', text)


def _subject_owner(beat: str) -> str | None:
    outside = _outside_quotes(beat).strip()
    if not outside:
        return None
    verbs = "|".join(sorted(ACTION_VERBS | SPEECH_VERBS, key=len, reverse=True))
    actor = rf"(?P<actor>{ACTOR_PATTERN})"
    match = re.match(rf"^{actor}\s+(?:[a-z]+ly\s+){{0,2}}(?:{verbs})\b", outside)
    return _normalize_actor(match.group("actor")) if match else None


def _owner_for_beat(beat: str) -> str | None:
    return _speech_owner(beat) or _subject_owner(beat)


def _owners_conflict(current: str | None, incoming: str | None) -> bool:
    if current is None or incoming is None or current == incoming:
        return False
    if current == "GREG" or incoming == "GREG":
        return True
    if current.startswith("PRONOUN:") or incoming.startswith("PRONOUN:"):
        return False
    return True


def _ambiguous_pronoun_review(text: str, owners: list[str | None]) -> bool:
    explicit_named = any(owner and owner.startswith(("NAME:", "DESC:")) for owner in owners)
    if not explicit_named:
        return False
    # A same-paragraph third-person subject plus an unresolved third-person
    # object is exactly the kind of referent chain the checker must not guess.
    outside = _outside_quotes(text)
    return bool(re.search(r"\b(?:He|She|They)\b[^.!?]*\b(?:him|her|them)\b", outside))


def inspect_paragraph(text: str, *, chapter: int, paragraph: int) -> list[Finding]:
    stripped = text.strip()
    if not stripped or not _has_quote_char(stripped):
        return []
    excerpt = _excerpt(stripped)
    if not _quote_structure_safe(stripped):
        return [Finding("review", "unbalanced_quotes", chapter, paragraph, excerpt)]
    if not _quoted_spans(stripped):
        return []
    if any(marker in stripped for marker in ("**", "__", "`", "](")):
        return [Finding("review", "formatted_or_embedded_quote", chapter, paragraph, excerpt)]

    beats = [stripped[start:end].strip() for start, end in _beat_ranges(stripped)]
    owners = [_owner_for_beat(beat) for beat in beats]

    current: str | None = None
    explicit_owners: list[str] = []
    collision = False
    for owner in owners:
        if owner is None:
            continue
        if owner == "GREG" or owner.startswith(("NAME:", "DESC:")):
            if owner not in explicit_owners:
                explicit_owners.append(owner)
        if current is None:
            current = owner
            continue
        if _owners_conflict(current, owner):
            collision = True
        if owner == "GREG" or owner.startswith(("NAME:", "DESC:")):
            current = owner
        elif current == "GREG":
            # Third-person subject after Greg is definitely another dramatic owner.
            collision = True

    findings: list[Finding] = []
    if collision or len(explicit_owners) > 1:
        findings.append(Finding("error", "mixed_explicit_owners", chapter, paragraph, excerpt))
    elif _ambiguous_pronoun_review(stripped, owners):
        findings.append(Finding("review", "ambiguous_pronoun_owner", chapter, paragraph, excerpt))
    return findings


def inspect_text(text: str, *, chapter: int = 0) -> list[Finding]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n+", text) if part.strip()]
    findings: list[Finding] = []
    for index, paragraph in enumerate(paragraphs, 1):
        findings.extend(inspect_paragraph(paragraph, chapter=chapter, paragraph=index))
    return findings


def chapter_paragraphs(chapter: Chapter) -> list[str]:
    paragraphs: list[str] = []
    for match in P_RE.finditer(chapter.prose_html):
        text = html.unescape(TAG_RE.sub("", match.group(1))).replace("\xa0", " ").strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def inspect_chapter(chapter: Chapter) -> list[Finding]:
    findings: list[Finding] = []
    for index, paragraph in enumerate(chapter_paragraphs(chapter), 1):
        findings.extend(inspect_paragraph(paragraph, chapter=chapter.number, paragraph=index))
    return findings


def check_chapters(chapters: dict[int, Chapter], numbers: Iterable[int]) -> dict[str, object]:
    selected = list(numbers)
    findings: list[Finding] = []
    for number in selected:
        chapter = chapters.get(number)
        if chapter is None:
            raise ValueError(f"chapter {number} is unavailable")
        findings.extend(inspect_chapter(chapter))
    errors = [finding for finding in findings if finding.severity == "error"]
    reviews = [finding for finding in findings if finding.severity == "review"]
    return {
        "chapters": selected,
        "error_count": len(errors),
        "review_count": len(reviews),
        "findings": [finding.as_dict() for finding in findings],
    }


@contextmanager
def _working_directory(path: Path) -> Iterator[None]:
    import os

    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def load_chapters(root: Path) -> dict[int, Chapter]:
    with _working_directory(root):
        return load_all_sources()


def _selected_numbers(args: argparse.Namespace, chapters: dict[int, Chapter]) -> list[int]:
    if not chapters:
        raise ValueError("no canonical chapters found")
    if args.latest:
        return [max(chapters)]
    if args.chapter is not None:
        return [args.chapter]
    if args.range is not None:
        match = re.fullmatch(r"(\d+)-(\d+)", args.range)
        if not match:
            raise ValueError("--range must use N-N syntax")
        start, end = map(int, match.groups())
        if start > end:
            raise ValueError("--range start must not exceed end")
        return list(range(start, end + 1))
    raise ValueError("select --latest, --chapter N, or --range N-N")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--latest", action="store_true")
    selection.add_argument("--chapter", type=int)
    selection.add_argument("--range")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    try:
        chapters = load_chapters(args.root.resolve())
        numbers = _selected_numbers(args, chapters)
        payload = check_chapters(chapters, numbers)
    except (OSError, ValueError, SystemExit) as exc:
        payload = {"error": str(exc)}
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"dialogue ownership check failed: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(
            f"dialogue ownership chapters {payload['chapters']}: "
            f"{payload['error_count']} errors, {payload['review_count']} reviews"
        )
        for finding in payload["findings"]:
            print(
                f"{finding['severity'].upper()} chapter {finding['chapter']} "
                f"paragraph {finding['paragraph']} {finding['code']}: {finding['excerpt']}"
            )

    unresolved = int(payload["error_count"]) + int(payload["review_count"])
    return 1 if args.strict and unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
