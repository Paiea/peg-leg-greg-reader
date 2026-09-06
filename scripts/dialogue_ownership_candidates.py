#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

TAG_RE = re.compile(r'<[^>]+>')
PARA_RE = re.compile(r'<p>(.*?)</p>', re.S)


def clean(s: str) -> str:
    s = TAG_RE.sub('', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def main() -> None:
    out = [
        '# Dialogue Ownership Candidates 001-020',
        '',
        'Generated review surface only. This file does not authorize automatic manuscript mutation.',
        'Review semantic paragraph ownership: when speech/action ownership changes character, split the paragraph.',
        '',
    ]
    total = 0
    for n in range(1, 21):
        path = Path('chapters') / f'{n:03d}.html'
        text = path.read_text(encoding='utf-8')
        article = text.split('<article class="prose">', 1)[1].split('</article>', 1)[0]
        paras = [clean(x) for x in PARA_RE.findall(article)]
        hits = [i for i, p in enumerate(paras) if '"' in p]
        out += [f'## Chapter {n:03d}', '']
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
    out.insert(5, f'Total dialogue paragraphs surfaced: {total}')
    out.insert(6, '')
    target = Path('state/editorial/dialogue-ownership/CANDIDATES_001_020.md')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(out), encoding='utf-8')
    print(f'wrote {target} with {total} dialogue paragraphs')


if __name__ == '__main__':
    main()
