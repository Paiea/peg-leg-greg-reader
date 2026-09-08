from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.illustration_state import PRESENTATION_ROLES, load_registry

REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "READER_PRESENTATION.json"
DEFAULT_PRESENTATION_ROLE = "scene-illustration"


def build_reader_presentation(registry: Iterable[dict]) -> list[dict]:
    presentation: list[dict] = []
    for record in registry:
        if record.get("status") != "live" or record.get("kind") != "chapter_illustration":
            continue
        chapter = record.get("chapter")
        asset = record.get("live_asset")
        if not isinstance(chapter, int) or chapter < 1:
            continue
        if not isinstance(asset, str) or not asset.strip():
            continue
        role = record.get("presentation_role", DEFAULT_PRESENTATION_ROLE)
        if role not in PRESENTATION_ROLES:
            raise ValueError(f"illustration {record.get('id', '<unknown>')} has invalid presentation_role: {role!r}")
        purpose = record.get("editorial_purpose", "")
        if not isinstance(purpose, str):
            raise ValueError(f"illustration {record.get('id', '<unknown>')} editorial_purpose must be text")
        presentation.append(
            {
                "illustration_id": record.get("id", ""),
                "candidate_id": record.get("candidate_id", ""),
                "chapter": chapter,
                "asset": asset,
                "paragraph_anchor": record.get("paragraph_anchor", ""),
                "presentation_role": role,
                "editorial_purpose": purpose.strip(),
                "alt_text": record.get("alt_text", ""),
                "caption": record.get("caption", ""),
            }
        )
    return sorted(presentation, key=lambda record: (record["chapter"], record["asset"]))


def main() -> None:
    registry = load_registry(REGISTRY_PATH)
    presentation = build_reader_presentation(registry)
    text = json.dumps(presentation, indent=2, ensure_ascii=False) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print(f"reader presentation already current: {len(presentation)} live chapter illustrations")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote reader presentation: {len(presentation)} live chapter illustrations")


if __name__ == "__main__":
    main()
