#!/usr/bin/env python3
"""Build a deterministic five-worker capture work order for 3L short-take audio."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

AUTHORITY = "3l/audio/PARALLEL_INSTANT_WORKER_AUTHORITY.md"


def _flatten_chunks(plans: Iterable[dict]) -> list[dict]:
    items: list[dict] = []
    for plan in plans:
        record = str(plan["record"])
        if plan.get("dragon_routing_locked") is not True:
            raise ValueError(f"record {record}: dragon routing is not locked")
        for chunk in plan.get("chunks", []):
            voices = list(chunk.get("required_voices", []))
            if not voices:
                raise ValueError(f"record {record} chunk {chunk.get('index')}: no required voices")
            if not set(voices) <= {"deep", "normal"}:
                raise ValueError(f"record {record} chunk {chunk.get('index')}: invalid required voices {voices}")
            transcript = chunk.get("transcript", "")
            if len(transcript) > 500:
                raise ValueError(f"record {record} chunk {chunk.get('index')}: transcript exceeds 500 chars")
            items.append(
                {
                    "record": record,
                    "title": plan.get("title"),
                    "chunk_index": int(chunk["index"]),
                    "transcript": transcript,
                    "char_count": int(chunk.get("char_count", len(transcript))),
                    "semantic_spans": chunk.get("semantic_spans", []),
                    "required_voices": voices,
                    "capture_count": len(voices),
                }
            )
    if not items:
        raise ValueError("no chunks found")
    return items


def _balanced_whole_chunk_assignments(items: list[dict], worker_count: int) -> list[list[dict]]:
    """Assign whole chunks to the least-loaded worker in stable canon order."""
    if worker_count < 1:
        raise ValueError("worker_count must be positive")
    if len(items) < worker_count:
        raise ValueError("worker_count cannot exceed chunk count")

    assignments: list[list[dict]] = [[] for _ in range(worker_count)]
    loads = [0] * worker_count
    for item in items:
        worker_index = min(range(worker_count), key=lambda index: (loads[index], index))
        assignments[worker_index].append(item)
        loads[worker_index] += item["capture_count"]
    return assignments


def build_work_order(plans: list[dict], worker_count: int = 5, branch: str = "") -> dict:
    items = _flatten_chunks(plans)
    assignments = _balanced_whole_chunk_assignments(items, worker_count)

    workers = []
    for worker_number, chunks in enumerate(assignments, start=1):
        worker_id = f"instant-{worker_number}"
        captures = [
            {
                "record": chunk["record"],
                "chunk_index": chunk["chunk_index"],
                "voice": voice,
                "transcript": chunk["transcript"],
                "preview_transcript": chunk["transcript"],
            }
            for chunk in chunks
            for voice in chunk["required_voices"]
        ]
        workers.append(
            {
                "worker_id": worker_id,
                "capture_count": len(captures),
                "chunk_count": len(chunks),
                "chunks": chunks,
                "captures": captures,
                "return_manifest": f"3l/audio/workers/records-002-003-{worker_id}-captures.json",
            }
        )

    expected_keys = {
        (item["record"], item["chunk_index"], voice)
        for item in items
        for voice in item["required_voices"]
    }
    actual_keys = [
        (capture["record"], capture["chunk_index"], capture["voice"])
        for worker in workers
        for capture in worker["captures"]
    ]
    if len(actual_keys) != len(set(actual_keys)):
        raise ValueError("duplicate capture assignment detected")
    if set(actual_keys) != expected_keys:
        raise ValueError("capture coverage mismatch")

    loads = [worker["capture_count"] for worker in workers]
    if max(loads) - min(loads) > 1:
        raise ValueError(f"worker loads are not balanced within one capture: {loads}")

    return {
        "status": "frozen_work_order",
        "authority": AUTHORITY,
        "branch": branch,
        "worker_count": worker_count,
        "records": [str(plan["record"]) for plan in plans],
        "source_plans": [f"3l/audio/record-{plan['record']}-short-dual-plan.json" for plan in plans],
        "total_chunks": len(items),
        "total_captures": len(actual_keys),
        "capture_loads": loads,
        "workers": workers,
    }


def _write_outputs(order: dict, output: Path, worker_dir: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    worker_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(order, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for worker in order["workers"]:
        worker_path = worker_dir / f"records-002-003-{worker['worker_id']}-work-order.json"
        payload = {
            "status": "frozen_worker_slice",
            "authority": order["authority"],
            "branch": order["branch"],
            "records": order["records"],
            **worker,
        }
        worker_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plans", nargs="+")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--worker-dir", required=True, type=Path)
    parser.add_argument("--worker-count", type=int, default=5)
    parser.add_argument("--branch", default="")
    args = parser.parse_args()

    plans = [json.loads(Path(path).read_text(encoding="utf-8")) for path in args.plans]
    order = build_work_order(plans, worker_count=args.worker_count, branch=args.branch)
    _write_outputs(order, args.output, args.worker_dir)
    print(
        f"{order['total_chunks']} chunks / {order['total_captures']} captures -> "
        f"{order['worker_count']} workers: {order['capture_loads']}"
    )


if __name__ == "__main__":
    main()
