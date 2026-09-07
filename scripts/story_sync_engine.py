#!/usr/bin/env python3
from __future__ import annotations

import copy
from typing import Any

SYNC_STATE_SCHEMA = "story_sync_state/v1"
SYNC_REPORT_SCHEMA = "story_sync_report/v1"
DISCOVERY_LEVELS = ("speculation", "repeated_signal", "strong_thread", "story_truth")
DISCOVERY_RANK = {name: index for index, name in enumerate(DISCOVERY_LEVELS)}
CONVERGENCE_PHASES = ("explore", "compare", "converge")
VISIBILITY_STATES = {"show", "hide", "merge", "compress"}
BRANCH_VIABILITY = {"viable", "weak", "redundant", "invalidated"}
PROPAGATION_DIRECTIONS = {"backward", "forward"}
EVIDENCE_KINDS = {"support", "challenge_survived", "contradiction"}


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


def _evidence_summary(discovery: dict[str, Any]) -> dict[str, Any]:
    evidence = discovery.get("evidence", [])
    if not isinstance(evidence, list):
        raise ValueError("discovery evidence must be a list")

    support_groups: set[str] = set()
    challenge_groups: set[str] = set()
    contradiction_groups: set[str] = set()
    dramatic_uses: set[str] = set()
    regions: set[str] = set()

    for item in evidence:
        if not isinstance(item, dict):
            raise ValueError("discovery evidence entries must be objects")
        source_id = item.get("source_id")
        independent_group = item.get("independent_group")
        kind = item.get("kind", "support")
        if not _nonempty(source_id) or not _nonempty(independent_group):
            raise ValueError("discovery evidence requires source_id and independent_group")
        if kind not in EVIDENCE_KINDS:
            raise ValueError(f"invalid discovery evidence kind: {kind}")

        uses = _string_list(item.get("dramatic_uses", []), field="dramatic_uses")
        item_regions = _string_list(item.get("regions", []), field="regions")
        dramatic_uses.update(uses)
        regions.update(item_regions)

        if kind == "support":
            support_groups.add(independent_group)
        elif kind == "challenge_survived":
            challenge_groups.add(independent_group)
        else:
            contradiction_groups.add(independent_group)

    return {
        "support_groups": sorted(support_groups),
        "challenge_groups": sorted(challenge_groups),
        "contradiction_groups": sorted(contradiction_groups),
        "dramatic_uses": sorted(dramatic_uses),
        "regions": sorted(regions),
    }


def validate_discovery(discovery: dict[str, Any]) -> None:
    if not isinstance(discovery, dict):
        raise ValueError("discovery must be an object")
    if not _nonempty(discovery.get("id")) or not _nonempty(discovery.get("finding")):
        raise ValueError("discovery requires id and finding")
    current_level = discovery.get("confidence")
    if current_level is not None and current_level not in DISCOVERY_LEVELS:
        raise ValueError("invalid discovery confidence")
    _evidence_summary(discovery)
    propagation = discovery.get("propagation", [])
    if not isinstance(propagation, list):
        raise ValueError("discovery propagation must be a list")
    for item in propagation:
        if not isinstance(item, dict):
            raise ValueError("propagation entries must be objects")
        if item.get("direction") not in PROPAGATION_DIRECTIONS:
            raise ValueError("propagation direction must be backward or forward")
        if not _nonempty(item.get("target")) or not _nonempty(item.get("reason")):
            raise ValueError("propagation requires target and reason")


def classify_discovery(discovery: dict[str, Any]) -> str:
    """Classify authority from independent support plus dramatic usefulness.

    Deterministic code does not decide whether an idea is artistically good. Model/human
    workers express that judgment through independent evidence, dramatic-use tags, region
    reach, and survived challenges. Repetition can earn REPEATED SIGNAL, but cannot by
    itself earn STRONG THREAD or STORY TRUTH.
    """
    validate_discovery(discovery)
    summary = _evidence_summary(discovery)
    support_count = len(summary["support_groups"])
    uses_count = len(summary["dramatic_uses"])
    region_count = len(summary["regions"])
    survived_challenges = len(summary["challenge_groups"])

    if support_count < 2:
        return "speculation"

    level = "repeated_signal"
    if uses_count >= 3 and region_count >= 2:
        level = "strong_thread"

    if (
        level == "strong_thread"
        and support_count >= 3
        and uses_count >= 4
        and region_count >= 3
        and survived_challenges >= 1
    ):
        return "story_truth"
    return level


def convergence_phase(story_confidence: float) -> str:
    if isinstance(story_confidence, bool) or not isinstance(story_confidence, (int, float)):
        raise ValueError("story_confidence must be numeric")
    if not 0 <= float(story_confidence) <= 1:
        raise ValueError("story_confidence must be between 0 and 1")
    if story_confidence < 0.45:
        return "explore"
    if story_confidence < 0.75:
        return "compare"
    return "converge"


