#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from generate_light import Chapter, load_all_sources, selected_numbers

CHAPTERS_DIR = Path('chapters')
FIGURE_ANCHOR_RE = re.compile(
    r'(?P<figures>(?:<figure\b.*?</figure>\s*)+)(?P<anchor><p\b[^>]*>.*?</p>)',
    re.IGNORECASE | re.DOTALL,
)
NAV_RE = re.compile(
    r'<nav\b(?=[^>]*\bclass=["\'][^"\']*\bchapter-nav\b[^"\']*["\'])[^>]*>.*?</nav>',
    re.IGNORECASE | re.DOTALL,
)
ARTICLE_RE = re.compile(
    r'<article\b[^>]*class=["\'][^"\']*\bprose\b[^"\']*["\'][^>]*>(.*?)</article>',
    re.IGNORECASE | re.DOTALL,
)


def preserved_figure_blocks(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding='utf-8')
    article_match = ARTICLE_RE.search(text)
    if not article_match:
        return []
    preserved: list[tuple[str, str]] = []
    for match in FIGURE_ANCHOR_RE.finditer(article_match.group(1)):
        preserved.append((match.group('anchor'), match.group('figures').strip()))
    return preserved


def restore_figures(prose_html: str, preserved: list[tuple[str, str]], *, chapter: int) -> str:
    updated = prose_html
    for anchor, figures in preserved:
        if anchor not in updated:
            raise SystemExit(
                f'Ch{chapter}: promoted art anchor no longer matches exact prose; reposition art before regenerating'
            )
        updated = updated.replace(anchor, figures + anchor, 1)
    return updated


def chapter_nav(number: int, generated: set[int]) -> str:
    available = set(generated)
    available.update({154, 155})
    previous = number - 1
    following = number + 1
    links: list[str] = []
    if previous in available:
        links.append(f'<a rel="prev" href="{previous:03d}.html">← Previous</a>')
    links.append('<a class="toclink" href="../index.html#chapters">Table of Contents</a>')
    if following in available:
        links.append(f'<a rel="next" href="{following:03d}.html">Next →</a>')
    return '<nav aria-label="Chapter navigation" class="chapter-nav">' + ''.join(links) + '</nav>'


def render_chapter(chapter: Chapter, generated: set[int], prose_html: str) -> str:
    light_path = f'../light/{chapter.number:03d}.html'
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><meta name="description" content="Peg-Leg Greg Chapter {chapter.number}: {html.escape(chapter.title.title())}."/><title>Chapter {chapter.number}: {html.escape(chapter.title.title())} — Peg-Leg Greg</title><link href="../assets/reader.css" rel="stylesheet"/></head><body><header class="site-head"><a href="../index.html">PEG-LEG GREG</a><nav aria-label="Reader navigation" class="site-nav"><a href="{light_path}">LIGHT</a><a href="../art.html">ART</a></nav></header><main class="chapter-shell"><header class="chapter-title"><div class="number">CHAPTER {chapter.number}</div><h1>{html.escape(chapter.title)}</h1></header><article class="prose">{prose_html}</article>{chapter_nav(chapter.number, generated)}</main></body></html>
'''


def patch_previous_edge(generated: set[int]) -> None:
    if 156 not in generated:
        return
    path = CHAPTERS_DIR / '155.html'
    if not path.exists():
        raise SystemExit('cannot connect illustrated edge: chapters/155.html is missing')
    original = path.read_text(encoding='utf-8')
    replacement = chapter_nav(155, generated)
    if NAV_RE.search(original):
        updated = NAV_RE.sub(replacement, original, count=1)
    else:
        raise SystemExit('cannot connect illustrated edge: Chapter 155 navigation not found')
    if updated != original:
        path.write_text(updated, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate exact-prose static Peg-Leg Greg Illustrated reader derivatives.')
    parser.add_argument('range', help='N-N, for example 156-235')
    args = parser.parse_args()

    all_chapters = load_all_sources()
    wanted = selected_numbers(args.range, all_chapters)
    if not wanted:
        raise SystemExit(f'no chapters available for {args.range}')
    generated = set(wanted)
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

    for number in wanted:
        chapter = all_chapters[number]
        path = CHAPTERS_DIR / f'{number:03d}.html'
        preserved = preserved_figure_blocks(path)
        prose = restore_figures(chapter.prose_html, preserved, chapter=number)
        path.write_text(render_chapter(chapter, generated, prose), encoding='utf-8')

    patch_previous_edge(generated)
    print(f'generated {len(wanted)} Illustrated chapters for {args.range}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
