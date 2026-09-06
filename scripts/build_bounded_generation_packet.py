from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "state" / "visual" / "GENERATION_QUEUE.json"
DEFAULT_OUTPUT = ROOT / "state" / "visual" / "GENERATION_PACKET_156_160.md"


def select_bounded_generation_batch(queue: list[dict], start_chapter: int, end_chapter: int) -> list[dict]:
    if end_chapter < start_chapter:
        raise ValueError("end chapter must be >= start chapter")
    return [
        dict(record)
        for record in queue
        if record.get("status") == "generation_ready"
        and isinstance(record.get("chapter"), int)
        and start_chapter <= record["chapter"] <= end_chapter
    ]


def render_bounded_generation_packet(records: Iterable[dict], start_chapter: int, end_chapter: int) -> str:
    lines = [
        f"# PEG-LEG GREG — BOUNDED GENERATION PACKET · Chapters {start_chapter}–{end_chapter}",
        "",
        "This packet is intentionally bounded. Generate/review only these chapter targets before widening the wave.",
        "",
    ]
    for record in records:
        selected = record.get("selected_character_references", [])
        lines.extend(
            [
                f"## Chapter {record['chapter']:03d} — {record.get('chapter_title', '')}",
                f"- Candidate: {record['candidate_id']}",
                f"- Prompt pack: {record.get('prompt_pack', '')}",
                f"- Deterministic target: {record.get('target_asset', '')}",
                f"- Paragraph anchor: {record.get('paragraph_anchor', '')}",
                f"- Framing: {record.get('framing_preference', '')}",
                f"- Selected continuity references: {json.dumps(selected, ensure_ascii=False)}",
                f"- Reference rationale: {record.get('reference_selection_notes', '')}",
                "- Approval checklist:",
                "  - [ ] manuscript moment matches",
                "  - [ ] recurring characters remain recognizable",
                "  - [ ] Greg lower-body state is not exposed unless materially required",
                "  - [ ] composition/style fit current PLG art",
                "  - [ ] paragraph anchor still matches uniquely before promotion",
                "",
            ]
        )
    return "\n".join(lines)


def main(start_chapter: int = 156, end_chapter: int = 160, output: Path = DEFAULT_OUTPUT) -> None:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8")) if QUEUE_PATH.exists() else []
    records = select_bounded_generation_batch(queue, start_chapter, end_chapter)
    packet = render_bounded_generation_packet(records, start_chapter, end_chapter) + "\n"
    previous = output.read_text(encoding="utf-8") if output.exists() else None
    if previous == packet:
        print(f"bounded generation packet already current: {len(records)} items")
        return
    output.write_text(packet, encoding="utf-8")
    print(f"wrote bounded generation packet: {len(records)} items for {start_chapter}-{end_chapter}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a bounded illustration generation packet.")
    parser.add_argument("--start", type=int, default=156)
    parser.add_argument("--end", type=int, default=160)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    main(args.start, args.end, args.output)
