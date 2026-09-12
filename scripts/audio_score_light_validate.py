#!/usr/bin/env python3
"""Validate R2 Audio Score Light source identity and wording budget."""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
from pathlib import Path

MAX_WORD_CHANGE_RATIO = 0.15
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
SOURCE_RE = re.compile(r"^Source:\s*`([^`]+)`\s*$", re.MULTILINE)
SHA_RE = re.compile(r"^Source SHA:\s*`?([0-9a-f]{40})`?\s*$", re.MULTILINE)


def normalized_words(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def word_change_ratio(source: str, light: str) -> float:
    a = normalized_words(source)
    b = normalized_words(light)
    if not a:
        return 0.0 if not b else 1.0
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    changed = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            changed += max(i2 - i1, j2 - j1)
    return changed / len(a)


def body_after_separator(text: str) -> str:
    marker = "\n---\n"
    if marker not in text:
        raise SystemExit("Light Score is missing the --- body separator")
    return text.split(marker, 1)[1].strip()


def parse_source_header(text: str) -> tuple[Path, str]:
    source_match = SOURCE_RE.search(text)
    sha_match = SHA_RE.search(text)
    if not source_match:
        raise SystemExit("Light Score is missing Source header")
    if not sha_match:
        raise SystemExit("Light Score is missing Source SHA header")
    return Path(source_match.group(1)), sha_match.group(1)


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def validate(chapter: str) -> float:
    n = int(chapter)
    chapter_id = f"{n:03d}"
    light_path = Path(f"r2/assets/audio-score-light/ch{chapter_id}.md")
    if not light_path.exists():
        raise SystemExit(f"Missing {light_path}")

    raw = light_path.read_text(encoding="utf-8")
    source_path, recorded_sha = parse_source_header(raw)
    if source_path.as_posix() != f"r2/assets/written/ch{chapter_id}.md":
        raise SystemExit(f"Unexpected source path: {source_path}")
    if not source_path.exists():
        raise SystemExit(f"Missing source {source_path}")

    actual_sha = git_blob_sha(source_path)
    if actual_sha != recorded_sha:
        raise SystemExit(
            f"Source SHA mismatch for {chapter_id}: recorded {recorded_sha}, actual {actual_sha}"
        )

    source_body = body_after_separator(source_path.read_text(encoding="utf-8"))
    light_body = body_after_separator(raw)
    ratio = word_change_ratio(source_body, light_body)
    if ratio > MAX_WORD_CHANGE_RATIO:
        raise SystemExit(
            f"{chapter_id}: {ratio:.2%} word-level change exceeds {MAX_WORD_CHANGE_RATIO:.0%} ceiling"
        )
    return ratio


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", help="chapter number, e.g. 013")
    args = ap.parse_args()
    chapter_id = f"{int(args.chapter):03d}"
    ratio = validate(args.chapter)
    print(f"{chapter_id}: {ratio:.2%} word-level change")


if __name__ == "__main__":
    main()
