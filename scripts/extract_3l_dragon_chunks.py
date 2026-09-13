#!/usr/bin/env python3
from pathlib import Path
import json

PERF = Path('3l/performance/record-001.performance.md')
OUT = Path('3l/audio/dragon-chunks/record-001')
TARGET_WORDS = 230
MAX_WORDS = 270
ROLE_LABELS = {'NARRATOR / GREG', 'GREG', 'DRAGON'}
BEATS = {'BEAT', 'LONG BEAT'}

text = PERF.read_text(encoding='utf-8')
blocks = []
role = None
buf = []
for line in text.splitlines():
    if line in ROLE_LABELS:
        if role == 'DRAGON' and any(x.strip() for x in buf):
            blocks.append('\n'.join(buf).strip())
        role = line
        buf = []
    elif role is not None and line not in BEATS:
        buf.append(line)
if role == 'DRAGON' and any(x.strip() for x in buf):
    blocks.append('\n'.join(buf).strip())

chunks = []
current = []
current_words = 0
for block in blocks:
    wc = len(block.split())
    if current and current_words + wc > MAX_WORDS:
        chunks.append(current)
        current = []
        current_words = 0
    current.append(block)
    current_words += wc
    if current_words >= TARGET_WORDS:
        chunks.append(current)
        current = []
        current_words = 0
if current:
    chunks.append(current)

OUT.mkdir(parents=True, exist_ok=True)
manifest = {'record': 1, 'target_words': TARGET_WORDS, 'max_words': MAX_WORDS, 'dragon_turn_count': len(blocks), 'chunks': []}
for i, chunk in enumerate(chunks, 1):
    body = '\n\n'.join(chunk).strip() + '\n'
    path = OUT / f'{i:02d}.txt'
    path.write_text(body, encoding='utf-8')
    manifest['chunks'].append({'order': i, 'path': str(path), 'turn_count': len(chunk), 'word_count': len(body.split()), 'char_count': len(body)})
(OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(json.dumps(manifest, indent=2))