def should_trigger_immediate_sync(discovery: dict[str, Any], level: str) -> bool:
    if level not in DISCOVERY_LEVELS:
        raise ValueError("invalid discovery level")
    return discovery.get("book_shaping") is True and DISCOVERY_RANK[level] >= DISCOVERY_RANK["strong_thread"]


def branch_sync_action(possibility: dict[str, Any], *, phase: str) -> str:
    if phase not in CONVERGENCE_PHASES:
        raise ValueError("invalid convergence phase")
    if not isinstance(possibility, dict) or not _nonempty(possibility.get("id")):
        raise ValueError("possibility requires id")
    status = possibility.get("status", "active")
    viability = possibility.get("viability", "viable")
    if viability not in BRANCH_VIABILITY:
        raise ValueError("invalid branch viability")
    if status in {"killed", "superseded"}:
        return "kill"
    if status != "active":
        raise ValueError("possibility status must be active, killed, or superseded")

    if viability == "viable":
        return "preserve"
    if phase == "explore":
        return "preserve"
    if viability in {"redundant", "invalidated"}:
        return "kill"
    if viability == "weak" and phase == "converge":
        return "kill"
    return "preserve"


def validate_assumption(assumption: dict[str, Any]) -> None:
    if not isinstance(assumption, dict) or not _nonempty(assumption.get("id")):
        raise ValueError("assumption requires id")
    status = assumption.get("status", "active")
    if status not in {"active", "superseded"}:
        raise ValueError("assumption status must be active or superseded")
    if status == "superseded":
        if not _nonempty(assumption.get("replaced_by")):
            raise ValueError("superseded assumption requires replaced_by")
        if not _nonempty(assumption.get("why")):
            raise ValueError("superseded assumption requires why")
        _string_list(assumption.get("evidence", []), field="superseded assumption evidence", allow_empty=False)


def _validate_canon_event(event: dict[str, Any]) -> None:
    if not isinstance(event, dict) or not _nonempty(event.get("id")):
        raise ValueError("canon event requires id")
    if event.get("canon") is not True:
        raise ValueError("canon_events may contain only accepted canon events")
    if event.get("visibility") not in VISIBILITY_STATES:
        raise ValueError("invalid canon event visibility")


def _validate_reader_requirement(requirement: dict[str, Any]) -> None:
    if not isinstance(requirement, dict) or not _nonempty(requirement.get("id")):
        raise ValueError("reader requirement requires id")
    if not _nonempty(requirement.get("payoff_event")):
        raise ValueError("reader requirement requires payoff_event")
    _string_list(requirement.get("required_setup_any", []), field="required_setup_any", allow_empty=False)


def validate_sync_state(state: dict[str, Any]) -> None:
    if not isinstance(state, dict) or state.get("schema") != SYNC_STATE_SCHEMA:
        raise ValueError(f"sync state schema must be {SYNC_STATE_SCHEMA}")
    convergence_phase(state.get("story_confidence", 0.0))

    for field in ("possibilities", "discoveries", "contradictions", "canon_events", "reader_requirements", "assumptions"):
        if not isinstance(state.get(field, []), list):
            raise ValueError(f"{field} must be a list")

    seen: set[str] = set()
    for possibility in state.get("possibilities", []):
        if not isinstance(possibility, dict) or not _nonempty(possibility.get("id")):
            raise ValueError("possibility requires id")
        if possibility["id"] in seen:
            raise ValueError(f"duplicate sync id: {possibility['id']}")
        seen.add(possibility["id"])
        branch_sync_action(possibility, phase="explore")

    for discovery in state.get("discoveries", []):
        validate_discovery(discovery)
        if discovery["id"] in seen:
            raise ValueError(f"duplicate sync id: {discovery['id']}")
        seen.add(discovery["id"])

    for contradiction in state.get("contradictions", []):
        if not isinstance(contradiction, dict) or not _nonempty(contradiction.get("id")):
            raise ValueError("contradiction requires id")
        if contradiction.get("status", "unresolved") not in {"unresolved", "resolved"}:
            raise ValueError("contradiction status must be unresolved or resolved")
        _string_list(contradiction.get("members", []), field="contradiction members", allow_empty=False)

    for event in state.get("canon_events", []):
        _validate_canon_event(event)
    for requirement in state.get("reader_requirements", []):
        _validate_reader_requirement(requirement)
    for assumption in state.get("assumptions", []):
        validate_assumption(assumption)


