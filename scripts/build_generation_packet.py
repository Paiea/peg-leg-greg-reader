from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "state" / "visual" / "GENERATION_QUEUE.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "GENERATION_PACKET.md"


def select_generation_batch(queue: list[dict], limit: int = 25) -> list[dict]:
    ready = [dict(record) for record in queue if record.get("status") == "generation_ready"]
    return ready[: max(limit, 0)]


def _temporal_evidence_lines(record: dict) -> list[str]:
    evidence = record.get("visual_scene_evidence")
    if not isinstance(evidence, dict):
        return []
    lines: list[str] = []
    condition = evidence.get("evidence_condition")
    if isinstance(condition, str) and condition.strip():
        lines.append(f"- Evidence condition: {condition.strip()}")
    states = evidence.get("character_states")
    if not isinstance(states, dict):
        return lines
    for character, state in states.items():
        if not isinstance(character, str) or not isinstance(state, dict):
            continue
        state_id = state.get("state_id", "")
        lines.append(f"- TEMPORAL {character}: {state_id}")
        for label, field in (
            ("appearance", "appearance"),
            ("body", "body_state"),
            ("mobility", "mobility_state"),
        ):
            values = state.get(field)
            if isinstance(values, dict) and values:
                rendered = "; ".join(f"{key}: {value}" for key, value in values.items())
                lines.append(f"  - {label}: {rendered}")
        must_show = state.get("must_show")
        if isinstance(must_show, list) and must_show:
            lines.append(f"  - must show: {', '.join(str(value) for value in must_show)}")
        must_not_show = state.get("must_not_show")
        if isinstance(must_not_show, list) and must_not_show:
            lines.append(f"  - must not show: {', '.join(str(value) for value in must_not_show)}")
    return lines


def _performance_reference_lines(record: dict) -> list[str]:
    reference = record.get("performance_reference")
    if not isinstance(reference, dict):
        return []
    visual = reference.get("visual_reference")
    if not isinstance(visual, dict):
        return []
    lines = [
        "- PERFORMANCE visual reference: fresh derived editorial evidence; use for blocking/action/props only, never as canon authority.",
        f"- PERFORMANCE archive: {reference.get('archive_path', '')}",
    ]
    active_task = visual.get("active_task")
    if isinstance(active_task, str) and active_task.strip():
        lines.append(f"- PERFORMANCE active task: {active_task.strip()}")
    props = [str(value).strip() for value in visual.get("props", []) if str(value).strip()]
    if props:
        lines.append(f"- PERFORMANCE props: {', '.join(props)}")
    beats = [str(value).strip() for value in visual.get("physical_beats", []) if str(value).strip()]
    if beats:
        lines.append("- PERFORMANCE physical beats:")
        lines.extend(f"  - {beat}" for beat in beats)
    return lines


def render_generation_packet(records: Iterable[dict]) -> str:
    lines = ["# PEG-LEG GREG — GENERATION PACKET", ""]
    for record in records:
        selected = record.get("selected_character_references", [])
        lines.extend(
            [
                f"## Chapter {record['chapter']:03d} — {record.get('chapter_title', '')}",
                f"- Candidate: {record['candidate_id']}",
                f"- Coverage before: {record.get('coverage_before', '')}",
                f"- Priority: {record.get('priority', '')}",
                f"- Style family: {record.get('style_family', '')}",
                f"- Framing preference: {record.get('framing_preference', '')}",
                f"- Visual hook: {record.get('visual_hook', '')}",
                f"- Scene summary: {record.get('scene_summary', '')}",
                f"- Characters: {', '.join(record.get('characters', []))}",
                f"- Location: {record.get('location', '')}",
                f"- Mood: {record.get('mood', '')}",
                f"- Character reference assets: {json.dumps(record.get('character_reference_assets', []), ensure_ascii=False)}",
                f"- Selected character references: {json.dumps(selected, ensure_ascii=False)}",
                f"- Character appearance notes: {json.dumps(record.get('character_appearance_notes', {}), ensure_ascii=False)}",
                f"- Reference selection rationale: {record.get('reference_selection_notes', '')}",
                f"- Continuity notes: {record.get('continuity_notes', '')}",
                f"- Prompt pack: {record['prompt_pack']}",
                f"- Target asset: {record['target_asset']}",
            ]
        )
        lines.extend(_temporal_evidence_lines(record))
        lines.extend(_performance_reference_lines(record))
        lines.append("")
    return "\n".join(lines)


def main(limit: int = 25) -> None:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8")) if QUEUE_PATH.exists() else []
    packet = render_generation_packet(select_generation_batch(queue, limit=limit)) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == packet:
        print("generation packet already current")
        return
    OUTPUT_PATH.write_text(packet, encoding="utf-8")
    print(f"wrote generation packet: {min(limit, len(queue))} ready items")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render the next illustration generation batch.")
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()
    main(limit=args.limit)
