from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
ACCEPTED_STATUSES = {"approved", "live"}

VIEW_PATTERNS = (
    (r"\bthree[- ]quarter\b", "three_quarter"),
    (r"\bprofile\b", "profile"),
    (r"\bover[- ]the[- ]shoulder\b|\bover shoulder\b", "over_shoulder"),
    (r"\bfront[- ]facing\b|\bfront view\b", "front"),
)
POSE_PATTERNS = (
    (r"\bwork(?:s|ing)?\b|\bworking at\b", "working"),
    (r"\bwrit(?:e|es|ing)\b", "writing"),
    (r"\bseated\b|\bsitting\b", "seated"),
    (r"\bstanding\b", "standing"),
    (r"\bwalking\b|\bmoving through\b", "moving"),
)
SCENE_KEYWORDS = {
    "backstage": "backstage",
    "theatre": "theatre",
    "theater": "theatre",
    "stage": "stage",
    "market": "market",
    "street": "street",
    "mill": "mill",
    "workshop": "workshop",
    "costume": "costume",
    "wagon": "travel",
    "road": "travel",
}


def _metadata_text(record: dict) -> str:
    return " ".join(
        str(record.get(field, ""))
        for field in ("alt_text", "caption", "notes")
        if isinstance(record.get(field, ""), str)
    ).lower()


def _first_match(patterns: tuple[tuple[str, str], ...], text: str) -> str:
    for pattern, value in patterns:
        if re.search(pattern, text):
            return value
    return ""


def backfill_tagged_registry_metadata(registry: list[dict]) -> tuple[list[dict], int]:
    updated = deepcopy(registry)
    changed = 0
    for record in updated:
        if record.get("status") not in ACCEPTED_STATUSES or not record.get("characters"):
            continue
        text = _metadata_text(record)
        before = json.dumps(record, sort_keys=True)

        if not record.get("view_angle"):
            view_angle = _first_match(VIEW_PATTERNS, text)
            if view_angle:
                record["view_angle"] = view_angle
        if not record.get("pose_family"):
            pose_family = _first_match(POSE_PATTERNS, text)
            if pose_family:
                record["pose_family"] = pose_family

        existing_tags = [tag for tag in record.get("scene_tags", []) if isinstance(tag, str) and tag.strip()]
        discovered = [value for keyword, value in SCENE_KEYWORDS.items() if re.search(rf"\b{re.escape(keyword)}\b", text)]
        merged_tags = list(dict.fromkeys(existing_tags + discovered))
        if merged_tags and merged_tags != record.get("scene_tags"):
            record["scene_tags"] = merged_tags

        if json.dumps(record, sort_keys=True) != before:
            record["metadata_backfill_source"] = "strong_text_metadata"
            changed += 1
    return updated, changed


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    updated, changed = backfill_tagged_registry_metadata(registry)
    text = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
    previous = REGISTRY_PATH.read_text(encoding="utf-8") if REGISTRY_PATH.exists() else None
    if previous == text:
        print("tagged registry metadata already current")
        return
    REGISTRY_PATH.write_text(text, encoding="utf-8")
    print(f"backfilled metadata on {changed} tagged accepted-art records")


if __name__ == "__main__":
    main()
