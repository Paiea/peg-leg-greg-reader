#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import shlex
import subprocess
import threading
import time
from typing import Any, Callable

from scripts import performance_index
from scripts import performance_production_funnel as funnel

TASK_VIEWS = {
    "reverse_edit": "comparison",
    "reverse-edit": "comparison",
    "dialogue_audit": "dialogue",
    "continuity_audit": "continuity",
    "illustration_reconcile": "illustration",
    "performance": "performance",
}
PROFILES = {
    "eco": {"max_workers": 2, "max_retries": 1},
    "standard": {"max_workers": 4, "max_retries": 1},
    "burst": {"max_workers": 8, "max_retries": 1},
}
_TELEMETRY_LOCK = threading.Lock()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object in {path}")
    return value


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _TELEMETRY_LOCK:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"expected object at {path}:{line_no}")
        rows.append(value)
    return rows


def _normalize_task(task: str) -> str:
    normalized = task.strip().lower().replace("-", "_")
    if normalized not in {key.replace("-", "_") for key in TASK_VIEWS}:
        raise ValueError(f"unsupported campaign task: {task}")
    return normalized


def _campaign_id(task: str, start: int, end: int, source_authority: str) -> str:
    if not source_authority.strip():
        raise ValueError("source_authority is required")
    return f"{task}-{start:03d}-{end:03d}-{source_authority[:8]}"


def _comparison_cache_valid(scene: dict[str, Any]) -> bool:
    comparison = scene.get("comparison")
    dependencies = scene.get("dependencies")
    if not isinstance(comparison, dict) or not isinstance(dependencies, dict):
        return False
    dep = dependencies.get("comparison")
    return isinstance(dep, dict) and bool(dep.get("compiler")) and bool(dep.get("dependency_hash"))


def _task_cache_valid(scene: dict[str, Any], task: str) -> bool:
    if task == "reverse_edit":
        return _comparison_cache_valid(scene)
    if task == "performance":
        return isinstance(scene.get("performance"), dict)
    if task == "dialogue_audit":
        return isinstance(scene.get("comparison"), dict)
    if task == "continuity_audit":
        return isinstance(scene.get("semantic"), dict) and not scene.get("semantic_conflicts")
    if task == "illustration_reconcile":
        return isinstance(scene.get("semantic"), dict)
    return False


def _packet_for_scene(scene: dict[str, Any], task: str) -> dict[str, Any]:
    scene_id = str(scene["scene_id"])
    source = scene.get("source") if isinstance(scene.get("source"), dict) else {}
    source_hash = str(source.get("hash", ""))
    view = TASK_VIEWS[task]
    missing_layers: list[str] = []
    if task == "reverse_edit":
        for key in ("semantic", "performance", "screenplay", "comparison"):
            if not isinstance(scene.get(key), dict):
                missing_layers.append(key)
    elif not _task_cache_valid(scene, task):
        missing_layers.append(task)
    dependency_hash = funnel.dependency_fingerprint(task, source_hash, view, missing_layers, funnel.COMPILER_VERSIONS)
    return {
        "schema": "performance_campaign_packet/v1",
        "packet_id": f"{scene_id}:{task}:{dependency_hash[:16]}",
        "scene_id": scene_id,
        "task": task,
        "view": view,
        "source_hash": source_hash,
        "dependency_hash": dependency_hash,
        "missing_layers": missing_layers,
        "creative_authority": False,
        "write_authority": "derived_only",
        "output_schema": "performance_scene_result/v1",
    }


