#!/usr/bin/env python3
"""Audit active Peg-Leg Greg canon for residual dialogue ownership candidates."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.apply_dialogue_ownership_novel import active_source_map
from scripts.dialogue_ownership_engine import mixed_owner_candidate, split_paragraph
from scripts.generate_light import load_all_sources

REPORT = ROOT / "state" / "editorial" / "dialogue-ownership-pass" / "WHOLE_NOVEL_REPORT.md"
P_RE = re.compile(r"<p>(.*?)</p>", re.S)


def paragraph_texts(prose_html: str) -> list[str]:
    result: list[str] = []
    for match in P_RE.finditer(prose_html):
        content = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        if content:
            result.append(content)
    return result


def main() -> int:
    sources = active_source_map()
    chapters = load_all_sources()
    if not sources or not chapters:
        raise SystemExit("canon sources are unavailable")

    frontier = max(sources)
    missing = [number for number in range(1, frontier + 1) if number not in chapters]
    if missing:
        preview = ", ".join(str(n) for n in missing[:30])
        raise SystemExit(f"active canon coverage has missing chapters: {preview}")

    transformable: Counter[int] = Counter()
    explicit_mixed: Counter[int] = Counter()
    dialogue_paragraphs = 0

    for number in range(1, frontier + 1):
        chapter = chapters[number]
        for paragraph in paragraph_texts(chapter.prose_html):
            if '"' not in paragraph:
                continue
            dialogue_paragraphs += 1
            if len(split_paragraph(paragraph)) > 1:
                transformable[number] += 1
            if mixed_owner_candidate(paragraph):
                explicit_mixed[number] += 1

    source_counts = Counter(str(path.relative_to(ROOT)) for path in sources.values())
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Whole-Novel Dialogue Ownership Report",
        "",
        "Status: GENERATED AUDIT",
        "",
        f"- Canon frontier: Chapter {frontier}",
        f"- Canon chapters checked: {frontier}",
        f"- Dialogue-bearing paragraphs checked: {dialogue_paragraphs}",
        f"- Residual automatically transformable paragraphs: {sum(transformable.values())}",
        f"- Residual explicit mixed-owner candidates: {sum(explicit_mixed.values())}",
        "",
        "## Active source map",
        "",
    ]
    for source, count in sorted(source_counts.items()):
        lines.append(f"- `{source}`: {count} active chapters")

    lines.extend(["", "## Residual transformable chapters", ""])
    if transformable:
        for chapter, count in sorted(transformable.items()):
            lines.append(f"- Chapter {chapter}: {count}")
    else:
        lines.append("None detected by the deterministic ownership engine.")

    lines.extend(["", "## Residual explicit mixed-owner candidates", ""])
    if explicit_mixed:
        for chapter, count in sorted(explicit_mixed.items()):
            lines.append(f"- Chapter {chapter}: {count}")
    else:
        lines.append("None detected by the explicit-owner audit.")

    lines.extend([
        "",
        "## Interpretation",
        "",
        "A zero residual count means the deterministic engine has converged on the patterns it knows how to classify. It does not prove every semantic attribution in the novel is perfect. Ambiguous pronouns, unusual action verbs, and context-dependent speaker changes can still require human reading. The governing rule remains `state/editorial/DIALOGUE_OWNERSHIP_ENGINE.md`.",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(
        f"audited chapters 1-{frontier}: {dialogue_paragraphs} dialogue paragraphs, "
        f"{sum(transformable.values())} transformable residuals, "
        f"{sum(explicit_mixed.values())} explicit mixed-owner candidates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
