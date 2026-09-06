#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

PARA_RE = re.compile(r'<p>(.*?)</p>', re.S)
TAG_RE = re.compile(r'<[^>]+>')
SPEECH = r'(?:said|asked|answered|replied|added|muttered|continued|told|called|shouted|whispered|yelled|said again|asked again)'
ACTION = r'(?:looked|smiled|laughed|nodded|frowned|shrugged|leaned|stood|sat|turned|stared|watched|pointed|held|took|picked|pushed|pulled|crossed|sighed|blinked|froze|stopped|waited|moved|walked|stepped|glanced|tapped|reached|opened|closed|followed|started|kept|put|set|folded|unfolded|lifted|lowered|handed|offered|touched|checked|tilted|shook|raised|dropped|waved|grinned|winced|flinched|paused|breathed|exhaled|inhaled|rubbed|scratched|shifted|backed|came|went|left|returned|approached|grabbed|caught|released|gestured)'


def clean(s: str) -> str:
    return re.sub(r'\s+', ' ', html.unescape(TAG_RE.sub('', s))).strip()


def explicit_speaker(p: str) -> str | None:
    if re.search(rf'\bI\s+{SPEECH}\b', p, re.I) or re.search(rf'\bI\s+said\s*,\s*"', p, re.I):
        return 'GREG'
    if re.search(rf'\b(?:he|she|they|[A-Z][a-z]+)\s+{SPEECH}\b', p):
        return 'OTHER'
    return None


def begins_dialogue(p: str) -> bool:
    return p.lstrip().startswith('"')


def quote_marked(p: str) -> str:
    parts = p.split('"')
    if len(parts) < 3:
        return p
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            out.append(part)
        elif i < len(parts) - 1:
            out.append(' <Q> ')
        else:
            out.append(part)
    return ''.join(out)


def action_subjects(p: str) -> list[tuple[int, str, str]]:
    """Return owner-changing physical/reaction beats outside quoted dialogue."""
    marked = quote_marked(p)
    spans = []
    # Sentence start, paragraph start, or immediately after a quoted line.
    pattern = re.compile(
        rf'(?:(?<=^)|(?<=[.!?])\s+|(?<=<Q>)\s+)(I|He|She|They|[A-Z][a-z]+)\s+({ACTION})\b',
        re.M,
    )
    for m in pattern.finditer(marked):
        subj = m.group(1)
        owner = 'GREG' if subj == 'I' else 'OTHER'
        frag = clean(marked[m.start():m.start()+140].replace('<Q>', '"…"'))
        spans.append((m.start(), owner, frag))
    return spans


def infer_speakers(paras: list[str]) -> list[str | None]:
    speakers: list[str | None] = []
    last_dialogue_speaker: str | None = None
    last_was_dialogue = False
    for p in paras:
        has_dialogue = '"' in p
        sp = explicit_speaker(p) if has_dialogue else None
        if has_dialogue and sp is None and begins_dialogue(p) and last_was_dialogue and last_dialogue_speaker:
            sp = 'OTHER' if last_dialogue_speaker == 'GREG' else 'GREG'
        speakers.append(sp)
        if has_dialogue:
            if sp:
                last_dialogue_speaker = sp
            last_was_dialogue = True
        else:
            last_was_dialogue = False
    return speakers


def main() -> None:
    out = [
        '# High-Confidence Dialogue Ownership Repairs 001-020',
        '',
        'Dry-run semantic manifest. No manuscript files are changed by this script.',
        'Speaker inference uses explicit attribution when available and adjacent-turn alternation only when a paragraph begins with dialogue.',
        'Only independent physical/reaction beats from the opposite owner are surfaced.',
        '',
    ]
    total = 0
    counts = {}
    for n in range(1, 21):
        path = Path('chapters') / f'{n:03d}.html'
        text = path.read_text(encoding='utf-8')
        article = text.split('<article class="prose">', 1)[1].split('</article>', 1)[0]
        raw_paras = PARA_RE.findall(article)
        paras = [clean(x) for x in raw_paras]
        speakers = infer_speakers(paras)
        chapter_hits = []
        for i, (p, sp) in enumerate(zip(paras, speakers)):
            if not sp or '"' not in p:
                continue
            mismatches = [(off, owner, frag) for off, owner, frag in action_subjects(p) if owner != sp]
            if mismatches:
                chapter_hits.append((i, sp, mismatches, p))
        counts[n] = len(chapter_hits)
        out += [f'## Chapter {n:03d} ({len(chapter_hits)} repairs)', '']
        for i, sp, mismatches, p in chapter_hits:
            total += 1
            out += [f'### P{i+1} speaker={sp}', f'- CURR: {p}']
            for _, owner, frag in mismatches:
                out.append(f'- SPLIT BEFORE {owner}: {frag}')
            out.append('')
    out.insert(6, f'Total high-confidence paragraphs: {total}')
    out.insert(7, 'Counts: ' + ', '.join(f'{n:03d}={counts[n]}' for n in range(1, 21)))
    out.insert(8, '')
    target = Path('state/editorial/dialogue-ownership/HIGH_CONFIDENCE_001_020.md')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(out), encoding='utf-8')
    print(f'wrote {target} with {total} high-confidence paragraphs')


if __name__ == '__main__':
    main()
