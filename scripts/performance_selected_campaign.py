#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts import performance_campaign as campaign
from scripts import performance_index
from scripts import performance_production_funnel as funnel


SPEAKER_OWNERSHIP_POLICY = {
    "authority": "screenplay_ground_truth",
    "instruction": "Run a speaker ownership audit when translating PERFORMANCE back into prose. The screenplay's explicit speaker labels are ground truth for who owns each spoken line.",
    "rules": [
        "Preserve clean two-person alternation when speaker ownership remains immediately legible.",
        "Be bullish on light attribution when three or more speakers are active, after narration or action interrupts an exchange, after a speaker re-enters from silence, during interruptions, or when alternation breaks.",
        "Never attach another character's action to dialogue spoken by someone else. Separate the action or add attribution so ownership is immediate.",
        "Prefer a natural action beat only when that action belongs to the speaker. Otherwise said/asked is good and should be used freely when it is the clearest repair.",
        "Do not tag every line. Add the minimum attribution needed for a fresh reader to assign every utterance without fragile inference.",
    ],
}


def _validate_ids(chapter_ids: list[int]) -> list[int]:
    if not chapter_ids:
        raise ValueError("chapter_ids must contain at least one chapter")
    if any(chapter < 1 for chapter in chapter_ids):
        raise ValueError("chapter_ids must be positive")
    if len(chapter_ids) != len(set(chapter_ids)):
        raise ValueError("duplicate chapter_ids are not allowed")
    return list(chapter_ids)


def _selection_id(task: str, chapter_ids: list[int], source_authority: str) -> str:
    payload = json.dumps(chapter_ids, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]
    return f"{task}-selected-{len(chapter_ids):03d}-{digest}-{source_authority[:8]}"


def read_campaign(campaign_root: Path) -> dict[str, Any]:
    return campaign._read_json(Path(campaign_root) / "campaign.json")


def plan_selected_campaign(
    *,
    task: str,
    chapter_ids: list[int],
    source_authority: str,
    chapter_root: Path,
    cache_root: Path,
    profile: str = "eco",
    executor: str = "codex",
    model: object = None,
    reasoning_tier: object = None,
) -> dict[str, Any]:
    task = campaign._normalize_task(task)
    ids = _validate_ids(chapter_ids)
    if not source_authority.strip():
        raise ValueError("source_authority is required")
    if profile not in campaign.PROFILES:
        raise ValueError(f"unknown execution profile: {profile}")

    chapter_root = Path(chapter_root)
    cache_root = Path(cache_root)
    compiled_root = cache_root / "compiler"
    scenes: list[dict[str, Any]] = []

    for chapter in ids:
        path = chapter_root / f"{chapter:03d}.html"
        if not path.exists():
            raise ValueError(f"canonical chapter missing: {path.name}")
        funnel.write_compiled_chapter(
            chapter,
            path.read_text(encoding="utf-8"),
            compiled_root,
        )
        manifest = campaign._read_json(compiled_root / f"{chapter:03d}" / "manifest.json")
        for scene_id in manifest.get("scene_order", []):
            if isinstance(scene_id, str):
                scenes.append(funnel.load_scene_record(compiled_root, scene_id))

    db_path = cache_root / "project-index.sqlite"
    index_summary = performance_index.rebuild_index(compiled_root, db_path)
    campaign_id = _selection_id(task, ids, source_authority)
    campaign_root = cache_root / "campaigns" / campaign_id
    campaign_root.mkdir(parents=True, exist_ok=True)

    packets: list[dict[str, Any]] = []
    cache_hits = 0
    for scene in scenes:
        if campaign._task_cache_valid(scene, task):
            cache_hits += 1
        else:
            packet = campaign._packet_for_scene(scene, task)
            if task == "reverse_edit":
                packet["speaker_ownership_policy"] = SPEAKER_OWNERSHIP_POLICY
            packets.append(packet)

    value = {
        "schema": "performance_campaign/v1",
        "campaign_id": campaign_id,
        "task": task,
        "source_authority": source_authority,
        "scope": {
            "selection": "explicit",
            "chapter_ids": ids,
            "showcase_priority": True,
            "canon_authority_preserved": True,
        },
        "execution": {
            "profile": profile,
            "executor": executor,
            "creative_authority": False,
            "canon_write_parallelism": 0,
            "max_worker_retries": campaign.PROFILES[profile]["max_retries"],
            "model": str(model) if model is not None else None,
            "reasoning_tier": str(reasoning_tier) if reasoning_tier is not None else None,
        },
        "paths": {
            "chapter_root": chapter_root.as_posix(),
            "cache_root": cache_root.as_posix(),
            "compiled_root": compiled_root.as_posix(),
            "index": db_path.as_posix(),
        },
        "plan": {
            "chapters_considered": len(ids),
            "scenes_considered": len(scenes),
            "cache_hits": cache_hits,
            "packets_planned": len(packets),
        },
    }
    campaign._write_json(campaign_root / "campaign.json", value)
    campaign._write_jsonl(campaign_root / "packets.jsonl", packets)
    for name in ("results.jsonl", "failures.jsonl", "telemetry.jsonl"):
        path = campaign_root / name
        if not path.exists():
            path.write_text("", encoding="utf-8")
    campaign._append_jsonl(
        campaign_root / "telemetry.jsonl",
        {
            "event": "campaign_planned",
            "campaign_id": campaign_id,
            "chapters_considered": len(ids),
            "scenes_considered": len(scenes),
            "cache_hits": cache_hits,
            "packets_planned": len(packets),
            "selection": "explicit",
        },
    )
    return {
        "campaign_id": campaign_id,
        "campaign_root": campaign_root.as_posix(),
        "chapter_ids": ids,
        "scenes_considered": len(scenes),
        "cache_hits": cache_hits,
        "packets_planned": len(packets),
        "index": index_summary,
    }


def _parse_ids(value: str) -> list[int]:
    try:
        return [int(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("chapter IDs must be comma-separated integers") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan and run a PLG campaign over an explicit noncontiguous chapter selection.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--task", required=True)
    run.add_argument("--chapter-ids", required=True, type=_parse_ids)
    run.add_argument("--source-authority", required=True)
    run.add_argument("--chapter-root", type=Path, default=Path("chapters"))
    run.add_argument("--cache-root", type=Path, default=Path(".cache/plg"))
    run.add_argument("--profile", choices=sorted(campaign.PROFILES), default="eco")
    run.add_argument("--executor", default="codex")
    run.add_argument("--model")
    run.add_argument("--reasoning-tier")
    args = parser.parse_args(argv)

    planned = plan_selected_campaign(
        task=args.task,
        chapter_ids=args.chapter_ids,
        source_authority=args.source_authority,
        chapter_root=args.chapter_root,
        cache_root=args.cache_root,
        profile=args.profile,
        executor=args.executor,
        model=args.model,
        reasoning_tier=args.reasoning_tier,
    )
    executed = campaign.run_campaign(Path(planned["campaign_root"]))
    print(json.dumps({"plan": planned, "run": executed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
