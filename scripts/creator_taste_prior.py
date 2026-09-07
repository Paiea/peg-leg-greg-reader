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
TASTE_MATCH_LEVELS = {"low", "medium", "high"}
SEARCH_PRIORITIES = {"none", "low", "medium", "high"}
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
            signal = aggregate.setdefault(observation["id"], {
                "id": observation["id"],
                "scope": "cross_project",
                "direction": observation["direction"],
                "summary": observation["summary"],
                "support_count": 0,
                "challenge_count": 0,
                "evidence_count": 0,
                "last_evidence_reference": decision_id,
                "conditions": copy.deepcopy(observation.get("conditions", [])),
            })
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


def validate_taste_context(context: dict[str, Any]) -> None:
    if not isinstance(context, dict) or context.get("schema") != CREATOR_TASTE_CONTEXT_SCHEMA:
        raise ValueError(f"creator taste context schema must be {CREATOR_TASTE_CONTEXT_SCHEMA}")
    if context.get("project") is not None and not _nonempty(context.get("project")):
        raise ValueError("creator taste context project must be nonempty when present")
    for field, expected_scope in (("cross_project_signals", "cross_project"), ("project_signals", "project")):
        signals = context.get(field, [])
        if not isinstance(signals, list):
            raise ValueError(f"creator taste context {field} must be a list")
        for signal in signals:
            if not isinstance(signal, dict) or not _nonempty(signal.get("id")):
                raise ValueError("creator taste context signal requires id")
            if signal.get("scope", expected_scope) != expected_scope:
                raise ValueError("creator taste context signal scope mismatch")
            _confidence(signal.get("confidence"))
            if not _nonempty(signal.get("summary")):
                raise ValueError("creator taste context signal requires summary")


def validate_creator_taste_prior(prior: dict[str, Any]) -> None:
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
    if not isinstance(possibility, dict):
        raise ValueError("possibility must be an object")
    alignment = _string_list(possibility.get("taste_alignment", []), field="taste_alignment")
    aligned = set(alignment)
    score = 0.0
    if prior.get("schema") == CREATOR_TASTE_CONTEXT_SCHEMA:
        validate_taste_context(prior)
        for signal in prior.get("cross_project_signals", []):
            if signal["id"] in aligned:
                score += float(signal["confidence"])
        for signal in prior.get("project_signals", []):
            if signal["id"] in aligned:
                score += float(signal["confidence"]) * 2.0
        return round(score, 6)
    validate_creator_taste_prior(prior)
    if "preferences" in prior:
        for preference in prior.get("preferences", []):
            if preference["id"] not in aligned:
                continue
            score += float(preference["confidence"]) * (2.0 if preference["scope"] == "project" else 1.0)
    else:
        for signal in prior.get("signals", []):
            if signal["id"] in aligned:
                score += float(signal["confidence"])
    return round(score, 6)


def record_creator_surprise_win(prior: dict[str, Any], *, decision_id: str, chosen_branch: str, predicted_branch: str, conditions: list[str]) -> dict[str, Any]:
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


def _qualitative(value: object, *, field: str, default: str = "low") -> str:
    if value is None:
        return default
    if isinstance(value, bool):
        return "high" if value else "low"
    if value not in TASTE_MATCH_LEVELS:
        raise ValueError(f"{field} must be low, medium, or high")
    return str(value)


def branch_search_priority(possibility: dict[str, Any], *, phase: str) -> str:
    """Return a taste-only search hint; never branch authority."""
    if phase not in {"explore", "compare", "converge"}:
        raise ValueError("invalid convergence phase")
    if not isinstance(possibility, dict):
        raise ValueError("possibility must be an object")
    if possibility.get("status", "active") != "active" or possibility.get("viability", "viable") in {"invalidated", "redundant"}:
        return "none"
    match = _qualitative(possibility.get("creator_prior_match"), field="creator_prior_match")
    surprise = _qualitative(possibility.get("creator_surprise"), field="creator_surprise")
    if phase == "converge":
        return "low" if match in {"high", "medium"} or surprise == "high" else "none"
    if phase == "compare":
        if match == "high" or surprise == "high":
            return "medium"
        if match == "medium" or surprise == "medium":
            return "low"
        return "low"
    if match == "high":
        return "high"
    if match == "medium" or surprise == "high":
        return "medium"
    return "low"


def _preserved_possibilities(state: dict[str, Any], report: dict[str, Any]) -> list[dict[str, Any]]:
    preserved = set(report.get("branches_preserved", []))
    return [item for item in state.get("possibilities", []) if isinstance(item, dict) and item.get("id") in preserved and item.get("status", "active") == "active"]


