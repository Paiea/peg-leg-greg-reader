#!/usr/bin/env python3
"""Build manuscript-only Peg-Leg Greg sources for NotebookLM.

The export follows repository manuscript authority for prose and the reader
Book/Act map for structural boundaries.

Books I and II remain single files. Book III onward exports one file per Act
so large later Books stay comfortably uploadable to NotebookLM.

No state, planning, summaries, or authorial-direction files are included in
the manuscript sources. A small optional structure map is emitted separately.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from reader_sections import BOOKS

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "state" / "manuscript"
OUT = ROOT / "exports" / "notebooklm"

BOOK1_DOCX = M / "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx"
BOOK2_DOCX = M / "Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx"
CH138_155 = M / "Peg_Leg_Greg_Running_Manuscript_Ch138-155.md"
CH156_219 = M / "Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md"
CH220_248 = M / "Peg_Leg_Greg_Running_Manuscript.md"


def docx_to_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for p in root.findall(".//w:body/w:p", ns):
        text = "".join((t.text or "") for t in p.findall(".//w:t", ns))
        if text.strip():
            paragraphs.append(text)
    return "\n\n".join(paragraphs).strip() + "\n"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def chapter_start(text: str, number: int) -> int:
    for pattern in (rf"(?im)^#{{1,6}}\s*CHAPTER\s+{number}\b.*$", rf"(?im)^CHAPTER\s+{number}\b.*$"):
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
        raise ValueError(f"Checkpoint gap: missing {sorted(set(expected) - set(nums))}")
    return "\n\n".join(read(path).strip() for _, path in found) + "\n", nums


def roman_token(label: str) -> str:
    return label.split()[-1]


def title_token(title: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", title.upper()).strip("_")


def write_source(filename: str, title: str, chapters: str, text: str) -> None:
    header = f"# PEG-LEG GREG — {title}\n\n**Manuscript-only NotebookLM source. Chapters {chapters}.**\n\n---\n\n"
    (OUT / filename).write_text(header + text.strip() + "\n", encoding="utf-8")


def clean_generated_sources() -> None:
    for path in OUT.glob("PLG_*.md"):
        path.unlink()


def write_structure_map(latest: int) -> None:
    lines = [
        "# Peg-Leg Greg — Current Structure Map",
        "",
        f"Current exported endpoint: **Chapter {latest}**.",
        "",
        "This file is optional orientation for NotebookLM. The manuscript files remain prose-only.",
        "",
    ]
    for book in BOOKS:
        if book.start > latest:
            continue
        book_end = book.effective_end(latest)
        lines.append(f"## {book.numeral} — Chapters {book.start}–{book_end}")
        lines.append("")
        for act in book.acts:
            if act.start > latest:
                continue
            act_end = act.effective_end(latest)
            lines.append(f"- {act.numeral}: Chapters {act.start}–{act_end}, **{act.title}**")
        lines.append("")
    (OUT / "PLG_STRUCTURE_MAP.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    required = [BOOK1_DOCX, BOOK2_DOCX, CH138_155, CH156_219, CH220_248]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        print("Missing required authority files:", *missing, sep="\n- ", file=sys.stderr)
        return 1

    recovered = read(CH156_219)
    running = read(CH220_248)
    checkpoints, nums = checkpoints_from(249)
    latest = max(nums)

    book1 = docx_to_text(BOOK1_DOCX)
    book2 = "\n\n".join([
        docx_to_text(BOOK2_DOCX).strip(),
        read(CH138_155).strip(),
        slice_chapters(recovered, 156, 181).strip(),
    ]) + "\n"
    late_manuscript = "\n\n".join([
        slice_chapters(recovered, 181).strip(),
        slice_chapters(running, 220).strip(),
        checkpoints.strip(),
    ]) + "\n"

    OUT.mkdir(parents=True, exist_ok=True)
    clean_generated_sources()

    write_source("PLG_BOOK_I_CH001-082.md", "BOOK I", "1–82", book1)
    write_source("PLG_BOOK_II_CH083-180.md", "BOOK II", "83–180", book2)

    for book in BOOKS[2:]:
        if book.start > latest:
            continue
        for act in book.acts:
            if act.start > latest:
                continue
            end = act.effective_end(latest)
            after_last = end + 1 if end < latest else None
            act_text = slice_chapters(late_manuscript, act.start, after_last)
            filename = (
                f"PLG_BOOK_{roman_token(book.numeral)}_ACT_{roman_token(act.numeral)}_"
                f"CH{act.start:03d}-{end:03d}_{title_token(act.title)}.md"
            )
            write_source(
                filename,
                f"{book.numeral} — {act.numeral}: {act.title}",
                f"{act.start}–{end}",
                act_text,
            )

    write_structure_map(latest)

    source_files = sorted(OUT.glob("PLG_BOOK_*.md"))
    (OUT / "README.md").write_text(f"""# Peg-Leg Greg — NotebookLM Sources

Upload the `PLG_BOOK_*.md` files in this folder to one NotebookLM notebook.

Books I and II are whole-Book sources. Book III onward is split by the current Act structure so individual uploads stay manageable as the manuscript grows.

`PLG_STRUCTURE_MAP.md` is optional. Add it when you want NotebookLM to know the intended Book/Act boundaries explicitly. Leave it out for a completely blind structural read.

These are deliberately **manuscript-only** sources. Do not add `MANUSCRIPT_STATE`, `STORY_NORTH_STAR`, plot notes, or other project-brain files for the first cold-read experiment.

Current exported endpoint: **Chapter {latest}**.

Current manuscript source files: **{len(source_files)}**.

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
""", encoding="utf-8")

    print(f"Built NotebookLM manuscript export through Chapter {latest}")
    for path in source_files:
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")
    print((OUT / "PLG_STRUCTURE_MAP.md").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
