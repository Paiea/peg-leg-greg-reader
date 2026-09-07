#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from scripts import performance_campaign
from scripts import performance_index
from scripts import performance_production_funnel as funnel


def _path(payload: dict[str, Any], key: str, default: str) -> Path:
    return Path(str(payload.get(key, default)))


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
    scene_id = str(payload["scene_id"])
    view = str(payload["view"])
    compiled_root = _path(payload, "compiled_root", ".cache/plg/compiler")
    record = funnel.load_scene_record(compiled_root, scene_id)
    return funnel.render_scene_view(record, view)


def query_scenes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    db_path = _path(payload, "db_path", ".cache/plg/project-index.sqlite")
    kwargs = {
        key: payload[key]
        for key in ("query", "scene_id", "chapter_start", "chapter_end", "token", "money", "verdict", "limit")
        if key in payload
    }
    return performance_index.query_scenes(db_path, **kwargs)


def plan_campaign(payload: dict[str, Any]) -> dict[str, Any]:
    return performance_campaign.plan_campaign(
        task=str(payload["task"]),
        chapter_start=int(payload["chapter_start"]),
        chapter_end=int(payload["chapter_end"]),
        source_authority=str(payload["source_authority"]),
        chapter_root=_path(payload, "chapter_root", "chapters"),
        cache_root=_path(payload, "cache_root", ".cache/plg"),
        profile=str(payload.get("profile", "eco")),
        executor=str(payload.get("executor", "codex")),
    )


def run_campaign(payload: dict[str, Any]) -> dict[str, Any]:
    return performance_campaign.run_campaign(_path(payload, "campaign_root", ".cache/plg/campaigns"))


def get_campaign_result(payload: dict[str, Any]) -> dict[str, Any]:
    return performance_campaign.get_campaign_result(_path(payload, "campaign_root", ".cache/plg/campaigns"))


def reduce_campaign(payload: dict[str, Any]) -> dict[str, Any]:
    return performance_campaign.reduce_campaign(_path(payload, "campaign_root", ".cache/plg/campaigns"))


def apply_survivors(payload: dict[str, Any]) -> dict[str, Any]:
    return performance_campaign.integrate_campaign(
        _path(payload, "campaign_root", ".cache/plg/campaigns"),
        _path(payload, "chapter_root", "chapters"),
        current_authority=str(payload["current_authority"]),
    )


TOOLS: dict[str, Callable[[dict[str, Any]], Any]] = {
    "compile_range": compile_range,
    "get_scene_view": get_scene_view,
    "query_scenes": query_scenes,
    "plan_campaign": plan_campaign,
    "run_campaign": run_campaign,
    "get_campaign_result": get_campaign_result,
    "reduce_campaign": reduce_campaign,
    "apply_survivors": apply_survivors,
}

TOOL_SPECS = {
    "compile_range": {"write": False, "description": "Compile a canonical chapter range into disposable scene state and rebuild the project index."},
    "get_scene_view": {"write": False, "description": "Return one narrow compiler view for an exact stable scene ID."},
    "query_scenes": {"write": False, "description": "Resolve compact scene pointers through the rebuildable SQLite/FTS index."},
    "plan_campaign": {"write": False, "description": "Plan a bounded campaign, compile scope, and suppress cache-valid work."},
    "run_campaign": {"write": False, "description": "Execute planned derived-only campaign packets with bounded concurrency."},
    "get_campaign_result": {"write": False, "description": "Return the compact reduced result for a campaign."},
    "reduce_campaign": {"write": False, "description": "Recompute deterministic campaign reduction without model work."},
    "apply_survivors": {"write": True, "description": "Sequentially validate and apply authorized surviving canon patches."},
}


def call_tool(name: str, payload: dict[str, Any]) -> Any:
    tool = TOOLS.get(name)
    if tool is None:
        raise ValueError(f"unknown PLG AI tool: {name}")
    if not isinstance(payload, dict):
        raise ValueError("tool payload must be a JSON object")
    return tool(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stable JSON tool interface for PLG compiler/campaign operations.")
    sub = parser.add_subparsers(dest="command", required=True)
    call = sub.add_parser("call")
    call.add_argument("tool", choices=sorted(TOOLS))
    source = call.add_mutually_exclusive_group(required=True)
    source.add_argument("--json")
    source.add_argument("--json-file", type=Path)
    args = parser.parse_args(argv)
    raw = args.json if args.json is not None else args.json_file.read_text(encoding="utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("tool payload must be a JSON object")
    print(json.dumps(call_tool(args.tool, payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
