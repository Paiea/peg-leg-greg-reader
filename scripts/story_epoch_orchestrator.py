#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from typing import Any

PLAN_SCHEMA = "story_epoch_plan/v1"
REDUCTION_SCHEMA = "story_epoch_reduction/v1"
CONTINUATION_SCHEMA = "story_epoch_continuation/v1"
ACT_IDS = ("act-i", "act-ii", "act-iii", "act-iv")
PHASES = {"explore", "compare", "converge", "render", "repair"}
LANES = {"dream", "rehearsal", "performance", "render", "stale_repair"}
SIGNALS = (
    "information_gain",
    "uncertainty_reduction",
    "downstream_reach",
    "novelty",
    "dramatic_importance",
    "render_readiness",
    "staleness",
)

_PHASE_WEIGHTS: dict[str, dict[str, float]] = {
    "explore": {
        "information_gain": 0.24,
        "uncertainty_reduction": 0.18,
        "downstream_reach": 0.16,
        "novelty": 0.24,
        "dramatic_importance": 0.14,
        "render_readiness": 0.02,
        "staleness": 0.02,
    },
    "compare": {
        "information_gain": 0.18,
        "uncertainty_reduction": 0.26,
        "downstream_reach": 0.16,
        "novelty": 0.10,
        "dramatic_importance": 0.18,
        "render_readiness": 0.04,
        "staleness": 0.08,
    },
    "converge": {
        "information_gain": 0.12,
        "uncertainty_reduction": 0.30,
        "downstream_reach": 0.20,
        "novelty": 0.04,
        "dramatic_importance": 0.20,
        "render_readiness": 0.08,
        "staleness": 0.06,
    },
    "render": {
        "information_gain": 0.06,
        "uncertainty_reduction": 0.08,
        "downstream_reach": 0.10,
        "novelty": 0.03,
        "dramatic_importance": 0.20,
        "render_readiness": 0.46,
        "staleness": 0.07,
    },
    "repair": {
        "information_gain": 0.03,
        "uncertainty_reduction": 0.10,
        "downstream_reach": 0.10,
        "novelty": 0.02,
        "dramatic_importance": 0.22,
        "render_readiness": 0.03,
        "staleness": 0.50,
    },
}

_LANE_BIAS: dict[str, dict[str, float]] = {
    "explore": {"dream": 0.20, "rehearsal": 0.16, "performance": 0.10},
    "compare": {"rehearsal": 0.20, "performance": 0.18, "dream": 0.04},
    "converge": {"rehearsal": 0.20, "performance": 0.16, "stale_repair": 0.10},
    "render": {"render": 0.70, "stale_repair": 0.10},
    "repair": {"stale_repair": 0.90, "render": 0.05},
}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_snapshot(snapshot: dict[str, Any]) -> None:
    if not isinstance(snapshot, dict):
        raise ValueError("epoch snapshot must be an object")
    if not isinstance(snapshot.get("epoch_number"), int) or snapshot["epoch_number"] < 0:
        raise ValueError("epoch snapshot requires nonnegative epoch_number")
    if not _nonempty(snapshot.get("story_state_version")):
        raise ValueError("epoch snapshot requires story_state_version")
    phase = snapshot.get("phase")
    if phase not in PHASES:
        raise ValueError(f"epoch phase must be one of: {', '.join(sorted(PHASES))}")
    frontier = snapshot.get("frontier")
    if not isinstance(frontier, list):
        raise ValueError("epoch snapshot requires frontier list")
    seen: set[str] = set()
    for task in frontier:
        _validate_frontier_task(task)
        if task["id"] in seen:
            raise ValueError(f"duplicate frontier task id: {task['id']}")
        seen.add(task["id"])


def _validate_frontier_task(task: dict[str, Any]) -> None:
    if not isinstance(task, dict):
        raise ValueError("frontier task must be an object")
    for field in ("id", "lane", "target_id"):
        if not _nonempty(task.get(field)):
            raise ValueError(f"frontier task requires {field}")
    if task["lane"] not in LANES:
        raise ValueError(f"invalid frontier lane: {task['lane']}")
    act = task.get("act")
    if act is not None and act not in ACT_IDS:
        raise ValueError("frontier task act must be one of the four persistent acts")
    cost = task.get("expected_cost")
    if isinstance(cost, bool) or not isinstance(cost, int) or cost <= 0:
        raise ValueError("frontier task expected_cost must be a positive integer")
    signals = task.get("priority_signals")
    if not isinstance(signals, dict):
        raise ValueError("frontier task requires priority_signals")
    for signal in SIGNALS:
        value = signals.get(signal, 0.0)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            raise ValueError(f"priority signal {signal} must be between 0 and 1")
    stop_conditions = task.get("stop_conditions", [])
    if not isinstance(stop_conditions, list) or any(not _nonempty(item) for item in stop_conditions):
        raise ValueError("frontier task stop_conditions must be a list of nonempty strings")


