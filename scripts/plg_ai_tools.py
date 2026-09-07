#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from scripts import brain_compiler
from scripts import brain_doctor as brain_doctor_module
from scripts import creator_taste_prior
from scripts import long_form_rendering_loop
from scripts import performance_campaign
from scripts import performance_index
from scripts import performance_production_funnel as funnel
from scripts import persistent_act_runtime
from scripts import story_sync_engine


def _path(payload: dict[str, Any], key: str, default: str) -> Path:
    return Path(str(payload.get(key, default)))


def _optional_json_input(payload: dict[str, Any], value_key: str, path_key: str) -> dict[str, Any] | None:
    if value_key in payload and payload[value_key] is not None:
        value = payload[value_key]
        if not isinstance(value, dict):
            raise ValueError(f"{value_key} must be a JSON object")
        return value
    if path_key in payload and payload[path_key] is not None:
        value = json.loads(Path(str(payload[path_key])).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"{path_key} must contain a JSON object")
        return value
    return None


def _optional_json_list_input(payload: dict[str, Any], value_key: str, path_key: str) -> list[dict[str, Any]] | None:
    if value_key in payload and payload[value_key] is not None:
        value = payload[value_key]
    elif path_key in payload and payload[path_key] is not None:
        value = json.loads(Path(str(payload[path_key])).read_text(encoding="utf-8"))
    else:
        return None
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{value_key} or {path_key} must contain a JSON object or list of objects")
    return value


