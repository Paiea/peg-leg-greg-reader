#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

TAG_RE = re.compile(r'<[^>]+>')
PARA_RE = re.compile(r'<p>(.*?)</p>', re.S)
SPEECH_VERBS = r'(?:said|asked|answered|replied|added|muttered|continued|told|called|shouted|whispered|yelled)'
SUBJECT = r'(?:I|He|She|They|[A-Z][a-z]+)'


def clean(s: str) -> str:
    s = TAG_RE.sub('', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def quoted_to_markers(s: str) -> str:
    # Replace alternating ASCII quoted spans with <Q>, preserving narration around them.
    parts = s.split('"')
    if len(parts) < 3:
        return s
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            out.append(part)
        elif i < len(parts) - 1:
            out.append(' <Q> ')
        else:
            out.append(part)
    return ''.join(out)


def likely_mixed_ownership(p: str) -> bool:
    if '"' not in p:
        return False
    marked = quoted_to_markers(p)
    if '<Q>' not in marked:
        return False

    # Dialogue followed by an independent action/reaction beat rather than a speech tag.
    after_action = re.search(
        rf'<Q>\s*(?:[,;:]\s*)?(?:{SUBJECT})\s+(?!{SPEECH_VERBS}\b)(?:[a-zA-Z]+)',
        marked,
    )
    if after_action:
        return True

    # A normal dialogue tag followed by another subject's independent beat in the same paragraph.
    tag_then_action = re.search(
        rf'<Q>\s*(?:[,;:]\s*)?{SUBJECT}\s+{SPEECH_VERBS}\b[^.!?]*[.!?]\s+{SUBJECT}\s+(?!{SPEECH_VERBS}\b)[A-Za-z]+',
        marked,
    )
    if tag_then_action:
        return True

    # Narration before dialogue plus an explicit speaker later. This is a review candidate because
    # the paragraph may have changed ownership before the spoken line.
    first_q = marked.find('<Q>')
    pre = marked[:first_q].strip()
    post = marked[first_q:]
    if pre and re.search(rf'\b{SUBJECT}\s+[A-Za-z]+', pre) and re.search(rf'\b{SUBJECT}\s+{SPEECH_VERBS}\b', post):
        return True

    return False


def main() -> None:
    out = [
        '# Focused Dialogue Ownership Candidates 001-020',
        '',
        'Generated review surface only. This file does not authorize automatic manuscript mutation.',
        'A candidate means dialogue and another character-shaped beat coexist in one paragraph. Human semantic review decides whether ownership actually changes.',
        '',
    ]
    total = 0
    counts = {}
    for n in range(1, 21):
        path = Path('chapters') / f'{n:03d}.html'
        text = path.read_text(encoding='utf-8')
        article = text.split('<article class="prose">', 1)[1].split('</article>', 1)[0]
        paras = [clean(x) for x in PARA_RE.findall(article)]
        hits = [i for i, p in enumerate(paras) if likely_mixed_ownership(p)]
        counts[n] = len(hits)
        out += [f'## Chapter {n:03d} ({len(hits)} candidates)', '']
        for i in hits:
            total += 1
            prev = paras[i - 1] if i > 0 else ''
            cur = paras[i]
            nxt = paras[i + 1] if i + 1 < len(paras) else ''
            out += [
                f'### P{i+1}',
                f'- PREV: {prev}',
                f'- CURR: {cur}',
                f'- NEXT: {nxt}',
                '',
            ]
    out.insert(5, f'Total focused candidates: {total}')
    out.insert(6, 'Counts: ' + ', '.join(f'{n:03d}={counts[n]}' for n in range(1, 21)))
    out.insert(7, '')
    target = Path('state/editorial/dialogue-ownership/CANDIDATES_001_020.md')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(out), encoding='utf-8')
    print(f'wrote {target} with {total} focused candidates')


if __name__ == '__main__':
    main()
