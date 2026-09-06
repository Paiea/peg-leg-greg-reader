from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_illustration_backlog import count_chapter_images
from scripts.illustration_state import load_registry, load_scene_candidates

CHAPTER_DIR = ROOT / "chapters"
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_COVERAGE.md"

IMG_RE = re.compile(r'<figure\b[^>]*class="[^"]*\bchapter-art\b[^>]*>.*?<img\b[^>]*src="([^"]+)"', re.I | re.S)


def _normalize_live_src(src: str) -> str:
    while src.startswith("../"):
        src = src[3:]
    return src.lstrip("./")


def _preview(values: list[int]) -> str:
    return ", ".join(str(value) for value in values) if values else "none"


def find_unmanaged_live_art(chapter_dir: Path, registry: list[dict]) -> list[str]:
    registered = {
        record.get("live_asset", "")
        for record in registry
        if record.get("status") == "live" and record.get("live_asset")
    }
    found: set[str] = set()
    for path in sorted(chapter_dir.glob("[0-9][0-9][0-9].html")):
        text = path.read_text(encoding="utf-8")
        for src in IMG_RE.findall(text):
            normalized = _normalize_live_src(src)
            if normalized and normalized not in registered:
                found.add(normalized)
    return sorted(found)


def assert_no_unmanaged_live_art(unmanaged: list[str]) -> None:
    if not unmanaged:
        return
    preview = ", ".join(unmanaged[:5])
    suffix = "" if len(unmanaged) <= 5 else f" (+{len(unmanaged) - 5} more)"
    raise ValueError(f"unmanaged live art: {preview}{suffix}")


def summarize_coverage(
    chapter_image_counts: dict[int, int],
    candidates: list[dict],
    registry: list[dict],
    unmanaged_live_art: int = 0,
) -> dict[str, int | list[int]]:
    counts = list(chapter_image_counts.values())
    candidate_chapters = {
        record.get("chapter")
        for record in candidates
        if record.get("status") in {"candidate", "prompt_ready"} and isinstance(record.get("chapter"), int)
    }
    registry_pipeline_chapters = {
        record.get("chapter")
        for record in registry
        if record.get("status") in {"generated", "approved", "live"} and isinstance(record.get("chapter"), int)
    }
    pipeline_chapters = candidate_chapters | registry_pipeline_chapters
    zero_art_chapters = {chapter for chapter, count in chapter_image_counts.items() if count == 0}
    zero_art_without_candidate = sorted(zero_art_chapters - pipeline_chapters)
    prompt_ready_chapters = sorted(
        {
            record.get("chapter")
            for record in candidates
            if record.get("status") == "prompt_ready" and isinstance(record.get("chapter"), int)
        }
    )
    generated_waiting_chapters = sorted(
        {
            record.get("chapter")
            for record in registry
            if record.get("status") == "generated" and isinstance(record.get("chapter"), int)
        }
    )
    return {
        "frontier": max(chapter_image_counts, default=0),
        "total_chapters": len(counts),
        "illustrated_chapters": sum(1 for count in counts if count > 0),
        "zero_art": len(zero_art_chapters),
        "one_art": sum(1 for count in counts if count == 1),
        "two_art": sum(1 for count in counts if count == 2),
        "three_plus_art": sum(1 for count in counts if count >= 3),
        "candidate_unbriefed": sum(1 for record in candidates if record.get("status") == "candidate"),
        "prompt_ready": sum(1 for record in candidates if record.get("status") == "prompt_ready"),
        "generated_awaiting_approval": sum(1 for record in registry if record.get("status") == "generated"),
        "approved_unpublished": sum(1 for record in registry if record.get("status") == "approved"),
        "rejected": sum(1 for record in registry if record.get("status") == "rejected"),
        "queued_candidates": sum(1 for record in candidates if record.get("status") in {"candidate", "prompt_ready"}),
        "registry_live": sum(1 for record in registry if record.get("status") == "live"),
        "zero_art_without_candidate": len(zero_art_without_candidate),
        "top_zero_art_without_candidate": zero_art_without_candidate[:10],
        "top_prompt_ready_chapters": prompt_ready_chapters[:10],
        "top_generated_waiting_chapters": generated_waiting_chapters[:10],
        "unmanaged_live_art": unmanaged_live_art,
    }


def render_coverage_report(summary: dict[str, int | list[int]]) -> str:
    return "\n".join(
        [
            "# PEG-LEG GREG — ILLUSTRATION COVERAGE",
            "",
            f"**Frontier: Chapter {summary['frontier']}**",
            "",
            "## Reader coverage",
            "",
            f"- Total chapter pages: {summary['total_chapters']}",
            f"- Illustrated chapters: {summary['illustrated_chapters']}",
            f"- Zero art: {summary['zero_art']}",
            f"- One art: {summary['one_art']}",
            f"- Two art: {summary['two_art']}",
            f"- Three+ art: {summary['three_plus_art']}",
            "",
            "## Production queue",
            "",
            f"- Candidate, needs prompt pack: {summary['candidate_unbriefed']}",
            f"- Prompt ready / generation ready: {summary['prompt_ready']}",
            f"- Generated, awaiting approval: {summary['generated_awaiting_approval']}",
            f"- Approved but unpublished: {summary['approved_unpublished']}",
            f"- Rejected generation attempts: {summary['rejected']}",
            f"- Zero-art chapters with no active candidate: {summary['zero_art_without_candidate']}",
            f"- Registry live records: {summary['registry_live']}",
            "",
            "## Next actionable chapters",
            "",
            f"- Need scene candidates: {_preview(summary['top_zero_art_without_candidate'])}",
            f"- Ready to generate: {_preview(summary['top_prompt_ready_chapters'])}",
            f"- Waiting for image approval: {_preview(summary['top_generated_waiting_chapters'])}",
            "",
            "## Migration status",
            "",
            f"- Unmanaged legacy live art: {summary['unmanaged_live_art']}",
            "- Existing unmanaged images are migration debt, not a CI failure. New illustration work should enter through the registry-first pipeline.",
            "",
        ]
    )


def main(strict: bool = False) -> None:
    candidates = load_scene_candidates(CANDIDATES_PATH)
    registry = load_registry(REGISTRY_PATH, root=ROOT)
    image_counts = count_chapter_images(CHAPTER_DIR)
    unmanaged = find_unmanaged_live_art(CHAPTER_DIR, registry)
    if strict:
        assert_no_unmanaged_live_art(unmanaged)
    summary = summarize_coverage(image_counts, candidates, registry, unmanaged_live_art=len(unmanaged))
    text = render_coverage_report(summary)
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print(
            f"illustration coverage already current: {summary['illustrated_chapters']}/{summary['total_chapters']} chapters illustrated; "
            f"{summary['unmanaged_live_art']} legacy assets unmanaged"
        )
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(
        f"wrote illustration coverage: {summary['illustrated_chapters']}/{summary['total_chapters']} chapters illustrated; "
        f"{summary['unmanaged_live_art']} legacy assets unmanaged"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report Illustrated Reader coverage and registry state.")
    parser.add_argument("--strict", action="store_true", help="Fail when live chapter art is missing from the registry.")
    args = parser.parse_args()
    main(strict=args.strict)
