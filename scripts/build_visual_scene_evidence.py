from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.character_visual_timeline import load_visual_timeline, resolve_scene_character_states
from scripts.illustration_state import load_registry, load_scene_candidates
from scripts.performance_roundtrip_references import load_visual_references, normalize_text

CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
BOUNDED_APPROVALS_PATH = ROOT / "state" / "visual" / "BOUNDED_GENERATION_APPROVALS.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
TIMELINE_PATH = ROOT / "state" / "visual" / "CHARACTER_VISUAL_TIMELINE.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "VISUAL_SCENE_EVIDENCE.json"


def merge_candidates(primary: Iterable[dict], overlay: Iterable[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    order: list[str] = []
    for record in list(primary) + list(overlay):
        candidate_id = record.get("id")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            continue
        if candidate_id not in merged:
            order.append(candidate_id)
        merged[candidate_id] = dict(record)
    return [merged[candidate_id] for candidate_id in order]


def _performance_reference_for_candidate(candidate: dict, performance_references: dict[int, dict]) -> dict | None:
    chapter = candidate.get("chapter")
    reference = performance_references.get(chapter) if isinstance(chapter, int) else None
    if not reference:
        return None
    candidate_anchor = candidate.get("paragraph_anchor")
    scene_anchors = reference.get("scene_anchors")
    if not isinstance(candidate_anchor, str) or not candidate_anchor.strip():
        return None
    if not isinstance(scene_anchors, list) or not scene_anchors:
        return None
    normalized_candidate = normalize_text(candidate_anchor)
    normalized_anchors = {
        normalize_text(anchor)
        for anchor in scene_anchors
        if isinstance(anchor, str) and anchor.strip()
    }
    return dict(reference) if normalized_candidate in normalized_anchors else None


def _existing_art_for_chapter(registry: Iterable[dict], chapter: int) -> list[dict]:
    art: list[dict] = []
    for record in registry:
        if record.get("chapter") != chapter or record.get("kind") != "chapter_illustration":
            continue
        if record.get("status") not in {"approved", "live"}:
            continue
        asset = record.get("live_asset") or record.get("source_asset")
        if not isinstance(asset, str) or not asset.strip():
            continue
        art.append(
            {
                "id": record.get("id", ""),
                "candidate_id": record.get("candidate_id", ""),
                "status": record.get("status", ""),
                "asset": asset,
                "alt_text": record.get("alt_text", ""),
                "paragraph_anchor": record.get("paragraph_anchor", ""),
                "presentation_role": record.get("presentation_role", "scene-illustration"),
            }
        )
    return sorted(art, key=lambda item: (item["status"] != "live", item["asset"]))


def _condition(character_states: dict[str, dict], performance_reference: dict | None) -> str:
    if character_states and performance_reference:
        return "prose_temporal_performance"
    if performance_reference:
        return "prose_performance"
    if character_states:
        return "prose_temporal"
    return "prose_only"


def build_visual_scene_evidence(
    candidates: Iterable[dict],
    registry: Iterable[dict],
    temporal_states: Iterable[dict],
    performance_references: dict[int, dict],
) -> list[dict]:
    timeline = list(temporal_states)
    registry_records = list(registry)
    evidence: list[dict] = []
    for candidate in candidates:
        candidate_id = candidate.get("id")
        chapter = candidate.get("chapter")
        if not isinstance(candidate_id, str) or not candidate_id.strip() or not isinstance(chapter, int):
            continue
        characters = [name for name in candidate.get("characters", []) if isinstance(name, str) and name.strip()]
        character_states = resolve_scene_character_states(timeline, characters, chapter)
        performance_reference = _performance_reference_for_candidate(candidate, performance_references)
        record = {
            "candidate_id": candidate_id,
            "chapter": chapter,
            "chapter_title": candidate.get("chapter_title", ""),
            "paragraph_anchor": candidate.get("paragraph_anchor", ""),
            "scene_summary": candidate.get("scene_summary", ""),
            "visual_hook": candidate.get("visual_hook", ""),
            "characters": characters,
            "location": candidate.get("location", ""),
            "mood": candidate.get("mood", ""),
            "scene_tags": list(candidate.get("scene_tags", [])),
            "scene_continuity_notes": candidate.get("continuity_notes", ""),
            "character_states": character_states,
            "existing_art": _existing_art_for_chapter(registry_records, chapter),
            "evidence_condition": _condition(character_states, performance_reference),
        }
        if performance_reference is not None:
            record["performance_reference"] = performance_reference
        evidence.append(record)
    return sorted(evidence, key=lambda record: (record["chapter"], record["candidate_id"]))


def _load_bounded_items(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("bounded generation approvals must be a JSON object")
    items = data.get("items", [])
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError("bounded generation approval items must be a JSON list of objects")
    return items


def main() -> None:
    candidates = load_scene_candidates(CANDIDATES_PATH)
    candidates = merge_candidates(candidates, _load_bounded_items(BOUNDED_APPROVALS_PATH))
    registry = load_registry(REGISTRY_PATH) if REGISTRY_PATH.exists() else []
    temporal_states = load_visual_timeline(TIMELINE_PATH) if TIMELINE_PATH.exists() else []
    chapters = [candidate["chapter"] for candidate in candidates if isinstance(candidate.get("chapter"), int)]
    performance_references = load_visual_references(chapters)
    evidence = build_visual_scene_evidence(candidates, registry, temporal_states, performance_references)
    text = json.dumps(evidence, indent=2, ensure_ascii=False) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print(f"visual scene evidence already current: {len(evidence)} scenes")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote visual scene evidence: {len(evidence)} scenes")


if __name__ == "__main__":
    main()
