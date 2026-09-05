#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path

from reader_sections import render_book_sections

RUNNING = Path('state/manuscript/Peg_Leg_Greg_Running_Manuscript.md')
RECOVERED = Path('state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md')
CHECKPOINT_GLOB = 'Peg_Leg_Greg_Chapter_*_EXACT_WIP.md'
CHAPTERS_DIR = Path('chapters')
LIGHT_DIR = Path('light')
MANIFEST = LIGHT_DIR / 'manifest.json'


@dataclass(frozen=True)
class Chapter:
    number: int
    title: str
    prose_html: str
    source: str


def parse_markdown_chapters(path: Path, source: str) -> dict[int, Chapter]:
    if not path.exists():
        return {}
    text = path.read_text(encoding='utf-8').replace('\r\n', '\n').replace('\r', '\n')
    boundary_re = re.compile(
        r'^(?:# CHAPTER (?P<standard_num>\d+)[ \t]*|## Chapter (?P<combined_num>\d+)[ \t]*[—–-][ \t]*(?P<combined_title>[^\n]+?)[ \t]*)$',
        re.MULTILINE,
    )
    matches = list(boundary_re.finditer(text))
    seen: set[int] = set()
    chapters: dict[int, Chapter] = {}
    for idx, match in enumerate(matches):
        raw_number = match.group('standard_num') or match.group('combined_num')
        number = int(raw_number)
        if number in seen:
            raise SystemExit(f'duplicate chapter {number} in {path}')
        seen.add(number)
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        chunk = text[match.end():end].strip()
        combined_title = match.group('combined_title')
        if combined_title is not None:
            title = combined_title.strip()
            body = chunk
        else:
            title_match = re.search(r'^##\s+(.+?)\s*$', chunk, re.MULTILINE)
            if not title_match:
                continue
            title = title_match.group(1).strip()
            body = chunk[title_match.end():].strip()
        chapters[number] = Chapter(number, title, markdown_blocks_to_html(body), source)
    return chapters


def markdown_blocks_to_html(body: str) -> str:
    blocks = [b.strip() for b in re.split(r'\n\s*\n+', body) if b.strip()]
    rendered = []
    for block in blocks:
        if re.fullmatch(r'-{20,}', block):
            continue
        escaped = html.escape(block, quote=False).replace('\n', '<br>\n')
        rendered.append(f'<p>{escaped}</p>')
    return '\n'.join(rendered)


def parse_published_chapter(path: Path) -> Chapter | None:
    match = re.search(r'(\d+)\.html$', path.name)
    if not match:
        return None
    number = int(match.group(1))
    text = path.read_text(encoding='utf-8')
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    prose_match = re.search(r'<article\b[^>]*class=["\'][^"\']*\bprose\b[^"\']*["\'][^>]*>(.*?)</article>', text, re.I | re.S)
    if not title_match or not prose_match:
        return None
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    prose = prose_match.group(1)
    prose = re.sub(r'<figure\b.*?</figure>', '', prose, flags=re.I | re.S)
    prose = re.sub(r'<script\b.*?</script>', '', prose, flags=re.I | re.S)
    prose = re.sub(r'<img\b[^>]*>', '', prose, flags=re.I | re.S)
    return Chapter(number, html.unescape(title), prose.strip(), 'published')


def load_all_sources() -> dict[int, Chapter]:
    chapters: dict[int, Chapter] = {}
    if CHAPTERS_DIR.exists():
        for path in sorted(CHAPTERS_DIR.glob('[0-9][0-9][0-9].html')):
            chapter = parse_published_chapter(path)
            if chapter and chapter.number <= 155:
                chapters[chapter.number] = chapter
    chapters.update(parse_markdown_chapters(RECOVERED, 'recovered'))

    running = parse_markdown_chapters(RUNNING, 'manuscript')
    chapters.update(running)
    running_edge = max(running, default=0)
    for path in sorted(RUNNING.parent.glob(CHECKPOINT_GLOB)):
        checkpoint = parse_markdown_chapters(path, 'checkpoint')
        chapters.update({n: chapter for n, chapter in checkpoint.items() if n > running_edge})
    return chapters


