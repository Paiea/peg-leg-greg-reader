#!/usr/bin/env python3
"""Validate Instant worker receipts and group successful captures by 3L record."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "3l" / "audio"
WORKERS = AUDIO / "workers"
MASTER = AUDIO / "records-002-010-five-worker-work-order.json"
AUTHORITY = "3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md"


def capture_key(item: dict) -> tuple[str, int, str]:
    return str(item["record"]), int(item["chunk_index"]), str(item["voice"])


def reconcile() -> dict:
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    assigned: dict[str, dict[tuple[str, int, str], dict]] = {}
    all_expected: set[tuple[str, int, str]] = set()
    for worker in master["workers"]:
        worker_id = worker["worker_id"]
        mapping = {}
        for item in worker["captures"]:
            key = capture_key(item)
            if key in all_expected:
                raise ValueError(f"duplicate master assignment {key}")
            mapping[key] = item
            all_expected.add(key)
        assigned[worker_id] = mapping

    successful: dict[tuple[str, int, str], dict] = {}
    worker_status = []
    for worker in master["workers"]:
        worker_id = worker["worker_id"]
        path = ROOT / worker["return_manifest"]
        if not path.exists():
            worker_status.append({"worker_id": worker_id, "status": "missing", "successful": 0})
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("worker_id") != worker_id:
            raise ValueError(f"{path}: worker_id mismatch")
        expected = assigned[worker_id]
        represented: set[tuple[str, int, str]] = set()
        successes = 0
        for item in manifest.get("captures", []):
            key = capture_key(item)
            if key not in expected:
                raise ValueError(f"{path}: unassigned capture {key}")
            if key in represented:
                raise ValueError(f"{path}: duplicate capture {key}")
            represented.add(key)
            source = expected[key]
            if item.get("transcript") != source["transcript"]:
                raise ValueError(f"{path}: transcript mismatch {key}")
            if item.get("preview_transcript") != source["preview_transcript"]:
                raise ValueError(f"{path}: preview transcript mismatch {key}")
            if item.get("status") != "success":
                continue
            if not item.get("context_id") or not item.get("preview_url"):
                raise ValueError(f"{path}: successful capture missing receipt data {key}")
            if key in successful:
                raise ValueError(f"duplicate returned capture across workers {key}")
            successful[key] = item
            successes += 1
        if len(represented) != int(manifest.get("assigned_capture_count", len(represented))):
            raise ValueError(f"{path}: assigned count does not reconcile")
        worker_status.append({"worker_id": worker_id, "status": manifest.get("status"), "successful": successes})

    for record in master["records"]:
        items = []
        for key, item in successful.items():
            if key[0] != record:
                continue
            items.append(
                {
                    "chunk": key[1],
                    "voice": key[2],
                    "transcript": item["transcript"],
                    "context_id": item["context_id"],
                    "preview_url": item["preview_url"],
                    "audio_url": item.get("audio_url"),
                    "status": "ready",
                }
            )
        items.sort(key=lambda item: (item["chunk"], item["voice"]))
        path = AUDIO / f"record-{record}-short-captures-workers.json"
        payload = {
            "record": record,
            "authority": AUTHORITY,
            "plan": f"3l/audio/record-{record}-short-dual-plan.json",
            "source_work_order": str(MASTER.relative_to(ROOT)),
            "captures": items,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = {
        "expected_capture_count": len(all_expected),
        "successful_capture_count": len(successful),
        "workers": worker_status,
    }
    print(json.dumps(result))
    return result


if __name__ == "__main__":
    reconcile()
