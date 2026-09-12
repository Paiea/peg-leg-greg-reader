#!/usr/bin/env python3
"""Build compact derived resume packets for Audio Score voice capture work."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

VALID_GENERATIONS = {"v2", "light"}
DURABLE_PREVIEW_PREFIX = "https://storage.googleapis.com/"


def take_map_path(repo_root: Path, generation: str, chapter: int) -> Path:
    if generation not in VALID_GENERATIONS:
        raise ValueError(f"unsupported Audio Score generation: {generation}")
    return Path(repo_root) / "greg-again" / "audio" / generation / "takes" / f"{chapter:03d}" / "short-takes.json"


def _durable_map_capture_orders(data: dict) -> set[int]:
    captured: set[int] = set()
    for take in data.get("takes", []):
        context_id = str(take.get("context_id", "")).strip()
        preview_url = str(take.get("preview_url", "")).strip()
        if context_id and preview_url.startswith(DURABLE_PREVIEW_PREFIX):
            captured.add(int(take["order"]))
    return captured


def _capture_result_orders(results_path: Path, expected: int) -> set[int]:
    if not results_path.exists():
        return set()

    captured: set[int] = set()
    with results_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            order = int(row["order"])
            if order in captured:
                raise ValueError(f"duplicate capture result for take {order}")
            if order < 1 or order > expected:
                raise ValueError(f"capture result order outside planned range: {order}")
            context_id = str(row.get("context_id", "")).strip()
            if not context_id:
                raise ValueError(f"missing context_id for take {order}")
            preview_url = str(row.get("preview_url", "")).strip()
            if not preview_url.startswith(DURABLE_PREVIEW_PREFIX):
                raise ValueError(f"invalid preview_url for take {order}: {preview_url}")
            captured.add(order)
    return captured


def build_resume_packet(take_map: Path, *, batch_size: int = 5) -> dict:
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    take_map = Path(take_map)
    data = json.loads(take_map.read_text(encoding="utf-8"))
    takes = data.get("takes", [])
    expected = int(data.get("take_count", len(takes)))
    if expected != len(takes):
        raise ValueError("take_count does not match planned takes")

    orders = [int(take["order"]) for take in takes]
    if orders != list(range(1, expected + 1)):
        raise ValueError("take orders are not contiguous from 1")

    captured = _durable_map_capture_orders(data)
    captured.update(_capture_result_orders(take_map.parent / "capture-results.tsv", expected))
    missing = [take for take in takes if int(take["order"]) not in captured]

    next_takes = [
        {
            "order": int(take["order"]),
            "transcript": take["transcript"],
            "preview_transcript": take["preview_transcript"],
        }
        for take in missing[:batch_size]
    ]

    return {
        "schema": "audio_score_resume/v1",
        "generation": data.get("generation", "v2"),
        "chapter": int(data["chapter"]),
        "chapter_id": data["chapter_id"],
        "title": data.get("title"),
        "voice": data.get("voice", "deep"),
        "source": data.get("source"),
        "source_blob_sha": data.get("source_blob_sha"),
        "status": "capture_complete" if not missing else "resume",
        "take_count": expected,
        "captured_count": len(captured),
        "missing_count": len(missing),
        "batch_size": batch_size,
        "next_takes": next_takes,
    }


def write_resume_packet(take_map: Path, *, batch_size: int = 5, output: Path | None = None) -> Path:
    packet = build_resume_packet(take_map, batch_size=batch_size)
    output = Path(output) if output else Path(take_map).parent / "resume.json"
    output.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chapter", type=int)
    parser.add_argument("--generation", choices=sorted(VALID_GENERATIONS), default="light")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    path = take_map_path(Path(args.repo_root), args.generation, args.chapter)
    if args.write:
        output = write_resume_packet(
            path,
            batch_size=args.batch_size,
            output=Path(args.output) if args.output else None,
        )
        print(json.dumps({"status": "written", "path": str(output)}, indent=2))
        return

    print(json.dumps(build_resume_packet(path, batch_size=args.batch_size), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