def _score(task: dict[str, Any], phase: str) -> float:
    signals = task["priority_signals"]
    weighted = sum(float(signals.get(name, 0.0)) * weight for name, weight in _PHASE_WEIGHTS[phase].items())
    weighted += _LANE_BIAS.get(phase, {}).get(task["lane"], 0.0)
    return weighted / task["expected_cost"]


def _work_order(task: dict[str, Any], *, snapshot_version: str, phase: str) -> dict[str, Any]:
    item = deepcopy(task)
    item["snapshot_version"] = snapshot_version
    item["budget_cap"] = int(task["expected_cost"])
    item["priority_score"] = round(_score(task, phase), 6)
    item["authority"] = "derived_work_order"
    item["canon_write_authorized"] = False
    return item


def _best_per_act(frontier: list[dict[str, Any]], phase: str) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for act_id in ACT_IDS:
        candidates = [task for task in frontier if task.get("act") == act_id]
        if not candidates:
            continue
        selected.append(max(candidates, key=lambda item: (_score(item, phase), -frontier.index(item))))
    return selected


def plan_epoch(snapshot: dict[str, Any], *, budget_units: int) -> dict[str, Any]:
    """Plan one bounded parallel work epoch from an immutable story snapshot.

    Workers receive only derived work orders tied to the same story-state version.
    Integration is deliberately excluded from this function and must happen later,
    serially, through the reduction queue.
    """
    _validate_snapshot(snapshot)
    if isinstance(budget_units, bool) or not isinstance(budget_units, int) or budget_units <= 0:
        raise ValueError("budget_units must be a positive integer")

    phase = snapshot["phase"]
    frontier = deepcopy(snapshot["frontier"])
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    spent = 0

    baseline = _best_per_act(frontier, phase)
    baseline_cost = sum(task["expected_cost"] for task in baseline)
    if baseline and len({task.get("act") for task in baseline}) == len(ACT_IDS) and baseline_cost <= budget_units:
        for task in baseline:
            selected.append(task)
            selected_ids.add(task["id"])
            spent += task["expected_cost"]

    ranked = sorted(
        (task for task in frontier if task["id"] not in selected_ids),
        key=lambda item: (-_score(item, phase), item["expected_cost"], item["id"]),
    )
    for task in ranked:
        cost = task["expected_cost"]
        if spent + cost > budget_units:
            continue
        selected.append(task)
        selected_ids.add(task["id"])
        spent += cost
        if spent == budget_units:
            break

    orders = [
        _work_order(task, snapshot_version=snapshot["story_state_version"], phase=phase)
        for task in selected
    ]
    return {
        "schema": PLAN_SCHEMA,
        "epoch_number": snapshot["epoch_number"],
        "snapshot_version": snapshot["story_state_version"],
        "phase": phase,
        "budget_units": budget_units,
        "allocated_budget": spent,
        "tasks": orders,
        "authority": "derived_only",
        "integration_policy": "workers_propose_evidence_and_deltas; serial_reducer_decides_what_moves_forward",
        "canon_write_authorized": False,
    }


def _validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict) or plan.get("schema") != PLAN_SCHEMA:
        raise ValueError(f"epoch plan schema must be {PLAN_SCHEMA}")
    if not _nonempty(plan.get("snapshot_version")):
        raise ValueError("epoch plan requires snapshot version")
    if not isinstance(plan.get("tasks"), list):
        raise ValueError("epoch plan requires tasks list")


