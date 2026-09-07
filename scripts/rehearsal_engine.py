#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

ACTOR_SCHEMA = "rehearsal_actor_registry/v1"
DISCOVERY_KINDS = {
    "movement",
    "dialogue_expand",
    "dialogue_contract",
    "speaker_legibility",
    "voice",
    "interaction_timing",
    "blocking",
    "object_behavior",
    "relationship_behavior",
    "character_hypothesis",
    "visual_beat",
    "source_win",
}
PROVENANCE_CLASSES = {"observed", "inferred", "rehearsal_hypothesis", "promoted_tendency"}
LOCK_STATUSES = {"preserved", "quarantined", "violated"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_actor_registry(path: str | Path) -> dict:
    registry = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_actor_registry(registry)
    return registry


def validate_actor_registry(registry: dict) -> None:
    if not isinstance(registry, dict) or registry.get("schema") != ACTOR_SCHEMA:
        raise ValueError(f"actor registry schema must be {ACTOR_SCHEMA}")
    actors = registry.get("actors")
    if not isinstance(actors, list) or not actors:
        raise ValueError("actor registry requires at least one actor")

    seen_actor_ids: set[str] = set()
    seen_roles: set[str] = set()
    for actor in actors:
        if not isinstance(actor, dict):
            raise ValueError("actor records must be objects")
        actor_id = actor.get("actor_id")
        actor_name = actor.get("actor_name")
        role = actor.get("role")
        if not all(_nonempty(v) for v in (actor_id, actor_name, role)):
            raise ValueError("actor_id, actor_name, and role are required")
        if actor_id in seen_actor_ids:
            raise ValueError(f"duplicate actor_id: {actor_id}")
        if role in seen_roles:
            raise ValueError(f"duplicate role binding: {role}")
        seen_actor_ids.add(actor_id)
        seen_roles.add(role)

        anchors = actor.get("user_anchors", [])
        if not isinstance(anchors, list):
            raise ValueError("user_anchors must be a list")
        for anchor in anchors:
            if not isinstance(anchor, dict) or not _nonempty(anchor.get("value")):
                raise ValueError("user anchor value is required")
            if anchor.get("provenance") != "user_casting_anchor":
                raise ValueError("user anchor provenance must be user_casting_anchor")

        derived = actor.get("derived_interpretation", [])
        if not isinstance(derived, list):
            raise ValueError("derived_interpretation must be a list")
        for item in derived:
            if not isinstance(item, dict) or not _nonempty(item.get("value")) or not _nonempty(item.get("provenance")):
                raise ValueError("derived interpretation requires value and provenance")

        visual = actor.get("visual")
        if not isinstance(visual, dict):
            raise ValueError("visual state is required")
        if visual.get("status") not in {"candidate", "selected", "demoted", "archived"}:
            raise ValueError("invalid visual status")
        if visual.get("era_sensitive") is not True:
            raise ValueError("visual state must be era_sensitive")


def actor_for_role(registry: dict, role: str) -> dict:
    validate_actor_registry(registry)
    matches = [actor for actor in registry["actors"] if actor["role"] == role]
    if not matches:
        raise KeyError(role)
    return copy.deepcopy(matches[0])


def compile_actor_packet(
    actor: dict,
    *,
    scene_id: str,
    role_context: dict,
    promoted_tendencies: tuple[dict, ...] | list[dict] = (),
) -> dict:
    if not _nonempty(scene_id):
        raise ValueError("scene_id is required")
    if not isinstance(role_context, dict):
        raise ValueError("role_context must be an object")

    visual = copy.deepcopy(actor.get("visual", {}))
    scene_visual = role_context.get("visual_state")
    if scene_visual is not None:
        if not isinstance(scene_visual, dict):
            raise ValueError("visual_state must be an object")
        visual.update(copy.deepcopy(scene_visual))

    tendencies: list[dict] = []
    for item in promoted_tendencies:
        if not isinstance(item, dict) or not _nonempty(item.get("value")):
            raise ValueError("promoted tendency value is required")
        tendencies.append({
            "value": item["value"],
            "provenance": "promoted_tendency",
            "source": item.get("source"),
        })

    return {
        "schema": "rehearsal_actor_packet/v1",
        "scene_id": scene_id,
        "actor_id": actor["actor_id"],
        "actor_name": actor["actor_name"],
        "role": actor["role"],
        "instruction": "Play this person in this situation. Do not optimize for a clever line.",
        "user_anchors": copy.deepcopy(actor.get("user_anchors", [])),
        "derived_interpretation": copy.deepcopy(actor.get("derived_interpretation", [])),
        "promoted_tendencies": tendencies,
        "scene": {
            key: copy.deepcopy(role_context[key])
            for key in (
                "current_body_state",
                "relationship_context",
                "objective",
                "pressure",
                "domain_responsibility",
                "knowledge",
                "ignorance",
                "active_task",
            )
            if key in role_context
        },
        "visual_state": visual,
    }


def build_rehearsal_packet(scene: dict, dramatic_lock: dict, actor_packets: list[dict], baseline: dict | None = None) -> dict:
    if not isinstance(scene, dict) or not _nonempty(scene.get("scene_id")):
        raise ValueError("scene_id is required")
    if not isinstance(dramatic_lock, dict):
        raise ValueError("dramatic_lock must be an object")
    if not isinstance(actor_packets, list) or not actor_packets:
        raise ValueError("actor_packets are required")

    roles = [packet.get("role") for packet in actor_packets]
    if any(not _nonempty(role) for role in roles) or len(set(roles)) != len(roles):
        raise ValueError("rehearsal requires unique actor role ownership")

    return {
        "schema": "rehearsal_packet/v1",
        "scene_id": scene["scene_id"],
        "source_hash": scene.get("source", {}).get("hash"),
        "dramatic_lock": copy.deepcopy(dramatic_lock),
        "actors": copy.deepcopy(actor_packets),
        "faithful_baseline": copy.deepcopy(baseline) if baseline is not None else None,
        "freedom": {
            "locked": ["plot", "facts", "knowledge", "causality", "major_relationship_state", "physical_state"],
            "unlocked": ["dialogue_wording", "dialogue_amount", "tags", "paragraph_breaks", "movement", "blocking", "pauses", "silence", "interruptions", "object_handling", "local_exchange_shape"],
        },
        "director_instruction": "Preserve canon truth, not source choreography.",
    }


def validate_discovery(discovery: dict) -> None:
    if not isinstance(discovery, dict):
        raise ValueError("discovery must be an object")
    if not _nonempty(discovery.get("scene_id")):
        raise ValueError("discovery scene_id is required")
    if discovery.get("kind") not in DISCOVERY_KINDS:
        raise ValueError("invalid discovery kind")
    if not _nonempty(discovery.get("finding")):
        raise ValueError("discovery finding is required")
    if discovery.get("provenance_class") not in PROVENANCE_CLASSES:
        raise ValueError("invalid discovery provenance_class")
    if discovery.get("dramatic_lock_status") not in LOCK_STATUSES:
        raise ValueError("invalid dramatic_lock_status")
    support = discovery.get("support", [])
    if not isinstance(support, list):
        raise ValueError("discovery support must be a list")


def independent_support_count(evidence: list[dict]) -> int:
    if not isinstance(evidence, list):
        raise ValueError("evidence must be a list")
    independent: set[tuple[str, str]] = set()
    for item in evidence:
        if not isinstance(item, dict):
            raise ValueError("evidence entries must be objects")
        evidence_type = item.get("type")
        if evidence_type not in {"canon", "accepted_prose"}:
            continue
        source = item.get("source") or item.get("scene_id")
        if not _nonempty(source):
            raise ValueError("independent evidence requires source")
        independent.add((evidence_type, source))
    return len(independent)
