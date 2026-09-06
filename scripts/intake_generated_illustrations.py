from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.illustration_state import load_registry, validate_registry

QUEUE_PATH = ROOT / "state" / "visual" / "GENERATION_QUEUE.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"


def intake_generated_assets(root: Path, queue: list[dict], registry: list[dict]) -> tuple[list[dict], int]:
    updated = [dict(record) for record in registry]
    known_assets = {record.get("source_asset") for record in updated if record.get("source_asset")}
    changed = 0
    for item in queue:
        target_asset = item.get("target_asset", "")
        if not target_asset or target_asset in known_assets or not (root / target_asset).is_file():
            continue
        art_id = Path(target_asset).stem
        updated.append(
            {
                "id": art_id,
                "candidate_id": item["candidate_id"],
                "chapter": item["chapter"],
                "kind": item["kind"],
                "status": "generated",
                "style_family": item.get("style_family", "sketch-ink-paint"),
                "framing_preference": item.get("framing_preference", "scene_appropriate"),
                "camera_angle": item.get("camera_angle", ""),
                "pose_family": item.get("pose_family", ""),
                "scene_tags": list(item.get("scene_tags", [])),
                "characters": list(item.get("characters", [])),
                "character_tag_source": "generation_queue" if item.get("characters") else "",
                "source_asset": target_asset,
                "live_asset": "",
                "caption": "",
                "alt_text": "",
                "approved_fit": item["fit_target"],
                "prompt_pack": item["prompt_pack"],
                "paragraph_anchor": item.get("paragraph_anchor", ""),
                "reference_selection_notes": item.get("reference_selection_notes", ""),
                "notes": "Auto-intaked from deterministic generation queue. Requires explicit approval before reader promotion.",
            }
        )
        known_assets.add(target_asset)
        changed += 1
    validate_registry(updated)
    return updated, changed


def main() -> None:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8")) if QUEUE_PATH.exists() else []
    registry = load_registry(REGISTRY_PATH)
    updated, changed = intake_generated_assets(ROOT, queue, registry)
    if not changed:
        print("no newly generated illustration assets found")
        return
    REGISTRY_PATH.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"intaked {changed} generated illustration assets")


if __name__ == "__main__":
    main()
