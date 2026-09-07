#!/usr/bin/env python3
from __future__ import annotations

import copy
from typing import Any

from scripts import story_sync_engine as story_sync

RUNTIME_SCHEMA = "persistent_act_runtime/v1"
ACT_STATE_SCHEMA = "persistent_act_state/v1"
SHARED_STATE_SCHEMA = "persistent_shared_story_state/v1"
DELTA_SCHEMA = "persistent_act_delta/v1"

ACT_IDS = ("act-i", "act-ii", "act-iii", "act-iv")
ACT_INDEX = {act_id: index for index, act_id in enumerate(ACT_IDS)}
MESSAGE_KINDS = {"forward_consequence", "backward_requirement"}
MESSAGE_STATUSES = {"open", "closed", "rejected"}
CONSTRAINT_RESPONSES = {"supported", "conflict", "third_path", "reject_source", "untested"}
DELTA_TYPES = {
    "local_possibility",
    "local_discovery",
    "local_unresolved_question",
    "state_in_hypothesis",
    "state_out_hypothesis",
    "forward_consequence",
    "backward_requirement",
    "constraint_response",
    "cross_direction_agreement",
    "shared_discovery",
}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _confidence(value: object, *, field: str = "confidence") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be between 0 and 1")
    result = float(value)
    if not 0 <= result <= 1:
        raise ValueError(f"{field} must be between 0 and 1")
    return result


