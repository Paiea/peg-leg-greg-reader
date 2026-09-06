from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"

PROGRESS_ORDER = {"generated": 1, "approved": 2, "live": 3}


def sync_candidate_statuses(candidates: list[dict], registry: list[dict]) -> tuple[list[dict], int]:
    best_progress: dict[str, str] = {}
    rejected_candidates: set[str] = set()
    for record in registry:
        candidate_id = record.get("candidate_id")
        status = record.get("status")
        if not isinstance(candidate_id, str):
            continue
        if status == "rejected":
            rejected_candidates.add(candidate_id)
            continue
        if status not in PROGRESS_ORDER:
            continue
        current = best_progress.get(candidate_id)
        if current is None or PROGRESS_ORDER[status] > PROGRESS_ORDER[current]:
            best_progress[candidate_id] = status

    updated: list[dict] = []
    changed = 0
    for original in candidates:
        candidate = dict(original)
        candidate_id = candidate.get("id")
        before = dict(candidate)
        progress = best_progress.get(candidate_id)
        if progress is not None:
            candidate["status"] = progress
            candidate.pop("latest_generation_status", None)
        elif candidate_id in rejected_candidates:
            # A rejected generation attempt is retryable production history, not a dead scene candidate.
            if candidate.get("status") in {"generated", "approved", "live", "rejected"}:
                candidate["status"] = "prompt_ready"
            candidate["latest_generation_status"] = "rejected"
        if candidate != before:
            changed += 1
        updated.append(candidate)
    return updated, changed


def main() -> None:
    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8")) if CANDIDATES_PATH.exists() else []
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    updated, changed = sync_candidate_statuses(candidates, registry)
    if not changed:
        print("scene candidate production statuses already current")
        return
    CANDIDATES_PATH.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"synchronized {changed} scene candidate production statuses")


if __name__ == "__main__":
    main()
