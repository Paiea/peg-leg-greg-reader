from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CATALOG_PATH = ROOT / "state" / "visual" / "CHARACTER_VISUAL_REFERENCES.json"

CURATED_REFERENCE_METADATA: dict[str, dict] = {
    "visual/homepage/peg-leg-greg-homepage-frontispiece.png": {
        "pose_family": "portrait_anchor",
        "scene_tags": ["frontispiece", "portrait"],
        "tags": ["curated", "strong_face", "style_anchor"],
        "style_family": "sketch-ink-paint",
        "metadata_source": "curated_backfill",
    },
    "assets/book-role-cards/book-i-warrior-005.webp": {
        "pose_family": "role_card",
        "scene_tags": ["role_card", "warrior", "character_anchor"],
        "tags": ["curated", "strong_face", "style_anchor"],
        "style_family": "sketch-ink-paint",
        "metadata_source": "curated_backfill",
    },
    "assets/book-role-cards/book-ii-stagehand-177.webp": {
        "framing": "above_waist",
        "view_angle": "three_quarter",
        "pose_family": "working",
        "scene_tags": ["backstage", "theatre", "work"],
        "tags": ["curated", "above_waist", "strong_face", "style_anchor"],
        "style_family": "sketch-ink-paint",
        "metadata_source": "curated_backfill",
    },
}


def backfill_reference_metadata(catalog: dict[str, dict]) -> tuple[dict[str, dict], int]:
    updated = deepcopy(catalog)
    changed = 0
    for character_record in updated.values():
        assets = [
            asset
            for asset in character_record.get("reference_assets", [])
            if isinstance(asset, str) and asset.strip()
        ]
        metadata = dict(character_record.get("reference_metadata", {}))
        for asset in assets:
            hint = CURATED_REFERENCE_METADATA.get(asset)
            if not hint:
                continue
            existing = metadata.get(asset, {}) if isinstance(metadata.get(asset), dict) else {}
            merged = {**hint, **existing}
            if metadata.get(asset) != merged:
                metadata[asset] = merged
                changed += 1
        if metadata:
            character_record["reference_metadata"] = metadata
    return updated, changed


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {}
    updated, changed = backfill_reference_metadata(catalog)
    text = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
    previous = CATALOG_PATH.read_text(encoding="utf-8") if CATALOG_PATH.exists() else None
    if previous == text:
        print("character reference metadata already current")
        return
    CATALOG_PATH.write_text(text, encoding="utf-8")
    print(f"backfilled metadata on {changed} character reference anchors")


if __name__ == "__main__":
    main()
