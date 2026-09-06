from __future__ import annotations

import re
from typing import Iterable

DEFAULT_REFERENCE_LIMIT = 3


def _context_terms(scene_context: dict | None) -> set[str]:
    if not scene_context:
        return set()
    terms = {
        str(tag).strip().lower()
        for tag in scene_context.get("scene_tags", [])
        if str(tag).strip()
    }
    for field in ("location", "mood"):
        value = scene_context.get(field, "")
        if isinstance(value, str):
            terms.update(token for token in re.findall(r"[a-z0-9_]+", value.lower()) if len(token) > 2)
    return terms


def score_reference(
    reference: dict,
    character: str,
    framing_preference: str = "scene_appropriate",
    scene_context: dict | None = None,
) -> dict:
    score = 0
    reasons: list[str] = []
    penalties: list[str] = []

    status = reference.get("status", "manual")
    if status == "live":
        score += 40
        reasons.append("live")
    elif status == "approved":
        score += 30
        reasons.append("approved")
    elif status == "manual":
        score += 30
        reasons.append("hand-curated")
    else:
        score -= 40
        penalties.append(f"non-production status: {status}")

    approved_fit = reference.get("approved_fit")
    if approved_fit == "exact":
        score += 25
        reasons.append("exact fit")
    elif approved_fit == "close_enough":
        score += 10
        reasons.append("close-enough fit")

    style_family = reference.get("style_family")
    if style_family == "sketch-ink-paint":
        score += 15
        reasons.append("PLG style")
    elif style_family == "legacy-import":
        penalties.append("legacy style")

    tags = {str(tag) for tag in reference.get("tags", [])}
    if "curated" in tags:
        score += 20
        reasons.append("hand-curated anchor")
    if "strong_face" in tags:
        score += 10
        reasons.append("strong face anchor")
    if "style_anchor" in tags:
        score += 8
        reasons.append("style anchor")

    if character == "Greg" and framing_preference == "above_waist":
        framing = reference.get("framing")
        if "above_waist" in tags or framing == "above_waist":
            score += 20
            reasons.append("above-waist Greg continuity")
        if (tags & {"full_body", "lower_body_visible"} or framing in {"full_body", "lower_body_visible"}) and "above_waist" not in tags:
            score -= 30
            penalties.append("lower-body mismatch")

    context_terms = _context_terms(scene_context)
    reference_scene_tags = {
        str(tag).strip().lower()
        for tag in reference.get("scene_tags", [])
        if str(tag).strip()
    }
    overlap = sorted(context_terms & reference_scene_tags)
    if overlap:
        score += min(20, 10 * len(overlap))
        reasons.append("scene context match")

    return {
        "score": score,
        "reasons": reasons,
        "penalties": penalties,
        "scene_matches": overlap,
    }


def _normalized_references(character_record: dict) -> list[dict]:
    references: list[dict] = []
    seen: set[str] = set()
    reference_metadata = character_record.get("reference_metadata", {})
    if not isinstance(reference_metadata, dict):
        reference_metadata = {}

    for asset in character_record.get("reference_assets", []):
        if not isinstance(asset, str) or not asset.strip() or asset in seen:
            continue
        seen.add(asset)
        metadata = reference_metadata.get(asset, {})
        if not isinstance(metadata, dict):
            metadata = {}
        tags = list(metadata.get("tags", []))
        if "curated" not in tags:
            tags.append("curated")
        references.append({
            "asset": asset,
            "status": "manual",
            "source": "manual",
            **metadata,
            "tags": tags,
        })

    for reference in character_record.get("references", []):
        if not isinstance(reference, dict):
            continue
        asset = reference.get("asset")
        if not isinstance(asset, str) or not asset.strip() or asset in seen:
            continue
        seen.add(asset)
        references.append(dict(reference))
    return references


def _diversity_adjustment(candidate: dict, selected: list[dict]) -> tuple[int, list[str]]:
    adjustment = 0
    notes: list[str] = []
    view_angle = candidate.get("view_angle")
    pose_family = candidate.get("pose_family")
    if view_angle and any(item.get("view_angle") == view_angle for item in selected):
        adjustment -= 20
        notes.append(f"repeat view angle: {view_angle}")
    if pose_family and any(item.get("pose_family") == pose_family for item in selected):
        adjustment -= 15
        notes.append(f"repeat pose family: {pose_family}")
    return adjustment, notes


def select_character_references(
    catalog: dict[str, dict],
    characters: Iterable[str],
    framing_preference: str = "scene_appropriate",
    limit_per_character: int = DEFAULT_REFERENCE_LIMIT,
    scene_context: dict | None = None,
    diversity_aware: bool = True,
) -> list[dict]:
    selected: list[dict] = []
    limit = max(limit_per_character, 0)
    for character in characters:
        character_record = catalog.get(character, {})
        remaining: list[dict] = []
        for reference in _normalized_references(character_record):
            quality = score_reference(
                reference,
                character,
                framing_preference=framing_preference,
                scene_context=scene_context,
            )
            remaining.append({
                "character": character,
                **reference,
                **quality,
            })

        character_selected: list[dict] = []
        while remaining and len(character_selected) < limit:
            ranked: list[tuple[int, str, dict, int, list[str]]] = []
            for candidate in remaining:
                diversity_adjustment, diversity_notes = (
                    _diversity_adjustment(candidate, character_selected)
                    if diversity_aware
                    else (0, [])
                )
                selection_score = candidate["score"] + diversity_adjustment
                ranked.append((
                    -selection_score,
                    candidate.get("asset", ""),
                    candidate,
                    diversity_adjustment,
                    diversity_notes,
                ))
            ranked.sort(key=lambda item: (item[0], item[1]))
            _, _, chosen, adjustment, notes = ranked[0]
            selected_record = dict(chosen)
            selected_record["diversity_adjustment"] = adjustment
            selected_record["diversity_notes"] = notes
            selected_record["selection_score"] = chosen["score"] + adjustment
            character_selected.append(selected_record)
            remaining = [item for item in remaining if item.get("asset") != chosen.get("asset")]
        selected.extend(character_selected)
    return selected
