from __future__ import annotations

from typing import Iterable

DEFAULT_REFERENCE_LIMIT = 3


def score_reference(reference: dict, character: str, framing_preference: str = "scene_appropriate") -> dict:
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
        if "above_waist" in tags:
            score += 20
            reasons.append("above-waist Greg continuity")
        if tags & {"full_body", "lower_body_visible"} and "above_waist" not in tags:
            score -= 30
            penalties.append("lower-body mismatch")

    return {
        "score": score,
        "reasons": reasons,
        "penalties": penalties,
    }


def _normalized_references(character_record: dict) -> list[dict]:
    references: list[dict] = []
    seen: set[str] = set()

    for asset in character_record.get("reference_assets", []):
        if not isinstance(asset, str) or not asset.strip() or asset in seen:
            continue
        seen.add(asset)
        references.append({
            "asset": asset,
            "status": "manual",
            "tags": ["curated"],
            "source": "manual",
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


def select_character_references(
    catalog: dict[str, dict],
    characters: Iterable[str],
    framing_preference: str = "scene_appropriate",
    limit_per_character: int = DEFAULT_REFERENCE_LIMIT,
) -> list[dict]:
    selected: list[dict] = []
    limit = max(limit_per_character, 0)
    for character in characters:
        character_record = catalog.get(character, {})
        scored: list[dict] = []
        for reference in _normalized_references(character_record):
            quality = score_reference(reference, character, framing_preference=framing_preference)
            scored.append({
                "character": character,
                **reference,
                **quality,
            })
        scored.sort(key=lambda item: (-item["score"], item.get("asset", "")))
        selected.extend(scored[:limit])
    return selected
