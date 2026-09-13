#!/usr/bin/env python3
"""Generate the current 3L written/audio production frontier through canon manuscripts."""

from __future__ import annotations

import json
import os
from pathlib import Path

from build_3l_parallel_audio_work_order import build_work_order, write_outputs
from build_3l_record_pages import build as build_reader
from plan_3l_short_dual_render import build_plan

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "3l" / "audio"
MANUSCRIPT = ROOT / "3l" / "manuscript"

NEW_DRAGON_ROUTES = {
    "004": [
        "“You woke with forty years of knowledge and treated the second life as a chance to perform the first more efficiently."
    ],
    "005": [
        "“You describe East Four as a detour because that is how you protected the decision from becoming a decision."
    ],
    "006": [
        "“You said the contract was four weeks. You remained at East Four for eleven years."
    ],
    "007": [
        "“You remember those names because in the first history they died and in the second they did not."
    ],
    "008": [
        "“You knew Nessa Vale first as a name on a board of dead people."
    ],
    "009": [
        "“You have given me several reasons without giving me the decision beneath them.",
        "“Then the table belongs in the answer. Not because a table is profound."
    ],
    "010": [
        "“You never told Bren. You had information about him and chose not to use it.",
        "“You had already observed events changing. Halden survived. North Vey did not rupture."
    ],
}


def write_routes() -> None:
    for record, prefixes in NEW_DRAGON_ROUTES.items():
        path = AUDIO / f"record-{record}-dragon-routing.json"
        path.write_text(
            json.dumps({"record": record, "dragon_prefixes": prefixes}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def build_plans() -> list[dict]:
    plans = []
    for number in range(2, 11):
        record = f"{number:03d}"
        source = MANUSCRIPT / f"record-{record}.md"
        route_path = AUDIO / f"record-{record}-dragon-routing.json"
        if not source.exists():
            raise ValueError(f"missing manuscript {source}")
        if not route_path.exists():
            raise ValueError(f"missing Dragon route {route_path}")
        route = json.loads(route_path.read_text(encoding="utf-8"))
        prefixes = route.get("dragon_prefixes")
        if not isinstance(prefixes, list) or not prefixes:
            raise ValueError(f"{route_path}: no Dragon prefixes")
        plan = build_plan(
            source.read_text(encoding="utf-8"),
            str(source.relative_to(ROOT)),
            max_chars=500,
            dragon_prefixes=prefixes,
        )
        if not any("normal" in chunk["required_voices"] for chunk in plan["chunks"]):
            raise ValueError(f"record {record}: locked route produced no Dragon capture")
        output = AUDIO / f"record-{record}-short-dual-plan.json"
        output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        plans.append(plan)
        print(record, plan["chunk_count"], "chunks", sum(len(c["required_voices"]) for c in plan["chunks"]), "captures")
    return plans


def write_current_worker_pointer(order: dict, master_path: Path) -> None:
    run_label = str(order["run_label"])
    pointer = {
        "status": "current_frozen_instant_work_order",
        "authority": "3l/audio/PARALLEL_INSTANT_WORKER_AUTHORITY.md",
        "master_work_order": str(master_path.relative_to(ROOT)),
        "run_label": run_label,
        "source_sha": str(order["source_sha"]),
        "worker_count": int(order["worker_count"]),
        "work_order_template": f"3l/audio/workers/{run_label}-instant-{{slot}}-work-order.json",
        "return_manifest_template": f"3l/audio/workers/{run_label}-instant-{{slot}}-captures.json",
        "claim_template": f"3l/audio/workers/claims/{{source_sha}}/{run_label}-instant-{{slot}}.json",
    }
    (AUDIO / "CURRENT_INSTANT_WORK_ORDER.json").write_text(
        json.dumps(pointer, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_workers(plans: list[dict]) -> dict:
    label = "records-002-010"
    order = build_work_order(
        plans,
        worker_count=5,
        branch="main",
        source_sha=os.environ.get("GITHUB_SHA", ""),
        run_label=label,
    )
    master_path = AUDIO / f"{label}-five-worker-work-order.json"
    write_outputs(
        order,
        master_path,
        AUDIO / "workers",
    )
    write_current_worker_pointer(order, master_path)
    return order


def main() -> None:
    write_routes()
    plans = build_plans()
    order = build_workers(plans)
    build_reader()
    print(
        "frontier built:",
        order["records"][0],
        "through",
        order["records"][-1],
        "captures=",
        order["total_captures"],
        "loads=",
        order["capture_loads"],
    )


if __name__ == "__main__":
    main()