def reduce_epoch_results(plan: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    """Collect worker returns without mutating story state or granting story authority."""
    _validate_plan(plan)
    if not isinstance(results, list):
        raise ValueError("epoch results must be a list")

    tasks_by_id = {task["id"]: task for task in plan["tasks"]}
    completed_ids: set[str] = set()
    retired_targets: list[str] = []
    integration_queue: list[dict[str, Any]] = []
    worker_results: list[dict[str, Any]] = []

    for result in results:
        if not isinstance(result, dict):
            raise ValueError("worker result must be an object")
        task_id = result.get("task_id")
        if task_id not in tasks_by_id:
            raise ValueError(f"unknown epoch task: {task_id}")
        if result.get("snapshot_version") != plan["snapshot_version"]:
            raise ValueError("worker snapshot version does not match epoch plan snapshot version")
        status = result.get("status")
        if status not in {"completed", "blocked", "failed", "skipped"}:
            raise ValueError("worker result requires valid status")
        if task_id in completed_ids:
            raise ValueError(f"duplicate worker result for task: {task_id}")
        completed_ids.add(task_id)
        task = tasks_by_id[task_id]

        proposed_delta = result.get("proposed_delta")
        if proposed_delta is not None:
            if not isinstance(proposed_delta, dict):
                raise ValueError("proposed_delta must be an object")
            integration_queue.append({
                "kind": "proposed_delta",
                "task_id": task_id,
                "target_id": task["target_id"],
                "snapshot_version": plan["snapshot_version"],
                "payload": deepcopy(proposed_delta),
                "authority": "proposal_only",
            })

        evidence = result.get("evidence", [])
        if not isinstance(evidence, list) or any(not isinstance(item, dict) for item in evidence):
            raise ValueError("worker evidence must be a list of objects")
        for item in evidence:
            integration_queue.append({
                "kind": "evidence",
                "task_id": task_id,
                "target_id": task["target_id"],
                "snapshot_version": plan["snapshot_version"],
                "payload": deepcopy(item),
                "authority": "evidence_only",
            })

        if result.get("retire_target") is True and task["target_id"] not in retired_targets:
            retired_targets.append(task["target_id"])
        worker_results.append(deepcopy(result))

    remaining_tasks = [deepcopy(task) for task in plan["tasks"] if task["id"] not in completed_ids]
    return {
        "schema": REDUCTION_SCHEMA,
        "epoch_number": plan.get("epoch_number"),
        "snapshot_version": plan["snapshot_version"],
        "phase": plan.get("phase"),
        "integration_queue": integration_queue,
        "retired_targets": retired_targets,
        "remaining_tasks": remaining_tasks,
        "worker_results": worker_results,
        "authority": "derived_only",
        "integration_required": bool(integration_queue),
        "canon_write_authorized": False,
    }


def compile_next_epoch_packet(
    snapshot: dict[str, Any],
    reduction: dict[str, Any],
    *,
    continuation_hint: str,
) -> dict[str, Any]:
    """Compile a hot-start handoff that preserves frontier state and avoids re-derivation."""
    _validate_snapshot(snapshot)
    if not isinstance(reduction, dict) or reduction.get("schema") != REDUCTION_SCHEMA:
        raise ValueError(f"epoch reduction schema must be {REDUCTION_SCHEMA}")
    if reduction.get("snapshot_version") != snapshot["story_state_version"]:
        raise ValueError("epoch reduction snapshot version does not match story snapshot version")
    if not _nonempty(continuation_hint):
        raise ValueError("continuation_hint must be nonempty")

    do_not_revisit = list(snapshot.get("do_not_revisit", []))
    for target_id in reduction.get("retired_targets", []):
        if target_id not in do_not_revisit:
            do_not_revisit.append(target_id)

    remaining = list(reduction.get("remaining_tasks", []))
    highest_value_targets = [
        {
            "task_id": task["id"],
            "target_id": task["target_id"],
            "lane": task["lane"],
            "act": task.get("act"),
            "priority_score": task.get("priority_score", 0.0),
        }
        for task in sorted(remaining, key=lambda item: (-float(item.get("priority_score", 0.0)), item["id"]))[:8]
    ]

    return {
        "schema": CONTINUATION_SCHEMA,
        "epoch_number": snapshot["epoch_number"] + 1,
        "story_state_version": snapshot["story_state_version"],
        "phase": snapshot["phase"],
        "renderable_regions": deepcopy(snapshot.get("renderable_regions", [])),
        "blocked_regions": deepcopy(snapshot.get("blocked_regions", [])),
        "stale_candidates": deepcopy(snapshot.get("stale_candidates", [])),
        "active_render_candidates": deepcopy(snapshot.get("active_render_candidates", [])),
        "performance_queue": deepcopy(snapshot.get("performance_queue", [])),
        "contradictions": deepcopy(snapshot.get("contradictions", [])),
        "convergence": deepcopy(snapshot.get("convergence", {})),
        "integration_queue": deepcopy(reduction.get("integration_queue", [])),
        "highest_value_targets": highest_value_targets,
        "do_not_revisit": do_not_revisit,
        "continuation_hint": continuation_hint,
        "authority": "derived_only_hot_start",
        "canon_write_authorized": False,
    }
