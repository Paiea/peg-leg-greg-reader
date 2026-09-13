#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from generate_light import LIGHT_DIR, SHOWCASE_MANIFEST, load_all_sources
from showcase import ShowcaseMap, build_showcase_map, load_showcase_manifest

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


def clean_numeric_pages(directory: Path, canonical_numbers: set[int], showcase: ShowcaseMap) -> list[int]:
    removed: list[int] = []
    for path in sorted(directory.glob('[0-9][0-9][0-9].html')):
        if not path.stem.isdigit():
            continue
        number = int(path.stem)
        if number not in canonical_numbers or showcase.showcase_number(number) is None:
            path.unlink()
            removed.append(number)
    return removed


def inject_terminal_card(directory: Path) -> bool:
    path = directory / f'{TERMINAL_CANON:03d}.html'
    if not path.exists():
        return False
    original = path.read_text(encoding='utf-8')
    if TERMINAL_CARD_MARKER in original:
        return False
    close_article = original.find('</article>')
    if close_article < 0:
        raise ValueError(f'Chapter {TERMINAL_CANON}: closing article not found for terminal card')
    insert_at = close_article + len('</article>')
    updated = original[:insert_at] + TERMINAL_CARD + original[insert_at:]
    path.write_text(updated, encoding='utf-8')
    return True


def main() -> int:
    all_chapters = load_all_sources()
    showcase = build_showcase_map(
        sorted(all_chapters),
        load_showcase_manifest(SHOWCASE_MANIFEST),
    )
    removed = clean_numeric_pages(LIGHT_DIR, set(all_chapters), showcase)
    card_added = inject_terminal_card(LIGHT_DIR)
    print(f'removed {len(removed)} hidden or orphan Text Reader pages')
    print('added PLG terminal R2 card' if card_added else 'PLG terminal R2 card already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())