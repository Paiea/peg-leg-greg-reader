import re
import subprocess
from pathlib import Path


def show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def chapters(text):
    pat = re.compile(r"(?ms)^# Chapter (\d+): ([^\n]+)\n\n(.*?)(?=\n---\n|\Z)")
    out = {}
    for match in pat.finditer(text):
        number = int(match.group(1))
        out[number] = (
            f"# Chapter {number}: {match.group(2)}\n\n{match.group(3).strip()}\n"
        )
    return out


a = chapters(
    show(
        "origin/experiment/r2-temporal-c-hybrid-r3-a",
        "r2/experiments/temporal-writing/c-hybrid/round-03/a/first-pass.md",
    )
)
b = chapters(
    show(
        "origin/experiment/r2-temporal-c-hybrid-r3-b",
        "r2/experiments/temporal-writing/c-hybrid/round-03/b/first-pass.md",
    )
)

selected = {}
for n in range(139, 153):
    selected[n] = a[n]
for n in range(153, 161):
    selected[n] = b[n]
for n in range(162, 165):
    selected[n] = b[n]

selected[161] = '''# Chapter 161: The Road Offer

Jorren's readiness note became money before it became rank.

The north-west road office offered him eight weeks as a seasonal field coordinator.

Not Guild Silver.

Not a substitute for Silver authority where a Guild contract required it.

City work.

Road crews.

Daily tasking, material counts, culvert sequencing, and the privilege of being blamed when three carts arrived before the gravel did.

"Pay?" I asked.

He told me.

Better than ordinary Bronze road work.

"They can do that?"

"Apparently they just did."

The offer letter was very specific about what he could sign and what still needed a city engineer or Guild Silver.

Somebody had learned from lawyers.

Jorren tapped the folded Silver application still living in his field book.

"If I take this, does it help later?"

"Probably."

"Useful certainty."

"You asked the man whose first Silver closeout has a crate dispute attached."

"Fair."

He took the road job.

The application stayed unsigned.

Three days later he left Carrow with a city tool wagon, two road laborers, and a clerk who had already corrected his spelling twice.

Before climbing aboard he pointed at my cord.

"Try not to become important."

"You first."

The clerk shouted that they were late.

Jorren climbed onto the wagon and became somebody else's scheduling problem...
'''

outdir = Path("r2/experiments/temporal-writing/c-hybrid/round-03/reconciled")
outdir.mkdir(parents=True, exist_ok=True)
for n in range(139, 165):
    (outdir / f"ch{n:03d}.md").write_text(selected[n], encoding="utf-8")

files = sorted(outdir.glob("ch*.md"))
nums = [int(path.stem[2:]) for path in files]
assert nums == list(range(139, 165)), nums
for path in files:
    number = int(path.stem[2:])
    text = path.read_text(encoding="utf-8")
    assert text.startswith(f"# Chapter {number}: ")
    assert "Status: **EXPERIMENTAL" not in text

print("Round 03 reconciled chapters 139-164: OK")
