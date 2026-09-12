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


def make_chunks(body: str) -> list[str]:
    paragraphs = body.split("\n\n")
    if any(len(p) > MAX_CHARS for p in paragraphs):
        too_long = max(len(p) for p in paragraphs)
        raise SystemExit(f"A single score paragraph exceeds {MAX_CHARS} chars ({too_long}); repair score boundary manually")

    chunks: list[str] = []
    current: list[str] = []
    for paragraph in paragraphs:
        candidate = "\n\n".join(current + [paragraph])
        if current and len(candidate) > TARGET_CHARS:
            chunks.append("\n\n".join(current))
            current = [paragraph]
        else:
            current.append(paragraph)
    if current:
        chunks.append("\n\n".join(current))

    if len(chunks) >= 2 and len(chunks[-1]) < 140:
        combined_paras = (chunks[-2] + "\n\n" + chunks[-1]).split("\n\n")
        best = None
        for cut in range(1, len(combined_paras)):
            a = "\n\n".join(combined_paras[:cut])
            b = "\n\n".join(combined_paras[cut:])
            if len(a) <= MAX_CHARS and len(b) <= MAX_CHARS:
                score = min(len(a), len(b))
                if best is None or score > best[0]:
                    best = (score, a, b)
        if best:
            chunks[-2], chunks[-1] = best[1], best[2]

    if any(not c or len(provider_text(c)) > MAX_CHARS for c in chunks):
        raise SystemExit("Planner produced an empty or oversized provider take")
    if "\n\n".join(chunks) != body:
        raise SystemExit("Planner failed exact source coverage reconstruction")
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
