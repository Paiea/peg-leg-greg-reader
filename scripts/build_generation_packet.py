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


def render_generation_packet(records: Iterable[dict]) -> str:
    lines = ["# PEG-LEG GREG — GENERATION PACKET", ""]
    for record in records:
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
                f"- Character appearance notes: {json.dumps(record.get('character_appearance_notes', {}), ensure_ascii=False)}",
                f"- Continuity notes: {record.get('continuity_notes', '')}",
                f"- Prompt pack: {record['prompt_pack']}",
                f"- Target asset: {record['target_asset']}",
                "",
            ]
        )
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
