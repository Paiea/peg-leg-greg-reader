from __future__ import annotations

from copy import deepcopy
from typing import Any


RENDERABILITY_SCHEMA = "renderability_report/v1"
STALENESS_SCHEMA = "render_staleness_report/v1"


def _score(value: Any, key: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{key} must be between 0 and 1")
    return number


def capture_dependencies(region: dict[str, Any]) -> dict[str, str]:
    """Capture only dependencies the region declares it actually consumes."""
    dependencies: dict[str, str] = {}
    for dependency in region.get("incoming_dependencies", []):
        dependency_id = str(dependency.get("id", "")).strip()
        version = str(dependency.get("version", "")).strip()
        if not dependency_id or not version:
            raise ValueError("render dependency requires id and version")
        if dependency_id in dependencies and dependencies[dependency_id] != version:
            raise ValueError(f"conflicting versions for render dependency: {dependency_id}")
        dependencies[dependency_id] = version
    return dependencies


def assess_renderability(
    region: dict[str, Any],
    *,
    stability_threshold: float = 0.6,
    invalidation_threshold: float = 0.5,
) -> dict[str, Any]:
    """Decide whether one local interval is safe enough to render.

    This is deliberately local. Open questions elsewhere in the book are recorded
    for observability but are not blockers unless the region declares a concrete
    incoming dependency or invalidation risk from them.
    """
    stability_threshold = _score(stability_threshold, "stability_threshold")
    invalidation_threshold = _score(invalidation_threshold, "invalidation_threshold")
    region_id = str(region.get("id", "")).strip()
    if not region_id:
        raise ValueError("renderable region requires id")

    blockers: list[str] = []
    if not region.get("state_in") or _score(region.get("state_in_stability", 0.0), "state_in_stability") < stability_threshold:
        blockers.append("state_in")
    if not str(region.get("required_movement", "")).strip() or _score(region.get("movement_confidence", 0.0), "movement_confidence") < stability_threshold:
        blockers.append("required_movement")
    if not region.get("character_state") or _score(region.get("character_state_confidence", 0.0), "character_state_confidence") < stability_threshold:
        blockers.append("character_state")

    dependencies = capture_dependencies(region)
    for dependency in region.get("incoming_dependencies", []):
        if not bool(dependency.get("required", True)):
            continue
        stability = _score(dependency.get("stability", 0.0), f"dependency:{dependency.get('id')}:stability")
        if stability < stability_threshold:
            blockers.append(f"dependency:{dependency['id']}")

    invalidation_risks: list[dict[str, Any]] = []
    for risk in region.get("unresolved_risks", []):
        probability = _score(risk.get("invalidation_probability", 0.0), f"risk:{risk.get('id')}:invalidation_probability")
        normalized = deepcopy(risk)
        normalized["invalidation_probability"] = probability
        invalidation_risks.append(normalized)
        if probability >= invalidation_threshold:
            blockers.append(f"risk:{risk['id']}")

    safe_uncertainty: list[str] = []
    unsafe_uncertainty: list[str] = []
    for uncertainty in region.get("remaining_uncertainty", []):
        uncertainty_id = str(uncertainty.get("id", "")).strip()
        if not uncertainty_id:
            continue
        if bool(uncertainty.get("safe_to_discover_in_prose", False)):
            safe_uncertainty.append(uncertainty_id)
        else:
            unsafe_uncertainty.append(uncertainty_id)
            blockers.append(f"uncertainty:{uncertainty_id}")

    global_open = [
        str(item.get("id"))
        for item in region.get("global_uncertainty", [])
        if item.get("id") and str(item.get("status", "open")) not in {"resolved", "closed", "retired"}
    ]

    return {
        "schema": RENDERABILITY_SCHEMA,
        "authority": "derived_only",
        "canon_write_authorized": False,
        "region_id": region_id,
        "act": region.get("act"),
        "renderable": not blockers,
        "blockers": blockers,
        "dependency_snapshot": dependencies,
        "invalidation_risks": invalidation_risks,
        "safe_prose_uncertainty": safe_uncertainty,
        "unsafe_local_uncertainty": unsafe_uncertainty,
        "ignored_global_uncertainty": global_open,
        "decision": "render" if not blockers else "blocked",
    }


def assess_staleness(candidate_dependencies: dict[str, str], current_versions: dict[str, str]) -> dict[str, Any]:
    """Invalidate only when a dependency captured by the candidate changed."""
    changed: list[dict[str, str | None]] = []
    for dependency_id in sorted(candidate_dependencies):
        candidate_version = str(candidate_dependencies[dependency_id])
        if dependency_id not in current_versions:
            changed.append({
                "id": dependency_id,
                "candidate_version": candidate_version,
                "current_version": None,
                "reason": "missing_current_dependency",
            })
            continue
        current_version = str(current_versions[dependency_id])
        if candidate_version != current_version:
            changed.append({
                "id": dependency_id,
                "candidate_version": candidate_version,
                "current_version": current_version,
                "reason": "version_changed",
            })
    return {
        "schema": STALENESS_SCHEMA,
        "authority": "derived_only",
        "canon_write_authorized": False,
        "stale": bool(changed),
        "changed_dependencies": changed,
        "tracked_dependency_count": len(candidate_dependencies),
    }
