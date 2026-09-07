#!/usr/bin/env python3
from __future__ import annotations

import copy
from typing import Any

from scripts import persistent_act_runtime as act_runtime

REHEARSAL_TARGET_SCHEMA = "story_rehearsal_target/v1"
REHEARSAL_RESULT_SCHEMA = "story_rehearsal_result/v1"
REHEARSAL_EVIDENCE_SCHEMA = "story_rehearsal_evidence/v1"

REHEARSAL_EXPERIMENT_MODES = {
    "plausibility_probe",
    "state_transition_test",
    "trajectory_worldline_test",
    "forward_consequence_test",
    "backward_prerequisite_test",
    "counterfactual_branch_comparison",
    "temporal_distance_rehearsal",
    "development_rehearsal",
    "performance",
}
HEAT_LEVELS = {"probe", "development", "high_heat"}
RESULT_OUTCOMES = {"support", "challenge", "inconclusive"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: object, *, field: str, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    if not allow_empty and not value:
        raise ValueError(f"{field} requires at least one value")
    if any(not _nonempty(item) for item in value):
        raise ValueError(f"{field} values must be nonempty strings")
    return list(value)


def _confidence(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("confidence must be between 0 and 1")
    number = float(value)
    if not 0 <= number <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return number


def build_rehearsal_target(
    *,
    target_id: str,
    acts: list[str],
    source_type: str,
    source_id: str,
    uncertainty: str,
    experiment_mode: str,
    heat: str,
    provenance: list[str],
    state_in: list[dict[str, Any]] | None = None,
    pressure: list[str] | None = None,
    forward_constraints: list[dict[str, Any]] | None = None,
    backward_constraints: list[dict[str, Any]] | None = None,
    required_result: str | None = None,
    result_locked: bool = False,
) -> dict[str, Any]:
    if not all(_nonempty(value) for value in (target_id, source_type, source_id, uncertainty)):
        raise ValueError("rehearsal target requires target_id, source_type, source_id, and uncertainty")
    act_values = _string_list(acts, field="acts", allow_empty=False)
    if any(act_id not in act_runtime.ACT_IDS for act_id in act_values):
        raise ValueError("rehearsal target acts must be persistent acts")
    if experiment_mode not in REHEARSAL_EXPERIMENT_MODES:
        raise ValueError("invalid rehearsal experiment_mode")
    if heat not in HEAT_LEVELS:
        raise ValueError("invalid rehearsal heat")
    provenance_values = _string_list(provenance, field="provenance", allow_empty=False)
    target = {
        "schema": REHEARSAL_TARGET_SCHEMA,
        "target_id": target_id,
        "acts": act_values,
        "source_type": source_type,
        "source_id": source_id,
        "uncertainty": uncertainty,
        "experiment_mode": experiment_mode,
        "heat": heat,
        "state_in": copy.deepcopy(state_in or []),
        "pressure": copy.deepcopy(pressure or []),
        "forward_constraints": copy.deepcopy(forward_constraints or []),
        "backward_constraints": copy.deepcopy(backward_constraints or []),
        "provenance": provenance_values,
        "authority_effect": "derived_experiment_no_story_truth",
    }
    if result_locked:
        if not _nonempty(required_result):
            raise ValueError("locked rehearsal result requires required_result")
        target["required_result"] = required_result
        target["result_locked"] = True
    elif required_result is not None:
        raise ValueError("required_result may be supplied only when result_locked is true")
    return target


def _is_behavioral_dimension(dimension: str) -> bool:
    lowered = dimension.lower()
    return any(token in lowered for token in (
        "trust", "romantic", "relationship", "attraction", "loyal", "fear", "betray", "conflict", "chemistry"
    ))


def compile_rehearsal_targets(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    """Compile the cheapest useful experiments from persistent temporal uncertainty."""
    act_runtime.validate_runtime(runtime)
    targets: list[dict[str, Any]] = []

    for act_id in act_runtime.ACT_IDS:
        questions = runtime["acts"][act_id]["local_state"].get("unresolved_questions", [])
        for index, question in enumerate(questions):
            if isinstance(question, dict):
                text = question.get("question") or question.get("statement")
                source_id = question.get("id") or f"{act_id}-q-{index+1}"
            else:
                text = question
                source_id = f"{act_id}-q-{index+1}"
            if not _nonempty(text):
                continue
            targets.append(build_rehearsal_target(
                target_id=f"rehearse:{source_id}",
                acts=[act_id],
                source_type="act_question",
                source_id=source_id,
                uncertainty=text,
                experiment_mode="plausibility_probe",
                heat="probe",
                provenance=[f"local:{act_id}:{source_id}"],
                state_in=runtime["acts"][act_id]["state_in"],
            ))

    for conflict in act_runtime.boundary_contradictions(runtime):
        behavioral = _is_behavioral_dimension(conflict["dimension"])
        targets.append(build_rehearsal_target(
            target_id=f"rehearse:{conflict['id']}",
            acts=[conflict["source_act"], conflict["target_act"]],
            source_type="boundary_contradiction",
            source_id=conflict["id"],
            uncertainty=(
                f"{conflict['dimension']} boundary is {conflict['source_value']} leaving {conflict['source_act']} "
                f"but {conflict['target_value']} entering {conflict['target_act']}; what lived transition, if any, makes this passable?"
            ),
            experiment_mode="performance" if behavioral else "state_transition_test",
            heat="high_heat" if behavioral else "development",
            provenance=[conflict["source_boundary_id"], conflict["target_boundary_id"]],
            state_in=runtime["acts"][conflict["target_act"]]["state_in"],
        ))

    shared = runtime["shared_story_state"]
    for message in shared.get("forward_consequences", []):
        if message.get("status", "open") != "open":
            continue
        targets.append(build_rehearsal_target(
            target_id=f"rehearse:{message['id']}",
            acts=[message["source_act"], message["target_act"]],
            source_type="forward_consequence",
            source_id=message["id"],
            uncertainty=f"Does this earlier consequence remain causally alive in {message['target_act']}? {message['statement']}",
            experiment_mode="forward_consequence_test",
            heat="development",
            provenance=copy.deepcopy(message.get("provenance", [])) or [message["id"]],
            forward_constraints=[copy.deepcopy(message)],
        ))

    for message in shared.get("backward_requirements", []):
        if message.get("status", "open") != "open":
            continue
        targets.append(build_rehearsal_target(
            target_id=f"rehearse:{message['id']}",
            acts=[message["target_act"], message["source_act"]],
            source_type="backward_requirement",
            source_id=message["id"],
            uncertainty=f"Does the proposed earlier prerequisite arise naturally, or is the later payoff asking for false history? {message['statement']}",
            experiment_mode="backward_prerequisite_test",
            heat="development",
            provenance=copy.deepcopy(message.get("provenance", [])) or [message["id"]],
            backward_constraints=[copy.deepcopy(message)],
        ))

    for agreement in shared.get("cross_direction_agreements", []):
        targets.append(build_rehearsal_target(
            target_id=f"rehearse:{agreement['id']}",
            acts=copy.deepcopy(agreement["acts"]),
            source_type="cross_direction_agreement",
            source_id=agreement["id"],
            uncertainty=f"Independent temporal regions agree on this possible thread. Does it survive a counterfactual alternative? {agreement['statement']}",
            experiment_mode="counterfactual_branch_comparison",
            heat="development",
            provenance=copy.deepcopy(agreement.get("provenance", [])) or [agreement["id"]],
        ))

    return targets


def _validate_implications(items: object, *, field: str) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        raise ValueError(f"{field} must be a list")
    normalized: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f"{field} items must be objects")
        if not _nonempty(item.get("id")) or not _nonempty(item.get("target_act")) or not _nonempty(item.get("statement")):
            raise ValueError(f"{field} item requires id, target_act, and statement")
        if item["target_act"] not in act_runtime.ACT_IDS:
            raise ValueError(f"{field} target_act must be persistent act")
        _confidence(item.get("confidence", 0.5))
        normalized.append(copy.deepcopy(item))
    return normalized


def validate_rehearsal_result(result: dict[str, Any]) -> None:
    if not isinstance(result, dict) or result.get("schema") != REHEARSAL_RESULT_SCHEMA:
        raise ValueError(f"rehearsal result schema must be {REHEARSAL_RESULT_SCHEMA}")
    for field in ("target_id", "source_act", "finding", "independent_group", "provenance"):
        if not _nonempty(result.get(field)):
            raise ValueError(f"rehearsal result requires {field}")
    if result["source_act"] not in act_runtime.ACT_IDS:
        raise ValueError("rehearsal result source_act must be persistent act")
    if result.get("experiment_mode") not in REHEARSAL_EXPERIMENT_MODES:
        raise ValueError("invalid rehearsal result experiment_mode")
    if result.get("heat") not in HEAT_LEVELS:
        raise ValueError("invalid rehearsal result heat")
    if result.get("outcome") not in RESULT_OUTCOMES:
        raise ValueError("invalid rehearsal result outcome")
    _confidence(result.get("confidence"))
    _string_list(result.get("dramatic_uses", []), field="dramatic_uses", allow_empty=False)
    regions = _string_list(result.get("regions", []), field="regions", allow_empty=False)
    if any(region not in act_runtime.ACT_IDS for region in regions):
        raise ValueError("rehearsal result regions must be persistent acts")
    for field in ("behavior_discovered", "relationship_movement", "unresolved_questions"):
        _string_list(result.get(field, []), field=field)
    _validate_implications(result.get("forward_consequences", []), field="forward_consequences")
    _validate_implications(result.get("backward_requirements", []), field="backward_requirements")


def reduce_rehearsal_result(result: dict[str, Any]) -> dict[str, Any]:
    """Cool evaluated rehearsal into compact evidence and derived directional deltas."""
    validate_rehearsal_result(result)
    outcome = result["outcome"]
    sync_kind = "support" if outcome == "support" else "contradiction" if outcome == "challenge" else None
    derived_deltas: list[dict[str, Any]] = []

    for item in result.get("forward_consequences", []):
        derived_deltas.append({
            "schema": act_runtime.DELTA_SCHEMA,
            "id": f"rehearsal:{result['target_id']}:forward:{item['id']}",
            "type": "forward_consequence",
            "source_act": result["source_act"],
            "target_act": item["target_act"],
            "provenance": result["provenance"],
            "payload": {
                "id": item["id"],
                "statement": item["statement"],
                "confidence": float(item.get("confidence", 0.5)),
            },
        })
    for item in result.get("backward_requirements", []):
        derived_deltas.append({
            "schema": act_runtime.DELTA_SCHEMA,
            "id": f"rehearsal:{result['target_id']}:backward:{item['id']}",
            "type": "backward_requirement",
            "source_act": result["source_act"],
            "target_act": item["target_act"],
            "provenance": result["provenance"],
            "payload": {
                "id": item["id"],
                "statement": item["statement"],
                "confidence": float(item.get("confidence", 0.5)),
            },
        })
    for index, question in enumerate(result.get("unresolved_questions", [])):
        derived_deltas.append({
            "schema": act_runtime.DELTA_SCHEMA,
            "id": f"rehearsal:{result['target_id']}:question:{index+1}",
            "type": "local_unresolved_question",
            "source_act": result["source_act"],
            "provenance": result["provenance"],
            "payload": question,
        })

    reduced = {
        "schema": REHEARSAL_EVIDENCE_SCHEMA,
        "target_id": result["target_id"],
        "source_act": result["source_act"],
        "experiment_mode": result["experiment_mode"],
        "heat": result["heat"],
        "outcome": outcome,
        "finding": result["finding"],
        "confidence": float(result["confidence"]),
        "behavior_discovered": copy.deepcopy(result.get("behavior_discovered", [])),
        "relationship_movement": copy.deepcopy(result.get("relationship_movement", [])),
        "unresolved_questions": copy.deepcopy(result.get("unresolved_questions", [])),
        "provenance": result["provenance"],
        "full_evidence_pointer": result.get("full_evidence_pointer"),
        "derived_deltas": derived_deltas,
        "authority_effect": "derived_evidence_no_auto_promotion",
    }
    if sync_kind is not None:
        reduced["story_sync_evidence"] = {
            "source_id": result["provenance"],
            "independent_group": result["independent_group"],
            "kind": sync_kind,
            "dramatic_uses": copy.deepcopy(result["dramatic_uses"]),
            "regions": copy.deepcopy(result["regions"]),
            "provenance": {
                "source": "REHEARSAL",
                "experiment_mode": result["experiment_mode"],
                "heat": result["heat"],
                "finding": result["finding"],
                "confidence": float(result["confidence"]),
            },
        }
    else:
        reduced["story_sync_evidence"] = None
    return reduced