def plan_campaign(
    *,
    task: str,
    chapter_start: int,
    chapter_end: int,
    source_authority: str,
    chapter_root: Path,
    cache_root: Path,
    profile: str = "eco",
    executor: str = "codex",
) -> dict[str, Any]:
    task = _normalize_task(task)
    if chapter_start < 1 or chapter_end < chapter_start:
        raise ValueError("invalid chapter range")
    if profile not in PROFILES:
        raise ValueError(f"unknown execution profile: {profile}")
    chapter_root = Path(chapter_root)
    cache_root = Path(cache_root)
    compiled_root = cache_root / "compiler"
    scenes: list[dict[str, Any]] = []
    for chapter in range(chapter_start, chapter_end + 1):
        path = chapter_root / f"{chapter:03d}.html"
        if not path.exists():
            raise ValueError(f"canonical chapter missing: {path.name}")
        funnel.write_compiled_chapter(chapter, path.read_text(encoding="utf-8"), compiled_root)
        manifest = _read_json(compiled_root / f"{chapter:03d}" / "manifest.json")
        for scene_id in manifest.get("scene_order", []):
            if isinstance(scene_id, str):
                scenes.append(funnel.load_scene_record(compiled_root, scene_id))

    db_path = cache_root / "project-index.sqlite"
    index_summary = performance_index.rebuild_index(compiled_root, db_path)
    campaign_id = _campaign_id(task, chapter_start, chapter_end, source_authority)
    campaign_root = cache_root / "campaigns" / campaign_id
    campaign_root.mkdir(parents=True, exist_ok=True)
    packets: list[dict[str, Any]] = []
    cache_hits = 0
    for scene in scenes:
        if _task_cache_valid(scene, task):
            cache_hits += 1
        else:
            packets.append(_packet_for_scene(scene, task))

    campaign = {
        "schema": "performance_campaign/v1",
        "campaign_id": campaign_id,
        "task": task,
        "source_authority": source_authority,
        "scope": {"chapters": {"start": chapter_start, "end": chapter_end}, "canon_not_showcase": True},
        "execution": {
            "profile": profile,
            "executor": executor,
            "creative_authority": False,
            "canon_write_parallelism": 0,
            "max_worker_retries": PROFILES[profile]["max_retries"],
            "model": None,
            "reasoning_tier": None,
        },
        "paths": {
            "chapter_root": chapter_root.as_posix(),
            "cache_root": cache_root.as_posix(),
            "compiled_root": compiled_root.as_posix(),
            "index": db_path.as_posix(),
        },
        "plan": {"scenes_considered": len(scenes), "cache_hits": cache_hits, "packets_planned": len(packets)},
    }
    _write_json(campaign_root / "campaign.json", campaign)
    _write_jsonl(campaign_root / "packets.jsonl", packets)
    for name in ("results.jsonl", "failures.jsonl", "telemetry.jsonl"):
        path = campaign_root / name
        if not path.exists():
            path.write_text("", encoding="utf-8")
    _append_jsonl(campaign_root / "telemetry.jsonl", {
        "event": "campaign_planned", "campaign_id": campaign_id,
        "scenes_considered": len(scenes), "cache_hits": cache_hits, "packets_planned": len(packets),
    })
    return {
        "campaign_id": campaign_id,
        "campaign_root": campaign_root.as_posix(),
        "scenes_considered": len(scenes),
        "cache_hits": cache_hits,
        "packets_planned": len(packets),
        "index": index_summary,
    }


def build_worker_prompt(packet: dict[str, Any], scene_record: dict[str, Any]) -> str:
    source = scene_record.get("source") if isinstance(scene_record.get("source"), dict) else {}
    try:
        view = funnel.render_scene_view(scene_record, str(packet.get("view", "comparison")))
    except (ValueError, KeyError):
        view = {"scene_id": packet.get("scene_id"), "source": {"hash": packet.get("source_hash")}}
    payload = {
        "packet": packet,
        "view": view,
        "source_prose": source.get("paragraphs", []) if packet.get("task") == "reverse_edit" else [],
    }
    return (
        "Execute this bounded PLG campaign packet. Do not redesign the project, widen scope, invent new doctrine, "
        "or mutate canon. Prefer the supplied compiler view. Return one JSON object only. "
        f"Write authority is {packet.get('write_authority', 'derived_only')}. Halt after this packet.\n\n"
        + json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)
    )


def _default_codex_executor(packet: dict[str, Any], prompt: str, config: dict[str, Any]) -> dict[str, Any]:
    command = shlex.split(os.environ.get("PLG_CODEX_EXEC", "codex exec --ephemeral -"))
    completed = subprocess.run(command, input=prompt, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"Codex exited {completed.returncode}")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Codex worker did not return a single JSON object") from exc
    if not isinstance(result, dict):
        raise RuntimeError("Codex worker result must be a JSON object")
    return result


def _local_executor(packet: dict[str, Any], prompt: str, config: dict[str, Any]) -> dict[str, Any]:
    command_text = os.environ.get("PLG_LOCAL_INFERENCE_COMMAND")
    if not command_text:
        raise RuntimeError("local executor requested but PLG_LOCAL_INFERENCE_COMMAND is not configured")
    completed = subprocess.run(shlex.split(command_text), input=prompt, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"local executor exited {completed.returncode}")
    result = json.loads(completed.stdout)
    if not isinstance(result, dict):
        raise RuntimeError("local executor result must be a JSON object")
    return result


