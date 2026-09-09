import re
import subprocess
from pathlib import Path

A_REF = 'origin/experiment/r2-temporal-c-hybrid-r5-a'
B_REF = 'origin/experiment/r2-temporal-c-hybrid-r5-b'
A_PATH = 'r2/experiments/temporal-writing/c-hybrid/round-05/a/first-pass.md'
B_PATH = 'r2/experiments/temporal-writing/c-hybrid/round-05/b/first-pass.md'
OUT = Path('r2/experiments/temporal-writing/c-hybrid/round-05/reconciled')


def show(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], text=True)


def split_chapters(text):
    pat = re.compile(r'(?ms)^# Chapter (\d+): ([^\n]+)\n\n(.*?)(?=\n---\n|\Z)')
    out = {}
    for match in pat.finditer(text):
        number = int(match.group(1))
        out[number] = f'# Chapter {number}: {match.group(2)}\n\n{match.group(3).strip()}\n'
    return out


a = split_chapters(show(A_REF, A_PATH))
b = split_chapters(show(B_REF, B_PATH))
selected = {n: a[n] for n in range(191, 205)}
selected[205] = b[205]

OUT.mkdir(parents=True, exist_ok=True)
for n in range(191, 206):
    (OUT / f'ch{n:03d}.md').write_text(selected[n], encoding='utf-8')

files = sorted(OUT.glob('ch*.md'))
nums = [int(p.stem[2:]) for p in files]
assert nums == list(range(191, 206)), nums
for p in files:
    n = int(p.stem[2:])
    text = p.read_text(encoding='utf-8')
    assert text.startswith(f'# Chapter {n}: ')
    assert 'Status: **EXPERIMENTAL' not in text

print('Round 05 reconciled chapters 191-205: OK')
