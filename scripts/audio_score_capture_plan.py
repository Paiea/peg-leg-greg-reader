#!/usr/bin/env python3
"""Build a deterministic preview-safe capture plan from an Audio Score.

The plan preserves exact source coverage separately from provider-facing text.
Provider-facing pronunciation aliases never edit story authority.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

MAX_CHARS = 500
TARGET_CHARS = 470

SUBSTITUTIONS = (
    (re.compile(r"\bMana\b"), "Ma-na"),
    (re.compile(r"\bmana\b"), "ma-na"),
    (re.compile(r"\bVale\b"), "Vayle"),
    (re.compile(r"\bSparring\b"), "Spar-ring"),
    (re.compile(r"\bsparring\b"), "spar-ring"),
)
NATURAL_BOUNDARY_RE = re.compile(r"(?:\n\n|(?<=[.!?])\s+|(?<=[,;:])\s+)")
WHITESPACE_RE = re.compile(r"\s+")


def provider_text(source: str) -> str:
    out = source
    for pattern, replacement in SUBSTITUTIONS:
        out = pattern.sub(replacement, out)
    return out


def score_body(text: str) -> str:
    marker = "\n---\n"
    if marker not in text:
        raise SystemExit("Audio Score is missing the --- body separator")
    return text.split(marker, 1)[1].strip()


def title_from_score(text: str) -> str:
    first = text.splitlines()[0].strip()
    m = re.match(r"# Chapter \d+:\s*(.+)$", first)
    if not m:
        raise SystemExit(f"Could not parse title from {first!r}")
    return m.group(1).strip()


def generation_paths(generation: str, chapter: str) -> tuple[Path, Path]:
    if generation == "v2":
        return (
            Path(f"r2/assets/audio-score/ch{chapter}.md"),
            Path(f"greg-again/audio/v2/takes/{chapter}/short-takes.json"),
        )
    if generation == "light":
        return (
            Path(f"r2/assets/audio-score-light/ch{chapter}.md"),
            Path(f"greg-again/audio/light/takes/{chapter}/short-takes.json"),
        )
    raise SystemExit(f"Unsupported generation: {generation}")


def _candidate_cuts(
    body: str, start: int, end: int, pattern: re.Pattern[str]
) -> list[int]:
    return [start + match.end() for match in pattern.finditer(body[start:end])]


def make_chunks(body: str) -> list[str]:
    chunks: list[str] = []
    start = 0
    total = len(body)

    while start < total:
        remaining = body[start:]
        if len(provider_text(remaining)) <= MAX_CHARS:
            chunks.append(remaining)
            break

        target_end = min(total, start + TARGET_CHARS)
        hard_end = min(total, start + MAX_CHARS)

        cuts = _candidate_cuts(body, start, target_end, NATURAL_BOUNDARY_RE)
        if not cuts:
            cuts = _candidate_cuts(body, start, hard_end, NATURAL_BOUNDARY_RE)
        if not cuts:
            cuts = _candidate_cuts(body, start, hard_end, WHITESPACE_RE)
        if not cuts:
            cuts = [hard_end]

        cut = cuts[-1]

        all_cuts = list(
            dict.fromkeys(
                _candidate_cuts(body, start, hard_end, NATURAL_BOUNDARY_RE)
                + _candidate_cuts(body, start, hard_end, WHITESPACE_RE)
                + [hard_end]
            )
        )
        valid = [
            candidate
            for candidate in all_cuts
            if candidate > start
            and len(provider_text(body[start:candidate])) <= MAX_CHARS
        ]
        if cut <= start or len(provider_text(body[start:cut])) > MAX_CHARS:
            if not valid:
                raise SystemExit("Could not find a preview-safe chunk boundary")
            cut = max(valid)

        chunks.append(body[start:cut])
        start = cut

    if "".join(chunks) != body:
        raise SystemExit("Planner failed exact source coverage reconstruction")
    if any(not chunk or len(provider_text(chunk)) > MAX_CHARS for chunk in chunks):
        raise SystemExit("Planner produced an empty or oversized provider take")
    return chunks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", help="chapter number, e.g. 013")
    ap.add_argument("--generation", choices=("v2", "light"), default="v2")
    ap.add_argument("--output")
    args = ap.parse_args()

    n = int(args.chapter)
    chapter = f"{n:03d}"
    source, default_output = generation_paths(args.generation, chapter)
    if not source.exists():
        raise SystemExit(f"Missing {source}")

    raw = source.read_text()
    body = score_body(raw)
    chunks = make_chunks(body)
    blob_sha = subprocess.check_output(["git", "hash-object", str(source)], text=True).strip()
    output = Path(args.output) if args.output else default_output
    output.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "chapter": n,
        "chapter_id": f"ga-{chapter}",
        "generation": args.generation,
        "title": title_from_score(raw),
        "source": str(source),
        "source_blob_sha": blob_sha,
        "voice": "deep",
        "status": "capture_plan",
        "factory": "preview_safe_short_take_capture_v1",
        "max_chars": MAX_CHARS,
        "provider_facing_substitutions": {
            "mana": "ma-na",
            "Mana": "Ma-na",
            "Vale": "Vayle",
            "sparring": "spar-ring",
        },
        "take_count": len(chunks),
        "takes": [
            {
                "order": i,
                "source_transcript": source_chunk,
                "transcript": provider_text(source_chunk),
                "preview_transcript": provider_text(source_chunk),
            }
            for i, source_chunk in enumerate(chunks, 1)
        ],
    }
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{chapter}: {len(chunks)} takes -> {output}")


if __name__ == "__main__":
    main()
