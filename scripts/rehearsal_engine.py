#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path

ACTOR_SCHEMA = "rehearsal_actor_registry/v1"
RELATIONSHIP_MEMORY_SCHEMA = "rehearsal_relationship_memory/v1"
REHEARSAL_MODES = {"faithful", "free", "directed"}
GREG_PERFORMANCE_CHANNELS = ("body", "voice", "inner_voice")
NON_GREG_PERFORMANCE_CHANNELS = ("body", "voice", "private_inner_voice")
PRIVATE_PERFORMANCE_CHANNELS = {"inner_voice", "private_inner_voice"}
PERFORMED_INTERPRETATION_AUTHORITY = "performed_interpretation"
INNER_VOICE_FORMS = {
    "sentence",
    "fragment",
    "image",
    "memory_fragment",
    "association",
    "half_word",
    "impulse",
    "calculation",
    "wrong_inference",
    "sensory_hook",
    "unfinished_thought",
    "bodily_anticipation",
    "emotional_recoil",
    "recognition",
    "suppressed_joke",
    "self_correction",
    "strategic_branch",
}
SUPPORTED_MEMORY_SOURCE_TYPES = {"canon", "accepted_prose", "user_anchor", "promoted_tendency"}
HYPOTHESIS_MEMORY_SOURCE_TYPES = {"rehearsal"}
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
    "private_interpretation",
    "visual_beat",
    "source_win",
}
PROVENANCE_CLASSES = {"observed", "inferred", "rehearsal_hypothesis", "promoted_tendency"}
LOCK_STATUSES = {"preserved", "quarantined", "violated"}
SOFT_CANON_WRITE_SURFACES = {
    "dialogue",
    "dialogue_wording",
    "dialogue_amount",
    "tags",
    "paragraph_breaks",
    "paragraphing",
    "movement",
    "blocking",
    "pauses",
    "silence",
    "interruptions",
    "object_handling",
    "reaction_placement",
    "interaction_timing",
    "local_exchange_shape",
    "tone",
    "internal_dialogue",
    "narration_rhythm",
    "attention_order",
    "sensory_emphasis",
    "memory_intrusion",
}
HARD_CANON_SURFACES = {
    "plot",
    "facts",
    "knowledge",
    "causality",
    "major_relationship_state",
    "physical_state",
    "chronology",
    "economics",
    "earned_competence",
    "injury_state",
}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_rehearsal_mode(mode: str, direction: str | None) -> None:
    if mode not in REHEARSAL_MODES:
        raise ValueError(f"invalid rehearsal mode: {mode}")
    if mode == "directed" and not _nonempty(direction):
        raise ValueError("directed rehearsal requires direction")
    if mode != "directed" and direction is not None:
        raise ValueError("direction is only valid for directed rehearsal")


def editorial_return_policy(mode: str = "standard") -> dict:
    if mode == "standard":
        return {
            "mode": mode,
            "actor_preference_can_trigger_write": False,
            "branch_canon_write_authorized": False,
            "max_local_scope": "local_patch",
            "production_safe": True,
            "soft_surfaces": sorted(SOFT_CANON_WRITE_SURFACES),
            "hard_surfaces": sorted(HARD_CANON_SURFACES),
        }
    if mode == "production":
        return {
            "mode": mode,
            "actor_preference_can_trigger_write": True,
            "branch_canon_write_authorized": True,
            "max_local_scope": "scene_rebuild",
            "production_safe": True,
            "soft_surfaces": sorted(SOFT_CANON_WRITE_SURFACES),
            "hard_surfaces": sorted(HARD_CANON_SURFACES),
        }
    if mode == "overtuned_calibration":
        return {
            "mode": mode,
            "actor_preference_can_trigger_write": True,
            "branch_canon_write_authorized": True,
            "max_local_scope": "scene_rebuild",
            "production_safe": False,
            "soft_surfaces": sorted(SOFT_CANON_WRITE_SURFACES),
            "hard_surfaces": sorted(HARD_CANON_SURFACES),
        }
    raise ValueError(f"unknown editorial return mode: {mode}")


