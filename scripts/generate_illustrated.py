#!/usr/bin/env python3
"""Generate Illustrated Reader chapter shells from exact manuscript authority.

This extends the existing illustrated reading mode beyond Chapter 155 without
inventing art. If promoted chapter art exists, it is distributed through the
prose; otherwise the chapter renders cleanly as prose in the same reader shell.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from generate_light import Chapter, load_all_sources, selected_numbers

CHAPTERS_DIR = Path("chapters")
ART_ROOT = Path("visual/chapter_art")
INDEX = Path("index.html")
ART_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def chapter_art(number: int) -> list[Path]:
    directory = ART_ROOT / f"{number:03d}"
    if not directory.exists():
        return []
    return sorted(
        path for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in ART_EXTENSIONS
    )


def _art_figure(path: Path, number: int) -> str:
    src = "../" + path.as_posix()
    return (
        '<figure class="chapter-art scene-illustration">'
        f'<img src="{html.escape(src, quote=True)}" '
        f'alt="A story scene from Chapter {number}." loading="lazy"/>'
        "</figure>"
    )


def prose_with_art(prose_html: str, art: list[Path], number: int) -> str:
    if not art:
        return prose_html
    paragraphs = re.findall(r"<p>.*?</p>", prose_html, flags=re.S)
    if not paragraphs:
        return prose_html + "\n" + "\n".join(_art_figure(path, number) for path in art)

    slots: dict[int, list[Path]] = {}
    total = len(paragraphs)
    for idx, path in enumerate(art, start=1):
        slot = max(1, min(total, round(idx * total / (len(art) + 1))))
        slots.setdefault(slot, []).append(path)

    rendered: list[str] = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        rendered.append(paragraph)
        for path in slots.get(idx, []):
            rendered.append(_art_figure(path, number))
    return "\n".join(rendered)


def render_chapter(chapter: Chapter, all_numbers: list[int], art: list[Path]) -> str:
    available = set(all_numbers)
    previous = chapter.number - 1
    following = chapter.number + 1
    prev_link = (
        f'<a rel="prev" href="{previous:03d}.html">← Chapter {previous}</a>'
        if previous in available else '<span class="is-disabled">← Previous</span>'
    )
    next_link = (
        f'<a rel="next" href="{following:03d}.html">Chapter {following} →</a>'
        if following in available else '<span class="is-disabled">Next →</span>'
    )
    prose = prose_with_art(chapter.prose_html, art, chapter.number)
    title = html.escape(chapter.title)
    title_case = html.escape(chapter.title.title())
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><meta name="description" content="Peg-Leg Greg Chapter {chapter.number}: {title_case}."/><title>Chapter {chapter.number}: {title_case} — Peg-Leg Greg</title><link href="../assets/reader.css" rel="stylesheet"/></head>
<body><header class="site-head"><a href="../index.html">PEG-LEG GREG</a><nav aria-label="Reader navigation" class="site-nav"><a href="../index.html#chapters">CHAPTERS</a><a href="../light/{chapter.number:03d}.html">TEXT</a><a href="../art.html">ART</a></nav></header>
<main class="chapter-shell"><nav class="chapter-nav chapter-nav-top" aria-label="Chapter navigation">{prev_link}<a href="../index.html#chapters">Chapters</a>{next_link}</nav><header class="chapter-title"><div class="number">CHAPTER {chapter.number}</div><h1>{title}</h1></header><article class="prose">{prose}</article><nav class="chapter-nav" aria-label="Chapter navigation">{prev_link}<a href="../index.html#chapters">Chapters</a>{next_link}</nav></main>
<script>try{{localStorage.setItem('plg:lastIllustratedChapter','{chapter.number}')}}catch(e){{}}</script></body></html>'''


def promote_index_links(numbers: list[int]) -> None:
    if not INDEX.exists():
        return
    text = INDEX.read_text(encoding="utf-8")
    for number in numbers:
        text = text.replace(f'href="light/{number:03d}.html"', f'href="chapters/{number:03d}.html"')
        text = text.replace(f'href="light.html?chapter={number}"', f'href="chapters/{number:03d}.html"')
    INDEX.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate static Illustrated Reader chapters from exact prose authority.")
    parser.add_argument("range", help="N-N, for example 156-219")
    args = parser.parse_args()

    all_chapters = load_all_sources()
    wanted = selected_numbers(args.range, all_chapters)
    if not wanted:
        raise SystemExit(f"no chapters available for {args.range}")

    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    all_numbers = sorted(all_chapters)
    for number in wanted:
        chapter = all_chapters[number]
        (CHAPTERS_DIR / f"{number:03d}.html").write_text(
            render_chapter(chapter, all_numbers, chapter_art(number)),
            encoding="utf-8",
        )
    promote_index_links(wanted)
    print(f"generated {len(wanted)} Illustrated Reader chapters: {wanted[0]}-{wanted[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
