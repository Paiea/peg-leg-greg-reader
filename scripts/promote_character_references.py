from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from scripts.score_character_references import score_reference

ROOT = Path(__file__).resolve().parents[1]
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


def _reference_from_registry(record: dict) -> dict | None:
    asset = record.get("live_asset") or record.get("source_asset")
    if not isinstance(asset, str) or not asset.strip():
        return None
    tags: list[str] = []
    framing = record.get("framing_preference")
    if framing == "above_waist":
        tags.append("above_waist")
    elif framing in {"full_body", "lower_body_visible"}:
        tags.append(str(framing))
    return {
        "asset": asset.strip(),
        "registry_id": record.get("id", ""),
        "status": record.get("status", ""),
        "approved_fit": record.get("approved_fit", ""),
        "style_family": record.get("style_family", ""),
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
        reference = _reference_from_registry(record)
        if not reference:
            continue
        for character in _record_characters(record, updated):
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
            key=lambda ref: -score_reference(ref, character, framing_preference=framing)["score"]
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
