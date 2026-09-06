from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "state" / "visual" / "GENERATION_QUEUE.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
DEFAULT_OUTPUT = ROOT / "state" / "visual" / "BOUNDED_PRODUCTION_REVIEW_156_160.md"


def _latest_registry_by_candidate(registry: list[dict]) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for record in registry:
        candidate_id = record.get("candidate_id")
        if isinstance(candidate_id, str) and candidate_id:
            latest[candidate_id] = record
    return latest


def review_bounded_batch(
    queue: list[dict],
    registry: list[dict],
    candidates: list[dict],
    start_chapter: int,
    end_chapter: int,
) -> list[dict]:
    queue_by_id = {record.get("candidate_id"): record for record in queue}
    registry_by_id = _latest_registry_by_candidate(registry)
    rows: list[dict] = []
    for candidate in candidates:
        chapter = candidate.get("chapter")
        candidate_id = candidate.get("id")
        if not isinstance(chapter, int) or not (start_chapter <= chapter <= end_chapter) or not candidate_id:
            continue
        queue_record = queue_by_id.get(candidate_id, {})
        registry_record = registry_by_id.get(candidate_id, {})
        registry_status = registry_record.get("status", "")

        if registry_status == "live":
            production_state = "live"
        elif registry_status == "approved":
            production_state = "approved_unpublished"
        elif registry_status == "generated":
            production_state = "generated_awaiting_approval"
        elif registry_status == "rejected" and candidate.get("status") in {"candidate", "prompt_ready"}:
            production_state = "rejected_retryable"
        elif queue_record.get("status") == "generation_ready":
            production_state = "ready_to_generate"
        elif candidate.get("anchor_blocked"):
            production_state = "blocked_anchor"
        else:
            production_state = "not_ready"

        readiness = {
            "prompt_pack": bool(queue_record.get("prompt_pack")),
            "deterministic_target": bool(queue_record.get("target_asset")),
            "valid_anchor": candidate.get("anchor_status") == "valid" and not candidate.get("anchor_blocked"),
            "strong_anchor": candidate.get("anchor_quality_status") in {None, "strong"},
            "reference_context": bool(queue_record.get("reference_selection_notes") or queue_record.get("selected_character_references")),
        }
        rows.append({
            "candidate_id": candidate_id,
            "chapter": chapter,
            "chapter_title": candidate.get("chapter_title", ""),
            "production_state": production_state,
            "registry_status": registry_status,
            "target_asset": queue_record.get("target_asset") or registry_record.get("live_asset") or registry_record.get("source_asset") or "",
            "prompt_pack": queue_record.get("prompt_pack", ""),
            "paragraph_anchor": candidate.get("paragraph_anchor", ""),
            "anchor_quality_status": candidate.get("anchor_quality_status", ""),
            "reference_selection_notes": queue_record.get("reference_selection_notes", ""),
            "readiness": readiness,
            "ready_checks_passed": all(readiness.values()) if production_state == "ready_to_generate" else None,
        })
    return sorted(rows, key=lambda row: (row["chapter"], row["candidate_id"]))


def render_review(rows: list[dict], start_chapter: int, end_chapter: int) -> str:
    lines = [
        f"# PEG-LEG GREG — BOUNDED PRODUCTION REVIEW · Chapters {start_chapter}–{end_chapter}",
        "",
        "This is the execution/review routing surface for the bounded packet. It does not pretend a pixel exists before generation. It records the real current state from queue + registry + candidate authority.",
        "",
    ]
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["production_state"]] = counts.get(row["production_state"], 0) + 1
    lines.append("## Summary")
    for key in sorted(counts):
        lines.append(f"- {key}: {counts[key]}")
    lines.append("")

    for row in rows:
        lines.extend([
            f"## Chapter {row['chapter']:03d} — {row.get('chapter_title', '')}",
            f"- Candidate: {row['candidate_id']}",
            f"- Production state: **{row['production_state']}**",
            f"- Target/current asset: {row.get('target_asset', '')}",
            f"- Prompt pack: {row.get('prompt_pack', '')}",
            f"- Paragraph anchor: {row.get('paragraph_anchor', '')}",
            f"- Anchor quality: {row.get('anchor_quality_status', '')}",
            f"- Reference rationale: {row.get('reference_selection_notes', '')}",
            "- Readiness checks:",
        ])
        for key, value in row["readiness"].items():
            lines.append(f"  - [{'x' if value else ' '}] {key.replace('_', ' ')}")
        if row["production_state"] == "ready_to_generate":
            lines.append("- Review outcome: generation can proceed" if row["ready_checks_passed"] else "- Review outcome: fix readiness gaps before generation")
        elif row["production_state"] == "generated_awaiting_approval":
            lines.append("- Review outcome: explicit approve/reject decision required")
        elif row["production_state"] == "rejected_retryable":
            lines.append("- Review outcome: rejected attempt recorded; candidate remains eligible for a later deterministic retry")
        elif row["production_state"] == "approved_unpublished":
            lines.append("- Review outcome: promote/integrate approved asset")
        elif row["production_state"] == "live":
            lines.append("- Review outcome: complete/live")
        lines.append("")
    return "\n".join(lines) + "\n"


def main(start_chapter: int = 156, end_chapter: int = 160, output: Path = DEFAULT_OUTPUT) -> None:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8")) if QUEUE_PATH.exists() else []
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8")) if CANDIDATES_PATH.exists() else []
    rows = review_bounded_batch(queue, registry, candidates, start_chapter, end_chapter)
    text = render_review(rows, start_chapter, end_chapter)
    if output.exists() and output.read_text(encoding="utf-8") == text:
        print(f"bounded production review already current: {len(rows)} items")
        return
    output.write_text(text, encoding="utf-8")
    print(f"wrote bounded production review: {len(rows)} items for {start_chapter}-{end_chapter}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review a bounded illustration production wave against queue/registry/candidate state.")
    parser.add_argument("--start", type=int, default=156)
    parser.add_argument("--end", type=int, default=160)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    main(args.start, args.end, args.output)
