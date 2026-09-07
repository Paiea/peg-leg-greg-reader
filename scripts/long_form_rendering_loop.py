from __future__ import annotations

from copy import deepcopy
from typing import Any


RENDER_PACKET_SCHEMA = "long_form_render_packet/v1"
REPROMPT_PACKET_SCHEMA = "long_form_reprompt_packet/v1"
INTERVAL_JOB_SCHEMA = "long_form_interval_job/v1"
EVALUATION_SCHEMA = "rendering_evaluation/v1"
PROSE_DISCOVERY_SCHEMA = "prose_discovery/v1"
RENDERING_EVIDENCE_SCHEMA = "derived_rendering_evidence/v1"


def compile_render_packet(interval: dict[str, Any], rendering_memory: list[str] | None = None) -> dict[str, Any]:
    """Compile one bounded prose interval without granting prose story authority."""
    return {
        "schema": RENDER_PACKET_SCHEMA,
        "authority": "derived_candidate_only",
        "canon_write_authorized": False,
        "interval_id": interval["id"],
        "act": interval.get("act"),
        "state_in": deepcopy(interval.get("state_in", {})),
        "state_out": deepcopy(interval.get("state_out", {})),
        "required_result": interval.get("required_result"),
        "reader_state": deepcopy(interval.get("reader_state", {})),
        "dependencies": deepcopy(interval.get("dependencies", {})),
        "story_truths": list(interval.get("story_truths", [])),
        "strong_threads": list(interval.get("strong_threads", [])),
        "case_law": list(interval.get("case_law", [])),
        "renderer_choices": list(interval.get("renderer_choices", [])),
        "rendering_memory": list(rendering_memory or []),
        "instructions": [
            "Render the bounded interval into prose; do not redesign the story.",
            "Treat renderer choices as live alternatives unless this bounded render must instantiate one.",
            "Do not reveal reader-hidden state.",
            "Do not mutate STORY SYNC maturity or canon authority.",
        ],
    }


def _normalize_issue(item: Any, default_prefix: str) -> dict[str, str]:
    if isinstance(item, dict):
        code = str(item.get("code", default_prefix)).strip() or default_prefix
        feedback = str(item.get("feedback", item.get("description", code))).strip()
        return {"code": code, "feedback": feedback}
    text = str(item).strip()
    return {"code": default_prefix, "feedback": text}


def normalize_evaluation(evaluation: dict[str, Any]) -> dict[str, Any]:
    """Normalize evaluator output into machine-actionable survival/failure evidence.

    Legacy scalar pass/fail fields remain supported so existing render callers do
    not need to migrate atomically.
    """
    if not isinstance(evaluation, dict):
        raise ValueError("rendering evaluation must be a JSON object")

    survives = [str(item) for item in evaluation.get("survives", [])]
    fails = [_normalize_issue(item, "story:unspecified") for item in evaluation.get("fails", [])]
    uncertain = [_normalize_issue(item, "uncertain:unspecified") for item in evaluation.get("uncertain", [])]

    if not fails:
        legacy_feedback = list(evaluation.get("feedback", []))
        feedback = str(legacy_feedback[0]) if legacy_feedback else ""
        if evaluation.get("causal_fidelity") == "fail":
            fails.append({"code": "story:causal_fidelity", "feedback": feedback or "Causal fidelity failed."})
        elif evaluation.get("continuity") == "fail":
            fails.append({"code": "continuity:state", "feedback": feedback or "Continuity failed."})
        elif evaluation.get("performance_fidelity") == "fail":
            fails.append({"code": "performance:behavior", "feedback": feedback or "Performance fidelity failed."})
        elif evaluation.get("prose_quality") == "fail":
            fails.append({"code": "prose:quality", "feedback": feedback or "Prose quality failed."})

    result = deepcopy(evaluation)
    result.update({
        "schema": EVALUATION_SCHEMA,
        "survives": survives,
        "fails": fails,
        "uncertain": uncertain,
        "future_repair_obligations": [str(item) for item in evaluation.get("future_repair_obligations", [])],
        "comparison_dimensions": deepcopy(evaluation.get("comparison_dimensions", {})),
    })
    return result


