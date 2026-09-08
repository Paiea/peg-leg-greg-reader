from __future__ import annotations

from copy import deepcopy
from typing import Any


TIME_ACTION_SCHEMA = "story_time_action_contract/v1"
GAP_MODES = {
    "continuous_scene",
    "compressed_repetition",
    "off_camera_gap",
    "deliberate_skip",
}


def _list(value: object, *, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{field} must be a list of nonempty strings")
    return list(value)


def compile_time_action_contract(interval: dict[str, Any]) -> dict[str, Any]:
    """Compile derived temporal/action pressure for one story interval.

    This helper does not invent canon or require a time jump. It makes elapsed
    causality and action residue explicit enough for REHEARSAL, STORY SYNC, or
    PROSE to test instead of defaulting to camera-on-every-day continuity.
    """
    if not isinstance(interval, dict) or not str(interval.get("id", "")).strip():
        raise ValueError("time/action contract requires interval id")

    raw_time = interval.get("time", {}) or {}
    raw_action = interval.get("action", {}) or {}
    if not isinstance(raw_time, dict) or not isinstance(raw_action, dict):
        raise ValueError("time and action must be objects")

    gap_mode = str(raw_time.get("gap_mode", "continuous_scene"))
    if gap_mode not in GAP_MODES:
        raise ValueError(f"gap_mode must be one of {sorted(GAP_MODES)}")

    time = {
        "gap_mode": gap_mode,
        "elapsed_hint": str(raw_time.get("elapsed_hint", "")).strip() or None,
        "off_camera_changes": _list(raw_time.get("off_camera_changes"), field="off_camera_changes"),
        "growth_allowed": _list(raw_time.get("growth_allowed"), field="growth_allowed"),
        "decay_risks": _list(raw_time.get("decay_risks"), field="decay_risks"),
        "missed_opportunities": _list(raw_time.get("missed_opportunities"), field="missed_opportunities"),
        "routine_changes": _list(raw_time.get("routine_changes"), field="routine_changes"),
    }
    action = {
        "pressure_sources": _list(raw_action.get("pressure_sources"), field="pressure_sources"),
        "physical_constraints": _list(raw_action.get("physical_constraints"), field="physical_constraints"),
        "state_changes": _list(raw_action.get("state_changes"), field="state_changes"),
        "residue": _list(raw_action.get("residue"), field="residue"),
        "win_condition_changes": _list(raw_action.get("win_condition_changes"), field="win_condition_changes"),
        "independent_vectors": _list(raw_action.get("independent_vectors"), field="independent_vectors"),
    }

    elapsed_evidence = (
        time["off_camera_changes"]
        + time["growth_allowed"]
        + time["decay_risks"]
        + time["missed_opportunities"]
        + time["routine_changes"]
    )
    temporal_weight = gap_mode == "continuous_scene" or bool(elapsed_evidence)

    action_active = bool(action["pressure_sources"] or action["physical_constraints"] or action["win_condition_changes"])
    action_residue = (not action_active) or bool(action["state_changes"] or action["residue"])

    warnings: list[str] = []
    if gap_mode != "continuous_scene" and not elapsed_evidence:
        warnings.append("time_gap_without_state_change")
    if action_active and not (action["state_changes"] or action["residue"]):
        warnings.append("action_without_residue")

    return {
        "schema": TIME_ACTION_SCHEMA,
        "authority": "derived_pressure_only",
        "canon_write_authorized": False,
        "interval_id": interval["id"],
        "time": time,
        "action": action,
        "checks": {
            "temporal_weight": temporal_weight,
            "action_residue": action_residue,
        },
        "warnings": warnings,
        "questions": [
            "What changed while the camera was off, including things the protagonist did not control?",
            "What became easier, harder, more expensive, colder, stronger, obsolete, or unavailable because time passed?",
            "What did waiting cost, and what did repetition earn?",
            "What action changed the next available state rather than merely filling pages with motion?",
            "Did the win condition change when new pressure arrived?",
            "What material, bodily, economic, relational, reputational, or procedural residue survives after the exciting beat?",
            "Which other people or systems continued acting independently during the scene or gap?",
        ],
        "rendering_principles": [
            "Do not keep the camera on every day merely to prove continuity.",
            "Do not announce elapsed time when changed state can prove it more naturally.",
            "Allow larger earned gains when enough plausible time has passed; allow equally large decay, missed opportunity, and social drift.",
            "Action includes thought, speech, sex, work, violence, movement, and decision when they constrain what can happen next.",
            "If an event leaves no changed state, test whether it is empty spectacle, a deliberately transient beat, or missing residue.",
            "Treat time as off-camera causality, not a neutral spacer between scenes.",
        ],
        "source": deepcopy(interval),
    }