def _write_derived_output(payload: dict[str, Any], result: Any) -> None:
    output_path = payload.get("output_path")
    if output_path is None:
        return
    path = Path(str(output_path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def brain_for(payload: dict[str, Any]) -> dict[str, Any]:
    snapshot = _optional_json_input(payload, "github_snapshot", "github_snapshot_path")
    return brain_compiler.compile_brain(
        task=str(payload["task"]),
        repo_root=_path(payload, "repo_root", "."),
        registry_path=_path(payload, "registry_path", "state/brain/ROUTING_REGISTRY.json"),
        authority_branch=payload.get("authority_branch"),
        authority_sha=payload.get("authority_sha"),
        github_snapshot=snapshot,
    )


def brain_doctor(payload: dict[str, Any]) -> dict[str, Any]:
    snapshot = _optional_json_input(payload, "github_snapshot", "github_snapshot_path")
    return brain_doctor_module.run_doctor(
        repo_root=_path(payload, "repo_root", "."),
        registry_path=_path(payload, "registry_path", "state/brain/ROUTING_REGISTRY.json"),
        github_snapshot=snapshot,
    )


def compile_range(payload: dict[str, Any]) -> dict[str, Any]:
    start = int(payload.get("chapter_start", payload.get("chapter", 1)))
    end = int(payload.get("chapter_end", start))
    chapter_root = _path(payload, "chapter_root", "chapters")
    cache_root = _path(payload, "cache_root", ".cache/plg")
    compiled_root = cache_root / "compiler"
    scenes = 0
    written: list[str] = []
    for chapter in range(start, end + 1):
        path = chapter_root / f"{chapter:03d}.html"
        if not path.exists():
            raise ValueError(f"canonical chapter missing: {path.name}")
        paths = funnel.write_compiled_chapter(chapter, path.read_text(encoding="utf-8"), compiled_root)
        written.extend(p.as_posix() for p in paths)
        manifest = json.loads((compiled_root / f"{chapter:03d}" / "manifest.json").read_text(encoding="utf-8"))
        scenes += len(manifest.get("scene_order", []))
    index = performance_index.rebuild_index(compiled_root, cache_root / "project-index.sqlite")
    return {"chapter_start": start, "chapter_end": end, "scene_count": scenes, "written": written, "index": index}


def get_scene_view(payload: dict[str, Any]) -> dict[str, Any]:
    scene_id = str(payload["scene_id"]); view = str(payload["view"]); compiled_root = _path(payload, "compiled_root", ".cache/plg/compiler")
    return funnel.render_scene_view(funnel.load_scene_record(compiled_root, scene_id), view)


def query_scenes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    db_path = _path(payload, "db_path", ".cache/plg/project-index.sqlite")
    kwargs = {key: payload[key] for key in ("query", "scene_id", "chapter_start", "chapter_end", "token", "money", "verdict", "limit") if key in payload}
    return performance_index.query_scenes(db_path, **kwargs)


def plan_campaign(payload: dict[str, Any]) -> dict[str, Any]:
    return performance_campaign.plan_campaign(task=str(payload["task"]), chapter_start=int(payload["chapter_start"]), chapter_end=int(payload["chapter_end"]), source_authority=str(payload["source_authority"]), chapter_root=_path(payload, "chapter_root", "chapters"), cache_root=_path(payload, "cache_root", ".cache/plg"), profile=str(payload.get("profile", "eco")), executor=str(payload.get("executor", "codex")), model=payload.get("model"), reasoning_tier=payload.get("reasoning_tier"))


def run_campaign(payload: dict[str, Any]) -> dict[str, Any]:
    if "campaign_root" in payload:
        return performance_campaign.run_campaign(_path(payload, "campaign_root", ".cache/plg/campaigns"))
    plan = plan_campaign(payload); run = performance_campaign.run_campaign(Path(plan["campaign_root"]))
    return {"campaign_id": plan["campaign_id"], "campaign_root": plan["campaign_root"], "plan": plan, "run": run}


def get_campaign_result(payload: dict[str, Any]) -> dict[str, Any]: return performance_campaign.get_campaign_result(_path(payload, "campaign_root", ".cache/plg/campaigns"))
def reduce_campaign(payload: dict[str, Any]) -> dict[str, Any]: return performance_campaign.reduce_campaign(_path(payload, "campaign_root", ".cache/plg/campaigns"))
def apply_survivors(payload: dict[str, Any]) -> dict[str, Any]: return performance_campaign.integrate_campaign(_path(payload, "campaign_root", ".cache/plg/campaigns"), _path(payload, "chapter_root", "chapters"), current_authority=str(payload["current_authority"]))


def sync_story(payload: dict[str, Any]) -> dict[str, Any]:
    state = _optional_json_input(payload, "state", "state_path")
    if state is None:
        raise ValueError("sync_story requires state or state_path")
    report = story_sync_engine.sync_story(state)
    report = creator_taste_prior.augment_sync_report(state, report)
    _write_derived_output(payload, report)
    return report


def run_story_rehearsal_cycle(payload: dict[str, Any]) -> dict[str, Any]:
    runtime_state = _optional_json_input(payload, "runtime", "runtime_path")
    if runtime_state is None:
        raise ValueError("run_story_rehearsal_cycle requires runtime or runtime_path")
    evidence = _optional_json_list_input(payload, "evidence", "evidence_path")
    creator_taste = _optional_json_input(payload, "creator_taste", "creator_taste_path")
    result = persistent_act_runtime.run_rehearsal_cycle(runtime_state, evidence=evidence, creator_taste=creator_taste)
    _write_derived_output(payload, result)
    return result


def run_story_rendering_cycle(payload: dict[str, Any]) -> dict[str, Any]:
    """Start or reduce one derived-only rendering step.

    Model generation/evaluation remains executor supplied. This surface only
    compiles packets and deterministically routes/retains returned evidence.
    """
    run = _optional_json_input(payload, "run", "run_path")
    if run is None:
        intervals = _optional_json_list_input(payload, "intervals", "intervals_path")
        if intervals is None:
            raise ValueError("run_story_rendering_cycle requires run/run_path or intervals/intervals_path")
        result = long_form_rendering_loop.start_rendering_run(
            intervals,
            attempt_budget_default=int(payload.get("attempt_budget_default", 2)),
            rendering_memory=list(payload.get("rendering_memory", [])),
        )
    else:
        returned_attempt = _optional_json_input(payload, "returned_attempt", "returned_attempt_path")
        if returned_attempt is None:
            raise ValueError("an existing rendering run requires returned_attempt or returned_attempt_path")
        result = long_form_rendering_loop.advance_rendering_run(run, returned_attempt)
    _write_derived_output(payload, result)
    return result


TOOLS: dict[str, Callable[[dict[str, Any]], Any]] = {
    "brain_for": brain_for, "brain_doctor": brain_doctor,
    "compile_range": compile_range, "get_scene_view": get_scene_view, "query_scenes": query_scenes,
    "plan_campaign": plan_campaign, "run_campaign": run_campaign, "get_campaign_result": get_campaign_result,
    "reduce_campaign": reduce_campaign, "sync_story": sync_story,
    "run_story_rehearsal_cycle": run_story_rehearsal_cycle,
    "run_story_rendering_cycle": run_story_rendering_cycle,
    "apply_survivors": apply_survivors,
}

TOOL_SPECS = {
    "brain_for": {"write": False, "read_only": True, "description": "Compile a compact task-specific PLG brain routing packet from durable repository metadata."},
    "brain_doctor": {"write": False, "read_only": True, "description": "Check PLG brain routing health and drift without modifying repository state."},
    "compile_range": {"write": False, "read_only": False, "description": "Compile a canonical chapter range into disposable scene state and rebuild the project index."},
    "get_scene_view": {"write": False, "read_only": True, "description": "Return one narrow compiler view for an exact stable scene ID."},
    "query_scenes": {"write": False, "read_only": True, "description": "Resolve compact scene pointers through the rebuildable SQLite/FTS index."},
    "plan_campaign": {"write": False, "read_only": False, "description": "Plan a bounded campaign, compile scope, and suppress cache-valid work."},
    "run_campaign": {"write": False, "read_only": False, "description": "Plan if needed, then execute derived-only campaign packets with bounded concurrency."},
    "get_campaign_result": {"write": False, "read_only": True, "description": "Return the compact reduced result for a campaign."},
    "reduce_campaign": {"write": False, "read_only": False, "description": "Recompute deterministic campaign reduction without model work."},
    "sync_story": {"write": False, "read_only": False, "description": "Synchronize long-form possibilities, discoveries, propagation, convergence, hidden canon, reader dependencies, and optional creator-taste rehearsal hints without mutating canon prose."},
    "run_story_rehearsal_cycle": {"write": False, "read_only": False, "description": "Run one derived-only four-persistent-act REHEARSAL/STORY SYNC cycle, optionally integrating compact experimental evidence and creator-taste search hints."},
    "run_story_rendering_cycle": {"write": False, "read_only": False, "description": "Start or reduce a derived-only prose rendering cycle with targeted reprompting, candidate comparison, forward-motion budgeting, and precise escalation back to REHEARSAL."},
    "apply_survivors": {"write": True, "read_only": False, "description": "Sequentially validate and apply authorized surviving canon patches."},
}


def call_tool(name: str, payload: dict[str, Any]) -> Any:
    tool = TOOLS.get(name)
    if tool is None: raise ValueError(f"unknown PLG AI tool: {name}")
    if not isinstance(payload, dict): raise ValueError("tool payload must be a JSON object")
    return tool(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stable JSON tool interface for PLG compiler/campaign operations."); sub = parser.add_subparsers(dest="command", required=True); call = sub.add_parser("call"); call.add_argument("tool", choices=sorted(TOOLS)); source = call.add_mutually_exclusive_group(required=True); source.add_argument("--json"); source.add_argument("--json-file", type=Path); args = parser.parse_args(argv)
    raw = args.json if args.json is not None else args.json_file.read_text(encoding="utf-8"); payload = json.loads(raw)
    if not isinstance(payload, dict): raise ValueError("tool payload must be a JSON object")
    print(json.dumps(call_tool(args.tool, payload), ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": raise SystemExit(main())
