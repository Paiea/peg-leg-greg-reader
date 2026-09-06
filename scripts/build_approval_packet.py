from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_APPROVAL_PACKET.md"


def generated_records_for_review(registry: list[dict]) -> list[dict]:
    return [dict(record) for record in registry if record.get("status") == "generated"]


def render_approval_packet(records: Iterable[dict]) -> str:
    lines = ["# PEG-LEG GREG — APPROVAL PACKET", ""]
    for record in records:
        approve = {
            "candidate_id": record["candidate_id"],
            "asset": record["source_asset"],
            "decision": "approve",
            "approved_fit": record.get("approved_fit", "exact"),
            "alt_text": "",
            "caption": "",
        }
        reject = {
            "candidate_id": record["candidate_id"],
            "asset": record["source_asset"],
            "decision": "reject",
            "reason": "",
        }
        lines.extend(
            [
                f"## Chapter {record['chapter']:03d} — {record['candidate_id']}",
                f"- Generated asset: {record['source_asset']}",
                f"- Prompt pack: {record.get('prompt_pack', '')}",
                "- Approve template:",
                "```json",
                json.dumps(approve, indent=2, ensure_ascii=False),
                "```",
                "- Reject template:",
                "```json",
                json.dumps(reject, indent=2, ensure_ascii=False),
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    packet = render_approval_packet(generated_records_for_review(registry)) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == packet:
        print("approval packet already current")
        return
    OUTPUT_PATH.write_text(packet, encoding="utf-8")
    print("wrote illustration approval packet")


if __name__ == "__main__":
    main()
