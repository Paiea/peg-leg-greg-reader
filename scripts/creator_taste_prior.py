#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

CREATOR_TASTE_SCHEMA = "creator_taste_prior/v1"
CREATOR_TASTE_PRIOR_SCHEMA = CREATOR_TASTE_SCHEMA
PROJECT_TASTE_OVERLAY_SCHEMA = "creator_taste_project/v1"
CREATOR_TASTE_EVIDENCE_SCHEMA = "creator_taste_evidence/v1"
CREATOR_TASTE_CONTEXT_SCHEMA = "creator_taste_context/v1"
CREATOR_TASTE_REPORT_SCHEMA = "creator_taste_report/v1"
TASTE_SCOPES = {"project", "cross_project"}
TASTE_EFFECTS = {"support", "challenge"}
TASTE_DIRECTIONS = {"prefer", "avoid", "explore"}
MAX_ACTIVE_SIGNALS = 25


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


def _confidence(value: object, *, field: str = "confidence") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be between 0 and 1")
    number = float(value)
    if not 0 <= number <= 1:
        raise ValueError(f"{field} must be between 0 and 1")
    return number


def _nonnegative_int(value: object, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")
    return value


def validate_prior(prior: dict[str, Any]) -> None:
    """Validate the compact rebuildable cross-project runtime prior."""
    if not isinstance(prior, dict) or prior.get("schema") != CREATOR_TASTE_PRIOR_SCHEMA:
        raise ValueError(f"creator taste prior schema must be {CREATOR_TASTE_PRIOR_SCHEMA}")
    signals = prior.get("signals", [])
    if not isinstance(signals, list):
        raise ValueError("creator taste prior signals must be a list")
    if len(signals) > MAX_ACTIVE_SIGNALS:
        raise ValueError(f"creator taste prior may contain at most {MAX_ACTIVE_SIGNALS} active signals")

    seen: set[str] = set()
    for signal in signals:
        if not isinstance(signal, dict) or not _nonempty(signal.get("id")):
            raise ValueError("creator taste signal requires id")
        if signal["id"] in seen:
            raise ValueError(f"duplicate creator taste signal: {signal['id']}")
        seen.add(signal["id"])
        if signal.get("scope") != "cross_project":
            raise ValueError("compiled creator taste prior may contain only cross_project signals")
        if signal.get("direction") not in TASTE_DIRECTIONS:
            raise ValueError("creator taste signal direction must be prefer, avoid, or explore")
        _confidence(signal.get("confidence"))
        evidence_count = _nonnegative_int(signal.get("evidence_count"), field="evidence_count")
        counterexample_count = _nonnegative_int(signal.get("counterexample_count"), field="counterexample_count")
        if counterexample_count > evidence_count:
            raise ValueError("counterexample_count cannot exceed evidence_count")
        if not _nonempty(signal.get("summary")):
            raise ValueError("creator taste signal requires summary")
        if "conditions" in signal:
            _string_list(signal.get("conditions", []), field="creator taste signal conditions")
        if "last_evidence_reference" in signal and not _nonempty(signal.get("last_evidence_reference")):
            raise ValueError("last_evidence_reference must be nonempty when present")


def validate_project_overlay(overlay: dict[str, Any]) -> None:
    if not isinstance(overlay, dict) or overlay.get("schema") != PROJECT_TASTE_OVERLAY_SCHEMA:
        raise ValueError(f"project taste overlay schema must be {PROJECT_TASTE_OVERLAY_SCHEMA}")
    if not _nonempty(overlay.get("project")):
        raise ValueError("project taste overlay requires project")
    signals = overlay.get("signals", [])
    if not isinstance(signals, list):
        raise ValueError("project taste signals must be a list")

    seen: set[str] = set()
    for signal in signals:
        if not isinstance(signal, dict) or not _nonempty(signal.get("id")):
            raise ValueError("project taste signal requires id")
        if signal["id"] in seen:
            raise ValueError(f"duplicate project taste signal: {signal['id']}")
        seen.add(signal["id"])
        if signal.get("scope", "project") != "project":
            raise ValueError("project taste overlay may contain only project signals")
        if signal.get("direction") not in TASTE_DIRECTIONS:
            raise ValueError("project taste signal direction must be prefer, avoid, or explore")
        _confidence(signal.get("confidence"))
        if not _nonempty(signal.get("summary")):
            raise ValueError("project taste signal requires summary")
        if "conditions" in signal:
            _string_list(signal.get("conditions", []), field="project taste signal conditions")


def validate_evidence_record(record: dict[str, Any]) -> None:
    if not isinstance(record, dict) or record.get("schema") != CREATOR_TASTE_EVIDENCE_SCHEMA:
        raise ValueError(f"creator taste evidence schema must be {CREATOR_TASTE_EVIDENCE_SCHEMA}")
    for field in ("decision_id", "project", "context", "choice", "source_type"):
        if not _nonempty(record.get(field)):
            raise ValueError(f"creator taste evidence requires {field}")
    if "reason" in record and not _nonempty(record.get("reason")):
        raise ValueError("creator taste evidence reason must be nonempty when present")
    signals = record.get("signals", [])
    if not isinstance(signals, list) or not signals:
        raise ValueError("creator taste evidence requires at least one signal")
    for signal in signals:
        if not isinstance(signal, dict) or not _nonempty(signal.get("id")):
            raise ValueError("creator taste evidence signal requires id")
        if signal.get("scope") not in TASTE_SCOPES:
            raise ValueError("creator taste evidence signal scope must be project or cross_project")
        if signal.get("direction") not in TASTE_DIRECTIONS:
            raise ValueError("creator taste evidence signal direction must be prefer, avoid, or explore")
        if not _nonempty(signal.get("summary")):
            raise ValueError("creator taste evidence signal requires summary")
        if signal.get("effect") not in TASTE_EFFECTS:
            raise ValueError("creator taste evidence signal effect must be support or challenge")
        if "conditions" in signal:
            _string_list(signal.get("conditions", []), field="creator taste evidence signal conditions")


def append_evidence_record(path: str | Path, record: dict[str, Any]) -> None:
    """Append one explicit creator decision while rejecting duplicate decision IDs."""
    validate_evidence_record(record)
    target = Path(path)
    existing: list[dict[str, Any]] = []
    if target.exists():
        for line in target.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            validate_evidence_record(item)
            existing.append(item)
    if any(item["decision_id"] == record["decision_id"] for item in existing):
        raise ValueError(f"duplicate decision_id: {record['decision_id']}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def rebuild_prior(records: list[dict[str, Any]], *, max_signals: int = MAX_ACTIVE_SIGNALS) -> dict[str, Any]:
    """Rebuild a bounded cross-project prior from explicit evidence only.

    Project-local observations are intentionally ignored here. A small beta-style prior
    keeps a single approval from becoming a permanent absolute while counterexamples
    reduce confidence without erasing supported history.
    """
    if isinstance(max_signals, bool) or not isinstance(max_signals, int) or not 1 <= max_signals <= MAX_ACTIVE_SIGNALS:
        raise ValueError(f"max_signals must be between 1 and {MAX_ACTIVE_SIGNALS}")
    if not isinstance(records, list):
        raise ValueError("creator taste evidence records must be a list")

    aggregate: dict[str, dict[str, Any]] = {}
    seen_decisions: set[str] = set()
    for record in records:
        validate_evidence_record(record)
        decision_id = record["decision_id"]
        if decision_id in seen_decisions:
            raise ValueError(f"duplicate decision_id: {decision_id}")
        seen_decisions.add(decision_id)
        for observation in record["signals"]:
            if observation["scope"] != "cross_project":
                continue
            signal = aggregate.setdefault(
                observation["id"],
                {
                    "id": observation["id"],
                    "scope": "cross_project",
                    "direction": observation["direction"],
                    "summary": observation["summary"],
                    "support_count": 0,
                    "challenge_count": 0,
                    "evidence_count": 0,
                    "last_evidence_reference": decision_id,
                    "conditions": copy.deepcopy(observation.get("conditions", [])),
                },
            )
            signal["direction"] = observation["direction"]
            signal["summary"] = observation["summary"]
            signal["last_evidence_reference"] = decision_id
            if observation.get("conditions"):
                signal["conditions"] = copy.deepcopy(observation["conditions"])
            signal["evidence_count"] += 1
            if observation["effect"] == "support":
                signal["support_count"] += 1
            else:
                signal["challenge_count"] += 1

    compiled: list[dict[str, Any]] = []
    for signal in aggregate.values():
        support = signal.pop("support_count")
        challenges = signal.pop("challenge_count")
        signal["counterexample_count"] = challenges
        signal["confidence"] = round((support + 1) / (support + challenges + 2), 6)
        if not signal.get("conditions"):
            signal.pop("conditions", None)
        compiled.append(signal)

    compiled.sort(key=lambda item: (-item["confidence"], -item["evidence_count"], item["id"]))
    prior = {"schema": CREATOR_TASTE_PRIOR_SCHEMA, "signals": compiled[:max_signals]}
    validate_prior(prior)
    return prior


def compile_taste_context(prior: dict[str, Any], overlay: dict[str, Any] | None = None) -> dict[str, Any]:
    """Compile only the small runtime prior; historical evidence never enters the packet."""
    validate_prior(prior)
    project: str | None = None
    project_signals: list[dict[str, Any]] = []
    if overlay is not None:
        validate_project_overlay(overlay)
        project = overlay["project"]
        project_signals = copy.deepcopy(overlay.get("signals", []))
    return {
        "schema": CREATOR_TASTE_CONTEXT_SCHEMA,
        "project": project,
        "cross_project_signals": copy.deepcopy(prior.get("signals", [])),
        "project_signals": project_signals,
        "authority_effect": "heuristic_only_no_story_authority",
    }


def validate_creator_taste_prior(prior: dict[str, Any]) -> None:
    """Validate the lightweight embedded preference form used by existing sync states."""
    if not isinstance(prior, dict) or prior.get("schema") != CREATOR_TASTE_SCHEMA:
        raise ValueError(f"creator taste schema must be {CREATOR_TASTE_SCHEMA}")
    if "signals" in prior and "preferences" not in prior:
        validate_prior(prior)
        return
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
        confidence = _confidence(preference.get("confidence"), field="creator taste preference confidence")
        _string_list(preference.get("tags", []), field="creator taste tags", allow_empty=False)
        support = _string_list(preference.get("support", []), field="creator taste support", allow_empty=False)
        _string_list(preference.get("counterexamples", []), field="creator taste counterexamples")
        if confidence >= 0.8 and len(set(support)) < 2:
            raise ValueError("high-confidence creator taste preference requires multiple supporting decisions")

    for item in surprise_wins:
        if not isinstance(item, dict):
            raise ValueError("creator surprise win must be an object")
        for field in ("decision_id", "chosen_branch", "predicted_branch"):
            if not _nonempty(item.get(field)):
                raise ValueError(f"creator surprise win requires {field}")
        _string_list(item.get("conditions", []), field="creator surprise win conditions", allow_empty=False)


def creator_taste_affinity(possibility: dict[str, Any], prior: dict[str, Any]) -> float:
    """Return a lightweight search-priority hint, never story authority."""
    validate_creator_taste_prior(prior)
    if not isinstance(possibility, dict):
        raise ValueError("possibility must be an object")
    alignment = _string_list(possibility.get("taste_alignment", []), field="taste_alignment")
    aligned = set(alignment)
    score = 0.0
    if "preferences" in prior:
        for preference in prior.get("preferences", []):
            if preference["id"] not in aligned:
                continue
            scope_weight = 2.0 if preference["scope"] == "project" else 1.0
            score += float(preference["confidence"]) * scope_weight
    else:
        for signal in prior.get("signals", []):
            if signal["id"] in aligned:
                score += float(signal["confidence"])
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
    """Add embedded creator-taste search hints after deterministic STORY SYNC has run."""
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
