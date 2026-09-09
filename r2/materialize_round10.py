from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "r2/experiments/temporal-writing/c-hybrid/round-10/reconciled"
A_BRANCH = "origin/experiment/r2-temporal-c-hybrid-r10-a"
B_BRANCH = "origin/experiment/r2-temporal-c-hybrid-r10-b"
A_PATH = "r2/experiments/temporal-writing/c-hybrid/round-10/a/first-pass.md"
B_PATH = "r2/experiments/temporal-writing/c-hybrid/round-10/b/first-pass.md"


def show(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)


def split(text: str) -> dict[int, str]:
    hits = list(re.finditer(r"(?m)^# Chapter (\d+): ", text))
    out = {}
    for i, hit in enumerate(hits):
        n = int(hit.group(1))
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        block = text[hit.start():end].strip()
        if block.endswith("---"):
            block = block[:-3].rstrip()
        out[n] = block + "\n"
    return out


a = split(show(A_BRANCH, A_PATH))
b = split(show(B_BRANCH, B_PATH))
selected = {n: a[n] for n in range(305, 319)}
selected.update({n: b[n] for n in range(319, 331)})

repairs = {
    309: (
        "Apparently this remained true even when I had touched the story first.",
        "Apparently this remained true even when mine had been the first name on the card.",
    ),
    319: (
        "Three weeks after the river inspection, a piece of blue-gray stone appeared on the Guild desk.",
        "By late winter, a piece of blue-gray stone appeared on the Guild desk.",
    ),
    320: ("Much more believable.", "Much more manageable."),
}
for n, (old, new) in repairs.items():
    if old not in selected[n]:
        raise SystemExit(f"repair anchor not found in {n}")
    selected[n] = selected[n].replace(old, new, 1)

OUT.mkdir(parents=True, exist_ok=True)
for p in OUT.glob("ch*.md"):
    p.unlink()
for n in range(305, 331):
    (OUT / f"ch{n:03d}.md").write_text(selected[n], encoding="utf-8")

assert len(list(OUT.glob("ch*.md"))) == 26
assert "touched the story first" not in selected[309]
assert "Three weeks after the river inspection" not in selected[319]
assert "Much more believable" not in selected[320]
print("materialized Round 10 reconciled chapters 305-330")