def load_manifest() -> dict:
    if not MANIFEST.exists():
        return {'latest': None, 'chapters': []}
    try:
        return json.loads(MANIFEST.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return {'latest': None, 'chapters': []}


def href_for(number: int, generated: set[int], *, from_chapter: bool) -> str:
    if number in generated:
        return f'{number:03d}.html'
    return f'../light.html?chapter={number}'


def chapter_nav(chapter: Chapter, all_numbers: list[int], generated: set[int]) -> tuple[str, str]:
    available = set(all_numbers)
    prev_html = '<span class="is-disabled">← Previous</span>'
    next_html = '<span class="is-disabled">Next →</span>'
    previous_number = chapter.number - 1
    next_number = chapter.number + 1
    if previous_number in available:
        prev_html = f'<a rel="prev" href="{href_for(previous_number, generated, from_chapter=True)}">← Chapter {previous_number}</a>'
    if next_number in available:
        next_html = f'<a rel="next" href="{href_for(next_number, generated, from_chapter=True)}">Chapter {next_number} →</a>'
    return prev_html, next_html


def render_chapter(chapter: Chapter, all_numbers: list[int], generated: set[int]) -> str:
    prev_html, next_html = chapter_nav(chapter, all_numbers, generated)
    illustrated = ''
    if (CHAPTERS_DIR / f'{chapter.number:03d}.html').exists():
        illustrated = f'<a class="mode-link" href="../chapters/{chapter.number:03d}.html">Illustrated Reader</a>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Peg-Leg Greg Chapter {chapter.number}: {html.escape(chapter.title.title())}, Text Reader.">
<title>Chapter {chapter.number}: {html.escape(chapter.title)} — Peg-Leg Greg Text Reader</title>
<link rel="stylesheet" href="../assets/reader.css">
<link rel="stylesheet" href="../assets/light.css">
</head>
<body class="light-edition">
<header class="site-head light-site-head"><a class="site-brand" href="../index.html">PEG-LEG GREG</a><nav class="site-nav" aria-label="Site navigation"><a href="../index.html">HOME</a><a href="../index.html#books">ILLUSTRATED READER</a><a aria-current="page" href="index.html">TEXT READER</a><a href="../latest.html">LATEST</a><a href="../art.html">ART</a></nav></header>
<main class="light-page">
<nav class="light-chapter-nav light-chapter-nav-top" aria-label="Chapter navigation">{prev_html}<a href="index.html">Chapters</a>{next_html}</nav>
<header class="light-chapter-title"><p class="light-kicker">TEXT READER · CHAPTER {chapter.number}</p><h1>{html.escape(chapter.title)}</h1><p class="light-mode-note">Text-only reading · no chapter illustrations</p></header>
<article class="prose light-prose">{chapter.prose_html}</article>
<div class="light-mode-switch">{illustrated}</div>
<nav class="light-chapter-nav" aria-label="Chapter navigation">{prev_html}<a href="index.html">Chapters</a>{next_html}</nav>
<p class="light-home-link"><a href="../index.html">Return to Peg-Leg Greg home</a></p>
</main>
<script>try{{localStorage.setItem('plg:lastLightChapter','{chapter.number}')}}catch(e){{}}</script>
</body>
</html>
'''


def render_index(all_chapters: dict[int, Chapter], generated: set[int]) -> str:
    latest = max(all_chapters) if all_chapters else None
    chapter_links: dict[int, str] = {}
    for n in sorted(all_chapters):
        c = all_chapters[n]
        href = f'{n:03d}.html' if n in generated else f'../light.html?chapter={n}'
        chapter_links[n] = f'<a href="{href}"><span class="num">{n}</span><span class="title">{html.escape(c.title.title())}</span></a>'
    book_sections = render_book_sections(chapter_links, illustrated=False, open_first_act=False)

    latest_link = f'<a class="primary-action" href="{latest:03d}.html">Read newest · Chapter {latest}</a>' if latest in generated else (f'<a class="primary-action" href="../light.html?chapter={latest}">Read newest · Chapter {latest}</a>' if latest else '')
    return f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Peg-Leg Greg Text Reader: fast, text-only chapters without illustrations."><title>Text Reader — Peg-Leg Greg</title><link rel="stylesheet" href="../assets/reader.css"><link rel="stylesheet" href="../assets/light.css"><link rel="stylesheet" href="../assets/book-contents.css"></head>
<body class="light-edition light-toc-page">
<header class="site-head light-site-head"><a class="site-brand" href="../index.html">PEG-LEG GREG</a><nav class="site-nav" aria-label="Site navigation"><a href="../index.html">HOME</a><a href="../index.html#books">ILLUSTRATED READER</a><a aria-current="page" href="index.html">TEXT READER</a><a href="../latest.html">LATEST</a><a href="../art.html">ART</a></nav></header>
<main class="light-page"><header class="light-hero"><p class="light-kicker">ONE BOOK · TWO READING MODES</p><h1>Text Reader</h1><p>Text-only Peg-Leg Greg with no chapter illustrations. Built for quick loading and uninterrupted reading.</p><div class="light-actions">{latest_link}<a class="secondary-action" href="../index.html#books">Illustrated Reader</a></div><p class="light-continue" data-light-continue hidden></p></header><section class="light-ranges" aria-label="Text Reader chapter sections">{book_sections}</section></main>
<script src="../assets/light-progress.js"></script>
</body></html>'''


def render_latest(chapter: Chapter, generated: set[int]) -> str:
    target = f'light/{chapter.number:03d}.html' if chapter.number in generated else f'light.html?chapter={chapter.number}'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Newest Peg-Leg Greg chapter."><title>Latest — Peg-Leg Greg</title><link rel="stylesheet" href="assets/reader.css"><link rel="stylesheet" href="assets/light.css"></head><body class="light-edition"><header class="site-head light-site-head"><a class="site-brand" href="index.html">PEG-LEG GREG</a><nav class="site-nav" aria-label="Site navigation"><a href="index.html">HOME</a><a href="index.html#books">ILLUSTRATED READER</a><a href="light/index.html">TEXT READER</a><a aria-current="page" href="latest.html">LATEST</a><a href="art.html">ART</a></nav></header><main class="light-page"><section class="latest-card"><p class="light-kicker">CURRENT CHAPTER</p><h1>Chapter {chapter.number}</h1><h2>{html.escape(chapter.title)}</h2><p>The newest chapter in the Text Reader.</p><a class="primary-action" href="{target}">Read Chapter {chapter.number}</a><p><a href="light/index.html">Browse the Text Reader</a> · <a href="index.html">Return home</a></p></section></main></body></html>'''


def selected_numbers(spec: str, all_chapters: dict[int, Chapter]) -> list[int]:
    if spec == 'current':
        return sorted(n for n in all_chapters if n >= 220 and all_chapters[n].source in {'manuscript', 'checkpoint'})
    m = re.fullmatch(r'(\d+)-(\d+)', spec)
    if not m:
        raise SystemExit('range must be current or N-N')
    start, end = map(int, m.groups())
    if start > end:
        start, end = end, start
    expected = list(range(start, end + 1))
    missing = [n for n in expected if n not in all_chapters]
    if missing:
        preview = ', '.join(str(n) for n in missing[:12])
        suffix = '…' if len(missing) > 12 else ''
        raise SystemExit(f'missing chapters for {spec}: {preview}{suffix}')
    return expected


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate static Peg-Leg Greg Light-edition publishing derivatives.')
    parser.add_argument('range', help='current or N-N, for example 156-219')
    args = parser.parse_args()

    all_chapters = load_all_sources()
    wanted = selected_numbers(args.range, all_chapters)
    if not wanted:
        raise SystemExit(f'no chapters available for {args.range}')

    LIGHT_DIR.mkdir(parents=True, exist_ok=True)
    for path in LIGHT_DIR.glob('[0-9][0-9][0-9].html'):
        if path.stem.isdigit() and int(path.stem) not in all_chapters:
            path.unlink()

    previous = load_manifest()
    generated = {
        int(item['number'])
        for item in previous.get('chapters', [])
        if str(item.get('number', '')).isdigit() and int(item['number']) in all_chapters
    }
    generated.update(wanted)

    all_numbers = sorted(all_chapters)
    for number in sorted(generated):
        chapter = all_chapters[number]
        (LIGHT_DIR / f'{number:03d}.html').write_text(render_chapter(chapter, all_numbers, generated), encoding='utf-8')

    manifest_chapters = [
        {'number': n, 'title': all_chapters[n].title, 'source': all_chapters[n].source, 'path': f'{n:03d}.html'}
        for n in sorted(generated)
    ]
    latest = max(all_chapters) if all_chapters else None
    MANIFEST.write_text(json.dumps({'latest': latest, 'chapters': manifest_chapters}, indent=2) + '\n', encoding='utf-8')
    (LIGHT_DIR / 'index.html').write_text(render_index(all_chapters, generated), encoding='utf-8')
    if latest is not None:
        Path('latest.html').write_text(render_latest(all_chapters[latest], generated), encoding='utf-8')
    print(f'generated {len(wanted)} Light chapters: {wanted[0]}-{wanted[-1]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())