def _reader_gaps(state: dict[str, Any]) -> list[dict[str, Any]]:
    events = {event["id"]: event for event in state.get("canon_events", [])}
    visible = {event_id for event_id, event in events.items() if event["visibility"] != "hide"}
    gaps: list[dict[str, Any]] = []
    for requirement in state.get("reader_requirements", []):
        payoff = events.get(requirement["payoff_event"])
        if payoff is None or payoff["visibility"] == "hide":
            continue
        candidates = requirement["required_setup_any"]
        if any(setup_id in visible for setup_id in candidates):
            continue
        hidden_support = [setup_id for setup_id in candidates if setup_id in events and events[setup_id]["visibility"] == "hide"]
        gaps.append({
            "id": requirement["id"],
            "payoff_event": requirement["payoff_event"],
            "required_setup_any": list(candidates),
            "hidden_support": hidden_support,
            "repair": "add the smallest sufficient visible setup; do not automatically unhide all supporting canon",
        })
    return gaps


def _sync_contradictions(state: dict[str, Any]) -> tuple[list[str], list[str]]:
    alive: list[str] = []
    immediate: list[str] = []
    for contradiction in state.get("contradictions", []):
        if contradiction.get("status", "unresolved") != "unresolved":
            continue
        alive.append(contradiction["id"])
        if contradiction.get("book_shaping") is True and contradiction.get("severity") in {"high", "critical"}:
            immediate.append(contradiction["id"])
    return alive, immediate


def _propagation_for(discovery: dict[str, Any], level: str) -> list[dict[str, Any]]:
    if DISCOVERY_RANK[level] < DISCOVERY_RANK["strong_thread"]:
        return []
    return [
        {
            "discovery_id": discovery["id"],
            "confidence": level,
            "direction": item["direction"],
            "target": item["target"],
            "reason": item["reason"],
            "action": "recompile_or_rehearse_target_before_mutating_accepted_canon",
        }
        for item in discovery.get("propagation", [])
    ]


def sync_story(state: dict[str, Any]) -> dict[str, Any]:
    """Synchronize derived long-form story state without merging competing ideas.

    The report is a plan/evidence surface. It does not mutate canon prose and does not
    automatically rewrite accepted events. Semantic workers remain responsible for the
    artistic judgments represented in evidence and branch viability.
    """
    validate_sync_state(state)
    phase = convergence_phase(float(state.get("story_confidence", 0.0)))

    discovery_levels: dict[str, str] = {}
    promoted: list[dict[str, str]] = []
    repeated_signals: list[str] = []
    strong_threads: list[str] = []
    story_truths: list[str] = []
    propagation: list[dict[str, Any]] = []
    immediate_discoveries: list[str] = []

    for discovery in state.get("discoveries", []):
        level = classify_discovery(discovery)
        discovery_levels[discovery["id"]] = level
        previous = discovery.get("confidence")
        if previous is not None and DISCOVERY_RANK[level] > DISCOVERY_RANK[previous]:
            promoted.append({"id": discovery["id"], "from": previous, "to": level})
        if level == "repeated_signal":
            repeated_signals.append(discovery["id"])
        elif level == "strong_thread":
            strong_threads.append(discovery["id"])
        elif level == "story_truth":
            story_truths.append(discovery["id"])
        propagation.extend(_propagation_for(discovery, level))
        if should_trigger_immediate_sync(discovery, level):
            immediate_discoveries.append(discovery["id"])

    branches_preserved: list[str] = []
    branches_killed: list[str] = []
    for possibility in state.get("possibilities", []):
        action = branch_sync_action(possibility, phase=phase)
        if action == "kill":
            branches_killed.append(possibility["id"])
        else:
            branches_preserved.append(possibility["id"])

    contradictions_alive, immediate_contradictions = _sync_contradictions(state)
    hidden_canon = [event["id"] for event in state.get("canon_events", []) if event["visibility"] == "hide"]
    superseded_assumptions = [copy.deepcopy(item) for item in state.get("assumptions", []) if item.get("status") == "superseded"]

    return {
        "schema": SYNC_REPORT_SCHEMA,
        "phase": phase,
        "story_confidence": float(state.get("story_confidence", 0.0)),
        "discovery_levels": discovery_levels,
        "promoted_discoveries": promoted,
        "repeated_signals": sorted(repeated_signals),
        "strong_threads": sorted(strong_threads),
        "story_truths": sorted(story_truths),
        "propagation": propagation,
        "branches_preserved": branches_preserved,
        "branches_killed": branches_killed,
        "contradictions_alive": contradictions_alive,
        "hidden_canon": hidden_canon,
        "reader_gaps": _reader_gaps(state),
        "superseded_assumptions": superseded_assumptions,
        "immediate_sync_discoveries": immediate_discoveries,
        "immediate_sync_contradictions": immediate_contradictions,
        "sync_required": bool(immediate_discoveries or immediate_contradictions),
        "authority_effect": "derived_only_no_canon_mutation",
        "merge_policy": "preserve_viable_divergence",
    }
