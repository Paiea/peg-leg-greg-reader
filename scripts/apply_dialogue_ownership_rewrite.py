#!/usr/bin/env python3
from __future__ import annotations

import re

from scripts import apply_dialogue_ownership_semantic as base


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
    subj_re = re.compile(rf'({actor})\s+({base.ACTION})\b')
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


# The rewrite layer deliberately reuses the established speaker inference and
# paragraph transformer, but gives them a stronger actor detector.
base.action_events = action_events

transform_paragraph = base.transform_paragraph
transform_html = base.transform_html


def main() -> int:
    return base.main()


if __name__ == '__main__':
    raise SystemExit(main())
