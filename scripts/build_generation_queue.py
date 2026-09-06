from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.illustration_state import load_registry, load_scene_candidates

CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "GENERATION_QUEUE.json"
ACTIVE_STATUSES = {"generated", "approved", "live"}
VERSION_RE = re.compile(r"-v(\d+)$")


def _next_version(candidate_id: str, registry: list[dict]) -> int:
    versions = []
    for record in registry:
        if record.get("candidate_id") != candidate_id:
            continue
        match = VERSION_RE.search(str(record.get("id", "")))
        if match:
            versions.append(int(match.group(1)))
    return max(versions, default=0) + 1


def build_generation_queue(candidates: list[dict], registry: list[dict]) -> list[dict]:
    active = {
        record.get("candidate_id")
        for record in registry
        if record.get("status") in ACTIVE_STATUSES
    }
    queue: list[dict] = []
    for candidate in candidates:
        if candidate.get("status") != "prompt_ready" or candidate.get("candidate_id") in active or candidate.get("id") in active:
            continue
        candidate_id = candidate["id"]
        if candidate_id in active:
            continue
        version = _next_version(candidate_id, registry)
        target_asset = f"visual/chapter_art/{candidate['chapter']:03d}/{candidate_id}-v{version}.webp"
        queue.append(
            {
                "candidate_id": candidate_id,
                "chapter": candidate["chapter"],
                "chapter_title": candidate["chapter_title"],
                "kind": candidate["kind"],
                "priority": candidate["priority"],
                "fit_target": candidate["fit_target"],
                "prompt_pack": f"state/visual/prompt-packs/{candidate_id}.md",
                "paragraph_anchor": candidate.get("paragraph_anchor", ""),
                "target_asset": target_asset,
                "status": "generation_ready",
            }
        )
    rank = {"high": 0, "medium": 1, "low": 2}
    return sorted(queue, key=lambda record: (rank.get(record["priority"], 9), record["chapter"], record["candidate_id"]))


def main() -> None:
    candidates = load_scene_candidates(CANDIDATES_PATH)
    registry = load_registry(REGISTRY_PATH)
    queue = build_generation_queue(candidates, registry)
    text = json.dumps(queue, indent=2, ensure_ascii=False) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print(f"generation queue already current: {len(queue)} ready")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote generation queue: {len(queue)} ready")


if __name__ == "__main__":
    main()
