#!/usr/bin/env python3
"""Conservative dialogue/action paragraph ownership cleanup.

Default scope is chapters 001-020. This pass changes paragraph boundaries only.
It deliberately leaves ambiguous cases alone for manual review.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FIRST_PERSON_TAG = re.compile(r'\bI (?:said|asked|answered|replied|added|muttered|told him|told her|told them|said again|asked again)\b')
THIRD_PERSON_TAG = re.compile(r'\b([A-Z][a-z]+) (?:said|asked|answered|replied|added|muttered|continued)\b')

# Exact reader-found/manual cases where an untagged turn still has clear ownership.
EXACT_REPLACEMENTS = {
    '002.html': [
        ('<p>"Your age." He smiled. "How old did you expect me to be?"</p>', '<p>"Your age."</p><p>He smiled. "How old did you expect me to be?"</p>'),
        ('<p>"Fine." He counted silver onto the desk.', '<p>"Fine."</p><p>He counted silver onto the desk.'),
        ('Antonius pushed the coins toward me. "Eight days, Greg." I picked them up.</p>', 'Antonius pushed the coins toward me. "Eight days, Greg."</p><p>I picked them up.</p>'),
        ('<p>"You," I said. She stared. I smiled.</p>', '<p>"You," I said.</p><p>She stared.</p><p>I smiled.</p>'),
    ],
    '003.html': [
        ('<p>"For a test? A bucket," Arlo said. I looked at the cart. The carter looked at me.</p>', '<p>"For a test? A bucket," Arlo said.</p><p>I looked at the cart. The carter looked at me.</p>'),
        ('<p>"Possibly," I said. He set the cup down.</p>', '<p>"Possibly," I said.</p><p>He set the cup down.</p>'),
        ('<p>"Everyone guesses. Professionals write the guess down," I said. He glared at me.</p>', '<p>"Everyone guesses. Professionals write the guess down," I said.</p><p>He glared at me.</p>'),
        ('<p>"Where did you get this idea?" Arlo asked. I smiled. He did not.</p>', '<p>"Where did you get this idea?" Arlo asked.</p><p>I smiled.</p><p>He did not.</p>'),
        ('<p>"Greg," Arlo said. I leaned over the bench.</p>', '<p>"Greg," Arlo said.</p><p>I leaned over the bench.</p>'),
        ('<p>"Cost?" I asked. He named a number. I swore. Arlo smiled for the first time all afternoon.</p>', '<p>"Cost?" I asked.</p><p>He named a number.</p><p>I swore.</p><p>Arlo smiled for the first time all afternoon.</p>'),
        # Stale attribution corruption in Arlo's workshop.
        ('<p>"What?" Antonius asked.</p><p>"Nothing," I said.</p><p>"You keep looking at me," Antonius said.</p><p>"I have a memorable-face problem," I said.</p><p>"Your face?" Antonius asked.</p><p>"Other people\'s." Antonius held out his hand.</p><p>"You\'ve been staring at my hands for five minutes," Arlo said.</p>', '<p>"What?" Arlo asked.</p><p>"Nothing," I said.</p><p>"You keep looking at me," Arlo said.</p><p>"I have a memorable-face problem," I said.</p><p>"Your face?" Arlo asked.</p><p>"Other people\'s."</p><p>Arlo held out his hand.</p><p>"You\'ve been staring at my hands for five minutes," Arlo said.</p>'),
    ],
    '004.html': [
        ('<p>"Too boring." He stayed in the next hand three raises longer than he should have.</p>', '<p>"Too boring."</p><p>He stayed in the next hand three raises longer than he should have.</p>'),
        ('<p>"For me? Apparently." She glanced at my stack.</p>', '<p>"For me? Apparently."</p><p>She glanced at my stack.</p>'),
        ('<p>"You leave small." I looked at the coins. Old calibration rose again. Small. She was right. And wrong.</p>', '<p>"You leave small."</p><p>I looked at the coins. Old calibration rose again. Small. She was right. And wrong.</p>'),
    ],
    '005.html': [
        ('<p>"That\'s not what I meant." I liked him slightly more for that. We went again.', '<p>"That\'s not what I meant."</p><p>I liked him slightly more for that. We went again.'),
        ('<p>"Excellent," I said. He looked concerned.</p>', '<p>"Excellent," I said.</p><p>He looked concerned.</p>'),
        ('<p>I said, "Again." He looked at my breathing.</p>', '<p>I said, "Again."</p><p>He looked at my breathing.</p>'),
        ('<p>"Compulsion." I smiled. He did not.</p>', '<p>"Compulsion."</p><p>I smiled.</p><p>He did not.</p>'),
        ('<p>"Income." He looked up.</p>', '<p>"Income."</p><p>He looked up.</p>'),
        ('<p>"Which?" I opened my mouth.</p>', '<p>"Which?"</p><p>I opened my mouth.</p>'),
        ('<p>I said, "It was." Antonius leaned back.</p>', '<p>I said, "It was."</p><p>Antonius leaned back.</p>'),
        ('<p>"When is the next payment?" I asked. He told me.</p>', '<p>"When is the next payment?" I asked.</p><p>He told me.</p>'),
        ('<p>"Stop borrowing." I laughed. He did not.</p>', '<p>"Stop borrowing."</p><p>I laughed.</p><p>He did not.</p>'),
        ('<p>I said, "I have plans." Antonius watched me.</p>', '<p>I said, "I have plans."</p><p>Antonius watched me.</p>'),
        ('<p>"Fine," I wheezed. He leaned over me.</p>', '<p>"Fine," I wheezed.</p><p>He leaned over me.</p>'),
        ('<p>"Excellent," I added. He continued staring.</p>', '<p>"Excellent," I added.</p><p>He continued staring.</p>'),
        ('<p>"Do you have another appointment?" I considered lying. He knew I did not.', '<p>"Do you have another appointment?"</p><p>I considered lying. He knew I did not.'),
        ('<p>I said, "Reasonable." Antonius had the new note before I arrived.', '<p>I said, "Reasonable."</p><p>Antonius had the new note before I arrived.'),
        ('<p>Finally I said, "Temporary." Antonius nodded.</p>', '<p>Finally I said, "Temporary."</p><p>Antonius nodded.</p>'),
        ('<p>"Tomorrow?" I calculated.</p>', '<p>"Tomorrow?"</p><p>I calculated.</p>'),
        ('<p>Antonius said, "Greg." I turned. He looked at the sword at my hip.</p>', '<p>Antonius said, "Greg."</p><p>I turned. He looked at the sword at my hip.</p>'),
        ('<p>"Nice sword." I looked down at it. The sixth sword.</p>', '<p>"Nice sword."</p><p>I looked down at it. The sixth sword.</p>'),
    ],
}


def conservative_explicit_split(html: str) -> tuple[str, int]:
    """Split only explicit-tag paragraphs where ownership changes are obvious."""
    changed = 0
    paragraphs = re.findall(r'<p>.*?</p>', html, flags=re.S)
    for old in paragraphs:
        inner = old[3:-4]
        if '"' not in inner:
            continue
        new = inner

        # Greg explicitly owns dialogue, then a third-person actor begins an independent beat.
        if FIRST_PERSON_TAG.search(inner):
            new = re.sub(
                r'((?:I (?:said|asked|answered|replied|added|muttered)[^.?!]*[.?!]|"[^\"]+"[^.?!]*\bI (?:said|asked|answered|replied|added|muttered)[^.?!]*[.?!]))\s+(?=(?:He|She|[A-Z][a-z]+)\b)',
                r'\1</p><p>',
                new,
                count=1,
            )

        # A named character explicitly owns dialogue, then Greg begins an independent beat.
        if THIRD_PERSON_TAG.search(inner):
            new = re.sub(
                r'((?:[A-Z][a-z]+ (?:said|asked|answered|replied|added|muttered|continued)[^.?!]*[.?!]|"[^\"]+"[^.?!]*\b[A-Z][a-z]+ (?:said|asked|answered|replied|added|muttered|continued)[^.?!]*[.?!]))\s+(?=I\b)',
                r'\1</p><p>',
                new,
                count=1,
            )

        if new != inner:
            replacement = '<p>' + new + '</p>'
            html = html.replace(old, replacement, 1)
            changed += 1
    return html, changed


def process(path: Path) -> tuple[int, list[str]]:
    html = path.read_text(encoding='utf-8')
    original = html
    notes: list[str] = []

    for old, new in EXACT_REPLACEMENTS.get(path.name, []):
        if old in html:
            html = html.replace(old, new, 1)
            notes.append('exact')

    html, safe_count = conservative_explicit_split(html)
    if safe_count:
        notes.extend(['safe-explicit'] * safe_count)

    if html != original:
        path.write_text(html, encoding='utf-8')
    return len(notes), notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=20)
    args = parser.parse_args()

    total = 0
    touched = []
    for n in range(args.start, args.end + 1):
        path = Path('chapters') / f'{n:03d}.html'
        if not path.exists():
            raise SystemExit(f'missing {path}')
        count, _ = process(path)
        if count:
            touched.append((n, count))
            total += count

    print(f'dialogue ownership: {total} paragraph repairs across {len(touched)} chapters')
    for n, count in touched:
        print(f'  chapter {n:03d}: {count}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
