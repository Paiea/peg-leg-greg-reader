#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import apply_dialogue_ownership_semantic as base

REWRITE_ACTION = base.ACTION[:-1] + r'|drummed|glared|denied)'


def action_events(p: str) -> list[tuple[int, str]]:
    """Find clear actor changes outside quotes, including descriptive noun phrases."""
    outside, closing_starts = base.quote_map(p)
    starts = {0}
    for i, ch in enumerate(p):
        if ch in '.!?' and outside[i]:
            starts.add(base.next_nonspace(p, i + 1))
    for pos in closing_starts:
        starts.add(base.next_nonspace(p, pos))

    actor = (
        r'I|He|She|They|[A-Z][a-z]+'
        r'|The\s+[a-z]+(?:\s+[a-z]+){0,2}'
        r'(?:\s+(?:with|in|at|by|from|near|behind|beside|under|over)\s+(?:the\s+)?[a-z]+(?:\s+[a-z]+){0,2})?'
    )
    subj_re = re.compile(rf'({actor})\s+({REWRITE_ACTION})\b')
    events: list[tuple[int, str]] = []
    for pos in sorted(starts):
        if pos >= len(p) or not outside[pos]:
            continue
        m = subj_re.match(p, pos)
        if not m:
            continue
        if not all(outside[j] for j in range(m.start(), min(m.end(), len(outside)))):
            continue
        owner = 'GREG' if m.group(1) == 'I' else 'OTHER'
        events.append((m.start(), owner))
    return events


# Exact local fallbacks are intentional. These are the cases where the spoken
# line is sound but semantic ownership is clearer if the surrounding prose is
# rebuilt. Keep the dialogue and words, change only paragraph ownership.
LOCAL_REPAIRS = (
    (
        '<p>The man with the scar laughed. Antonius looked at my Bronze plate. "Collateral?"</p>',
        '<p>The man with the scar laughed.</p><p>Antonius looked at my Bronze plate. "Collateral?"</p>',
    ),
    (
        '<p>His man laughed again. Antonius did not. "How does a nineteen-year-old Bronze know this?"</p>',
        '<p>His man laughed again.</p><p>Antonius did not. "How does a nineteen-year-old Bronze know this?"</p>',
    ),
    (
        '<p>"If I had an answer you\'d believe, I wouldn\'t need your money." He denied the large loan. Of course he did.',
        '<p>"If I had an answer you\'d believe, I wouldn\'t need your money."</p><p>He denied the large loan. Of course he did.',
    ),
    (
        'Useful. Also something I should probably examine later. Antonius pushed the coins toward me. "Eight days, Greg." I picked them up.</p>',
        'Useful. Also something I should probably examine later.</p><p>Antonius pushed the coins toward me. "Eight days, Greg."</p><p>I picked them up.</p>',
    ),
    (
        '<p>She stopped. "Do I know you?" I knew her future immediately.',
        '<p>She stopped. "Do I know you?"</p><p>I knew her future immediately.',
    ),
    (
        'Arlo picked up a shale chip. "Tell me exactly what you think this does." I almost told him.',
        'Arlo picked up a shale chip. "Tell me exactly what you think this does."</p><p>I almost told him.',
    ),
    (
        '<p>"Why?" Arlo asked. I considered telling him that one day his surname might be stamped on equipment used across three kingdoms.',
        '<p>"Why?" Arlo asked.</p><p>I considered telling him that one day his surname might be stamped on equipment used across three kingdoms.',
    ),
    (
        '<p>He looked at the window. "Enough to tell you this was a bad idea." I felt the first real pinch of fear.',
        '<p>He looked at the window. "Enough to tell you this was a bad idea."</p><p>I felt the first real pinch of fear.',
    ),
    (
        '<p>"Then we\'ve discovered another stable property," I said. He should have thrown me out. Instead he looked back at the sample.',
        '<p>"Then we\'ve discovered another stable property," I said.</p><p>He should have thrown me out. Instead he looked back at the sample.',
    ),
    (
        '<p>Jorren laughed. Antonius looked at me. "And you came here proud."</p>',
        '<p>Jorren laughed.</p><p>Antonius looked at me. "And you came here proud."</p>',
    ),
    (
        '<p>"That is a cruel summary of scientific progress." Antonius slid the paper back.</p>',
        '<p>"That is a cruel summary of scientific progress."</p><p>Antonius slid the paper back.</p>',
    ),
    (
        '<p>"Better than no evidence." He almost smiled. I leaned forward.</p>',
        '<p>"Better than no evidence."</p><p>He almost smiled.</p><p>I leaned forward.</p>',
    ),
    (
        '<p>"How much do you think the idea is worth?" he asked. I nearly answered with the future.',
        '<p>"How much do you think the idea is worth?" he asked.</p><p>I nearly answered with the future.',
    ),
    (
        '<p>"From?" I looked at him.</p>',
        '<p>"From?"</p><p>I looked at him.</p>',
    ),
    (
        '<p>"If Vale sent you, don\'t sign anything without reading it." I smiled.</p>',
        '<p>"If Vale sent you, don\'t sign anything without reading it."</p><p>I smiled.</p>',
    ),
    (
        '<p>"Can I help you?" I stared. </p>',
        '<p>"Can I help you?"</p><p>I stared. </p>',
    ),
    (
        '<p>"Token." I gave her the Bronze plate. She checked it.</p>',
        '<p>"Token."</p><p>I gave her the Bronze plate.</p><p>She checked it.</p>',
    ),
    (
        '<p>"Most beginners don\'t know what that means." I almost said, It was obvious.',
        '<p>"Most beginners don\'t know what that means."</p><p>I almost said, It was obvious.',
    ),
    (
        '<p>"I said if this becomes something, I\'m not your employee." I blinked.',
        '<p>"I said if this becomes something, I\'m not your employee."</p><p>I blinked.',
    ),
    (
        '<p>"You looked at my workshop like you were measuring it." I glanced around. I had been.</p>',
        '<p>"You looked at my workshop like you were measuring it."</p><p>I glanced around. I had been.</p>',
    ),
)


def cleanup_local_dialogue(text: str) -> str:
    for old, new in LOCAL_REPAIRS:
        text = text.replace(old, new)
    return text


base.action_events = action_events
semantic_transform_html = base.transform_html
transform_paragraph = base.transform_paragraph


def transform_html(html: str) -> tuple[str, int]:
    transformed, count = semantic_transform_html(html)
    cleaned = cleanup_local_dialogue(transformed)
    if cleaned != transformed:
        count += 1
    return cleaned, count


base.transform_html = transform_html


def main() -> int:
    return base.main()


if __name__ == '__main__':
    raise SystemExit(main())
