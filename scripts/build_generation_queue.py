from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_illustration_backlog import count_chapter_images
from scripts.illustration_edit_hold import edit_hold_active, load_hold
from scripts.illustration_state import load_registry, load_scene_candidates
from scripts.performance_roundtrip_references import load_visual_references, normalize_text
from scripts.score_character_references import select_character_references

CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
CHARACTER_REFERENCES_PATH = ROOT / "state" / "visual" / "CHARACTER_VISUAL_REFERENCES.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "GENERATION_QUEUE.json"
CHAPTER_DIR = ROOT / "chapters"
ACTIVE_STATUSES = {"generated", "approved", "live"}
VERSION_RE = re.compile(r"-v(\d+)$")
DEFAULT_STYLE_FAMILY = "sketch-ink-paint"
DEFAULT_GREG_FRAMING = "above_waist"
DEFAULT_GREG_CONTINUITY = (
    "Keep style consistent with accepted PLG artwork. Prefer above-waist Greg framing and avoid unnecessary lower-body visibility "
    "unless the manuscript moment materially requires it. Match recurring characters to supplied reference assets and appearance notes."
)


def _next_version(candidate_id: str, registry: list[dict]) -> int:
    versions = []
    for record in registry:
        if record.get("candidate_id") != candidate_id:
            continue
        match = VERSION_RE.search(str(record.get("id", "")))
        if match:
            versions.append(int(match.group(1)))
    return max(versions, default=0) + 1


def _appearance_notes(characters: list[str], character_references: dict[str, dict]) -> dict[str, str]:
    notes: dict[str, str] = {}
    for character in characters:
        value = character_references.get(character, {}).get("appearance_notes", "")
        if isinstance(value, str) and value.strip():
            notes[character] = value.strip()
    return notes


def _reference_selection_notes(selected: list[dict]) -> str:
    if not selected:
        return "No visual reference asset selected; use written appearance notes and manuscript evidence."
    parts: list[str] = []
    for reference in selected:
        reasons = ", ".join(reference.get("reasons", [])) or "baseline reference"
        penalties = list(reference.get("penalties", [])) + list(reference.get("diversity_notes", []))
        suffix = f"; penalties/selection notes: {', '.join(penalties)}" if penalties else ""
        selection_score = reference.get("selection_score", reference.get("score", 0))
        parts.append(
            f"{reference.get('character', '')}: {reference.get('asset', '')} "
            f"(base {reference.get('score', 0)}, selected {selection_score}; {reasons}{suffix})"
        )
    return " | ".join(parts)


def _performance_reference_for_candidate(candidate: dict, performance_references: dict[int, dict]) -> dict | None:
    reference = performance_references.get(candidate.get("chapter"))
    if not reference:
        return None
    candidate_anchor = candidate.get("paragraph_anchor")
    scene_anchors = reference.get("scene_anchors")
    if not isinstance(candidate_anchor, str) or not candidate_anchor.strip():
        return None
    if not isinstance(scene_anchors, list) or not scene_anchors:
        return None
    normalized_candidate = normalize_text(candidate_anchor)
    normalized_scene_anchors = {
        normalize_text(anchor)
        for anchor in scene_anchors
        if isinstance(anchor, str) and anchor.strip()
    }
    if normalized_candidate not in normalized_scene_anchors:
        return None
    return reference


