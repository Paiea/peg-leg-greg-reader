#!/usr/bin/env python3
from __future__ import annotations

import copy
from typing import Any

from scripts import story_sync_engine as story_sync

RUNTIME_SCHEMA = "persistent_act_runtime/v1"
ACT_STATE_SCHEMA = "persistent_act_state/v1"
SHARED_STATE_SCHEMA = "persistent_shared_story_state/v1"
DELTA_SCHEMA = "persistent_act_delta/v1"
REHEARSAL_TARGET_SCHEMA = "persistent_rehearsal_target/v1"
REHEARSAL_EVIDENCE_SCHEMA = "persistent_rehearsal_evidence/v1"

ACT_IDS = ("act-i", "act-ii", "act-iii", "act-iv")
ACT_INDEX = {act_id: index for index, act_id in enumerate(ACT_IDS)}
MESSAGE_KINDS = {"forward_consequence", "backward_requirement"}
MESSAGE_STATUSES = {"open", "closed", "rejected"}
CONSTRAINT_RESPONSES = {"supported", "conflict", "third_path", "reject_source", "untested"}
EXPERIMENT_MODES = {
    "plausibility_probe",
    "state_transition_test",
    "trajectory_worldline_test",
    "forward_consequence_test",
    "backward_prerequisite_test",
    "counterfactual_branch_comparison",
    "temporal_distance_rehearsal",
    "performance",
}
FIDELITY_LEVELS = {"probe", "development", "high_heat"}
DELTA_TYPES = {
    "local_possibility",
    "local_possibility_update",
    "local_discovery",
    "local_unresolved_question",
    "state_in_hypothesis",
    "state_out_hypothesis",
    "forward_consequence",
    "backward_requirement",
    "constraint_response",
    "cross_direction_agreement",
    "shared_discovery",
    "shared_discovery_evidence",
}
EMBODIED_DIMENSION_TOKENS = (
    "trust",
    "relationship",
    "romantic",
    "romance",
    "loyal",
    "fear",
    "attraction",
    "intimacy",
    "desire",
    "betrayal",
)


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
    if not isinstance(acts, dict) or set(acts.keys()) != set(ACT_IDS):
        raise ValueError("runtime requires four persistent act channels: act-i, act-ii, act-iii, act-iv")
    for act_id in ACT_IDS:
        _validate_act_state(act_id, acts[act_id])
    shared = runtime.get("shared_story_state")
    if not isinstance(shared, dict):
        raise ValueError("runtime requires shared_story_state")
    story_sync.validate_sync_state(shared.get("sync_state"))
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


def sync_shared_story(runtime: dict[str, Any], *, creator_taste: dict[str, Any] | None = None) -> dict[str, Any]:
    """Delegate shared discovery maturity to STORY SYNC; creator taste stays heuristic."""
    validate_runtime(runtime)
    return story_sync.sync_story(
        copy.deepcopy(runtime["shared_story_state"]["sync_state"]),
        creator_taste=copy.deepcopy(creator_taste) if creator_taste is not None else None,
    )


