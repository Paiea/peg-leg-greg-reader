import re
import subprocess
from pathlib import Path

A_REF = 'origin/experiment/r2-temporal-c-hybrid-r8-a'
B_REF = 'origin/experiment/r2-temporal-c-hybrid-r8-b'
A_PATH = 'r2/experiments/temporal-writing/c-hybrid/round-08/a/first-pass.md'
B_PATH = 'r2/experiments/temporal-writing/c-hybrid/round-08/b/first-pass.md'
OUT = Path('r2/experiments/temporal-writing/c-hybrid/round-08/reconciled')


def show(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], text=True)


def split_chapters(text):
    pat = re.compile(r'(?ms)^# Chapter (\d+): ([^\n]+)\n\n(.*?)(?=\n---\n|\Z)')
    out = {}
    for match in pat.finditer(text):
        n = int(match.group(1))
        out[n] = f'# Chapter {n}: {match.group(2)}\n\n{match.group(3).strip()}\n'
    return out


a = split_chapters(show(A_REF, A_PATH))
b = split_chapters(show(B_REF, B_PATH))
selected = {n: a[n] for n in range(253, 267)}
selected.update({n: b[n] for n in range(267, 279)})

OUT.mkdir(parents=True, exist_ok=True)
for n in range(253, 279):
    (OUT / f'ch{n:03d}.md').write_text(selected[n], encoding='utf-8')

files = sorted(OUT.glob('ch*.md'))
nums = [int(p.stem[2:]) for p in files]
assert nums == list(range(253, 279)), nums
for p in files:
    n = int(p.stem[2:])
    text = p.read_text(encoding='utf-8')
    assert text.startswith(f'# Chapter {n}: ')
    assert 'Status: **EXPERIMENTAL' not in text

print('Round 08 reconciled chapters 253-278: OK')