def _configured_executor(campaign: dict[str, Any]) -> Callable[[dict[str, Any], str, dict[str, Any]], dict[str, Any]]:
    execution = campaign.get("execution") if isinstance(campaign.get("execution"), dict) else {}
    name = execution.get("executor", "codex")
    if name == "codex":
        return _default_codex_executor
    if name == "local":
        return _local_executor
    if name == "manual":
        raise RuntimeError("manual executor can plan/reduce but cannot run packets")
    raise RuntimeError(f"unknown campaign executor: {name}")


def _load_scene_for_packet(compiled_root: Path, packet: dict[str, Any]) -> dict[str, Any]:
    try:
        return funnel.load_scene_record(compiled_root, str(packet["scene_id"]))
    except (OSError, ValueError):
        return {"scene_id": packet.get("scene_id"), "source": {"hash": packet.get("source_hash"), "paragraphs": []}, "mechanical": {}, "dependencies": {}}


def _persist_worker_result(compiled_root: Path, packet: dict[str, Any], result: dict[str, Any]) -> None:
    scene_id = str(packet.get("scene_id", ""))
    try:
        scene = funnel.load_scene_record(compiled_root, scene_id)
    except (OSError, ValueError):
        return
    dep = str(packet.get("dependency_hash", ""))
    compiler_name = "performance-campaign-worker/v1"
    for layer in ("semantic", "performance"):
        payload = result.get(layer)
        if isinstance(payload, dict):
            scene = funnel.merge_derived_layer(scene, layer, payload, compiler=compiler_name, dependency_hash=dep)
    if isinstance(result.get("screenplay"), str) and result["screenplay"].strip():
        scene = funnel.set_screenplay_result(scene, result["screenplay"], compiler=compiler_name, dependency_hash=dep)
    if isinstance(result.get("comparison"), dict):
        scene = funnel.set_comparison_result(scene, result["comparison"], compiler=compiler_name, dependency_hash=dep)
    match = funnel.SCENE_ID_RE.match(scene_id)
    if match:
        _write_json(compiled_root / match.group("chapter") / f"s{int(match.group('number')):03d}.json", scene)


def _usage_fields(result: dict[str, Any]) -> tuple[Any, Any, Any]:
    usage = result.get("usage") if isinstance(result.get("usage"), dict) else {}
    return usage.get("input_tokens"), usage.get("output_tokens"), usage.get("cached_tokens")


