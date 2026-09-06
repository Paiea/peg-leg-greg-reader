#!/usr/bin/env python3
"""Build manuscript-only Peg-Leg Greg sources for NotebookLM and editorial reading.

The export follows repository manuscript authority for prose and the reader
Book/Act map for structural boundaries.

Books I and II remain single NotebookLM files. Book III onward exports one
file per Act so large later Books stay comfortably uploadable to NotebookLM.
The editorial read surface is split into small canonical chapter windows for
cheap exact-prose retrieval by workers.

No state, planning, summaries, or authorial-direction files are included in
the manuscript sources. A small optional structure map is emitted separately.
"""

from __future__ import annotations

import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

from reader_sections import BOOKS

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "state" / "manuscript"
OUT = ROOT / "exports" / "notebooklm"
READABLE_OUT = ROOT / "state" / "manuscript-readable"
CHAPTERS = ROOT / "chapters"
READABLE_CHUNK_SIZE = 10
STATIC_EXACT_LAST = 155

BOOK1_DOCX = M / "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx"
BOOK2_DOCX = M / "Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx"
CH138_155 = M / "Peg_Leg_Greg_Running_Manuscript_Ch138-155.md"
CH156_219 = M / "Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md"
CH220_248 = M / "Peg_Leg_Greg_Running_Manuscript.md"

CHAPTER_BOUNDARY = re.compile(r"(?im)^(?:#{1,6}\s*)?CHAPTER\s+(\d+)\b.*$")
READABLE_HEADER = (
    "# DERIVED EDITORIAL READ SURFACE\n\n"
    "**NON-AUTHORITATIVE. GENERATED FROM CURRENT MANUSCRIPT AUTHORITY. DO NOT EDIT.**\n\n"
)


class _CanonicalChapterHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_h1 = False
        self.in_prose = False
        self.figure_depth = 0
        self.in_paragraph = False
        self.title_parts: list[str] = []
        self.paragraph_parts: list[str] = []
        self.paragraphs: list[str] = []

    @staticmethod
    def _classes(attrs: list[tuple[str, str | None]]) -> set[str]:
        for name, value in attrs:
            if name == "class" and value:
                return set(value.split())
        return set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h1":
            self.in_h1 = True
        if tag == "article" and "prose" in self._classes(attrs):
            self.in_prose = True
            return
        if not self.in_prose:
            return
        if tag == "figure":
            self.figure_depth += 1
            return
        if self.figure_depth:
            return
        if tag == "p":
            self.in_paragraph = True
            self.paragraph_parts = []
        elif tag == "br" and self.in_paragraph:
            self.paragraph_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_h1 = False
        if not self.in_prose:
            return
        if tag == "figure" and self.figure_depth:
            self.figure_depth -= 1
            return
        if self.figure_depth:
            return
        if tag == "p" and self.in_paragraph:
            self.paragraphs.append("".join(self.paragraph_parts))
            self.paragraph_parts = []
            self.in_paragraph = False
        elif tag == "article":
            self.in_prose = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.title_parts.append(data)
        if self.in_prose and not self.figure_depth and self.in_paragraph:
            self.paragraph_parts.append(data)


def html_chapter_to_readable(html: str, canonical_number: int) -> str:
    parser = _CanonicalChapterHTMLParser()
    parser.feed(html)
    parser.close()
    title = "".join(parser.title_parts).strip()
    if not title:
        raise ValueError(f"Canonical Chapter {canonical_number} has no title")
    if not parser.paragraphs:
        raise ValueError(f"Canonical Chapter {canonical_number} has no prose paragraphs")
    body = "\n\n".join(parser.paragraphs)
    return f"CHAPTER {canonical_number}\n{title}\n\n{body}\n"


def static_exact_chapters(first: int = 1, last: int = STATIC_EXACT_LAST) -> dict[int, str]:
    chapters: dict[int, str] = {}
    for number in range(first, last + 1):
        path = CHAPTERS / f"{number:03d}.html"
        if not path.exists():
            raise ValueError(f"Missing canonical static Chapter {number}: {path.relative_to(ROOT)}")
        chapters[number] = html_chapter_to_readable(
            path.read_text(encoding="utf-8"),
            canonical_number=number,
        )
    return chapters


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