def can_auto_apply_rehearsal_candidate(candidate: dict, policy: dict) -> bool:
    if not isinstance(candidate, dict) or not isinstance(policy, dict):
        return False
    if not policy.get("branch_canon_write_authorized"):
        return False
    if not policy.get("actor_preference_can_trigger_write"):
        return False
    if candidate.get("actor_prefers") is not True:
        return False
    if candidate.get("dramatic_lock_status") != "preserved":
        return False
    if candidate.get("reader_check") != "pass":
        return False
    if candidate.get("source_match") is not True:
        return False
    target_branch = candidate.get("target_branch")
    if not _nonempty(target_branch) or target_branch == "main":
        return False
    changed_surfaces = candidate.get("changed_surfaces")
    if not isinstance(changed_surfaces, list) or not changed_surfaces:
        return False
    return set(changed_surfaces).issubset(SOFT_CANON_WRITE_SURFACES)


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


def relationship_memory_key(role: str, counterpart_role: str) -> str:
    if not _nonempty(role) or not _nonempty(counterpart_role):
        raise ValueError("relationship memory roles are required")
    return f"{role}::{counterpart_role}"


def validate_relationship_memory_registry(registry: dict) -> None:
    if not isinstance(registry, dict) or registry.get("schema") != RELATIONSHIP_MEMORY_SCHEMA:
        raise ValueError(f"relationship memory schema must be {RELATIONSHIP_MEMORY_SCHEMA}")
    relationships = registry.get("relationships")
    if not isinstance(relationships, dict):
        raise ValueError("relationship memory relationships must be an object")

    for key, record in relationships.items():
        if not _nonempty(key) or "::" not in key or not isinstance(record, dict):
            raise ValueError("relationship memory key must be directional role::counterpart")
        for lane in ("supported", "hypothesis"):
            entries = record.get(lane, [])
            if not isinstance(entries, list):
                raise ValueError(f"relationship memory {lane} lane must be a list")
            for entry in entries:
                if not isinstance(entry, dict):
                    raise ValueError(f"relationship memory {lane} entries must be objects")
                if not _nonempty(entry.get("value")) or not _nonempty(entry.get("source_type")) or not _nonempty(entry.get("source")):
                    raise ValueError(f"relationship memory {lane} entry requires value, source_type, and source")
                source_type = entry["source_type"]
                if lane == "supported" and source_type not in SUPPORTED_MEMORY_SOURCE_TYPES:
                    raise ValueError("supported relationship memory cannot use synthetic rehearsal evidence")
                if lane == "hypothesis" and source_type not in HYPOTHESIS_MEMORY_SOURCE_TYPES:
                    raise ValueError("hypothesis relationship memory must remain synthetic rehearsal evidence")


def relationship_memory_for(registry: dict, role: str, counterpart_roles: list[str]) -> dict:
    validate_relationship_memory_registry(registry)
    supported: list[dict] = []
    hypothesis: list[dict] = []
    for counterpart in counterpart_roles:
        key = relationship_memory_key(role, counterpart)
        record = registry["relationships"].get(key)
        if not record:
            continue
        supported.extend(copy.deepcopy(record.get("supported", [])))
        hypothesis.extend(copy.deepcopy(record.get("hypothesis", [])))
    if not supported and not hypothesis:
        return {}
    return {"supported": supported, "hypothesis": hypothesis}


