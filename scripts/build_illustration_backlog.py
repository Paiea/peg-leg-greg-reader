from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.illustration_state import load_registry, load_scene_candidates

CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_BACKLOG.md"
CHAPTER_DIR = ROOT / "chapters"

CARD_ORDER = {"book_card": 0, "act_card": 1, "role_card": 2, "chapter_illustration": 3}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def count_chapter_images(chapter_dir: Path = CHAPTER_DIR) -> dict[int, int]:
    counts: dict[int, int] = {}
    for path in sorted(chapter_dir.glob("[0-9][0-9][0-9].html")):
        try:
            chapter = int(path.stem)
        except ValueError:
            continue
        text = path.read_text(encoding="utf-8")
        counts[chapter] = len(re.findall(r'<figure\b[^>]*class="[^"]*\bchapter-art\b', text, flags=re.I))
    return counts


def build_backlog(
    candidates: list[dict],
    registry: list[dict],
    chapter_image_counts: dict[int, int],
) -> list[dict]:
    live_candidate_ids = {
        record.get("candidate_id")
        for record in registry
        if record.get("status") in {"approved", "live"}
    }
    backlog: list[dict] = []
    for candidate in candidates:
        if candidate.get("status") in {"live", "rejected", "approved"}:
            continue
        if candidate.get("id") in live_candidate_ids:
            continue
        item = dict(candidate)
        item["image_count"] = chapter_image_counts.get(candidate["chapter"], 0)
        backlog.append(item)

    def sort_key(item: dict):
        kind = item.get("kind", "chapter_illustration")
        if kind != "chapter_illustration":
            coverage_rank = -1
        else:
            coverage_rank = min(item.get("image_count", 0), 3)
        return (
            CARD_ORDER.get(kind, 99),
            coverage_rank,
            PRIORITY_ORDER.get(item.get("priority"), 99),
            item.get("chapter", 10**9),
            item.get("id", ""),
        )

    return sorted(backlog, key=sort_key)


def render_backlog(backlog: list[dict]) -> str:
    lines = [
        "# PEG-LEG GREG — ILLUSTRATION BACKLOG",
        "",
        "Generated from manuscript-informed scene candidates plus current Illustrated Reader coverage.",
        "",
    ]
    if not backlog:
        lines.extend(["No queued illustration candidates.", ""])
        return "\n".join(lines)

    for item in backlog:
        count = item.get("image_count", 0)
        noun = "image" if count == 1 else "images"
        lines.extend(
            [
                f"## Chapter {item['chapter']} — {item['chapter_title']}",
                "",
                f"- **Candidate:** `{item['id']}`",
                f"- **Kind:** `{item['kind']}`",
                f"- **Priority:** `{item['priority']}`",
                f"- **Current coverage:** {count} {noun}",
                f"- **Fit target:** `{item['fit_target']}`",
                f"- **Visual hook:** {item['visual_hook']}",
                f"- **Scene:** {item['scene_summary']}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    candidates = load_scene_candidates(CANDIDATES_PATH)
    registry = load_registry(REGISTRY_PATH)
    backlog = build_backlog(candidates, registry, count_chapter_images())
    text = render_backlog(backlog)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print(f"illustration backlog already current: {len(backlog)} candidates")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote illustration backlog: {len(backlog)} candidates")


if __name__ == "__main__":
    main()
