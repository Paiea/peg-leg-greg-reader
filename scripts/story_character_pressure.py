from __future__ import annotations

from copy import deepcopy
from difflib import SequenceMatcher
import re
from typing import Any


CHARACTER_PRESSURE_SCHEMA = "story_character_pressure/v1"
DEEP_TIERS = {"core", "recurring"}
KNOWN_TIERS = {"core", "recurring", "local", "extra"}


def _list(value: object, *, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{field} must be a list of nonempty strings")
    return [item.strip() for item in value]


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-z]", "", name.casefold())


def _edit_distance(left: str, right: str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    previous = list(range(len(right) + 1))
    for i, lchar in enumerate(left, start=1):
        current = [i]
        for j, rchar in enumerate(right, start=1):
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            substitution = previous[j - 1] + (lchar != rchar)
            current.append(min(insertion, deletion, substitution))
        previous = current
    return previous[-1]


def names_collide(left: str, right: str) -> bool:
    """Conservative warning heuristic for generated-name confusion.

    This is intentionally a warning, not a naming authority. It catches exact
    duplicates and high-similarity fantasy-name variants that are easy to read
    as the same person when encountered across a long manuscript.
    """
    a = _normalize_name(left)
    b = _normalize_name(right)
    if not a or not b:
        return False
    if a == b:
        return True
    if min(len(a), len(b)) >= 4 and _edit_distance(a, b) <= 1:
        return True
    ratio = SequenceMatcher(a=a, b=b).ratio()
    if min(len(a), len(b)) >= 5 and ratio >= 0.72:
        return True
    return False


def _normalize_character(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError("characters must be objects")
    character_id = str(item.get("id", "")).strip()
    name = str(item.get("name", "")).strip()
    if not character_id or not name:
        raise ValueError("each character requires id and name")
    tier = str(item.get("tier", "local")).strip() or "local"
    if tier not in KNOWN_TIERS:
        raise ValueError(f"unknown character tier: {tier}")

    return {
        "id": character_id,
        "name": name,
        "tier": tier,
        "want": str(item.get("want", "")).strip() or None,
        "off_camera_motion": _list(item.get("off_camera_motion"), field="off_camera_motion"),
        "competence": _list(item.get("competence"), field="competence"),
        "cost_or_limit": _list(item.get("cost_or_limit"), field="cost_or_limit"),
        "scene_vectors": _list(item.get("scene_vectors"), field="scene_vectors"),
        "relationship_specificity": _list(item.get("relationship_specificity"), field="relationship_specificity"),
        "voice_or_behavior_markers": _list(item.get("voice_or_behavior_markers"), field="voice_or_behavior_markers"),
        "private_information": _list(item.get("private_information"), field="private_information"),
        "time_changes": _list(item.get("time_changes"), field="time_changes"),
    }


def compile_character_pressure(region: dict[str, Any]) -> dict[str, Any]:
    """Compile derived cast pressure for one story region.

    The helper does not invent or promote character canon. It makes weak cast
    dependence, missing independent motion, and generated-name collisions
    visible before a long-form renderer silently duplicates function/voice.
    """
    if not isinstance(region, dict) or not str(region.get("id", "")).strip():
        raise ValueError("character pressure requires region id")

    characters = [_normalize_character(item) for item in region.get("characters", [])]
    active_roster = []
    for item in region.get("active_roster", []) or []:
        if not isinstance(item, dict):
            raise ValueError("active_roster entries must be objects")
        roster_id = str(item.get("id", "")).strip()
        roster_name = str(item.get("name", "")).strip()
        if not roster_id or not roster_name:
            raise ValueError("active_roster entries require id and name")
        active_roster.append({"id": roster_id, "name": roster_name})

    warnings: list[str] = []
    deep = [item for item in characters if item["tier"] in DEEP_TIERS]

    for character in deep:
        cid = character["id"]
        if not character["want"]:
            warnings.append(f"character_without_want:{cid}")
        if not character["off_camera_motion"]:
            warnings.append(f"character_without_off_camera_life:{cid}")
        if not character["scene_vectors"]:
            warnings.append(f"character_without_scene_agency:{cid}")
        if not character["competence"]:
            warnings.append(f"character_without_distinguishing_leverage:{cid}")
        if not character["cost_or_limit"]:
            warnings.append(f"character_without_cost_or_limit:{cid}")
        if not character["relationship_specificity"]:
            warnings.append(f"character_relationship_too_generic:{cid}")

    all_named = [{"id": item["id"], "name": item["name"]} for item in characters]
    known_ids = {item["id"] for item in all_named}
    all_named.extend(item for item in active_roster if item["id"] not in known_ids)

    for index, left in enumerate(all_named):
        for right in all_named[index + 1 :]:
            if left["id"] == right["id"]:
                continue
            if names_collide(left["name"], right["name"]):
                pair = sorted((left["id"], right["id"]))
                warning = f"name_similarity_collision:{pair[0]}:{pair[1]}"
                if warning not in warnings:
                    warnings.append(warning)

    deep_has_independent_motion = all(bool(item["off_camera_motion"]) for item in deep)
    deep_has_scene_agency = all(bool(item["scene_vectors"]) for item in deep)
    deep_has_leverage = all(bool(item["competence"]) for item in deep)
    deep_has_cost = all(bool(item["cost_or_limit"]) for item in deep)
    deep_has_relationship_specificity = all(bool(item["relationship_specificity"]) for item in deep)

    return {
        "schema": CHARACTER_PRESSURE_SCHEMA,
        "authority": "derived_pressure_only",
        "canon_write_authorized": False,
        "region_id": region["id"],
        "characters": characters,
        "active_roster": deepcopy(active_roster),
        "checks": {
            "core_cast_has_independent_motion": deep_has_independent_motion,
            "core_cast_has_scene_agency": deep_has_scene_agency,
            "core_cast_has_distinguishing_leverage": deep_has_leverage,
            "core_cast_has_cost_or_limit": deep_has_cost,
            "core_cast_has_relationship_specificity": deep_has_relationship_specificity,
        },
        "warnings": warnings,
        "questions": [
            "What does each recurring character want that would still matter if the protagonist left town?",
            "What is each recurring character doing off-camera while the protagonist works, heals, waits, or pursues another problem?",
            "Who can initiate a scene, create a problem, refuse access, solve part of the problem, or make the protagonist update rather than merely react?",
            "Which supporting character could plausibly solve this scene better than the protagonist, and what changes if they do?",
            "What competence, leverage, resource, obligation, blind spot, or cost makes this person behave differently from another cast member?",
            "How does this character behave differently with the protagonist than with at least one other person?",
            "If time passes, what changes in this character without the protagonist causing it?",
            "Are any generated names visually or phonetically similar enough to create long-form reader confusion?",
        ],
        "principles": [
            "Supporting characters are causal actors, not protagonist furniture.",
            "Greg or any lead should not own every good idea, solution, escalation, or interpretation.",
            "A recurring character should be able to improve, worsen, drift, ally, refuse, earn, lose, or reorganize life off-camera.",
            "Different characters should not be distinguished only by adjective, profession, or one verbal gimmick.",
            "Relationship voice is relational: the same person may behave differently with different people without becoming inconsistent.",
            "Names must be checked against the active roster before generation settles them; similarity warnings should trigger renaming early, before prose repetition makes the name sticky.",
            "Do not inflate one-scene extras into full biographies. Spend depth where recurrence and story leverage justify it.",
        ],
        "source": deepcopy(region),
    }