def compile_actor_packet(
    actor: dict,
    *,
    scene_id: str,
    role_context: dict,
    promoted_tendencies: tuple[dict, ...] | list[dict] = (),
    relationship_memory: dict | None = None,
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

    role = actor["role"]
    actor_name = actor["actor_name"]
    channels = GREG_PERFORMANCE_CHANNELS if role == "Greg" and actor_name == "Nico" else NON_GREG_PERFORMANCE_CHANNELS

    packet = {
        "schema": "rehearsal_actor_packet/v1",
        "scene_id": scene_id,
        "actor_id": actor["actor_id"],
        "actor_name": actor_name,
        "role": role,
        "instruction": "Play this person in this situation. Do not optimize for a clever line.",
        "performance_channels": list(channels),
        "private_interpretation_authority": PERFORMED_INTERPRETATION_AUTHORITY,
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
    if relationship_memory:
        if not isinstance(relationship_memory, dict):
            raise ValueError("relationship_memory must be an object")
        packet["relationship_memory"] = copy.deepcopy(relationship_memory)
    return packet


def build_rehearsal_packet(
    scene: dict,
    dramatic_lock: dict,
    actor_packets: list[dict],
    baseline: dict | None = None,
    *,
    mode: str = "free",
    direction: str | None = None,
    take_id: str | None = None,
    variance_group_id: str | None = None,
    memory_snapshot_id: str | None = None,
) -> dict:
    if not isinstance(scene, dict) or not _nonempty(scene.get("scene_id")):
        raise ValueError("scene_id is required")
    if not isinstance(dramatic_lock, dict):
        raise ValueError("dramatic_lock must be an object")
    if not isinstance(actor_packets, list) or not actor_packets:
        raise ValueError("actor_packets are required")
    _validate_rehearsal_mode(mode, direction)

    roles = [packet.get("role") for packet in actor_packets]
    if any(not _nonempty(role) for role in roles) or len(set(roles)) != len(roles):
        raise ValueError("rehearsal requires unique actor role ownership")

    return {
        "schema": "rehearsal_packet/v1",
        "scene_id": scene["scene_id"],
        "source_hash": scene.get("source", {}).get("hash"),
        "mode": mode,
        "direction": direction,
        "take_id": take_id,
        "variance_group_id": variance_group_id,
        "memory_snapshot_id": memory_snapshot_id,
        "dramatic_lock": copy.deepcopy(dramatic_lock),
        "actors": copy.deepcopy(actor_packets),
        "faithful_baseline": copy.deepcopy(baseline) if baseline is not None else None,
        "freedom": {
            "locked": ["plot", "facts", "knowledge", "causality", "major_relationship_state", "physical_state"],
            "unlocked": ["dialogue_wording", "dialogue_amount", "tags", "paragraph_breaks", "movement", "blocking", "pauses", "silence", "interruptions", "object_handling", "local_exchange_shape", "tone"],
        },
        "director_instruction": "Preserve canon truth, not source choreography.",
    }


def _allowed_knowledge(actor_packet: dict | None) -> set[str] | None:
    if actor_packet is None:
        return None
    knowledge = actor_packet.get("scene", {}).get("knowledge")
    if knowledge is None:
        return set()
    if isinstance(knowledge, list):
        return {item for item in knowledge if isinstance(item, str)}
    if isinstance(knowledge, dict):
        allowed = {str(key) for key in knowledge.keys()}
        allowed.update(value for value in knowledge.values() if isinstance(value, str))
        return allowed
    if isinstance(knowledge, str):
        return {knowledge}
    raise ValueError("actor packet knowledge must be a string, list, or object")


def validate_performance_output(output: dict, *, actor_packet: dict | None = None) -> None:
    if not isinstance(output, dict):
        raise ValueError("performance output must be an object")
    role = output.get("role")
    actor_name = output.get("actor_name")
    if not _nonempty(role) or not _nonempty(actor_name):
        raise ValueError("performance output requires actor_name and role")

    for channel in ("body", "voice"):
        value = output.get(channel, [])
        if not isinstance(value, list):
            raise ValueError(f"{channel} performance channel must be a list")

    if "inner_voice" in output and "private_inner_voice" in output:
        raise ValueError("performance output cannot contain both inner voice channels")
    if role == "Greg" and "private_inner_voice" in output:
        raise ValueError("Greg uses inner_voice, not private_inner_voice")
    if role != "Greg" and "inner_voice" in output:
        raise ValueError("non-Greg actors use private_inner_voice")

    private_channel = "inner_voice" if role == "Greg" else "private_inner_voice"
    private_events = output.get(private_channel, [])
    if not isinstance(private_events, list):
        raise ValueError(f"{private_channel} must be a list")

    allowed_knowledge = _allowed_knowledge(actor_packet)
    for event in private_events:
        if not isinstance(event, dict):
            raise ValueError("private inner performance events must be objects")
        if event.get("form") not in INNER_VOICE_FORMS:
            raise ValueError("invalid private inner performance form")
        if not _nonempty(event.get("value")):
            raise ValueError("private inner performance value is required")
        if event.get("authority") != PERFORMED_INTERPRETATION_AUTHORITY:
            raise ValueError("private inner performance must be a performed_interpretation")
        uses_knowledge = event.get("uses_knowledge", [])
        if not isinstance(uses_knowledge, list):
            raise ValueError("uses_knowledge must be a list")
        if allowed_knowledge is not None:
            unsupported = [item for item in uses_knowledge if item not in allowed_knowledge]
            if unsupported:
                raise ValueError(f"unsupported knowledge in private performance: {unsupported[0]}")

    observed_inputs = output.get("observed_inputs", [])
    if not isinstance(observed_inputs, list):
        raise ValueError("observed_inputs must be a list")
    for observed in observed_inputs:
        if not isinstance(observed, dict):
            raise ValueError("observed input must be an object")
        if observed.get("source_channel") in PRIVATE_PERFORMANCE_CHANNELS:
            raise ValueError("actor cannot observe another actor's private channel")


def actor_observable_view(output: dict, *, observer_role: str) -> dict:
    if not isinstance(output, dict) or not _nonempty(observer_role):
        raise ValueError("observable view requires output and observer_role")
    return {
        key: copy.deepcopy(output[key])
        for key in ("actor_name", "role", "body", "voice")
        if key in output
    }


def novelizer_performance_view(output: dict) -> dict:
    if not isinstance(output, dict):
        raise ValueError("novelizer performance view requires output")
    keys = ["actor_name", "role", "body", "voice"]
    if output.get("role") == "Greg" and "inner_voice" in output:
        keys.append("inner_voice")
    return {key: copy.deepcopy(output[key]) for key in keys if key in output}


def build_take_spec(
    mode: str,
    *,
    take_id: str,
    memory_snapshot_id: str,
    direction: str | None = None,
    variance_group_id: str | None = None,
) -> dict:
    _validate_rehearsal_mode(mode, direction)
    if not _nonempty(take_id):
        raise ValueError("take_id is required")
    if not _nonempty(memory_snapshot_id):
        raise ValueError("memory_snapshot_id is required")
    return {
        "mode": mode,
        "take_id": take_id,
        "variance_group_id": variance_group_id,
        "memory_snapshot_id": memory_snapshot_id,
        "direction": direction,
    }


def validate_variance_group(takes: list[dict]) -> None:
    if not isinstance(takes, list) or not takes:
        raise ValueError("variance group requires takes")
    for take in takes:
        if not isinstance(take, dict):
            raise ValueError("variance takes must be objects")
        if any(key in take for key in ("sibling_take_context", "sibling_outputs", "sibling_findings")):
            raise ValueError("variance take cannot contain sibling context or output")
        _validate_rehearsal_mode(take.get("mode"), take.get("direction"))
        if not _nonempty(take.get("take_id")):
            raise ValueError("variance take_id is required")
        if not _nonempty(take.get("variance_group_id")):
            raise ValueError("variance_group_id is required")
        if not _nonempty(take.get("memory_snapshot_id")):
            raise ValueError("variance memory snapshot is required")

    group_ids = {take["variance_group_id"] for take in takes}
    if len(group_ids) != 1:
        raise ValueError("variance takes must share one variance_group_id")
    snapshots = {take["memory_snapshot_id"] for take in takes}
    if len(snapshots) != 1:
        raise ValueError("variance siblings must share one frozen memory snapshot")
    take_ids = [take["take_id"] for take in takes]
    if len(take_ids) != len(set(take_ids)):
        raise ValueError("variance take_id values must be unique")


def stable_variance_findings(takes: list[dict]) -> list[dict]:
    validate_variance_group(takes)
    counts: Counter[str] = Counter()
    for take in takes:
        findings = take.get("observable_findings", [])
        if not isinstance(findings, list):
            raise ValueError("observable_findings must be a list")
        counts.update({finding for finding in findings if _nonempty(finding)})
    return [
        {"finding": finding, "support_count": count, "authority": "rehearsal_evidence"}
        for finding, count in sorted(counts.items())
        if count >= 2
    ]


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