def split_chapters_exact(text: str) -> dict[int, str]:
    matches = list(CHAPTER_BOUNDARY.finditer(text))
    if not matches:
        raise ValueError("No chapter boundaries found")
    chapters: dict[int, str] = {}
    order: list[int] = []
    for index, match in enumerate(matches):
        number = int(match.group(1))
        if number in chapters:
            raise ValueError(f"Duplicate Chapter {number} in assembled manuscript")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chapters[number] = text[match.start():end].rstrip() + "\n"
        order.append(number)
    expected = list(range(order[0], order[-1] + 1))
    if order != expected:
        raise ValueError(f"Manuscript chapter coverage/order mismatch: expected {expected[0]}-{expected[-1]}, got {order}")
    return chapters


def join_exact_ranges(texts: list[str]) -> dict[int, str]:
    joined: dict[int, str] = {}
    for text in texts:
        current = split_chapters_exact(text)
        overlap = set(joined).intersection(current)
        if overlap:
            raise ValueError(f"Duplicate chapters across exact authority ranges: {sorted(overlap)}")
        joined.update(current)
    numbers = list(joined)
    if numbers and numbers != list(range(numbers[0], numbers[-1] + 1)):
        raise ValueError(f"Exact authority range coverage/order mismatch: got {numbers}")
    return joined


def build_readable_chunks(chapters: dict[int, str], out: Path, chunk_size: int = READABLE_CHUNK_SIZE) -> list[Path]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    numbers = list(chapters)
    if numbers != sorted(numbers) or len(numbers) != len(set(numbers)):
        raise ValueError("chapters must be supplied once in canonical order")
    if numbers and numbers != list(range(numbers[0], numbers[-1] + 1)):
        raise ValueError("chapters must be contiguous")

    out.mkdir(parents=True, exist_ok=True)
    for path in out.glob("[0-9][0-9][0-9]-[0-9][0-9][0-9].md"):
        path.unlink()

    paths: list[Path] = []
    for offset in range(0, len(numbers), chunk_size):
        window = numbers[offset:offset + chunk_size]
        first, last = window[0], window[-1]
        path = out / f"{first:03d}-{last:03d}.md"
        body = "\n".join(chapters[number].rstrip() for number in window) + "\n"
        path.write_text(
            READABLE_HEADER
            + f"Canonical chapters: **{first}–{last}**. Canonical chapter IDs and titles follow below.\n\n---\n\n"
            + body,
            encoding="utf-8",
        )
        paths.append(path)
    return paths


def validate_readable_chunks(out: Path, expected_numbers: list[int]) -> None:
    found: list[int] = []
    for path in sorted(out.glob("[0-9][0-9][0-9]-[0-9][0-9][0-9].md")):
        text = path.read_text(encoding="utf-8")
        if "NON-AUTHORITATIVE" not in text or "DO NOT EDIT" not in text:
            raise ValueError(f"Readable chunk missing derived warning: {path.name}")
        found.extend(int(match.group(1)) for match in CHAPTER_BOUNDARY.finditer(text))
    if found != expected_numbers:
        raise ValueError(f"Readable chunk coverage/order mismatch: expected {expected_numbers}, got {found}")


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

    readable_chapters = static_exact_chapters()
    late_readable = join_exact_ranges([recovered, running, checkpoints])
    readable_chapters.update(late_readable)
    expected_numbers = list(range(1, latest + 1))
    if list(readable_chapters) != expected_numbers:
        raise ValueError(
            f"Assembled manuscript coverage/order mismatch: expected 1-{latest}, "
            f"got {list(readable_chapters)}"
        )

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
    readable_paths = build_readable_chunks(readable_chapters, READABLE_OUT)
    validate_readable_chunks(READABLE_OUT, expected_numbers)

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
    print(f"Built {len(readable_paths)} editorial read chunks through Chapter {latest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
