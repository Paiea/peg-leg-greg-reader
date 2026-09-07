#!/usr/bin/env python3
from __future__ import annotations

import copy
from typing import Any

CREATOR_TASTE_SCHEMA = "creator_taste_prior/v1"
CREATOR_TASTE_REPORT_SCHEMA = "creator_taste_report/v1"
TASTE_SCOPES = {"project", "cross_project"}


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


def validate_creator_taste_prior(prior: dict[str, Any]) -> None:
    if not isinstance(prior, dict) or prior.get("schema") != CREATOR_TASTE_SCHEMA:
        raise ValueError(f"creator taste schema must be {CREATOR_TASTE_SCHEMA}")
    preferences = prior.get("preferences", [])
    surprise_wins = prior.get("surprise_wins", [])
    if not isinstance(preferences, list):
        raise ValueError("creator taste preferences must be a list")
    if not isinstance(surprise_wins, list):
        raise ValueError("creator taste surprise_wins must be a list")

    seen: set[str] = set()
    for preference in preferences:
        if not isinstance(preference, dict) or not _nonempty(preference.get("id")):
            raise ValueError("creator taste preference requires id")
        if preference["id"] in seen:
            raise ValueError(f"duplicate creator taste preference: {preference['id']}")
        seen.add(preference["id"])
        if preference.get("scope") not in TASTE_SCOPES:
            raise ValueError("creator taste preference scope must be project or cross_project")
        if not _nonempty(preference.get("statement")):
            raise ValueError("creator taste preference requires statement")
        confidence = preference.get("confidence")
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
            raise ValueError("creator taste preference confidence must be between 0 and 1")
        _string_list(preference.get("tags", []), field="creator taste tags", allow_empty=False)
        support = _string_list(preference.get("support", []), field="creator taste support", allow_empty=False)
        _string_list(preference.get("counterexamples", []), field="creator taste counterexamples")
        if float(confidence) >= 0.8 and len(set(support)) < 2:
            raise ValueError("high-confidence creator taste preference requires multiple supporting decisions")

    for item in surprise_wins:
        if not isinstance(item, dict):
            raise ValueError("creator surprise win must be an object")
        for field in ("decision_id", "chosen_branch", "predicted_branch"):
            if not _nonempty(item.get(field)):
                raise ValueError(f"creator surprise win requires {field}")
        _string_list(item.get("conditions", []), field="creator surprise win conditions", allow_empty=False)


def creator_taste_affinity(possibility: dict[str, Any], prior: dict[str, Any]) -> float:
    """Return a lightweight search-priority hint, never story authority.

    Project-specific evidence intentionally weighs more than cross-project evidence.
    The value is only used to decide which already-plausible branches deserve rehearsal.
    """
    validate_creator_taste_prior(prior)
    if not isinstance(possibility, dict):
        raise ValueError("possibility must be an object")
    alignment = _string_list(possibility.get("taste_alignment", []), field="taste_alignment")
    aligned = set(alignment)
    score = 0.0
    for preference in prior.get("preferences", []):
        if preference["id"] not in aligned:
            continue
        scope_weight = 2.0 if preference["scope"] == "project" else 1.0
        score += float(preference["confidence"]) * scope_weight
    return round(score, 6)


def record_creator_surprise_win(
    prior: dict[str, Any],
    *,
    decision_id: str,
    chosen_branch: str,
    predicted_branch: str,
    conditions: list[str],
) -> dict[str, Any]:
    """Record contextual disagreement without rewriting preferences into absolutes."""
    validate_creator_taste_prior(prior)
    for value, field in ((decision_id, "decision_id"), (chosen_branch, "chosen_branch"), (predicted_branch, "predicted_branch")):
        if not _nonempty(value):
            raise ValueError(f"{field} is required")
    condition_values = _string_list(conditions, field="creator surprise win conditions", allow_empty=False)
    updated = copy.deepcopy(prior)
    updated.setdefault("surprise_wins", []).append({
        "decision_id": decision_id,
        "chosen_branch": chosen_branch,
        "predicted_branch": predicted_branch,
        "conditions": condition_values,
    })
    return updated


def _preserved_possibilities(state: dict[str, Any], report: dict[str, Any]) -> list[dict[str, Any]]:
    preserved = set(report.get("branches_preserved", []))
    return [
        item
        for item in state.get("possibilities", [])
        if isinstance(item, dict)
        and item.get("id") in preserved
        and item.get("status", "active") == "active"
    ]


def _taste_targets(state: dict[str, Any], report: dict[str, Any], prior: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, float], str | None]:
    if report.get("phase") == "converge":
        return [], {}, None

    possibilities = _preserved_possibilities(state, report)
    affinity = {item["id"]: creator_taste_affinity(item, prior) for item in possibilities}
    likely = sorted(
        (item for item in possibilities if affinity[item["id"]] > 0),
        key=lambda item: (-affinity[item["id"]], item["id"]),
    )[:2]

    targets: list[dict[str, Any]] = [
        {
            "source_type": "creator_taste",
            "source_id": item["id"],
            "purpose": "creator_likely_probe",
            "heat": "low",
            "reason": "creator prior suggests this plausible branch deserves some exploration; REHEARSAL remains free to reject it",
            "taste_affinity": affinity[item["id"]],
            "taste_alignment": copy.deepcopy(item.get("taste_alignment", [])),
        }
        for item in likely
    ]

    likely_ids = {item["id"] for item in likely}
    explicit_surprises = [
        item for item in possibilities
        if item.get("creator_surprise") is True and item["id"] not in likely_ids
    ]
    neutral_surprises = [
        item for item in possibilities
        if affinity[item["id"]] == 0 and item["id"] not in likely_ids
    ]
    pool = explicit_surprises or neutral_surprises
    surprise = sorted(pool, key=lambda item: item["id"])[0] if pool else None
    surprise_id = surprise["id"] if surprise is not None else None
    if surprise is not None:
        targets.append({
            "source_type": "creator_taste",
            "source_id": surprise["id"],
            "purpose": "creator_surprise_probe",
            "heat": "low",
            "reason": surprise.get("surprise_reason") or "plausible preserved branch is not predicted by the current creator prior; keep one non-obvious path alive",
            "taste_affinity": affinity[surprise["id"]],
        })

    return targets, affinity, surprise_id


def augment_sync_report(state: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    """Add creator-taste search hints after deterministic STORY SYNC has already run.

    This function never changes discovery levels, branch actions, canon, propagation, or
    convergence phase. It may only append low-heat rehearsal/search targets and an
    inspectable heuristic report.
    """
    prior = state.get("creator_taste_prior")
    if prior is None:
        return report
    validate_creator_taste_prior(prior)
    augmented = copy.deepcopy(report)
    targets, affinity, surprise_id = _taste_targets(state, augmented, prior)
    augmented.setdefault("rehearsal_targets", []).extend(targets)
    augmented["creator_taste"] = {
        "schema": CREATOR_TASTE_REPORT_SCHEMA,
        "authority_effect": "heuristic_only_no_story_authority",
        "phase": augmented.get("phase"),
        "preferences": copy.deepcopy(prior.get("preferences", [])),
        "surprise_wins": copy.deepcopy(prior.get("surprise_wins", [])),
        "branch_affinity": affinity,
        "creator_surprise_branch": surprise_id,
        "policy": "nudges_what_gets_rehearsed_never_what_becomes_true",
    }
    return augmented
