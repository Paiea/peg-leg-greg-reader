import re
import subprocess
from pathlib import Path


def show(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], text=True)


def chapters(text):
    pat = re.compile(r'(?ms)^# Chapter (\d+): ([^\n]+)\n\n(.*?)(?=\n---\n|\Z)')
    out = {}
    for m in pat.finditer(text):
        n = int(m.group(1))
        out[n] = f'# Chapter {n}: {m.group(2)}\n\n{m.group(3).strip()}\n'
    return out


a = chapters(show('origin/experiment/r2-temporal-c-hybrid-r4-a', 'r2/experiments/temporal-writing/c-hybrid/round-04/a/first-pass.md'))
b = chapters(show('origin/experiment/r2-temporal-c-hybrid-r4-b', 'r2/experiments/temporal-writing/c-hybrid/round-04/b/first-pass.md'))

selected = {}
for n in range(165, 178):
    selected[n] = a[n]
for n in range(178, 191):
    selected[n] = b[n]

selected[182] = selected[182].replace(
    'I started marking uncertain memories with a small circle.',
    'I started adding small circles beside the WATCH entries.'
)

selected[186] = '''# Chapter 186: The Third Route

By the time the third outside customer arrived, Senn had been running our half-day route ledger long enough to become offended by it professionally.

North mill used Hesk.

East dye house used Marris.

The new customer was a bathhouse south of Carrow that wanted monthly service and refused both delivery days.

Dena proposed inventing a new day.

Senn proposed inventing a column.

Arlo proposed inventing a larger kiln again.

Pellin proposed murder.

Senn spread the existing carrier sheets across the desk.

"We already have a southbound linen carrier crossing two streets from the bathhouse."

Dena frowned.

"Do they carry fragile freight?"

"They carry glass oil bottles."

"Poorly?"

"Three breakage claims in eight months."

"That is not comforting."

"It is data."

The bathhouse paid a higher service fee for the inconvenient schedule.

The linen carrier accepted a crate-condition line and return timing that Senn could actually fit into the ledger.

No horse.

No company cart.

Three outside routes now existed because other people's lives were already moving in useful directions...
'''

selected[189] = selected[189].replace(
    'The road office offered Jorren another twelve weeks.',
    "Near the end of Jorren's original eight-week appointment, the road office offered him another twelve weeks."
)

selected[190] = selected[190].replace(
    '''"I'm trying not to become the author of your career."\n\nHe stared at me.\n\nI stared back.\n\n"That was a strange sentence."\n\nIt was.\n\nI tried again.\n\n"I'm trying not to tell you what you should want because I got a cord."\n\n"Better."''',
    '''"I'm trying not to decide what you should want because I got a cord."\n\nJorren studied me for a moment.\n\n"Better."'''
)

outdir = Path('r2/experiments/temporal-writing/c-hybrid/round-04/reconciled')
outdir.mkdir(parents=True, exist_ok=True)
for n in range(165, 191):
    (outdir / f'ch{n:03d}.md').write_text(selected[n], encoding='utf-8')

files = sorted(outdir.glob('ch*.md'))
nums = [int(p.stem[2:]) for p in files]
assert nums == list(range(165, 191)), nums
for p in files:
    t = p.read_text(encoding='utf-8')
    n = int(p.stem[2:])
    assert t.startswith(f'# Chapter {n}: ')
    assert 'Status: **EXPERIMENTAL' not in t
    assert 'author of your career' not in t
    assert 'narrative' not in t.lower()

print('Round 04 reconciled chapters 165-190: OK')