def _contextual_priority(possibility: dict[str, Any], *, phase: str, creator_taste: dict[str, Any] | None) -> str:
    base = branch_search_priority(possibility, phase=phase)
    if base == "none":
        return "none"
    if phase == "converge":
        return "low" if base != "none" else "none"
    direct_match = _qualitative(possibility.get("creator_prior_match"), field="creator_prior_match")
    affinity = creator_taste_affinity(possibility, creator_taste) if creator_taste is not None else 0.0
    if direct_match == "high" or affinity >= 1.0:
        return "high"
    if direct_match == "medium" or affinity > 0:
        return "medium"
    return base


def augment_sync_report(state: dict[str, Any], report: dict[str, Any], *, creator_taste: dict[str, Any] | None = None) -> dict[str, Any]:
    """Decorate a deterministic STORY SYNC report with search hints only."""
    prior = creator_taste if creator_taste is not None else state.get("creator_taste_prior")
    if prior is None:
        return report
    if prior.get("schema") == CREATOR_TASTE_CONTEXT_SCHEMA:
        validate_taste_context(prior)
    else:
        validate_creator_taste_prior(prior)

    augmented = copy.deepcopy(report)
    phase = augmented.get("phase")
    possibilities_by_id = {item.get("id"): item for item in state.get("possibilities", []) if isinstance(item, dict)}
    affinity: dict[str, float] = {}

    for decision in augmented.get("branch_decisions", []):
        possibility = possibilities_by_id.get(decision.get("id"), {})
        priority = "none" if decision.get("action") == "kill" else _contextual_priority(possibility, phase=phase, creator_taste=prior)
        decision["creator_search_priority"] = priority
        decision["search_priority"] = priority
        if decision.get("action") != "kill":
            affinity[decision["id"]] = creator_taste_affinity(possibility, prior)

    if phase != "converge":
        preserved = _preserved_possibilities(state, augmented)
        likely = [item for item in preserved if _contextual_priority(item, phase=phase, creator_taste=prior) in {"high", "medium"} and (_qualitative(item.get("creator_prior_match"), field="creator_prior_match") in {"high", "medium"} or creator_taste_affinity(item, prior) > 0)]
        likely = sorted(likely, key=lambda item: (-creator_taste_affinity(item, prior), item["id"]))[:2]
        for item in likely:
            augmented.setdefault("rehearsal_targets", []).append({
                "source_type": "creator_taste",
                "source_id": item["id"],
                "purpose": "creator_likely_probe",
                "heat": "low",
                "reason": "creator prior suggests this viable branch deserves some exploration; REHEARSAL remains free to reject it",
                "creator_search_priority": _contextual_priority(item, phase=phase, creator_taste=prior),
            })

        likely_ids = {item["id"] for item in likely}
        explicit_surprises = [item for item in preserved if _qualitative(item.get("creator_surprise"), field="creator_surprise") == "high" and item["id"] not in likely_ids]
        if explicit_surprises:
            surprise = sorted(explicit_surprises, key=lambda item: item["id"])[0]
            augmented.setdefault("rehearsal_targets", []).append({
                "source_type": "creator_taste",
                "source_id": surprise["id"],
                "purpose": "creator_surprise_probe",
                "heat": "low",
                "reason": surprise.get("surprise_reason") or "plausible non-obvious branch deserves one counter-prior rehearsal lane",
                "creator_search_priority": _contextual_priority(surprise, phase=phase, creator_taste=prior),
            })

    if prior.get("schema") == CREATOR_TASTE_CONTEXT_SCHEMA:
        augmented["creator_taste"] = {
            "schema": CREATOR_TASTE_REPORT_SCHEMA,
            "authority_effect": "heuristic_only_no_story_authority",
            "phase": phase,
            "project": prior.get("project"),
            "cross_project_signals": copy.deepcopy(prior.get("cross_project_signals", [])),
            "project_signals": copy.deepcopy(prior.get("project_signals", [])),
            "branch_affinity": affinity,
            "policy": "nudges_what_gets_rehearsed_never_what_becomes_true",
        }
    else:
        augmented["creator_taste"] = {
            "schema": CREATOR_TASTE_REPORT_SCHEMA,
            "authority_effect": "heuristic_only_no_story_authority",
            "phase": phase,
            "preferences": copy.deepcopy(prior.get("preferences", [])),
            "surprise_wins": copy.deepcopy(prior.get("surprise_wins", [])),
            "branch_affinity": affinity,
            "policy": "nudges_what_gets_rehearsed_never_what_becomes_true",
        }
    return augmented