def diagnose_evaluation(evaluation: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_evaluation(evaluation)
    fails = normalized["fails"]
    feedback = [item["feedback"] for item in fails if item.get("feedback")]
    feedback.extend(str(item) for item in evaluation.get("feedback", []) if str(item) not in feedback)

    if fails:
        codes = [str(item.get("code", "")) for item in fails]
        if any(code.startswith("story:") for code in codes):
            failure_class, route = "story", "story_rehearsal"
        elif any(code.startswith("continuity:") for code in codes):
            failure_class, route = "continuity", "continuity_repair"
        elif any(code.startswith("performance:") or code.startswith("relationship:") for code in codes):
            failure_class, route = "performance", "performance_rehearsal"
        elif any(code.startswith("prose:") for code in codes):
            failure_class, route = "prose", "reprompt"
        else:
            failure_class, route = "story", "story_rehearsal"
        return {
            "failure_class": failure_class,
            "route": route,
            "feedback": feedback,
            "survives": list(normalized["survives"]),
            "fails": deepcopy(fails),
            "uncertain": deepcopy(normalized["uncertain"]),
            "future_repair_obligations": list(normalized["future_repair_obligations"]),
        }

    return {
        "failure_class": "accept",
        "route": "advance",
        "feedback": list(evaluation.get("feedback", [])),
        "survives": list(normalized["survives"]),
        "fails": [],
        "uncertain": deepcopy(normalized["uncertain"]),
        "future_repair_obligations": list(normalized["future_repair_obligations"]),
    }


def build_reprompt_packet(interval: dict[str, Any], prior_candidate: str, diagnosis: dict[str, Any]) -> dict[str, Any]:
    if diagnosis.get("route") != "reprompt":
        raise ValueError("targeted prose reprompt is only valid for a prose failure")
    return {
        "schema": REPROMPT_PACKET_SCHEMA,
        "authority": "derived_candidate_only",
        "canon_write_authorized": False,
        "interval_id": interval["id"],
        "prior_candidate": prior_candidate,
        "locked_story_contract": {
            "state_in": deepcopy(interval.get("state_in", {})),
            "state_out": deepcopy(interval.get("state_out", {})),
            "required_result": interval.get("required_result"),
            "reader_state": deepcopy(interval.get("reader_state", {})),
            "dependencies": deepcopy(interval.get("dependencies", {})),
        },
        "locked_survivors": list(diagnosis.get("survives", [])),
        "targeted_feedback": list(diagnosis.get("feedback", [])),
        "uncertain": deepcopy(diagnosis.get("uncertain", [])),
        "future_repair_obligations": list(diagnosis.get("future_repair_obligations", [])),
        "instructions": "Fix only the diagnosed prose weakness. Do not alter surviving elements. Do not solve this by changing story facts, causal structure, character truth, reader knowledge, dependencies, or required state transition.",
    }


def _candidate_score(candidate: dict[str, Any]) -> tuple[int, int, float, str]:
    evaluation = candidate.get("evaluation", {})
    diagnosis = diagnose_evaluation(evaluation)
    valid = 1 if diagnosis["route"] == "advance" else 0
    normalized = normalize_evaluation(evaluation)
    supplied = dict(normalized.get("comparison_dimensions", {}))
    supplied.update({key: value for key, value in evaluation.get("scores", {}).items() if key not in supplied})
    numeric = [float(value) for value in supplied.values() if isinstance(value, (int, float))]
    average = sum(numeric) / len(numeric) if numeric else 0.0
    return valid, len(normalized["survives"]), average, str(candidate.get("id", ""))


def compare_candidates(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if not candidates:
        raise ValueError("candidate comparison requires at least one candidate")
    ranked = sorted(candidates, key=_candidate_score, reverse=True)
    winner = ranked[0]
    return {
        "winner_id": winner.get("id"),
        "ranked_ids": [item.get("id") for item in ranked],
        "reason": "Prefer candidates with no diagnosed contract failure, then more explicit surviving requirements, then supplied comparison dimensions; ties are deterministic.",
    }


def collect_loser_evidence(candidates: list[dict[str, Any]], winner_id: str, *, interval_id: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("id", ""))
        if candidate_id == winner_id:
            continue
        for item in candidate.get("evaluation", {}).get("useful_evidence", []):
            evidence.append({
                "schema": RENDERING_EVIDENCE_SCHEMA,
                "authority": "none",
                "canon_write_authorized": False,
                "interval_id": interval_id,
                "source_candidate_id": candidate_id,
                "kind": str(item.get("kind", "rendering_observation")),
                "content": str(item.get("content", "")),
                "status": "available_for_rehearsal_or_story_sync_evaluation",
            })
    return evidence


def extract_prose_discoveries(candidate: dict[str, Any], *, interval_id: str) -> list[dict[str, Any]]:
    discoveries: list[dict[str, Any]] = []
    for index, item in enumerate(candidate.get("evaluation", {}).get("prose_discoveries", []), start=1):
        claim = str(item.get("claim", "")).strip()
        if not claim:
            continue
        discoveries.append({
            "schema": PROSE_DISCOVERY_SCHEMA,
            "id": f"{interval_id}:prose-discovery:{index}",
            "authority": "speculation_only",
            "canon_write_authorized": False,
            "status": "proposed_to_story_sync",
            "interval_id": interval_id,
            "source_candidate_id": candidate.get("id"),
            "claim": claim,
            "dimensions": [str(value) for value in item.get("dimensions", [])],
            "evidence": str(item.get("evidence", "")),
            "instruction": "Treat this as prose-generated speculative evidence. STORY SYNC decides whether it deserves any maturity later.",
        })
    return discoveries


def retain_candidate(interval: dict[str, Any], candidates: list[dict[str, Any]], comparison: dict[str, Any]) -> dict[str, Any]:
    winner_id = comparison["winner_id"]
    winner = next((item for item in candidates if item.get("id") == winner_id), None)
    if winner is None:
        raise ValueError("comparison winner is not present in candidates")
    lessons = list(winner.get("evaluation", {}).get("lessons", []))
    return {
        "interval_id": interval["id"],
        "authority": "derived_candidate_only",
        "canon_write_authorized": False,
        "winner": deepcopy(winner),
        "comparison": deepcopy(comparison),
        "state_in": deepcopy(interval.get("state_in", {})),
        "state_out": deepcopy(interval.get("state_out", {})),
        "dependency_snapshot": deepcopy(interval.get("dependencies", {})),
        "rendering_memory_delta": lessons,
        "prose_discoveries": extract_prose_discoveries(winner, interval_id=interval["id"]),
        "loser_evidence": collect_loser_evidence(candidates, str(winner_id), interval_id=interval["id"]),
    }


def _rehearsal_request(interval: dict[str, Any], diagnosis: dict[str, Any]) -> dict[str, Any]:
    feedback = diagnosis.get("feedback", [])
    problem = feedback[0] if feedback else f"{diagnosis['failure_class']} failure in {interval['id']}"
    return {
        "interval_id": interval["id"],
        "failure_class": diagnosis["failure_class"],
        "problem": problem,
        "locked_dependencies": deepcopy(interval.get("dependencies", {})),
        "instruction": "Test only this concrete gap, reduce the result through STORY SYNC, then return to the same rendering interval.",
    }


def compile_interval_job(
    interval: dict[str, Any],
    *,
    snapshot_version: str,
    attempt_budget: int = 2,
    rendering_memory: list[str] | None = None,
) -> dict[str, Any]:
    """Create one independent render frontier job from an immutable story snapshot."""
    if attempt_budget < 1:
        raise ValueError("interval attempt budget must be at least one")
    if not str(snapshot_version).strip():
        raise ValueError("interval job requires snapshot_version")
    return {
        "schema": INTERVAL_JOB_SCHEMA,
        "authority": "derived_candidate_only",
        "canon_write_authorized": False,
        "status": "rendering",
        "interval_id": interval["id"],
        "snapshot_version": str(snapshot_version),
        "dependency_snapshot": deepcopy(interval.get("dependencies", {})),
        "attempt_budget": int(attempt_budget),
        "interval": deepcopy(interval),
        "rendering_memory": list(rendering_memory or []),
        "active_attempts": [],
        "next_packet": compile_render_packet(interval, rendering_memory),
    }


def reduce_interval_attempt(job: dict[str, Any], returned_attempt: dict[str, Any]) -> dict[str, Any]:
    """Reduce one prose attempt independently of any global chapter cursor."""
    result = deepcopy(job)
    interval = result["interval"]
    candidate = deepcopy(returned_attempt["candidate"])
    attempt_number = int(returned_attempt.get("attempt_number", 1))
    diagnosis = diagnose_evaluation(candidate.get("evaluation", {}))
    attempts = list(result.get("active_attempts", []))
    attempts.append(candidate)
    result["active_attempts"] = attempts

    if diagnosis["route"] in {"story_rehearsal", "performance_rehearsal", "continuity_repair"}:
        result["status"] = diagnosis["route"]
        result["rehearsal_request"] = _rehearsal_request(interval, diagnosis)
        result.pop("next_packet", None)
        return result

    budget = int(result.get("attempt_budget", 2))
    if diagnosis["route"] == "reprompt" and attempt_number < budget:
        result["status"] = "reprompt"
        result["next_packet"] = build_reprompt_packet(interval, str(candidate.get("text", "")), diagnosis)
        return result

    valid_candidates = [item for item in attempts if diagnose_evaluation(item.get("evaluation", {}))["route"] == "advance"]
    if not valid_candidates:
        result["status"] = "story_rehearsal"
        result["rehearsal_request"] = _rehearsal_request(interval, diagnosis)
        result.pop("next_packet", None)
        return result

    comparison = compare_candidates(valid_candidates)
    retained = retain_candidate(interval, attempts, comparison)
    result["status"] = "retained"
    result["retained"] = retained
    result["rendering_memory"] = list(result.get("rendering_memory", [])) + list(retained["rendering_memory_delta"])
    result.pop("next_packet", None)
    result.pop("rehearsal_request", None)
    return result


def advance_rendering_run(run: dict[str, Any], returned_attempt: dict[str, Any]) -> dict[str, Any]:
    """Compatibility reducer for the original sequential bounded rendering run."""
    result = deepcopy(run)
    intervals = result.get("intervals", [])
    cursor = int(result.get("cursor", 0))
    if cursor >= len(intervals):
        result["status"] = "complete"
        return result
    interval = intervals[cursor]
    candidate = deepcopy(returned_attempt["candidate"])
    attempt_number = int(returned_attempt.get("attempt_number", 1))
    diagnosis = diagnose_evaluation(candidate.get("evaluation", {}))

    attempts = list(result.get("active_attempts", []))
    attempts.append(candidate)
    result["active_attempts"] = attempts

    if diagnosis["route"] in {"story_rehearsal", "performance_rehearsal", "continuity_repair"}:
        result["status"] = diagnosis["route"]
        result["rehearsal_request"] = _rehearsal_request(interval, diagnosis)
        return result

    budget = int(interval.get("attempt_budget", result.get("attempt_budget_default", 2)))
    if diagnosis["route"] == "reprompt" and attempt_number < budget:
        result["status"] = "reprompt"
        result["next_packet"] = build_reprompt_packet(interval, str(candidate.get("text", "")), diagnosis)
        return result

    valid_candidates = [item for item in attempts if diagnose_evaluation(item.get("evaluation", {}))["route"] == "advance"]
    if not valid_candidates:
        result["status"] = "performance_rehearsal" if diagnosis["failure_class"] == "performance" else "story_rehearsal"
        result["rehearsal_request"] = _rehearsal_request(interval, diagnosis)
        return result

    comparison = compare_candidates(valid_candidates)
    retained = retain_candidate(interval, attempts, comparison)
    result.setdefault("ledger", []).append(retained)
    result.setdefault("rendering_memory", []).extend(retained["rendering_memory_delta"])
    result["cursor"] = cursor + 1
    result["active_attempts"] = []
    result.pop("next_packet", None)
    result.pop("rehearsal_request", None)
    if result["cursor"] >= len(intervals):
        result["status"] = "complete"
    else:
        result["status"] = "rendering"
        result["next_packet"] = compile_render_packet(intervals[result["cursor"]], result.get("rendering_memory", []))
    return result


def start_rendering_run(intervals: list[dict[str, Any]], *, attempt_budget_default: int = 2, rendering_memory: list[str] | None = None) -> dict[str, Any]:
    if not intervals:
        raise ValueError("rendering run requires at least one interval")
    if attempt_budget_default < 1:
        raise ValueError("attempt budget must be at least one")
    run = {
        "schema": "long_form_rendering_run/v1",
        "authority": "derived_candidate_only",
        "canon_write_authorized": False,
        "status": "rendering",
        "attempt_budget_default": attempt_budget_default,
        "intervals": deepcopy(intervals),
        "cursor": 0,
        "ledger": [],
        "rendering_memory": list(rendering_memory or []),
        "active_attempts": [],
    }
    run["next_packet"] = compile_render_packet(intervals[0], run["rendering_memory"])
    return run
