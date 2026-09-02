#!/usr/bin/env python3
"""Build manuscript-only Peg-Leg Greg sources for NotebookLM.

The export follows repository authority rather than the public reader crawl:
Book I: authoritative Ch1-82 DOCX
Book II: authoritative Ch83-137 DOCX + exact Ch138-155 MD + recovered exact Ch156-180
Book III: recovered exact Ch181-219 + running Ch220-248 + exact checkpoint Ch249+

No state, planning, summaries, or authorial-direction files are included in the exported books.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "state" / "manuscript"
OUT = ROOT / "exports" / "notebooklm"

BOOK1_DOCX = M / "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx"
BOOK2_DOCX = M / "Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx"
CH138_155 = M / "Peg_Leg_Greg_Running_Manuscript_Ch138-155.md"
CH156_219 = M / "Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md"
CH220_248 = M / "Peg_Leg_Greg_Running_Manuscript.md"


def docx_to_text(path: Path) -> str:
    """Extract paragraph text from DOCX without altering prose."""
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for p in root.findall(".//w:body/w:p", ns):
        parts = [t.text or "" for t in p.findall(".//w:t", ns)]
        text = "".join(parts)
        if text.strip():
            paragraphs.append(text)
    return "\n\n".join(paragraphs).strip() + "\n"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def chapter_start(text: str, number: int) -> int:
    patterns = [
        rf"(?im)^#{{1,6}}\s*CHAPTER\s+{number}\b.*$",
        rf"(?im)^CHAPTER\s+{number}\b.*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.start()
    raise ValueError(f"Could not find Chapter {number} boundary")


def slice_chapters(text: str, first: int, after_last: int | None = None) -> str:
    start = chapter_start(text, first)
    end = chapter_start(text, after_last) if after_last is not None else len(text)
    return text[start:end].strip() + "\n"


def checkpoint_number(path: Path) -> int | None:
    match = re.search(r"Chapter_(\d+)_EXACT", path.name, re.I)
    return int(match.group(1)) if match else None


def checkpoints_from(first: int) -> tuple[str, list[int]]:
    found: list[tuple[int, Path]] = []
    for path in M.glob("Peg_Leg_Greg_Chapter_*_EXACT*.md"):
        n = checkpoint_number(path)
        if n is not None and n >= first:
            found.append((n, path))
    found.sort()
    if not found:
        raise ValueError(f"No exact checkpoint chapters found from {first}")
    nums = [n for n, _ in found]
    expected = list(range(first, max(nums) + 1))
    if nums != expected:
        missing = sorted(set(expected) - set(nums))
        raise ValueError(f"Checkpoint gap: missing {missing}")
    return "\n\n".join(read(path).strip() for _, path in found) + "\n", nums


def clean_source_banner(text: str) -> str:
    # Keep chapter prose untouched. Only normalize surrounding whitespace.
    return text.strip() + "\n"


def write_book(filename: str, title: str, chapters: str, text: str) -> None:
    header = (
        f"# PEG-LEG GREG — {title}\n\n"
        f"**Manuscript-only NotebookLM source. Chapters {chapters}.**\n\n"
        "This export contains story text only. Planning/state files are intentionally excluded.\n\n"
        "---\n\n"
    )
    (OUT / filename).write_text(header + clean_source_banner(text), encoding="utf-8")


def main() -> int:
    required = [BOOK1_DOCX, BOOK2_DOCX, CH138_155, CH156_219, CH220_248]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        print("Missing required authority files:", *missing, sep="\n- ", file=sys.stderr)
        return 1

    recovered = read(CH156_219)
    running = read(CH220_248)
    checkpoints, nums = checkpoints_from(249)

    book1 = docx_to_text(BOOK1_DOCX)
    book2 = "\n\n".join([
        docx_to_text(BOOK2_DOCX).strip(),
        read(CH138_155).strip(),
        slice_chapters(recovered, 156, 181).strip(),
    ]) + "\n"
    book3 = "\n\n".join([
        slice_chapters(recovered, 181).strip(),
        slice_chapters(running, 220).strip(),
        checkpoints.strip(),
    ]) + "\n"

    OUT.mkdir(parents=True, exist_ok=True)
    write_book("PLG_BOOK_I_CH001-082.md", "BOOK I", "1–82", book1)
    write_book("PLG_BOOK_II_CH083-180.md", "BOOK II", "83–180", book2)
    write_book(
        f"PLG_BOOK_III_CH181-{max(nums):03d}.md",
        "BOOK III — CURRENT",
        f"181–{max(nums)}",
        book3,
    )

    readme = f"""# Peg-Leg Greg — NotebookLM Sources

Upload the three `PLG_BOOK_*.md` files in this folder to one NotebookLM notebook.

These are deliberately **manuscript-only** sources. Do not add `MANUSCRIPT_STATE`, `STORY_NORTH_STAR`, plot notes, or other project-brain files for the first cold-read experiment.

Current exported endpoint: **Chapter {max(nums)}**.

Suggested first chat prompt:

> Read Peg-Leg Greg broadly across the complete manuscript before answering. Treat this as a serious long-form fantasy novel and come in as an engaged reader and book-club partner, not as someone whose job is to encourage me.
>
> I don't want you to infer the novel from chapter titles or project notes. Ground your interpretation in the actual prose, scenes, dialogue, character behavior, and changes across the manuscript.
>
> Look longitudinally. Pay attention to changes that take dozens or hundreds of chapters to become visible. Surprise me with patterns, strengths, weaknesses, themes, character developments, contradictions, and things I may have written without consciously realizing it.
>
> Don't automatically criticize slowness, mundane life, or repetition, but don't protect them from criticism either.
>
> I told you I dabbled in writing and then showed you Peg-Leg Greg. You've now read the actual thing. **What do you think I made?**
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    print(f"Built NotebookLM manuscript export through Chapter {max(nums)}")
    for path in sorted(OUT.glob("PLG_BOOK_*.md")):
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
