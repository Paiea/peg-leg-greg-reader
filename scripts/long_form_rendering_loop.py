from __future__ import annotations

from copy import deepcopy
from typing import Any


RENDER_PACKET_SCHEMA = "long_form_render_packet/v1"
REPROMPT_PACKET_SCHEMA = "long_form_reprompt_packet/v1"


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


def diagnose_evaluation(evaluation: dict[str, Any]) -> dict[str, Any]:
    feedback = list(evaluation.get("feedback", []))
    if evaluation.get("causal_fidelity") == "fail":
        return {"failure_class": "story", "route": "story_rehearsal", "feedback": feedback}
    if evaluation.get("continuity") == "fail":
        return {"failure_class": "continuity", "route": "continuity_repair", "feedback": feedback}
    if evaluation.get("performance_fidelity") == "fail":
        return {"failure_class": "performance", "route": "performance_rehearsal", "feedback": feedback}
    if evaluation.get("prose_quality") == "fail":
        return {"failure_class": "prose", "route": "reprompt", "feedback": feedback}
    return {"failure_class": "accept", "route": "advance", "feedback": feedback}


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
        },
        "targeted_feedback": list(diagnosis.get("feedback", [])),
        "instructions": "Fix only the diagnosed prose weakness. Do not solve this by changing story facts, causal structure, character truth, reader knowledge, or required state transition.",
    }


def _candidate_score(candidate: dict[str, Any]) -> tuple[int, float, str]:
    evaluation = candidate.get("evaluation", {})
    diagnosis = diagnose_evaluation(evaluation)
    valid = 1 if diagnosis["route"] == "advance" else 0
    scores = evaluation.get("scores", {})
    numeric = [float(value) for value in scores.values() if isinstance(value, (int, float))]
    average = sum(numeric) / len(numeric) if numeric else 0.0
    return valid, average, str(candidate.get("id", ""))


def compare_candidates(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if not candidates:
        raise ValueError("candidate comparison requires at least one candidate")
    ranked = sorted(candidates, key=_candidate_score, reverse=True)
    winner = ranked[0]
    return {
        "winner_id": winner.get("id"),
        "ranked_ids": [item.get("id") for item in ranked],
        "reason": "Prefer contract-valid candidates, then aggregate supplied prose scores; ties are deterministic.",
    }


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
        "rendering_memory_delta": lessons,
    }


def _rehearsal_request(interval: dict[str, Any], diagnosis: dict[str, Any]) -> dict[str, Any]:
    feedback = diagnosis.get("feedback", [])
    problem = feedback[0] if feedback else f"{diagnosis['failure_class']} failure in {interval['id']}"
    return {
        "interval_id": interval["id"],
        "failure_class": diagnosis["failure_class"],
        "problem": problem,
        "instruction": "Test only this concrete gap, reduce the result through STORY SYNC, then return to the same rendering interval.",
    }


def advance_rendering_run(run: dict[str, Any], returned_attempt: dict[str, Any]) -> dict[str, Any]:
    """Reduce one executor-supplied prose attempt into advance/reprompt/rehearsal.

    This function never calls a model and never writes canon. It is intentionally a
    deterministic reducer so an overnight executor can run model work elsewhere.
    """
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
        # The local polish budget is exhausted. Do not loop forever and do not
        # pretend failed prose is acceptable. Escalate the concrete failure.
        result["status"] = "performance_rehearsal" if diagnosis["failure_class"] == "performance" else "story_rehearsal"
        result["rehearsal_request"] = _rehearsal_request(interval, diagnosis)
        return result

    comparison = compare_candidates(valid_candidates)
    retained = retain_candidate(interval, valid_candidates, comparison)
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
