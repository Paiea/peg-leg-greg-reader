from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOLD_PATH = ROOT / "state" / "visual" / "PRODUCTION_HOLD.json"
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
CHAPTER_DIR = ROOT / "chapters"
REPORT_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_RECONCILIATION_REPORT.md"


def edit_hold_active(state: dict | None) -> bool:
    state = state or {}
    return (
        state.get("mode") == "structural_edit_hold"
        and bool(state.get("active"))
        and not bool(state.get("generation_allowed"))
    )


def _normalize_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def _chapter_text_from_html(path: Path) -> str:
    return _normalize_text(path.read_text(encoding="utf-8"))


def reconcile_candidates(candidates: list[dict], chapter_texts: dict[int, str]) -> list[dict]:
    rows: list[dict] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("id", ""))
        source_chapter = candidate.get("chapter")
        anchor = str(candidate.get("paragraph_anchor", "")).strip()
        normalized_anchor = _normalize_text(anchor)

        if not isinstance(source_chapter, int) or source_chapter not in chapter_texts:
            status = "chapter_missing"
            matches = 0
        elif not normalized_anchor:
            status = "no_anchor"
            matches = 0
        else:
            chapter_text = _normalize_text(chapter_texts[source_chapter])
            matches = chapter_text.count(normalized_anchor)
            if matches == 1:
                status = "stable"
            elif matches > 1:
                status = "anchor_ambiguous"
            else:
                status = "anchor_drift"

        rows.append(
            {
                "candidate_id": candidate_id,
                "source_chapter": source_chapter,
                "chapter_title": candidate.get("chapter_title", ""),
                "reconciliation_status": status,
                "match_count": matches,
                "scene_summary": candidate.get("scene_summary", ""),
                "visual_hook": candidate.get("visual_hook", ""),
                "paragraph_anchor": anchor,
                "candidate_status": candidate.get("status", ""),
            }
        )
    return sorted(rows, key=lambda row: (row.get("source_chapter") if isinstance(row.get("source_chapter"), int) else 999999, row["candidate_id"]))


def render_reconciliation_report(rows: list[dict], hold: dict | None = None) -> str:
    hold = hold or {}
    counts: dict[str, int] = {}
    for row in rows:
        status = row["reconciliation_status"]
        counts[status] = counts.get(status, 0) + 1

    lines = [
        "# PEG-LEG GREG — ILLUSTRATION / STRUCTURAL EDIT RECONCILIATION",
        "",
        f"- Structural-edit hold active: {'yes' if edit_hold_active(hold) else 'no'}",
        f"- Generation allowed: {'yes' if hold.get('generation_allowed', True) else 'no'}",
        f"- Candidate count: {len(rows)}",
    ]
    for status in ["stable", "anchor_drift", "anchor_ambiguous", "chapter_missing", "no_anchor"]:
        lines.append(f"- {status}: {counts.get(status, 0)}")
    lines.extend(
        [
            "",
            "Candidate IDs are semantic visual identities. Chapter numbers and paragraph anchors are current-placement metadata, not permanent identity.",
            "During structural compression, do not preserve weak prose or chapter boundaries for illustration state. After the edit, re-read the surviving manuscript beat and explicitly remap, retire, or replace candidates that are not stable.",
            "This report never auto-reassigns a candidate to another chapter even if matching text appears elsewhere.",
            "",
            "## Needs reconciliation",
            "",
        ]
    )

    needs = [row for row in rows if row["reconciliation_status"] != "stable"]
    if not needs:
        lines.append("- None.")
    else:
        for row in needs:
            lines.extend(
                [
                    f"### {row['candidate_id']}",
                    f"- Source chapter: {row.get('source_chapter')}",
                    f"- Status: **{row['reconciliation_status']}**",
                    f"- Scene intent: {row.get('scene_summary', '')}",
                    f"- Visual hook: {row.get('visual_hook', '')}",
                    f"- Old anchor: {row.get('paragraph_anchor', '')}",
                    "- Action: inspect the compressed manuscript; explicitly remap the surviving beat, retire the candidate if the beat was cut, or replace it if the visual idea no longer earns its place.",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def load_hold(path: Path = HOLD_PATH) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("production hold must be a JSON object")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Report illustration candidate stability across structural manuscript edits.")
    parser.add_argument("--production-allowed", action="store_true", help="Exit 0 only when structural-edit hold does not block production.")
    args = parser.parse_args()

    hold = load_hold()
    if args.production_allowed:
        raise SystemExit(1 if edit_hold_active(hold) else 0)

    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8")) if CANDIDATES_PATH.exists() else []
    if not isinstance(candidates, list):
        raise ValueError("scene candidates must be a JSON array")
    chapter_numbers = {row.get("chapter") for row in candidates if isinstance(row.get("chapter"), int)}
    chapter_texts = {
        chapter: _chapter_text_from_html(CHAPTER_DIR / f"{chapter:03d}.html")
        for chapter in chapter_numbers
        if (CHAPTER_DIR / f"{chapter:03d}.html").exists()
    }
    rows = reconcile_candidates(candidates, chapter_texts)
    text = render_reconciliation_report(rows, hold)
    previous = REPORT_PATH.read_text(encoding="utf-8") if REPORT_PATH.exists() else None
    if previous != text:
        REPORT_PATH.write_text(text, encoding="utf-8")
    unstable = sum(1 for row in rows if row["reconciliation_status"] != "stable")
    print(
        f"illustration structural-edit reconciliation: {len(rows)} candidates, {unstable} needing review, "
        f"hold={'active' if edit_hold_active(hold) else 'inactive'}"
    )


if __name__ == "__main__":
    main()
