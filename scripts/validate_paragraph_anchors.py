from __future__ import annotations

import html
import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
CHAPTER_DIR = ROOT / "chapters"
REPORT_PATH = ROOT / "state" / "visual" / "PARAGRAPH_ANCHOR_REPORT.md"


def _normalize_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def _chapter_text_from_html(path: Path) -> str:
    return _normalize_text(path.read_text(encoding="utf-8"))


def validate_candidate_anchors(candidates: list[dict], chapter_text: dict[int, str]) -> list[dict]:
    report: list[dict] = []
    for candidate in candidates:
        anchor = str(candidate.get("paragraph_anchor", "")).strip()
        chapter = candidate.get("chapter")
        normalized_anchor = _normalize_text(anchor)
        normalized_chapter = _normalize_text(chapter_text.get(chapter, "")) if isinstance(chapter, int) else ""
        if not normalized_anchor:
            status = "missing"
            matches = 0
        else:
            matches = normalized_chapter.count(normalized_anchor)
            status = "valid" if matches == 1 else "missing" if matches == 0 else "ambiguous"
        report.append(
            {
                "candidate_id": candidate.get("id", ""),
                "chapter": chapter,
                "paragraph_anchor": anchor,
                "anchor_status": status,
                "match_count": matches,
            }
        )
    return report


def apply_anchor_validation(candidates: list[dict], report: list[dict]) -> tuple[list[dict], int]:
    by_id = {row.get("candidate_id"): row for row in report}
    updated = deepcopy(candidates)
    changed = 0
    for candidate in updated:
        row = by_id.get(candidate.get("id"))
        if not row:
            continue
        status = row["anchor_status"]
        before = json.dumps(candidate, sort_keys=True)
        candidate["anchor_status"] = status
        candidate["anchor_match_count"] = row["match_count"]
        if status == "valid":
            if candidate.pop("anchor_blocked", None) is not None and candidate.get("status") == "candidate":
                candidate["status"] = "prompt_ready"
        else:
            candidate["anchor_blocked"] = True
            if candidate.get("status") == "prompt_ready":
                candidate["status"] = "candidate"
        if json.dumps(candidate, sort_keys=True) != before:
            changed += 1
    return updated, changed


def render_anchor_report(report: list[dict]) -> str:
    lines = ["# PEG-LEG GREG — PARAGRAPH ANCHOR REPORT", ""]
    valid = sum(1 for row in report if row["anchor_status"] == "valid")
    missing = sum(1 for row in report if row["anchor_status"] == "missing")
    ambiguous = sum(1 for row in report if row["anchor_status"] == "ambiguous")
    lines.extend([
        f"- Valid: {valid}",
        f"- Missing: {missing}",
        f"- Ambiguous: {ambiguous}",
        "",
    ])
    for row in report:
        if row["anchor_status"] == "valid":
            continue
        lines.append(
            f"- Chapter {row.get('chapter')}: {row.get('candidate_id')} — {row['anchor_status']} ({row['match_count']} matches)"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8")) if CANDIDATES_PATH.exists() else []
    chapters = {
        candidate["chapter"]: _chapter_text_from_html(CHAPTER_DIR / f"{candidate['chapter']:03d}.html")
        for candidate in candidates
        if isinstance(candidate.get("chapter"), int) and (CHAPTER_DIR / f"{candidate['chapter']:03d}.html").exists()
    }
    report = validate_candidate_anchors(candidates, chapters)
    updated, changed = apply_anchor_validation(candidates, report)
    candidate_text = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
    if CANDIDATES_PATH.read_text(encoding="utf-8") != candidate_text:
        CANDIDATES_PATH.write_text(candidate_text, encoding="utf-8")
    report_text = render_anchor_report(report)
    if not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != report_text:
        REPORT_PATH.write_text(report_text, encoding="utf-8")
    blocked_rows = [row for row in report if row["anchor_status"] != "valid"]
    print(f"validated paragraph anchors: {len(report)} candidates, {len(blocked_rows)} blocked, {changed} candidate records updated")
    for row in blocked_rows:
        print(
            f"anchor blocked: chapter {row.get('chapter')} {row.get('candidate_id')} "
            f"{row['anchor_status']} ({row['match_count']} matches): {row.get('paragraph_anchor', '')}"
        )


if __name__ == "__main__":
    main()
