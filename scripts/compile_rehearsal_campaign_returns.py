#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

WORKER_SCHEMA = "rehearsal_campaign_worker_result/v1"
TARGET_BRANCH = "editor/rehearsal-simulation-engine"
HARD_SURFACES = {
    "plot",
    "facts",
    "knowledge",
    "causality",
    "major_relationship_state",
    "physical_state",
    "chronology",
    "economics",
    "earned_competence",
    "injury_state",
    "mystery_state",
}
WRITABLE_SURFACES = {
    "dialogue",
    "paragraphing",
    "movement",
    "blocking",
    "silence",
    "interaction_timing",
    "reaction_placement",
    "object_handling",
    "local_exchange_shape",
    "tone",
    "internal_dialogue",
    "narration_rhythm",
    "attention_order",
    "sensory_emphasis",
    "memory_intrusion",
}
VALID_DISPOSITIONS = {"source_win", "returns", "blocked"}


def validate_worker_result(result: dict) -> None:
    if result.get("schema") != WORKER_SCHEMA:
        raise ValueError("invalid worker result schema")
    batch = result.get("batch")
    if not isinstance(batch, dict):
        raise ValueError("worker result batch is required")
    start, end = batch.get("start"), batch.get("end")
    authority = batch.get("source_authority")
    if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
        raise ValueError("invalid claimed batch")
    if not isinstance(authority, str) or not authority:
        raise ValueError("batch source authority is required")
    chapters = result.get("chapters")
    if not isinstance(chapters, list):
        raise ValueError("chapters must be a list")
    expected = list(range(start, end + 1))
    actual = [item.get("chapter") for item in chapters if isinstance(item, dict)]
    if actual != expected:
        raise ValueError("worker chapters must exactly cover claimed batch in order")
    for item in chapters:
        if item.get("disposition") not in VALID_DISPOSITIONS:
            raise ValueError("invalid chapter disposition")
        if not isinstance(item.get("discoveries"), list) or not isinstance(item.get("rejected_hot"), list):
            raise ValueError("discoveries and rejected_hot must be lists")
    candidates = result.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    seen_ids: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("candidates must be objects")
        cid = candidate.get("id")
        if not isinstance(cid, str) or not cid or cid in seen_ids:
            raise ValueError("candidate ids must be unique non-empty strings")
        seen_ids.add(cid)
        chapter = candidate.get("chapter")
        if not isinstance(chapter, int) or not start <= chapter <= end:
            raise ValueError("candidate chapter must remain inside claimed batch")
        surfaces = candidate.get("changed_surfaces")
        if not isinstance(surfaces, list) or not surfaces:
            raise ValueError("candidate changed_surfaces are required")
        hard = HARD_SURFACES.intersection(surfaces)
        if hard:
            raise ValueError(f"hard surface is not writable: {sorted(hard)}")
        invalid = set(surfaces) - WRITABLE_SURFACES
        if invalid:
            raise ValueError(f"invalid writable surface: {sorted(invalid)}")
        if candidate.get("actor_prefers") is not True:
            raise ValueError("candidate requires actor preference")
        if candidate.get("dramatic_lock_status") != "preserved":
            raise ValueError("candidate must preserve dramatic lock")
        if candidate.get("reader_check") != "pass":
            raise ValueError("candidate reader check must pass")
        before, after = candidate.get("before"), candidate.get("after")
        if not isinstance(before, str) or not before or not isinstance(after, str) or not after:
            raise ValueError("candidate before and after prose are required")


def compile_worker_result(root: str | Path, result: dict) -> dict:
    root = Path(root)
    validate_worker_result(result)
    batch = result["batch"]
    candidates = result["candidates"]
    if not candidates:
        return {
            "result": "source_win",
            "source_authority": batch["source_authority"],
            "manifest": None,
        }

    patches: list[dict] = []
    for candidate in candidates:
        chapter = candidate["chapter"]
        path = root / "chapters" / f"{chapter:03d}.html"
        if not path.exists():
            raise ValueError(f"chapter file missing for claimed batch: {chapter}")
        text = path.read_text(encoding="utf-8")
        count = text.count(candidate["before"])
        if count != 1:
            raise ValueError(
                f"literal exact source required for {candidate['id']}: found {count}"
            )
        patches.append(dict(candidate))

    manifest = {
        "schema": "rehearsal_free_returns/v1",
        "campaign": f"canon-{batch['start']:03d}-{batch['end']:03d}-autonomous-boundary-hunt",
        "mode": "free_production",
        "target_branch": TARGET_BRANCH,
        "source_authority": batch["source_authority"],
        "patches": patches,
    }
    return {
        "result": "returns",
        "source_authority": batch["source_authority"],
        "manifest": manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a schema-bound REHEARSAL worker result into an exact-source return manifest.")
    parser.add_argument("--worker-result", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    worker_result = json.loads((root / args.worker_result).read_text(encoding="utf-8"))
    compiled = compile_worker_result(root, worker_result)
    summary_path = root / args.summary
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps({k: v for k, v in compiled.items() if k != "manifest"}, indent=2) + "\n", encoding="utf-8")
    if compiled["manifest"] is not None:
        manifest_path = root / args.manifest
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(compiled["manifest"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"result": compiled["result"], "manifest": None if compiled["manifest"] is None else args.manifest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
