import re
import subprocess
from pathlib import Path

A_REF = 'origin/experiment/r2-temporal-c-hybrid-r7-a'
B_REF = 'origin/experiment/r2-temporal-c-hybrid-r7-b'
A_PATH = 'r2/experiments/temporal-writing/c-hybrid/round-07/a/first-pass.md'
B_PATH = 'r2/experiments/temporal-writing/c-hybrid/round-07/b/first-pass.md'
OUT = Path('r2/experiments/temporal-writing/c-hybrid/round-07/reconciled')


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
selected = {n: a[n] for n in range(227, 241)}
selected.update({n: b[n] for n in range(241, 253)})

selected[244] = '''# Chapter 244: The Mill Causeway

The archive wagon waited behind flax.

Not the plant.

Three carts of it.

The mill causeway had a temporary board at each end.

**ONE LOADED CART AT A TIME.**

A spring repair had reset the downstream stones, but the north wing wall was still under observation until winter.

The flax-mill foreman stood beside the gate with a chalk board and the authority to annoy everyone equally.

Pel held up the municipal seal.

"Archive wagon."

"Loaded wagon."

"Under two tons."

"Still loaded."

Pel looked at Tamar's road notice pinned beside the gate.

Then at me.

I had Silver.

This was useless.

The cart ahead crossed.

The foreman checked a red chalk mark on the wing wall.

No movement.

He waved us through.

Halfway across, Kess looked over the rail at the millrace.

"What happens if the mark moves?"

The foreman shouted from behind us.

"I stop letting carts cross."

"Then?"

"Road office sends somebody with more education."

A quarry wagon reached the far queue and its driver began complaining before he read the sign.

The foreman pointed at it without speaking.

We cleared the causeway.

Current procedure had survived without asking Greg anything...
'''

selected[245] = '''# Chapter 245: The School Wall

The second archive box led us to a school garden wall.

The village had requested an old charged-marker record because the school and the neighboring cooper disagreed about who owned twelve feet of crumbling masonry.

Pel's copy described:

**CHARGED STONE / DISTRICT EIGHTEEN / EAST COMMON.**

The modern index called it a boundary marker.

The schoolmaster wanted that to mean the wall was municipal.

The cooper wanted it to mean the wall was school property.

Pel wanted both of them to stop deciding what the document meant before we found the stone.

A groundskeeper knew where it was.

"Blue one. Mint grows badly beside it."

The marker had been built directly into the garden wall sometime after the school expanded.

We removed two loose facing stones from the school side.

Faint old charge touched the edge of my plane.

Stable.

The surveyor brushed dirt from the inscription while I held the field narrow.

No surge.

No revelation.

Just letters under mortar.

Pel leaned closer.

"That is not a parcel mark."

The schoolmaster stopped smiling.

The cooper started.

Pel pointed at him.

"Neither is that permission to smile yet."

He stopped...
'''

selected[246] = '''# Chapter 246: The Wrong Record

The stone said:

**ROAD SERVICE XVIII / EAST LIMIT.**

Not property.

Road service.

The surveyor checked the old map again.

The road district boundary had once crossed the common behind the current school.

The modern archive index had grouped the stone with charged property markers because an older clerk had apparently decided all old charged stones belonged in one useful drawer.

Pel stared at the index copy.

"I hate this person."

"Dead?" Kess asked.

"Almost certainly."

"Convenient."

The schoolmaster pointed at the wall.

"So who repairs that?"

The surveyor looked at the cooper.

The cooper looked at Pel.

Pel looked at me.

I stepped back.

"Silver does not improve property law."

The charged stone itself was clearer.

The road office now had responsibility to decide whether an obsolete service marker remained active, should be capped, or could be formally abandoned.

Pel corrected the archive index before we left.

**ROAD DISTRICT SERVICE MARKER. NOT PARCEL BOUNDARY.**

The wall still needed repair.

The argument had lost one wrong answer...
'''

OUT.mkdir(parents=True, exist_ok=True)
for n in range(227, 253):
    (OUT / f'ch{n:03d}.md').write_text(selected[n], encoding='utf-8')

files = sorted(OUT.glob('ch*.md'))
nums = [int(p.stem[2:]) for p in files]
assert nums == list(range(227, 253)), nums
for p in files:
    n = int(p.stem[2:])
    text = p.read_text(encoding='utf-8')
    assert text.startswith(f'# Chapter {n}: ')
    assert 'Status: **EXPERIMENTAL' not in text

assert selected[244].startswith('# Chapter 244: The Mill Causeway')
assert selected[245].startswith('# Chapter 245: The School Wall')
assert selected[246].startswith('# Chapter 246: The Wrong Record')

print('Round 07 reconciled chapters 227-252: OK')
