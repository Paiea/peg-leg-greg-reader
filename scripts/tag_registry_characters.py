from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CATALOG_PATH = ROOT / "state" / "visual" / "CHARACTER_VISUAL_REFERENCES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
ACCEPTED_STATUSES = {"approved", "live"}


def detect_characters(record: dict, catalog: dict[str, dict]) -> tuple[list[str], str]:
    known = list(catalog)
    explicit = record.get("characters")
    explicit_found = [
        name for name in explicit
        if isinstance(name, str) and name in catalog
    ] if isinstance(explicit, list) else []

    text = " ".join(
        value
        for value in (record.get("alt_text", ""), record.get("caption", ""), record.get("notes", ""))
        if isinstance(value, str)
    )
    text_found: list[str] = []
    if text.strip():
        for character in known:
            pattern = r"(?<![\w'-])" + re.escape(character) + r"(?![\w'-])"
            if re.search(pattern, text, flags=re.IGNORECASE):
                text_found.append(character)

    found = [character for character in known if character in explicit_found or character in text_found]
    if not found:
        return [], ""
    if explicit_found and text_found:
        source = "explicit+text_metadata"
    elif explicit_found:
        source = "explicit"
    else:
        source = "text_metadata"
    return found, source


def tag_registry_characters(registry: list[dict], catalog: dict[str, dict]) -> tuple[list[dict], int]:
    updated: list[dict] = []
    changed = 0
    for record in registry:
        new = dict(record)
        if new.get("status") in ACCEPTED_STATUSES:
            characters, source = detect_characters(new, catalog)
            if characters and new.get("characters") != characters:
                new["characters"] = characters
                new["character_tag_source"] = source
                changed += 1
            elif characters and new.get("character_tag_source") != source:
                new["character_tag_source"] = source
                changed += 1
        updated.append(new)
    return updated, changed


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {}
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    updated, changed = tag_registry_characters(registry, catalog)
    if not changed:
        print("registry character tags already current")
        return
    REGISTRY_PATH.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"tagged character metadata on {changed} registry records")


if __name__ == "__main__":
    main()
