from __future__ import annotations

from copy import deepcopy
from typing import Any


CANDIDATE_SCHEMA = "dream_candidate/v1"
REHEARSAL_PROBE_SCHEMA = "dream_rehearsal_probe/v1"

REPRESENTATIONS = {
    "causal_graph",
    "timeline",
    "state_transition",
    "counterfactual_worldline",
    "backward_prerequisite",
    "dialogue",
    "performance",
    "interiority",
    "compressed_summary",
    "reader_experience",
    "prose",
    "backward_retelling",
}

SEARCH_LENSES = {
    "romance",
    "horror_failure",
    "comedy",
    "mechanic_exploitation",
    "social_consequence",
    "reversal",
    "mundane_human_behavior",
    "strange_but_causal",
    "genre_default_destroyer",
    "reader_desire",
    "protagonist_nightmare",
    "unnoticed_consequence",
}


def _unit_score(value: Any, key: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{key} must be between 0 and 1")
    return number


def _normalize_scores(scores: dict[str, Any] | None = None) -> dict[str, float]:
    supplied = scores or {}
    return {
        "surprise": _unit_score(supplied.get("surprise", 0.0), "surprise"),
        "causality": _unit_score(supplied.get("causality", 0.0), "causality"),
        "reach": _unit_score(supplied.get("reach", 0.0), "reach"),
        "novelty_distance": _unit_score(supplied.get("novelty_distance", 0.0), "novelty_distance"),
        "form_information_gain": _unit_score(supplied.get("form_information_gain", 0.0), "form_information_gain"),
    }


def _normalize_concepts(values: list[str] | tuple[str, ...] | None) -> list[str]:
    return sorted({str(value).strip() for value in (values or []) if str(value).strip()})


def _validate_representation(representation: str) -> str:
    representation = str(representation)
    if representation not in REPRESENTATIONS:
        raise ValueError(f"unsupported DREAM representation: {representation}")
    return representation


def build_candidate(
    *,
    candidate_id: str,
    source: dict[str, Any],
    summary: str,
    concept_keys: list[str],
    affected_dimensions: list[str] | None = None,
    representation: str = "causal_graph",
    mutation_operator: str = "seed",
    search_lens: str = "strange_but_causal",
    scores: dict[str, Any] | None = None,
    cheap_causal_test: dict[str, Any] | None = None,
    parents: list[str] | None = None,
    contradictions: list[str] | None = None,
    status: str = "generated",
) -> dict[str, Any]:
    """Normalize one executor-supplied speculative mutation.

    DREAM is deliberately permissive about content and deliberately strict about
    authority. This reducer never promotes a possibility into story state.
    """
    candidate_id = str(candidate_id).strip()
    if not candidate_id:
        raise ValueError("DREAM candidate requires a stable id")
    if not isinstance(source, dict) or not source.get("kind") or not source.get("id"):
        raise ValueError("DREAM candidate source requires kind and id")
    representation = _validate_representation(representation)
    search_lens = str(search_lens)
    if search_lens not in SEARCH_LENSES:
        raise ValueError(f"unsupported DREAM search lens: {search_lens}")
    causal = deepcopy(cheap_causal_test or {"status": "untested", "reasons": []})
    if causal.get("status") not in {"untested", "pass", "fail", "counterfactual_only"}:
        raise ValueError("cheap causal test status must be untested/pass/fail/counterfactual_only")
    causal.setdefault("reasons", [])
    return {
        "schema": CANDIDATE_SCHEMA,
        "id": candidate_id,
        "source": deepcopy(source),
        "parents": list(parents or []),
        "content": {
            "summary": str(summary),
            "concept_keys": _normalize_concepts(concept_keys),
            "affected_dimensions": _normalize_concepts(affected_dimensions),
        },
        "representation": representation,
        "mutation_operator": str(mutation_operator),
        "search_lens": search_lens,
        "authority": "none",
        "canon_write_authorized": False,
        "contradictions": list(contradictions or []),
        "scores": _normalize_scores(scores),
        "cheap_causal_test": causal,
        "status": str(status),
    }


def candidate_value(candidate: dict[str, Any]) -> float:
    """Transparent search value, not evidence strength or story authority."""
    causal_status = candidate.get("cheap_causal_test", {}).get("status")
    if causal_status == "fail":
        return 0.0
    scores = _normalize_scores(candidate.get("scores", {}))
    base = scores["surprise"] * scores["causality"] * scores["reach"]
    value = base + (0.15 * scores["novelty_distance"]) + (0.05 * scores["form_information_gain"])
    return round(min(1.2, max(0.0, value)), 6)


def conceptual_similarity(left: dict[str, Any], right: dict[str, Any]) -> float:
    a = set(left.get("content", {}).get("concept_keys", []))
    b = set(right.get("content", {}).get("concept_keys", []))
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def _form_gain(candidate: dict[str, Any]) -> float:
    return float(candidate.get("scores", {}).get("form_information_gain", 0.0))


def select_diverse_survivors(
    candidates: list[dict[str, Any]],
    *,
    limit: int,
    similarity_threshold: float = 0.75,
    form_diversity_gain_threshold: float = 0.25,
) -> dict[str, Any]:
    if limit < 1:
        raise ValueError("DREAM survivor limit must be at least one")
    if not 0.0 <= similarity_threshold <= 1.0:
        raise ValueError("similarity threshold must be between 0 and 1")

    decisions: dict[str, str] = {}
    viable: list[dict[str, Any]] = []
    for raw in candidates:
        candidate = deepcopy(raw)
        candidate_id = str(candidate.get("id", ""))
        if candidate.get("cheap_causal_test", {}).get("status") == "fail":
            decisions[candidate_id] = "cheap_causal_fail"
            continue
        viable.append(candidate)

    viable.sort(key=lambda item: (candidate_value(item), str(item.get("id", ""))), reverse=True)
    survivors: list[dict[str, Any]] = []
    for candidate in viable:
        candidate_id = str(candidate.get("id", ""))
        if len(survivors) >= limit:
            decisions.setdefault(candidate_id, "budget_exhausted")
            continue
        duplicate_of = None
        representation_exception = False
        for retained in survivors:
            if conceptual_similarity(candidate, retained) < similarity_threshold:
                continue
            duplicate_of = retained
            if candidate.get("representation") != retained.get("representation") and max(_form_gain(candidate), _form_gain(retained)) >= form_diversity_gain_threshold:
                representation_exception = True
                continue
            break
        else:
            duplicate_of = None

        if duplicate_of is not None and not representation_exception:
            decisions[candidate_id] = "duplicate_cluster"
            continue

        candidate["status"] = "survivor"
        survivors.append(candidate)
        decisions[candidate_id] = "survivor"

    return {
        "schema": "dream_survivor_selection/v1",
        "authority": "none",
        "canon_write_authorized": False,
        "survivors": survivors,
        "decisions": decisions,
    }


def _child_from_parent(
    parent: dict[str, Any],
    *,
    candidate_id: str,
    summary: str,
    concept_keys: list[str],
    operator: str,
    representation: str | None = None,
    scores: dict[str, Any] | None = None,
) -> dict[str, Any]:
    parent_scores = deepcopy(parent.get("scores", {}))
    if scores:
        parent_scores.update(scores)
    return build_candidate(
        candidate_id=candidate_id,
        source=deepcopy(parent["source"]),
        summary=summary,
        concept_keys=concept_keys,
        affected_dimensions=list(parent.get("content", {}).get("affected_dimensions", [])),
        representation=representation or str(parent.get("representation", "causal_graph")),
        mutation_operator=operator,
        search_lens=str(parent.get("search_lens", "strange_but_causal")),
        scores=parent_scores,
        cheap_causal_test={"status": "untested", "reasons": ["mutation requires fresh cheap causal test"]},
        parents=[str(parent["id"])],
        contradictions=list(parent.get("contradictions", [])),
    )


def mutate_candidate(
    parent: dict[str, Any],
    *,
    candidate_id: str,
    summary: str,
    concept_keys: list[str],
    operator: str,
    scores: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _child_from_parent(
        parent,
        candidate_id=candidate_id,
        summary=summary,
        concept_keys=concept_keys,
        operator=operator,
        scores=scores,
    )


def cross_candidates(
    left: dict[str, Any],
    right: dict[str, Any],
    *,
    candidate_id: str,
    summary: str,
    concept_keys: list[str],
    representation: str | None = None,
) -> dict[str, Any]:
    averaged = {}
    for key in ("surprise", "causality", "reach", "novelty_distance", "form_information_gain"):
        averaged[key] = (float(left.get("scores", {}).get(key, 0.0)) + float(right.get("scores", {}).get(key, 0.0))) / 2.0
    source = {
        "kind": "crossover",
        "id": f"{left['id']}+{right['id']}",
        "acts": sorted(set(left.get("source", {}).get("acts", [])) | set(right.get("source", {}).get("acts", []))),
    }
    return build_candidate(
        candidate_id=candidate_id,
        source=source,
        summary=summary,
        concept_keys=concept_keys,
        affected_dimensions=list(set(left.get("content", {}).get("affected_dimensions", [])) | set(right.get("content", {}).get("affected_dimensions", []))),
        representation=representation or str(left.get("representation", "causal_graph")),
        mutation_operator="crossover",
        search_lens=str(left.get("search_lens", "strange_but_causal")),
        scores=averaged,
        cheap_causal_test={"status": "untested", "reasons": ["crossover requires fresh cheap causal test"]},
        parents=[str(left["id"]), str(right["id"])],
    )


def shift_form(
    parent: dict[str, Any],
    *,
    candidate_id: str,
    representation: str,
    operator: str,
    form_information_gain: float = 0.0,
) -> dict[str, Any]:
    scores = deepcopy(parent.get("scores", {}))
    scores["form_information_gain"] = form_information_gain
    child = _child_from_parent(
        parent,
        candidate_id=candidate_id,
        summary=str(parent.get("content", {}).get("summary", "")),
        concept_keys=list(parent.get("content", {}).get("concept_keys", [])),
        operator=operator,
        representation=representation,
        scores=scores,
    )
    child["cheap_causal_test"] = deepcopy(parent.get("cheap_causal_test", {"status": "untested", "reasons": []}))
    return child


def compile_rehearsal_probe(candidate: dict[str, Any]) -> dict[str, Any]:
    representation = str(candidate.get("representation", "causal_graph"))
    if representation == "performance":
        mode = "performance"
    elif representation in {"counterfactual_worldline", "timeline", "backward_retelling"}:
        mode = "trajectory_worldline_test"
    elif representation in {"state_transition", "backward_prerequisite"}:
        mode = "state_transition_test"
    else:
        mode = "plausibility_probe"
    return {
        "schema": REHEARSAL_PROBE_SCHEMA,
        "authority": "derived_only_no_story_authority",
        "canon_write_authorized": False,
        "source_candidate_id": candidate["id"],
        "question": candidate.get("content", {}).get("summary", ""),
        "concept_keys": list(candidate.get("content", {}).get("concept_keys", [])),
        "representation": representation,
        "experiment_mode": mode,
        "instruction": "Test this speculative DREAM survivor. Return evidence only; do not promote it directly into story state.",
    }
