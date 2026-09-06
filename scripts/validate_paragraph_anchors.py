from __future__ import annotations

import html
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
CHAPTER_DIR = ROOT / "chapters"
REPORT_PATH = ROOT / "state" / "visual" / "PARAGRAPH_ANCHOR_REPORT.md"
BLOCK_THRESHOLD = 60
PRONOUN_START = {"i", "he", "she", "it", "we", "they", "you", "this", "that"}
STOPWORDS = {"the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "at", "for", "with", "was", "were", "is", "are", "be", "been", "had", "has", "have", "my", "his", "her", "their", "our"}


def _normalize_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def _chapter_text_from_html(path: Path) -> str:
    return _normalize_text(path.read_text(encoding="utf-8"))


def _anchor_quality(anchor: str, chapter: str) -> tuple[int, list[str]]:
    words = re.findall(r"[a-z0-9']+", anchor.lower())
    chapter_words = re.findall(r"[a-z0-9']+", chapter.lower())
    frequencies = Counter(chapter_words)
    score = 100
    issues: list[str] = []
    if len(words) < 5:
        score -= 60
        issues.append("very short anchor")
    elif len(words) < 8:
        score -= 20
        issues.append("short anchor")
    if words and words[0] in PRONOUN_START and len(words) < 9:
        score -= 30
        issues.append("short pronoun-led anchor")
    content_words = [word for word in words if word not in STOPWORDS and len(word) > 2]
    distinctive = [word for word in content_words if frequencies.get(word, 0) == 1]
    if len(content_words) >= 2 and len(distinctive) < 2:
        score -= 25
        issues.append("low distinctive-token count")
    return max(score, 0), issues


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
            quality_score, quality_issues = 0, ["missing anchor"]
        else:
            matches = normalized_chapter.count(normalized_anchor)
            status = "valid" if matches == 1 else "missing" if matches == 0 else "ambiguous"
            quality_score, quality_issues = _anchor_quality(normalized_anchor, normalized_chapter)
        quality_status = "strong" if quality_score >= BLOCK_THRESHOLD else "weak"
        should_block = status != "valid" or quality_status == "weak"
        report.append({
            "candidate_id": candidate.get("id", ""),
            "chapter": chapter,
            "paragraph_anchor": anchor,
            "anchor_status": status,
            "match_count": matches,
            "anchor_quality_score": quality_score,
            "anchor_quality_status": quality_status,
            "anchor_quality_issues": quality_issues,
            "should_block": should_block,
        })
    return report


def apply_anchor_validation(candidates: list[dict], report: list[dict]) -> tuple[list[dict], int]:
    by_id = {row.get("candidate_id"): row for row in report}
    updated = deepcopy(candidates)
    changed = 0
    for candidate in updated:
        row = by_id.get(candidate.get("id"))
        if not row:
            continue
        before = json.dumps(candidate, sort_keys=True)
        candidate["anchor_status"] = row["anchor_status"]
        candidate["anchor_match_count"] = row["match_count"]
        candidate["anchor_quality_score"] = row["anchor_quality_score"]
        candidate["anchor_quality_status"] = row["anchor_quality_status"]
        if not row["should_block"]:
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
    weak = sum(1 for row in report if row["anchor_quality_status"] == "weak")
    blocked = sum(1 for row in report if row["should_block"])
    lines.extend([f"- Valid exact matches: {valid}", f"- Weak-quality anchors: {weak}", f"- Blocked: {blocked}", ""])
    for row in report:
        if not row["should_block"]:
            continue
        issues = ", ".join(row.get("anchor_quality_issues", []))
        lines.append(f"- Chapter {row.get('chapter')}: {row.get('candidate_id')} — {row['anchor_status']} / {row['anchor_quality_status']} ({row['match_count']} matches; score {row['anchor_quality_score']}; {issues})")
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
    blocked_rows = [row for row in report if row["should_block"]]
    print(f"validated paragraph anchors: {len(report)} candidates, {len(blocked_rows)} blocked, {changed} candidate records updated")
    for row in blocked_rows:
        print(f"anchor blocked: chapter {row.get('chapter')} {row.get('candidate_id')} {row['anchor_status']}/{row['anchor_quality_status']} score={row['anchor_quality_score']}: {row.get('paragraph_anchor', '')}")


if __name__ == "__main__":
    main()
