#!/usr/bin/env python3
"""Materialize Audio Score Light baselines from exact written prose."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def body_after_separator(raw: str) -> str:
    marker = "\n---\n"
    if marker not in raw:
        raise SystemExit("Written source is missing the --- body separator")
    return raw.split(marker, 1)[1].strip()


def render_light(*, raw: str, source_path: Path, source_sha: str) -> str:
    first = raw.splitlines()[0].strip()
    if not first.startswith("# Chapter ") or ":" not in first:
        raise SystemExit(f"Could not parse chapter title from {first!r}")
    body = body_after_separator(raw)
    return (
        f"{first}\n\n"
        "Status: **AUDIO SCORE LIGHT / SCORE 2 BASELINE**\n\n"
        f"Source: `{source_path.as_posix()}`\n"
        f"Source SHA: `{source_sha}`\n"
        "Protocol: `r2/AUDIO_SCORE_LIGHT.md`\n"
        "Voice target: `deep`\n"
        "Word-level change: `0.00%`\n\n"
        "This is a light speech-generation transcript. The baseline preserves the written wording exactly; later micro-edits must remain inside the Light doctrine.\n\n"
        "---\n\n"
        f"{body}\n"
    )


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def materialize(chapter: int) -> Path:
    chapter_id = f"{chapter:03d}"
    source_path = Path(f"r2/assets/written/ch{chapter_id}.md")
    if not source_path.exists():
        raise SystemExit(f"Missing {source_path}")
    raw = source_path.read_text(encoding="utf-8")
    output = Path(f"r2/assets/audio-score-light/ch{chapter_id}.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_light(raw=raw, source_path=source_path, source_sha=git_blob_sha(source_path)),
        encoding="utf-8",
    )
    return output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=30)
    args = ap.parse_args()
    if args.start < 1 or args.end < args.start:
        raise SystemExit("Invalid chapter range")
    for chapter in range(args.start, args.end + 1):
        print(materialize(chapter))


if __name__ == "__main__":
    main()
