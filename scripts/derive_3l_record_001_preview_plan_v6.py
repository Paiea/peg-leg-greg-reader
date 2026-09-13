#!/usr/bin/env python3
"""Derive the locked speaker-pure preview plan for 3L Record 001 v6.

Experimental Record-001-only parser. It exists to reproduce the approved v6
listening build. Future records should author an explicit audio plan rather than
extend these chapter-specific speaker heuristics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

DRAGON_SHORT = {
    '“Mm.”', '“Food has arrived.”', '“Is your name Dinner?”', '“Unfortunate.”',
    '“Oh.”', '“I see.”', '“Then I am undone.”', '“Speak, master.”', '“Command me.”',
    '“Good.”', '“For a moment I was concerned you were stupid.”', '“Yes. The concern remains.”',
    '“What did you think my name would buy you?”', '“Thirty.”',
    '“You traveled six days to negotiate thirty seconds.”', '“Twenty-eight.”',
    '“Zero.”', '“You have already used the name.”', '“No.”',
    '“You know what that is.”', '“Your horse?”', '“Ah.”',
    '“How do you know the Line will fail?”', '“When?”', '“Where?”', '“You were not.”'
}
DRAGON_LONG_STARTS = (
    '“No. And before you repeat the number',
    '“This was part of the fourth.',
    '“You crossed half a kingdom on a leg',
    '“Nine living things have known that name',
    '“That does not frighten me, Greg.',
    '“You believe I am examining what you know.',
    '“I am not trying to collect facts, Greg.',
    '“The western Line has not failed during your lifetime.',
    '“No.',
)
MAX_CHARS = 430
SENTENCE_RE = re.compile(r'(?<=[.!?])\s+(?=[“A-Z0-9])')
MAJOR_ENDINGS = {
    'I am trying to determine what kind of cause produces you.”': 700,
    '“How do you know the Line will fail?”': 700,
    '“When?”': 900,
    '“Forty years from now.”': 900,
    '“Where?”': 900,
    '“I was there.”': 1000,
    '“You were not.”': 1000,
}


def split_long(text: str) -> list[str]:
    if len(text) <= MAX_CHARS:
        return [text]
    sentences = SENTENCE_RE.split(text)
    pieces: list[str] = []
    cur = ''
    for sentence in sentences:
        if len(sentence) > MAX_CHARS:
            for word in sentence.split():
                cand = (cur + ' ' + word).strip()
                if cur and len(cand) > MAX_CHARS:
                    pieces.append(cur)
                    cur = word
                else:
                    cur = cand
            continue
        cand = (cur + ' ' + sentence).strip()
        if cur and len(cand) > MAX_CHARS:
            pieces.append(cur)
            cur = sentence
        else:
            cur = cand
    if cur:
        pieces.append(cur)
    return pieces


def derive(source_path: Path) -> dict:
    raw = source_path.read_text()
    paras = [
        p.strip() for p in re.split(r'\n\s*\n', raw)
        if p.strip() and not p.strip().startswith('## ')
    ]

    labeled = []
    dragon_open = False
    for idx, p in enumerate(paras):
        if dragon_open:
            if not p.startswith('“'):
                raise SystemExit(f'Expected continued Dragon quote at paragraph {idx}: {p[:120]!r}')
            voice = 'normal'
            dragon_open = not p.endswith('”')
        elif p.startswith('“'):
            if p in DRAGON_SHORT or p.startswith(DRAGON_LONG_STARTS):
                voice = 'normal'
                dragon_open = not p.endswith('”')
            else:
                voice = 'deep'
                if '”' not in p:
                    raise SystemExit(f'Unexpected multi-paragraph Greg quote at paragraph {idx}: {p[:160]!r}')
        else:
            voice = 'deep'
        labeled.append({'paragraph_index': idx, 'voice': voice, 'text': p})
    if dragon_open:
        raise SystemExit('Unclosed Dragon quotation at EOF')

    runs = []
    for item in labeled:
        if runs and runs[-1]['voice'] == item['voice']:
            runs[-1]['paragraphs'].append(item['text'])
        else:
            runs.append({'voice': item['voice'], 'paragraphs': [item['text']]})

    chunks = []
    for dramatic_run, run in enumerate(runs, start=1):
        technical = []
        cur = ''
        for para in run['paragraphs']:
            for piece in split_long(para):
                cand = (cur + '\n\n' + piece).strip() if cur else piece
                if cur and len(cand) > MAX_CHARS:
                    technical.append(cur)
                    cur = piece
                else:
                    cur = cand
        if cur:
            technical.append(cur)
        for part_in_run, text in enumerate(technical, start=1):
            chunks.append({
                'id': f'{len(chunks)+1:03d}',
                'dramatic_run': dramatic_run,
                'part_in_run': part_in_run,
                'voice': run['voice'],
                'text': text,
                'chars': len(text),
            })

    for i, chunk in enumerate(chunks):
        pause = 80 if i + 1 < len(chunks) and chunks[i+1]['dramatic_run'] == chunk['dramatic_run'] else 280
        stripped = chunk['text'].strip()
        for ending, ms in MAJOR_ENDINGS.items():
            if stripped.endswith(ending):
                pause = ms
        chunk['pause_after_ms'] = pause

    if any(c['chars'] > MAX_CHARS for c in chunks):
        raise SystemExit('Technical chunk exceeds preview ceiling')
    dragon_runs = [r for r in runs if r['voice'] == 'normal']
    if len(dragon_runs) != 38:
        raise SystemExit(f'Expected 38 Dragon dramatic runs, got {len(dragon_runs)}')
    if len(chunks) != 128:
        raise SystemExit(f'Expected 128 technical chunks, got {len(chunks)}')
    if not any('A prophet watches the future.' in c['text'] and c['voice'] == 'normal' for c in chunks):
        raise SystemExit('Dragon diagnosis ownership check failed')
    if not any('Not this time.' in c['text'] and c['voice'] == 'deep' for c in chunks):
        raise SystemExit('Final Greg ownership check failed')

    return {
        'schema_version': 1,
        'record': '001',
        'title': 'THE PETITIONER',
        'source_path': str(source_path),
        'source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'greg_voice': 'deep',
        'dragon_voice': 'normal',
        'dragon_dsp': 'none',
        'max_preview_chars': MAX_CHARS,
        'final_tail_ms': 2000,
        'paragraphs': len(paras),
        'dramatic_runs': len(runs),
        'dragon_dramatic_runs': len(dragon_runs),
        'technical_chunks': len(chunks),
        'chunks': chunks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='3l/manuscript/record-001.md')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    plan = derive(Path(args.source))
    Path(args.output).write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: plan[k] for k in ('paragraphs', 'dramatic_runs', 'dragon_dramatic_runs', 'technical_chunks')}, indent=2))


if __name__ == '__main__':
    main()