def run_campaign(
    campaign_root: Path,
    *,
    executor_fn: Callable[[dict[str, Any], str, dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    campaign_root = Path(campaign_root)
    campaign = _read_json(campaign_root / "campaign.json")
    execution = campaign.get("execution") if isinstance(campaign.get("execution"), dict) else {}
    profile = str(execution.get("profile", "eco"))
    if profile not in PROFILES:
        raise ValueError(f"unknown execution profile: {profile}")
    max_workers = PROFILES[profile]["max_workers"]
    max_retries = int(execution.get("max_worker_retries", PROFILES[profile]["max_retries"]))
    executor = executor_fn or _configured_executor(campaign)
    packets = _read_jsonl(campaign_root / "packets.jsonl")
    existing_results = _read_jsonl(campaign_root / "results.jsonl")
    completed_ids = {row.get("packet_id") for row in existing_results if row.get("status") == "completed" and isinstance(row.get("packet_id"), str)}
    pending = [packet for packet in packets if packet.get("packet_id") not in completed_ids]
    compiled_root = Path(str((campaign.get("paths") or {}).get("compiled_root", ".cache/plg/compiler")))
    telemetry_path = campaign_root / "telemetry.jsonl"

    def execute_one(packet: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        scene = _load_scene_for_packet(compiled_root, packet)
        prompt = build_worker_prompt(packet, scene)
        last_error: Exception | None = None
        for attempt in range(max_retries + 1):
            if attempt:
                _append_jsonl(telemetry_path, {"event": "worker_retry", "packet_id": packet["packet_id"], "scene_id": packet["scene_id"], "attempt": attempt + 1})
            _append_jsonl(telemetry_path, {"event": "worker_launch", "packet_id": packet["packet_id"], "scene_id": packet["scene_id"], "executor": execution.get("executor"), "model": execution.get("model"), "reasoning_tier": execution.get("reasoning_tier"), "attempt": attempt + 1})
            started = time.perf_counter()
            try:
                raw = executor(packet, prompt, execution)
                if not isinstance(raw, dict):
                    raise RuntimeError("worker result must be a JSON object")
                result = dict(raw)
                result.setdefault("status", "completed")
                result["packet_id"] = packet["packet_id"]
                result["scene_id"] = packet["scene_id"]
                elapsed_ms = int((time.perf_counter() - started) * 1000)
                input_tokens, output_tokens, cached_tokens = _usage_fields(result)
                _append_jsonl(telemetry_path, {"event": "worker_complete", "packet_id": packet["packet_id"], "scene_id": packet["scene_id"], "executor": execution.get("executor"), "model": execution.get("model"), "reasoning_tier": execution.get("reasoning_tier"), "elapsed_ms": elapsed_ms, "input_tokens": input_tokens, "output_tokens": output_tokens, "cached_tokens": cached_tokens, "verdict": (result.get("comparison") or {}).get("verdict") if isinstance(result.get("comparison"), dict) else None})
                _persist_worker_result(compiled_root, packet, result)
                return "completed", result
            except Exception as exc:
                last_error = exc
                _append_jsonl(telemetry_path, {"event": "worker_failure", "packet_id": packet["packet_id"], "scene_id": packet["scene_id"], "attempt": attempt + 1, "error": str(exc), "elapsed_ms": int((time.perf_counter() - started) * 1000)})
        return "failed", {"packet_id": packet["packet_id"], "scene_id": packet["scene_id"], "status": "failed", "error": str(last_error) if last_error else "worker failed", "attempts": max_retries + 1}

    new_results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    if pending:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [pool.submit(execute_one, packet) for packet in pending]
            for future in as_completed(futures):
                status, row = future.result()
                (new_results if status == "completed" else failures).append(row)
    _write_jsonl(campaign_root / "results.jsonl", existing_results + sorted(new_results, key=lambda row: str(row.get("packet_id", ""))))
    existing_failures = _read_jsonl(campaign_root / "failures.jsonl")
    _write_jsonl(campaign_root / "failures.jsonl", existing_failures + sorted(failures, key=lambda row: str(row.get("packet_id", ""))))
    reduced = reduce_campaign(campaign_root)
    return {"campaign_id": campaign.get("campaign_id"), "workers_launched": len(pending), "completed": len(new_results), "failures": len(failures), "resumed": len(completed_ids), "summary": reduced}


def _telemetry_metrics(campaign_root: Path) -> dict[str, Any]:
    events = _read_jsonl(Path(campaign_root) / "telemetry.jsonl")
    launches = [event for event in events if event.get("event") == "worker_launch"]
    retries = [event for event in events if event.get("event") == "worker_retry"]
    completes = [event for event in events if event.get("event") == "worker_complete"]
    def token_sum(field: str) -> int | None:
        values = [event.get(field) for event in completes if isinstance(event.get(field), int)]
        return sum(values) if values else None
    return {"worker_launch_events": len(launches), "retry_events": len(retries), "elapsed_worker_ms": sum(int(event.get("elapsed_ms", 0) or 0) for event in completes), "reported_input_tokens": token_sum("input_tokens"), "reported_output_tokens": token_sum("output_tokens"), "reported_cached_tokens": token_sum("cached_tokens")}


def reduce_campaign(campaign_root: Path) -> dict[str, Any]:
    campaign_root = Path(campaign_root)
    results = _read_jsonl(campaign_root / "results.jsonl")
    failures_file = _read_jsonl(campaign_root / "failures.jsonl")
    source_wins = 0
    performance_candidates = 0
    ambiguous = 0
    candidate_scenes: list[str] = []
    ambiguous_scenes: list[str] = []
    survivors: list[str] = []
    failed_scenes: list[str] = []
    for result in results:
        comparison = result.get("comparison") if isinstance(result.get("comparison"), dict) else {}
        verdict = comparison.get("verdict")
        if verdict == "source_win":
            source_wins += 1
        elif verdict == "performance_candidate":
            performance_candidates += 1
            if isinstance(result.get("scene_id"), str): candidate_scenes.append(result["scene_id"])
        elif verdict == "ambiguous":
            ambiguous += 1
            if isinstance(result.get("scene_id"), str): ambiguous_scenes.append(result["scene_id"])
        record = result.get("record") if isinstance(result.get("record"), dict) else {}
        if record.get("verdict") == "change_survives" and isinstance(result.get("scene_id"), str): survivors.append(result["scene_id"])
    failed_scenes.extend(row["scene_id"] for row in failures_file if isinstance(row.get("scene_id"), str))
    summary = {"results": len(results), "source_wins": source_wins, "performance_candidates": performance_candidates, "ambiguous": ambiguous, "candidate_scenes": sorted(set(candidate_scenes)), "ambiguous_scenes": sorted(set(ambiguous_scenes)), "surviving_patches": len(survivors), "survivor_scenes": sorted(set(survivors)), "failures": len(set(failed_scenes)), "failed_scenes": sorted(set(failed_scenes)), "telemetry": _telemetry_metrics(campaign_root)}
    _write_json(campaign_root / "reducer.json", summary)
    _write_json(campaign_root / "summary.json", summary)
    return summary


def get_campaign_result(campaign_root: Path) -> dict[str, Any]:
    campaign_root = Path(campaign_root)
    return _read_json(campaign_root / "summary.json") if (campaign_root / "summary.json").exists() else reduce_campaign(campaign_root)


def _survivor_records(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for result in results:
        record = result.get("record")
        if isinstance(record, dict) and record.get("verdict") == "change_survives":
            funnel.validate_record(record)
            records.append(record)
    return records


def integrate_campaign(campaign_root: Path, chapter_root: Path, *, current_authority: str) -> dict[str, Any]:
    campaign_root = Path(campaign_root)
    campaign = _read_json(campaign_root / "campaign.json")
    source_authority = campaign.get("source_authority")
    if current_authority != source_authority:
        raise ValueError(f"authority drift: campaign={source_authority} current={current_authority}")
    records = _survivor_records(_read_jsonl(campaign_root / "results.jsonl"))
    if not records:
        return {"changed": [], "survivors": 0}
    by_chapter: dict[int, list[dict[str, Any]]] = {}
    for record in records: by_chapter.setdefault(int(record["chapter"]), []).append(record)
    merged_records: list[dict[str, Any]] = []
    for chapter, chapter_records in sorted(by_chapter.items()):
        if len(chapter_records) == 1:
            merged_records.append(chapter_records[0])
            continue
        patches = [patch for record in chapter_records for patch in record["patches"]]
        merged = {"chapter": chapter, "verdict": "change_survives", "screen": {"decision": "deep_review", "signals": ["performance_campaign"], "reason": "Multiple scene-level PERFORMANCE survivors were reduced into one chapter transaction."}, "dramatic": "\n\n".join(str(record["dramatic"]) for record in chapter_records), "performance": "\n\n".join(str(record["performance"]) for record in chapter_records), "screenplay": "\n\n".join(str(record["screenplay"]) for record in chapter_records), "comparison": "\n\n".join(str(record["comparison"]) for record in chapter_records), "patches": patches}
        funnel.validate_record(merged)
        merged_records.append(merged)
    batch = {"schema": "performance_production_batch/v1", "source_authority": source_authority, "scope": [record["chapter"] for record in merged_records], "records": merged_records}
    funnel.validate_batch(batch)
    changed = funnel.apply_batch_to_root(batch, Path(chapter_root))
    _append_jsonl(campaign_root / "telemetry.jsonl", {"event": "integration_complete", "survivors": len(records), "changed": [path.as_posix() for path in changed]})
    return {"changed": [path.as_posix() for path in changed], "survivors": len(records)}


def _parse_range(value: str) -> tuple[int, int]:
    if ":" not in value:
        chapter = int(value)
        return chapter, chapter
    left, right = value.split(":", 1)
    return int(left), int(right)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan, run, reduce, inspect, or integrate PLG PERFORMANCE campaigns.")
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--task", required=True); plan.add_argument("--chapters", required=True); plan.add_argument("--source-authority", required=True)
    plan.add_argument("--chapter-root", type=Path, default=Path("chapters")); plan.add_argument("--cache-root", type=Path, default=Path(".cache/plg")); plan.add_argument("--profile", choices=sorted(PROFILES), default="eco"); plan.add_argument("--executor", default="codex")
    run = sub.add_parser("run"); run.add_argument("campaign_root", type=Path)
    reduce_cmd = sub.add_parser("reduce"); reduce_cmd.add_argument("campaign_root", type=Path)
    status = sub.add_parser("status"); status.add_argument("campaign_root", type=Path)
    integrate = sub.add_parser("integrate"); integrate.add_argument("campaign_root", type=Path); integrate.add_argument("--chapter-root", type=Path, default=Path("chapters")); integrate.add_argument("--current-authority", required=True)
    args = parser.parse_args(argv)
    if args.command == "plan":
        start, end = _parse_range(args.chapters)
        result = plan_campaign(task=args.task, chapter_start=start, chapter_end=end, source_authority=args.source_authority, chapter_root=args.chapter_root, cache_root=args.cache_root, profile=args.profile, executor=args.executor)
    elif args.command == "run": result = run_campaign(args.campaign_root)
    elif args.command == "reduce": result = reduce_campaign(args.campaign_root)
    elif args.command == "status": result = get_campaign_result(args.campaign_root)
    else: result = integrate_campaign(args.campaign_root, args.chapter_root, current_authority=args.current_authority)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