def build_generation_queue(
    candidates: list[dict],
    registry: list[dict],
    chapter_image_counts: dict[int, int] | None = None,
    character_references: dict[str, dict] | None = None,
    production_hold: dict | None = None,
    performance_references: dict[int, dict] | None = None,
) -> list[dict]:
    if edit_hold_active(production_hold):
        return []

    character_references = character_references or {}
    performance_references = performance_references or {}
    active = {
        record.get("candidate_id")
        for record in registry
        if record.get("status") in ACTIVE_STATUSES
    }
    queue: list[dict] = []
    for candidate in candidates:
        if (
            candidate.get("status") != "prompt_ready"
            or candidate.get("anchor_blocked")
            or candidate.get("candidate_id") in active
            or candidate.get("id") in active
        ):
            continue
        candidate_id = candidate["id"]
        if candidate_id in active:
            continue
        version = _next_version(candidate_id, registry)
        target_asset = f"visual/chapter_art/{candidate['chapter']:03d}/{candidate_id}-v{version}.webp"
        coverage_before = chapter_image_counts.get(candidate["chapter"], 0) if chapter_image_counts is not None else None
        characters = list(candidate.get("characters", []))
        greg_in_frame = "Greg" in characters
        framing_preference = candidate.get("framing_preference") or (DEFAULT_GREG_FRAMING if greg_in_frame else "scene_appropriate")
        continuity_notes = candidate.get("continuity_notes") or (
            DEFAULT_GREG_CONTINUITY
            if greg_in_frame
            else "Match recurring characters to supplied reference assets and appearance notes while preserving the shared PLG visual language."
        )
        scene_tags = list(candidate.get("scene_tags", []))
        scene_context = {
            "location": candidate.get("location", ""),
            "mood": candidate.get("mood", ""),
            "scene_tags": scene_tags,
        }
        selected_references = select_character_references(
            character_references,
            characters,
            framing_preference=framing_preference,
            scene_context=scene_context,
            diversity_aware=True,
        )
        character_assets = [reference["asset"] for reference in selected_references]
        character_notes = _appearance_notes(characters, character_references)
        record = {
            "candidate_id": candidate_id,
            "chapter": candidate["chapter"],
            "chapter_title": candidate["chapter_title"],
            "kind": candidate["kind"],
            "priority": candidate["priority"],
            "fit_target": candidate["fit_target"],
            "spoiler_level": candidate["spoiler_level"],
            "scene_summary": candidate["scene_summary"],
            "visual_hook": candidate["visual_hook"],
            "characters": characters,
            "location": candidate.get("location", ""),
            "mood": candidate.get("mood", ""),
            "scene_tags": scene_tags,
            "style_family": candidate.get("style_family", DEFAULT_STYLE_FAMILY),
            "framing_preference": framing_preference,
            "camera_angle": candidate.get("camera_angle", ""),
            "pose_family": candidate.get("pose_family", ""),
            "character_reference_assets": character_assets,
            "selected_character_references": selected_references,
            "character_reference_scores": {
                reference["asset"]: reference["selection_score"] for reference in selected_references
            },
            "reference_selection_notes": _reference_selection_notes(selected_references),
            "character_appearance_notes": character_notes,
            "continuity_notes": continuity_notes,
            "prompt_pack": f"state/visual/prompt-packs/{candidate_id}.md",
            "paragraph_anchor": candidate.get("paragraph_anchor", ""),
            "anchor_status": candidate.get("anchor_status", ""),
            "target_asset": target_asset,
            "coverage_before": coverage_before,
            "status": "generation_ready",
        }
        performance_reference = _performance_reference_for_candidate(candidate, performance_references)
        if performance_reference:
            record["performance_reference"] = performance_reference
        queue.append(record)
    rank = {"high": 0, "medium": 1, "low": 2}

    def sort_key(record: dict) -> tuple:
        coverage = record.get("coverage_before")
        coverage_rank = coverage if isinstance(coverage, int) else 999
        return (coverage_rank, rank.get(record["priority"], 9), record["chapter"], record["candidate_id"])

    return sorted(queue, key=sort_key)


def main() -> None:
    candidates = load_scene_candidates(CANDIDATES_PATH)
    registry = load_registry(REGISTRY_PATH)
    image_counts = count_chapter_images(CHAPTER_DIR)
    character_references = json.loads(CHARACTER_REFERENCES_PATH.read_text(encoding="utf-8")) if CHARACTER_REFERENCES_PATH.exists() else {}
    if not isinstance(character_references, dict):
        raise ValueError("character visual references must be a JSON object")
    performance_references = load_visual_references(
        int(candidate["chapter"])
        for candidate in candidates
        if isinstance(candidate.get("chapter"), int)
    )
    production_hold = load_hold()
    queue = build_generation_queue(
        candidates,
        registry,
        chapter_image_counts=image_counts,
        character_references=character_references,
        production_hold=production_hold,
        performance_references=performance_references,
    )
    text = json.dumps(queue, indent=2, ensure_ascii=False) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        if edit_hold_active(production_hold):
            print("generation queue already current: structural-edit hold active; 0 ready")
        else:
            print(f"generation queue already current: {len(queue)} ready")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    if edit_hold_active(production_hold):
        print("wrote generation queue: structural-edit hold active; 0 ready")
    else:
        print(f"wrote generation queue: {len(queue)} ready")


if __name__ == "__main__":
    main()