def boundary_contradictions(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    """Surface explicit adjacent STATE OUT / STATE IN disagreements."""
    validate_runtime(runtime)
    conflicts: list[dict[str, Any]] = []
    for index in range(len(ACT_IDS) - 1):
        source_act = ACT_IDS[index]
        target_act = ACT_IDS[index + 1]
        for source in runtime["acts"][source_act]["state_out"]:
            for target in runtime["acts"][target_act]["state_in"]:
                if source["dimension"] != target["dimension"] or source.get("value") == target.get("value"):
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
            "heat": "high" if _is_embodied_dimension(item["dimension"]) else "medium",
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
    open_messages = [item for item in _all_messages(runtime) if item.get("status", "open") != "closed"]
    unresolved_messages = [item for item in closure["messages"] if item["closure_status"] not in {"closed", "supported"}]
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
    """Return non-starving baseline scheduling plus evidence-driven bonus work."""
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
            "reason": "cross-act requirement conflicts with accumulated local reality; test adaptation or a third path",
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


def compile_act_packet(runtime: dict[str, Any], act_id: str, *, creator_taste: dict[str, Any] | None = None) -> dict[str, Any]:
    validate_runtime(runtime)
    if act_id not in ACT_INDEX:
        raise ValueError("act_id must identify one of the four persistent act channels")
    act = runtime["acts"][act_id]
    shared_report = sync_shared_story(runtime, creator_taste=creator_taste)
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
        elif delta_type == "local_possibility_update":
            possibility_id = payload.pop("possibility_id", None)
            if not _nonempty(possibility_id):
                raise ValueError("local_possibility_update requires possibility_id")
            possibilities = updated["acts"][source_act]["local_state"]["possibilities"]
            match = next((item for item in possibilities if item.get("id") == possibility_id), None)
            if match is None:
                raise ValueError(f"unknown local possibility: {possibility_id}")
            match.update(payload)
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
            if payload.get("response") not in CONSTRAINT_RESPONSES or not _nonempty(payload.get("message_id")) or not _nonempty(payload.get("reason")):
                raise ValueError("constraint_response delta requires message_id, response, and reason")
            updated["acts"][source_act]["local_state"]["constraint_responses"].append(payload)
        elif delta_type == "cross_direction_agreement":
            _validate_agreement(payload)
            updated["shared_story_state"].setdefault("cross_direction_agreements", []).append(payload)
        elif delta_type == "shared_discovery":
            story_sync.validate_discovery(payload)
            updated["shared_story_state"]["sync_state"]["discoveries"].append(payload)
        elif delta_type == "shared_discovery_evidence":
            discovery_id = payload.get("discovery_id")
            evidence_item = payload.get("evidence")
            if not _nonempty(discovery_id) or not isinstance(evidence_item, dict):
                raise ValueError("shared_discovery_evidence requires discovery_id and evidence")
            discoveries = updated["shared_story_state"]["sync_state"]["discoveries"]
            match = next((item for item in discoveries if item.get("id") == discovery_id), None)
            if match is None:
                raise ValueError(f"unknown shared discovery: {discovery_id}")
            match.setdefault("evidence", []).append(copy.deepcopy(evidence_item))
            story_sync.validate_discovery(match)
    validate_runtime(updated)
    return updated


def _is_embodied_dimension(dimension: str) -> bool:
    lowered = dimension.lower()
    return any(token in lowered for token in EMBODIED_DIMENSION_TOKENS)


def _target(
    *,
    target_id: str,
    source_kind: str,
    source_id: str,
    acts: list[str],
    experiment_mode: str,
    fidelity: str,
    reason: str,
    dimension: str | None = None,
) -> dict[str, Any]:
    if experiment_mode not in EXPERIMENT_MODES or fidelity not in FIDELITY_LEVELS:
        raise ValueError("invalid rehearsal target experiment mode or fidelity")
    item: dict[str, Any] = {
        "schema": REHEARSAL_TARGET_SCHEMA,
        "id": target_id,
        "source_kind": source_kind,
        "source_id": source_id,
        "acts": copy.deepcopy(acts),
        "experiment_mode": experiment_mode,
        "fidelity": fidelity,
        "reason": reason,
        "authority_effect": "derived_only_no_story_authority",
    }
    if dimension is not None:
        item["dimension"] = dimension
    return item


def compile_rehearsal_targets(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    """Translate open uncertainty into experiment choices without inventing story truth."""
    validate_runtime(runtime)
    targets: list[dict[str, Any]] = []
    for conflict in boundary_contradictions(runtime):
        embodied = _is_embodied_dimension(conflict["dimension"])
        targets.append(_target(
            target_id=f"target:{conflict['id']}",
            source_kind="boundary_contradiction",
            source_id=conflict["id"],
            acts=[conflict["source_act"], conflict["target_act"]],
            experiment_mode="performance" if embodied else "state_transition_test",
            fidelity="high_heat" if embodied else "development",
            reason=conflict["reason"],
            dimension=conflict["dimension"],
        ))
    for message in _all_messages(runtime):
        if message.get("status", "open") != "open":
            continue
        mode = "forward_consequence_test" if message["kind"] == "forward_consequence" else "backward_prerequisite_test"
        targets.append(_target(
            target_id=f"target:message:{message['id']}",
            source_kind=message["kind"],
            source_id=message["id"],
            acts=[message["source_act"], message["target_act"]],
            experiment_mode=mode,
            fidelity="probe",
            reason=message["statement"],
        ))
    for act_id in ACT_IDS:
        for index, question in enumerate(runtime["acts"][act_id]["local_state"].get("unresolved_questions", [])):
            if isinstance(question, dict):
                question_id = str(question.get("id") or f"question:{act_id}:{index}")
                reason = str(question.get("question") or question.get("finding") or question_id)
            else:
                question_id = f"question:{act_id}:{index}"
                reason = str(question)
            targets.append(_target(
                target_id=f"target:{question_id}",
                source_kind="local_unresolved_question",
                source_id=question_id,
                acts=[act_id],
                experiment_mode="plausibility_probe",
                fidelity="probe",
                reason=reason,
            ))
    closure = constraint_closure(runtime)
    for collision in closure["constraint_collisions"]:
        targets.append(_target(
            target_id=f"target:collision:{collision['message_id']}",
            source_kind="constraint_collision",
            source_id=collision["message_id"],
            acts=[collision["source_act"], collision["target_act"]],
            experiment_mode="counterfactual_branch_comparison",
            fidelity="development",
            reason=collision["reason"],
        ))
    for agreement in runtime["shared_story_state"].get("cross_direction_agreements", []):
        targets.append(_target(
            target_id=f"target:agreement:{agreement['id']}",
            source_kind="cross_direction_agreement",
            source_id=agreement["id"],
            acts=list(agreement["acts"]),
            experiment_mode="temporal_distance_rehearsal",
            fidelity="development",
            reason=agreement["statement"],
        ))
    sync_report = sync_shared_story(runtime)
    mode_by_purpose = {
        "compare_live_contradiction": "counterfactual_branch_comparison",
        "challenge_strong_thread": "trajectory_worldline_test",
        "resolve_unresolved_question": "plausibility_probe",
        "test_repeated_signal": "trajectory_worldline_test",
        "creator_likely_probe": "plausibility_probe",
        "creator_surprise_probe": "counterfactual_branch_comparison",
    }
    for item in sync_report.get("rehearsal_targets", []):
        source_id = item.get("source_id")
        if not _nonempty(source_id):
            continue
        regions = [region for region in item.get("regions", []) if region in ACT_INDEX]
        if not regions:
            regions = list(ACT_IDS)
        purpose = item.get("purpose", "test_repeated_signal")
        mode = mode_by_purpose.get(purpose, "trajectory_worldline_test")
        heat = item.get("heat", "medium")
        fidelity = "development" if heat in {"high", "medium"} else "probe"
        targets.append(_target(
            target_id=f"target:sync:{source_id}:{purpose}",
            source_kind="story_sync",
            source_id=source_id,
            acts=regions,
            experiment_mode=mode,
            fidelity=fidelity,
            reason=item.get("reason", "STORY SYNC requested additional evidence"),
        ))
    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for item in targets:
        unique[(item["source_id"], item["experiment_mode"])] = item
    return list(unique.values())


def validate_rehearsal_evidence(evidence: dict[str, Any]) -> None:
    if not isinstance(evidence, dict) or evidence.get("schema") != REHEARSAL_EVIDENCE_SCHEMA:
        raise ValueError(f"rehearsal evidence schema must be {REHEARSAL_EVIDENCE_SCHEMA}")
    for field in ("id", "target_id", "source_act", "finding", "provenance"):
        if not _nonempty(evidence.get(field)):
            raise ValueError(f"rehearsal evidence requires {field}")
    if evidence["source_act"] not in ACT_INDEX:
        raise ValueError("rehearsal evidence source_act must be persistent act")
    if evidence.get("experiment_mode") not in EXPERIMENT_MODES:
        raise ValueError("invalid rehearsal evidence experiment_mode")
    if evidence.get("fidelity") not in FIDELITY_LEVELS:
        raise ValueError("invalid rehearsal evidence fidelity")
    _confidence(evidence.get("confidence", 0.5), field="rehearsal evidence confidence")
    for field in (
        "local_discoveries",
        "forward_consequences",
        "backward_requirements",
        "branch_updates",
        "story_sync_discoveries",
        "story_sync_evidence_updates",
    ):
        if not isinstance(evidence.get(field, []), list):
            raise ValueError(f"rehearsal evidence {field} must be a list")


def reduce_rehearsal_evidence(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    """Reduce one bounded experiment result into compact derived state deltas."""
    validate_rehearsal_evidence(evidence)
    source_act = evidence["source_act"]
    provenance = evidence["provenance"]
    evidence_id = evidence["id"]
    deltas: list[dict[str, Any]] = []
    for index, item in enumerate(evidence.get("local_discoveries", [])):
        deltas.append({"schema": DELTA_SCHEMA, "id": f"{evidence_id}:local:{index}", "type": "local_discovery", "source_act": source_act, "provenance": provenance, "payload": copy.deepcopy(item)})
    for collection, delta_type in (("forward_consequences", "forward_consequence"), ("backward_requirements", "backward_requirement")):
        for index, item in enumerate(evidence.get(collection, [])):
            target_act = item.get("target_act")
            if target_act not in ACT_INDEX:
                raise ValueError(f"{collection} evidence requires target_act")
            payload = {key: copy.deepcopy(value) for key, value in item.items() if key != "target_act"}
            deltas.append({"schema": DELTA_SCHEMA, "id": f"{evidence_id}:{delta_type}:{index}", "type": delta_type, "source_act": source_act, "target_act": target_act, "provenance": provenance, "payload": payload})
    for index, item in enumerate(evidence.get("branch_updates", [])):
        if not isinstance(item, dict) or not _nonempty(item.get("possibility_id")):
            raise ValueError("branch update requires possibility_id")
        deltas.append({"schema": DELTA_SCHEMA, "id": f"{evidence_id}:branch:{index}", "type": "local_possibility_update", "source_act": source_act, "provenance": provenance, "payload": copy.deepcopy(item)})
    for index, item in enumerate(evidence.get("story_sync_discoveries", [])):
        deltas.append({"schema": DELTA_SCHEMA, "id": f"{evidence_id}:sync:{index}", "type": "shared_discovery", "source_act": source_act, "provenance": provenance, "payload": copy.deepcopy(item)})
    for index, item in enumerate(evidence.get("story_sync_evidence_updates", [])):
        if not isinstance(item, dict) or not _nonempty(item.get("discovery_id")) or not isinstance(item.get("evidence"), dict):
            raise ValueError("story_sync_evidence_update requires discovery_id and evidence")
        deltas.append({"schema": DELTA_SCHEMA, "id": f"{evidence_id}:sync-evidence:{index}", "type": "shared_discovery_evidence", "source_act": source_act, "provenance": provenance, "payload": copy.deepcopy(item)})
    return deltas


def branch_entropy(runtime: dict[str, Any]) -> dict[str, Any]:
    """Return a transparent branch-pressure proxy, not information-theoretic entropy."""
    validate_runtime(runtime)
    local_open: list[str] = []
    for act_id in ACT_IDS:
        for possibility in runtime["acts"][act_id]["local_state"].get("possibilities", []):
            if possibility.get("status", "active") == "active" and possibility.get("viability", "viable") not in {"invalidated", "redundant"}:
                local_open.append(f"{act_id}:{possibility.get('id')}")
    sync_report = sync_shared_story(runtime)
    shared_open = list(sync_report.get("branches_preserved", []))
    contradictions = list(sync_report.get("contradictions_alive", []))
    open_messages = [item["id"] for item in _all_messages(runtime) if item.get("status", "open") == "open"]
    return {
        "metric": "branch_entropy_proxy",
        "open_branch_count": len(local_open) + len(shared_open),
        "local_open_branches": local_open,
        "shared_preserved_branches": shared_open,
        "unresolved_contradiction_count": len(contradictions),
        "open_message_count": len(open_messages),
        "pressure_score": len(local_open) + len(shared_open) + len(contradictions) + len(open_messages),
        "policy": "proxy_tracks_open_search_pressure_not_story_authority",
    }


def run_rehearsal_cycle(
    runtime: dict[str, Any],
    *,
    evidence: list[dict[str, Any]] | None = None,
    creator_taste: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run one derived-only four-temporal-perspective REHEARSAL/STORY SYNC cycle."""
    validate_runtime(runtime)
    before_entropy = branch_entropy(runtime)
    deltas: list[dict[str, Any]] = []
    for item in evidence or []:
        deltas.extend(reduce_rehearsal_evidence(item))
    evolved = integrate_deltas(runtime, deltas) if deltas else copy.deepcopy(runtime)
    after_entropy = branch_entropy(evolved)
    sync_report = sync_shared_story(evolved, creator_taste=creator_taste)
    return {
        "schema": "persistent_rehearsal_cycle/v1",
        "story_id": evolved["story_id"],
        "shared_story_sync": sync_report,
        "act_packets": {act_id: compile_act_packet(evolved, act_id, creator_taste=creator_taste) for act_id in ACT_IDS},
        "schedule": schedule_work(evolved),
        "rehearsal_targets": compile_rehearsal_targets(evolved),
        "boundary_contradictions": boundary_contradictions(evolved),
        "constraint_closure": constraint_closure(evolved),
        "temporal_consistency": temporal_consistency(evolved),
        "applied_deltas": deltas,
        "branch_entropy": {
            "before": before_entropy,
            "after": after_entropy,
            "open_branch_delta": after_entropy["open_branch_count"] - before_entropy["open_branch_count"],
            "pressure_delta": after_entropy["pressure_score"] - before_entropy["pressure_score"],
        },
        "evolved_runtime": evolved,
        "authority_effect": "derived_only_no_canon_mutation",
    }
