from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.score_character_references import score_reference

CATALOG_PATH = ROOT / "state" / "visual" / "CHARACTER_VISUAL_REFERENCES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
MIN_PROMOTION_SCORE = 60
MAX_AUTO_REFERENCES_PER_CHARACTER = 6


def _record_characters(record: dict, catalog: dict[str, dict]) -> list[str]:
    explicit = record.get("characters", [])
    if isinstance(explicit, list):
        found = [character for character in explicit if isinstance(character, str) and character in catalog]
        if found:
            return found
    text = " ".join(
        value for value in [record.get("alt_text", ""), record.get("caption", ""), record.get("notes", "")]
        if isinstance(value, str)
    ).lower()
    return [character for character in catalog if character.lower() in text]


def _identity_explicit(record: dict, character: str) -> bool:
    text = " ".join(
        value for value in [record.get("alt_text", ""), record.get("caption", "")]
        if isinstance(value, str)
    )
    pattern = r"(?<![\w'-])" + re.escape(character) + r"(?![\w'-])"
    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def _reference_from_registry(record: dict, character: str) -> dict | None:
    asset = record.get("live_asset") or record.get("source_asset")
    if not isinstance(asset, str) or not asset.strip():
        return None
    tags: list[str] = []
    framing = record.get("framing_preference") or record.get("framing")
    if framing == "above_waist":
        tags.append("above_waist")
    elif framing in {"full_body", "lower_body_visible"}:
        tags.append(str(framing))
    if _identity_explicit(record, character):
        tags.append("identity_explicit")
    characters = [name for name in record.get("characters", []) if isinstance(name, str)]
    if characters == [character]:
        tags.append("single_character_anchor")
    return {
        "asset": asset.strip(),
        "registry_id": record.get("id", ""),
        "status": record.get("status", ""),
        "approved_fit": record.get("approved_fit", ""),
        "style_family": record.get("style_family", ""),
        "framing_preference": framing or "",
        "view_angle": record.get("view_angle") or record.get("camera_angle", ""),
        "pose_family": record.get("pose_family", ""),
        "scene_tags": list(record.get("scene_tags", [])),
        "tags": tags,
        "source": "auto-promoted",
    }


def promote_character_references(
    catalog: dict[str, dict],
    registry: list[dict],
    min_score: int = MIN_PROMOTION_SCORE,
    max_auto_references_per_character: int = MAX_AUTO_REFERENCES_PER_CHARACTER,
) -> tuple[dict[str, dict], int]:
    updated = deepcopy(catalog)
    promoted = 0

    for character in updated:
        updated[character].setdefault("references", [])

    for record in registry:
        if record.get("status") not in {"approved", "live"}:
            continue
        for character in _record_characters(record, updated):
            reference = _reference_from_registry(record, character)
            if not reference:
                continue
            character_record = updated[character]
            existing_assets = {
                asset for asset in character_record.get("reference_assets", []) if isinstance(asset, str)
            } | {
                ref.get("asset") for ref in character_record.get("references", []) if isinstance(ref, dict)
            }
            if reference["asset"] in existing_assets:
                continue
            framing = "above_waist" if character == "Greg" else "scene_appropriate"
            quality = score_reference(reference, character, framing_preference=framing)
            if quality["score"] < min_score:
                continue
            promoted_reference = {**reference, "quality_score": quality["score"]}
            character_record["references"].append(promoted_reference)
            promoted += 1

    for character, character_record in updated.items():
        references = [ref for ref in character_record.get("references", []) if isinstance(ref, dict)]
        framing = "above_waist" if character == "Greg" else "scene_appropriate"
        references.sort(
            key=lambda ref: (
                -score_reference(ref, character, framing_preference=framing)["score"],
                ref.get("asset", ""),
            )
        )
        character_record["references"] = references[: max(max_auto_references_per_character, 0)]

    return updated, promoted


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {}
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    updated, promoted = promote_character_references(catalog, registry)
    text = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
    previous = CATALOG_PATH.read_text(encoding="utf-8") if CATALOG_PATH.exists() else None
    if previous == text:
        print("character visual references already current")
        return
    CATALOG_PATH.write_text(text, encoding="utf-8")
    print(f"promoted {promoted} character visual references")


if __name__ == "__main__":
    main()
