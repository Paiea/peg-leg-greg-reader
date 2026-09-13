#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

from generate_light import load_all_sources
from showcase import ShowcaseMap, build_showcase_map, load_showcase_manifest

CHAPTERS_DIR = Path('chapters')
SHOWCASE_MANIFEST = Path('publishing/showcase_chapters.json')
TERMINAL_CANON = 503
TERMINAL_CARD_MARKER = 'plg-terminal-end-card'
TERMINAL_CARD = '''
<section class="plg-terminal-end-card" aria-labelledby="plg-terminal-title">
  <p class="plg-terminal-kicker">THE END</p>
  <h2 id="plg-terminal-title">Original Peg-Leg Greg ends at <em>THE AMATEUR</em>.</h2>
  <p>Greg’s life keeps going. The book does not.</p>
  <p class="plg-terminal-r2-copy">Want to meet Greg again? R2 is a separate second run, rebuilt from the beginning and made audio-first.</p>
  <a class="plg-terminal-r2-link" href="../r2/">START R2 →</a>
</section>
'''


def _nav_html(canon: int, showcase: ShowcaseMap, *, top: bool) -> str:
    previous = showcase.previous_visible(canon)
    following = showcase.next_visible(canon)
    prev_html = '<span class="is-disabled">← Previous</span>'
    next_html = '<span class="is-disabled">Next →</span>'
    if previous is not None:
        prev_html = (
            f'<a rel="prev" href="{previous:03d}.html">'
            f'← Chapter {showcase.showcase_number(previous)}</a>'
        )
    if following is not None:
        next_html = (
            f'<a rel="next" href="{following:03d}.html">'
            f'Chapter {showcase.showcase_number(following)} →</a>'
        )
    classes = 'chapter-nav chapter-nav-top' if top else 'chapter-nav'
    return (
        f'<nav class="{classes}" aria-label="Chapter navigation">'
        f'{prev_html}<a href="../index.html#books">Chapters</a>{next_html}</nav>'
    )


def _inject_terminal_card(text: str, canon: int) -> str:
    if canon != TERMINAL_CANON or TERMINAL_CARD_MARKER in text:
        return text
    close_article = text.find('</article>')
    if close_article < 0:
        raise ValueError(f'Chapter {canon}: closing article not found for terminal card')
    insert_at = close_article + len('</article>')
    return text[:insert_at] + TERMINAL_CARD + text[insert_at:]


def patch_illustrated_html(text: str, canon: int, showcase: ShowcaseMap) -> str:
    display = showcase.showcase_number(canon)
    if display is None:
        return text

    updated = text.replace('../index.html#chapters', '../index.html#books')
    if 'href="../r2/"' not in updated:
        updated = updated.replace(
            '<a href="../art.html">ART</a>',
            '<a href="../art.html">ART</a><a href="../r2/">R2</a>',
            1,
        )
    updated = re.sub(
        r'(<title>\s*Chapter\s+)\d+(\s*:)',
        rf'\g<1>{display}\g<2>',
        updated,
        count=1,
        flags=re.I,
    )
    updated = re.sub(
        r'(<div[^>]*class=["\'][^"\']*number[^"\']*["\'][^>]*>\s*CHAPTER\s+)\d+(\s*</div>)',
        rf'\g<1>{display}\g<2>',
        updated,
        count=1,
        flags=re.I,
    )
    updated = re.sub(
        r'(content=["\'][^"\']*Peg-Leg Greg Chapter\s+)\d+(\s*:)',
        rf'\g<1>{display}\g<2>',
        updated,
        count=1,
        flags=re.I,
    )

    nav_re = re.compile(
        r'<nav[^>]*class=["\'][^"\']*chapter-nav[^"\']*["\'][^>]*>.*?</nav>',
        re.I | re.S,
    )
    matches = list(nav_re.finditer(updated))
    if matches:
        pieces: list[str] = []
        cursor = 0
        for index, match in enumerate(matches):
            pieces.append(updated[cursor:match.start()])
            pieces.append(_nav_html(canon, showcase, top=index == 0))
            cursor = match.end()
        pieces.append(updated[cursor:])
        updated = ''.join(pieces)
    else:
        main_match = re.search(
            r'<main[^>]*class=["\'][^"\']*chapter-shell[^"\']*["\'][^>]*>',
            updated,
            re.I,
        )
        if not main_match:
            raise ValueError(f'Chapter {canon}: chapter-shell main not found')
        top_nav = _nav_html(canon, showcase, top=True)
        updated = updated[:main_match.end()] + top_nav + updated[main_match.end():]
        close_main = updated.rfind('</main>')
        if close_main < 0:
            raise ValueError(f'Chapter {canon}: closing main not found')
        bottom_nav = _nav_html(canon, showcase, top=False)
        updated = updated[:close_main] + bottom_nav + updated[close_main:]

    return _inject_terminal_card(updated, canon)


def main() -> int:
    all_chapters = load_all_sources()
    showcase = build_showcase_map(sorted(all_chapters), load_showcase_manifest(SHOWCASE_MANIFEST))
    changed = 0
    checked = 0
    for path in sorted(CHAPTERS_DIR.glob('[0-9][0-9][0-9].html')):
        if not path.stem.isdigit():
            continue
        canon = int(path.stem)
        if canon not in all_chapters:
            continue
        checked += 1
        original = path.read_text(encoding='utf-8')
        updated = patch_illustrated_html(original, canon, showcase)
        if updated != original:
            path.write_text(updated, encoding='utf-8')
            changed += 1
    print(f'patched {changed} of {checked} Illustrated chapter shells for Showcase')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())