def _string_list(value: object, *, field: str, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    if not allow_empty and not value:
        raise ValueError(f"{field} requires at least one value")
    if any(not _nonempty(item) for item in value):
        raise ValueError(f"{field} values must be nonempty strings")
    return list(value)


def _validate_boundary(boundary: dict[str, Any], *, field: str) -> None:
    if not isinstance(boundary, dict):
        raise ValueError(f"{field} boundary must be an object")
    for key in ("id", "dimension"):
        if not _nonempty(boundary.get(key)):
            raise ValueError(f"{field} boundary requires {key}")
    if "value" not in boundary:
        raise ValueError(f"{field} boundary requires value")
    _confidence(boundary.get("confidence", 0.5), field=f"{field} boundary confidence")
    _string_list(boundary.get("provenance", []), field=f"{field} boundary provenance")


def _validate_local_state(local_state: dict[str, Any], *, act_id: str) -> None:
    if not isinstance(local_state, dict):
        raise ValueError(f"{act_id} local_state must be an object")
    for field in ("possibilities", "discoveries", "unresolved_questions", "constraint_responses"):
        if not isinstance(local_state.get(field), list):
            raise ValueError(f"{act_id} local_state requires {field} list")
    for response in local_state.get("constraint_responses", []):
        if not isinstance(response, dict) or not _nonempty(response.get("message_id")):
            raise ValueError(f"{act_id} constraint response requires message_id")
        if response.get("response") not in CONSTRAINT_RESPONSES:
            raise ValueError(f"{act_id} invalid constraint response")
        if not _nonempty(response.get("reason")):
            raise ValueError(f"{act_id} constraint response requires reason")


def _validate_act_state(act_id: str, state: dict[str, Any]) -> None:
    if not isinstance(state, dict):
        raise ValueError(f"{act_id} state must be an object")
    for field in ("state_in", "state_out"):
        if field not in state:
            raise ValueError(f"{act_id} requires {field}")
        if not isinstance(state[field], list):
            raise ValueError(f"{act_id} {field} must be a list")
        for item in state[field]:
            _validate_boundary(item, field=f"{act_id} {field}")
    if "local_state" not in state:
        raise ValueError(f"{act_id} requires local_state")
    _validate_local_state(state["local_state"], act_id=act_id)


def _validate_message(message: dict[str, Any], *, expected_kind: str | None = None) -> None:
    if not isinstance(message, dict):
        raise ValueError("shared message must be an object")
    for field in ("id", "kind", "source_act", "target_act", "statement"):
        if not _nonempty(message.get(field)):
            raise ValueError(f"shared message requires {field}")
    if message["kind"] not in MESSAGE_KINDS:
        raise ValueError("invalid shared message kind")
    if expected_kind is not None and message["kind"] != expected_kind:
        raise ValueError(f"message kind must be {expected_kind}")
    if message["source_act"] not in ACT_INDEX or message["target_act"] not in ACT_INDEX:
        raise ValueError("shared message source/target must be persistent acts")
    if message["source_act"] == message["target_act"]:
        raise ValueError("shared message must cross act boundaries")
    if message["kind"] == "forward_consequence" and ACT_INDEX[message["source_act"]] >= ACT_INDEX[message["target_act"]]:
        raise ValueError("forward consequence must point later in the trajectory")
    if message["kind"] == "backward_requirement" and ACT_INDEX[message["source_act"]] <= ACT_INDEX[message["target_act"]]:
        raise ValueError("backward requirement must point earlier in the trajectory")
    _confidence(message.get("confidence", 0.5), field="message confidence")
    _string_list(message.get("provenance", []), field="message provenance")
    if message.get("status", "open") not in MESSAGE_STATUSES:
        raise ValueError("invalid message status")


def _validate_agreement(agreement: dict[str, Any]) -> None:
    if not isinstance(agreement, dict) or not _nonempty(agreement.get("id")) or not _nonempty(agreement.get("statement")):
        raise ValueError("cross-direction agreement requires id and statement")
    acts = _string_list(agreement.get("acts", []), field="cross-direction agreement acts", allow_empty=False)
    if len(set(acts)) < 2 or any(act_id not in ACT_INDEX for act_id in acts):
        raise ValueError("cross-direction agreement requires at least two persistent acts")
    _confidence(agreement.get("confidence", 0.5), field="cross-direction agreement confidence")
    _string_list(agreement.get("provenance", []), field="cross-direction agreement provenance")


def validate_runtime(runtime: dict[str, Any]) -> None:
    if not isinstance(runtime, dict) or runtime.get("schema") != RUNTIME_SCHEMA:
        raise ValueError(f"runtime schema must be {RUNTIME_SCHEMA}")
    if not _nonempty(runtime.get("story_id")):
        raise ValueError("runtime requires story_id")

    acts = runtime.get("acts")
    if not isinstance(acts, dict) or tuple(acts.keys()) != ACT_IDS:
        if not isinstance(acts, dict) or set(acts.keys()) != set(ACT_IDS):
            raise ValueError("runtime requires four persistent act channels: act-i, act-ii, act-iii, act-iv")
    if set(acts.keys()) != set(ACT_IDS):
        raise ValueError("runtime requires four persistent act channels: act-i, act-ii, act-iii, act-iv")
    for act_id in ACT_IDS:
        _validate_act_state(act_id, acts[act_id])

    shared = runtime.get("shared_story_state")
    if not isinstance(shared, dict):
        raise ValueError("runtime requires shared_story_state")
    sync_state = shared.get("sync_state")
    story_sync.validate_sync_state(sync_state)
    for collection, kind in (("forward_consequences", "forward_consequence"), ("backward_requirements", "backward_requirement")):
        if not isinstance(shared.get(collection), list):
            raise ValueError(f"shared_story_state requires {collection} list")
        for item in shared[collection]:
            _validate_message(item, expected_kind=kind)
    if not isinstance(shared.get("cross_direction_agreements", []), list):
        raise ValueError("cross_direction_agreements must be a list")
    for item in shared.get("cross_direction_agreements", []):
        _validate_agreement(item)
    if not isinstance(shared.get("contradictions", []), list):
        raise ValueError("shared contradictions must be a list")


def sync_shared_story(runtime: dict[str, Any]) -> dict[str, Any]:
    """Delegate shared discovery maturity to the existing STORY SYNC authority."""
    validate_runtime(runtime)
    return story_sync.sync_story(copy.deepcopy(runtime["shared_story_state"]["sync_state"]))


def boundary_contradictions(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    """Surface explicit adjacent STATE OUT / STATE IN disagreements.

    Deterministic code compares only hypotheses that share a declared dimension. It does
    not attempt semantic contradiction detection from prose.
    """
    validate_runtime(runtime)
    conflicts: list[dict[str, Any]] = []
    for index in range(len(ACT_IDS) - 1):
        source_act = ACT_IDS[index]
        target_act = ACT_IDS[index + 1]
        source_items = runtime["acts"][source_act]["state_out"]
        target_items = runtime["acts"][target_act]["state_in"]
        for source in source_items:
            for target in target_items:
                if source["dimension"] != target["dimension"]:
                    continue
                if source.get("value") == target.get("value"):
                    continue
                conflicts.append({
                    "id": f"boundary:{source_act}:{target_act}:{source['dimension']}:{source['id']}:{target['id']}",
                    "kind": "boundary_contradiction",
                    "source_act": source_act,
                    "target_act": target_act,
                    "dimension": source["dimension"],
                    "source_value": copy.deepcopy(source.get("value")),
                    "target_value": copy.deepcopy(target.get("value")),
                    "source_boundary_id": source["id"],
                    "target_boundary_id": target["id"],
                    "confidence": min(float(source.get("confidence", 0.5)), float(target.get("confidence", 0.5))),
                    "reason": "adjacent temporal boundary beliefs disagree; test a lived bridge rather than smoothing the transition",
                })
    return conflicts


def _all_messages(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    shared = runtime["shared_story_state"]
    return list(shared.get("forward_consequences", [])) + list(shared.get("backward_requirements", []))


def _responses_for(runtime: dict[str, Any], message_id: str, target_act: str) -> list[dict[str, Any]]:
    return [
        item
        for item in runtime["acts"][target_act]["local_state"].get("constraint_responses", [])
        if item.get("message_id") == message_id
    ]


def constraint_closure(runtime: dict[str, Any]) -> dict[str, Any]:
    validate_runtime(runtime)
    messages: list[dict[str, Any]] = []
    collisions: list[dict[str, Any]] = []

    for message in _all_messages(runtime):
        responses = _responses_for(runtime, message["id"], message["target_act"])
        if message.get("status", "open") == "closed":
            closure_status = "closed"
        elif message.get("status") == "rejected":
            closure_status = "reject_source"
        elif responses:
            closure_status = responses[-1]["response"]
        else:
            closure_status = "untested"
        record = {
            "id": message["id"],
            "kind": message["kind"],
            "source_act": message["source_act"],
            "target_act": message["target_act"],
            "closure_status": closure_status,
            "statement": message["statement"],
            "confidence": float(message.get("confidence", 0.5)),
            "responses": copy.deepcopy(responses),
        }
        messages.append(record)
        if closure_status in {"conflict", "reject_source", "third_path"}:
            collisions.append({
                "message_id": message["id"],
                "source_act": message["source_act"],
                "target_act": message["target_act"],
                "status": closure_status,
                "reason": responses[-1]["reason"] if responses else "constraint requires cross-act resolution",
            })

    rehearsal_targets = [
        {
            "kind": "behavioral_bridge",
            "source_id": item["id"],
            "source_act": item["source_act"],
            "target_act": item["target_act"],
            "dimension": item["dimension"],
            "heat": "high" if any(token in item["dimension"].lower() for token in ("trust", "relationship", "romantic", "loyal", "fear")) else "medium",
            "reason": "REHEARSE whether actors can naturally traverse these boundary states under pressure; do not interpolate the change abstractly",
        }
        for item in boundary_contradictions(runtime)
    ]

    return {
        "messages": messages,
        "constraint_collisions": collisions,
        "boundary_contradictions": boundary_contradictions(runtime),
        "rehearsal_targets": rehearsal_targets,
    }


def temporal_consistency(runtime: dict[str, Any]) -> dict[str, Any]:
    validate_runtime(runtime)
    boundaries = boundary_contradictions(runtime)
    closure = constraint_closure(runtime)
    open_messages = [
        item for item in _all_messages(runtime)
        if item.get("status", "open") != "closed"
    ]
    unresolved_messages = [
        item for item in closure["messages"]
        if item["closure_status"] not in {"closed", "supported"}
    ]
    pressure = len(boundaries) + len(unresolved_messages) + len(closure["constraint_collisions"])
    return {
        "adjacent_boundary_pairs": len(ACT_IDS) - 1,
        "boundary_contradiction_count": len(boundaries),
        "open_long_range_messages": len(open_messages),
        "unresolved_message_count": len(unresolved_messages),
        "constraint_collision_count": len(closure["constraint_collisions"]),
        "open_pressure_count": pressure,
        "trajectory_status": "candidate_passable" if pressure == 0 else "open",
        "policy": "temporal_consistency_is_evidence_of_convergence_not_story_authority",
    }


def schedule_work(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a non-starving scheduling surface plus evidence-driven bonus work."""
    validate_runtime(runtime)
    work: list[dict[str, Any]] = [
        {
            "kind": "baseline_local_search",
            "act": act_id,
            "budget": 1,
            "priority": "baseline",
            "reason": "persistent temporal-slab experiment guarantees every act continued local search",
        }
        for act_id in ACT_IDS
    ]

    closure = constraint_closure(runtime)
    for bridge in closure["rehearsal_targets"]:
        work.append({
            "kind": "boundary_rehearsal",
            "act": bridge["target_act"],
            "acts": [bridge["source_act"], bridge["target_act"]],
            "source_id": bridge["source_id"],
            "budget": 3 if bridge["heat"] == "high" else 2,
            "priority": bridge["heat"],
            "reason": bridge["reason"],
        })

    for collision in closure["constraint_collisions"]:
        work.append({
            "kind": "constraint_collision",
            "act": collision["target_act"],
            "acts": [collision["source_act"], collision["target_act"]],
            "source_id": collision["message_id"],
            "budget": 3,
            "priority": "high",
            "reason": "cross-act requirement conflicts with accumulated local reality; test which side should adapt or whether a third path emerges",
        })

    for agreement in runtime["shared_story_state"].get("cross_direction_agreements", []):
        work.append({
            "kind": "cross_direction_agreement",
            "acts": copy.deepcopy(agreement["acts"]),
            "source_id": agreement["id"],
            "budget": 2,
            "priority": "medium",
            "reason": "independent temporal regions support compatible structure; pressure-test the thread before promotion",
        })

    sync_report = sync_shared_story(runtime)
    for target in sync_report.get("rehearsal_targets", []):
        regions = [region for region in target.get("regions", []) if region in ACT_INDEX]
        if not regions:
            continue
        heat = target.get("heat", "medium")
        work.append({
            "kind": "story_sync_rehearsal",
            "act": regions[0],
            "acts": regions,
            "source_id": target.get("source_id"),
            "budget": 3 if heat == "high" else 2,
            "priority": heat,
            "reason": target.get("reason", "STORY SYNC requested additional evidence"),
        })

    return work


def compile_act_packet(runtime: dict[str, Any], act_id: str) -> dict[str, Any]:
    validate_runtime(runtime)
    if act_id not in ACT_INDEX:
        raise ValueError("act_id must identify one of the four persistent act channels")
    act = runtime["acts"][act_id]
    shared_report = sync_shared_story(runtime)
    messages = _all_messages(runtime)
    return {
        "schema": "persistent_act_packet/v1",
        "story_id": runtime["story_id"],
        "act_id": act_id,
        "state_in": copy.deepcopy(act["state_in"]),
        "local_state": copy.deepcopy(act["local_state"]),
        "state_out": copy.deepcopy(act["state_out"]),
        "incoming_forward_consequences": [copy.deepcopy(item) for item in messages if item["kind"] == "forward_consequence" and item["target_act"] == act_id],
        "incoming_backward_requirements": [copy.deepcopy(item) for item in messages if item["kind"] == "backward_requirement" and item["target_act"] == act_id],
        "outgoing_forward_consequences": [copy.deepcopy(item) for item in messages if item["kind"] == "forward_consequence" and item["source_act"] == act_id],
        "outgoing_backward_requirements": [copy.deepcopy(item) for item in messages if item["kind"] == "backward_requirement" and item["source_act"] == act_id],
        "boundary_contradictions": [copy.deepcopy(item) for item in boundary_contradictions(runtime) if act_id in {item["source_act"], item["target_act"]}],
        "cross_direction_agreements": [copy.deepcopy(item) for item in runtime["shared_story_state"].get("cross_direction_agreements", []) if act_id in item.get("acts", [])],
        "shared_story_truths": copy.deepcopy(shared_report.get("story_truths", [])),
        "shared_strong_threads": copy.deepcopy(shared_report.get("strong_threads", [])),
        "shared_repeated_signals": copy.deepcopy(shared_report.get("repeated_signals", [])),
        "convergence_phase": shared_report.get("phase"),
        "temporal_consistency": temporal_consistency(runtime),
        "authority_effect": "derived_local_packet_no_canon_mutation",
    }


def _validate_delta(delta: dict[str, Any]) -> None:
    if not isinstance(delta, dict) or delta.get("schema") != DELTA_SCHEMA:
        raise ValueError(f"delta schema must be {DELTA_SCHEMA}")
    if not _nonempty(delta.get("id")) or delta.get("type") not in DELTA_TYPES:
        raise ValueError("delta requires id and valid type")
    if delta.get("source_act") not in ACT_INDEX:
        raise ValueError("delta source_act must be persistent act")
    if not _nonempty(delta.get("provenance")):
        raise ValueError("delta requires provenance")
    if not isinstance(delta.get("payload"), dict):
        raise ValueError("delta payload must be an object")


def integrate_deltas(runtime: dict[str, Any], deltas: list[dict[str, Any]]) -> dict[str, Any]:
    """Integrate derived act deltas without turning local invention into shared truth."""
    validate_runtime(runtime)
    if not isinstance(deltas, list):
        raise ValueError("deltas must be a list")
    updated = copy.deepcopy(runtime)
    seen_ids: set[str] = set()

    for delta in deltas:
        _validate_delta(delta)
        if delta["id"] in seen_ids:
            raise ValueError(f"duplicate delta id: {delta['id']}")
        seen_ids.add(delta["id"])
        source_act = delta["source_act"]
        payload = copy.deepcopy(delta["payload"])
        delta_type = delta["type"]

        if delta_type == "local_possibility":
            updated["acts"][source_act]["local_state"]["possibilities"].append(payload)
        elif delta_type == "local_discovery":
            updated["acts"][source_act]["local_state"]["discoveries"].append(payload)
        elif delta_type == "local_unresolved_question":
            updated["acts"][source_act]["local_state"]["unresolved_questions"].append(payload)
        elif delta_type in {"state_in_hypothesis", "state_out_hypothesis"}:
            _validate_boundary(payload, field=delta_type)
            updated["acts"][source_act]["state_in" if delta_type == "state_in_hypothesis" else "state_out"].append(payload)
        elif delta_type in MESSAGE_KINDS:
            target_act = delta.get("target_act")
            if target_act not in ACT_INDEX:
                raise ValueError(f"{delta_type} delta requires target_act")
            message = {
                "id": payload["id"],
                "kind": delta_type,
                "source_act": source_act,
                "target_act": target_act,
                "statement": payload["statement"],
                "confidence": payload.get("confidence", 0.5),
                "provenance": [delta["provenance"]],
                "status": payload.get("status", "open"),
            }
            if "thread_key" in payload:
                message["thread_key"] = payload["thread_key"]
            _validate_message(message, expected_kind=delta_type)
            collection = "forward_consequences" if delta_type == "forward_consequence" else "backward_requirements"
            updated["shared_story_state"][collection].append(message)
        elif delta_type == "constraint_response":
            response = payload
            if response.get("response") not in CONSTRAINT_RESPONSES or not _nonempty(response.get("message_id")) or not _nonempty(response.get("reason")):
                raise ValueError("constraint_response delta requires message_id, response, and reason")
            updated["acts"][source_act]["local_state"]["constraint_responses"].append(response)
        elif delta_type == "cross_direction_agreement":
            _validate_agreement(payload)
            updated["shared_story_state"].setdefault("cross_direction_agreements", []).append(payload)
        elif delta_type == "shared_discovery":
            story_sync.validate_discovery(payload)
            updated["shared_story_state"]["sync_state"]["discoveries"].append(payload)

    validate_runtime(updated)
    return updated
