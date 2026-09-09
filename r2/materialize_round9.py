from __future__ import annotations

import re
import subprocess
from pathlib import Path

# Round 09 reconciled materializer.
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "r2/experiments/temporal-writing/c-hybrid/round-09/reconciled"

A_BRANCH = "origin/experiment/r2-temporal-c-hybrid-r9-a"
B_BRANCH = "origin/experiment/r2-temporal-c-hybrid-r9-b"
A_PATH = "r2/experiments/temporal-writing/c-hybrid/round-09/a/first-pass.md"
B_PATH = "r2/experiments/temporal-writing/c-hybrid/round-09/b/first-pass.md"


def git_show(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)


def chapters(text: str) -> dict[int, str]:
    matches = list(re.finditer(r"(?m)^# Chapter (\d+): ", text))
    result: dict[int, str] = {}
    for idx, match in enumerate(matches):
        number = int(match.group(1))
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        if block.endswith("---"):
            block = block[:-3].rstrip()
        result[number] = block + "\n"
    return result


a = chapters(git_show(A_BRANCH, A_PATH))
b = chapters(git_show(B_BRANCH, B_PATH))

selected: dict[int, str] = {}
for n in range(279, 293):
    selected[n] = a[n]
for n in range(293, 305):
    selected[n] = b[n]

old_281 = "No relation to Pellin, which disappointed Renn because he had briefly believed municipal investigation was developing themes."
new_281 = "No relation to Pellin, which disappointed Renn for reasons he did not explain."
if old_281 not in selected[281]:
    raise SystemExit("Round 09 A281 repair anchor not found")
selected[281] = selected[281].replace(old_281, new_281, 1)

old_297 = "\nThe river did not reward us with danger for taking it seriously...\n"
if old_297 not in selected[297]:
    raise SystemExit("Round 09 B297 repair anchor not found")
selected[297] = selected[297].replace(old_297, "\n", 1)

OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob("ch*.md"):
    old.unlink()

for n in range(279, 305):
    path = OUT / f"ch{n:03d}.md"
    path.write_text(selected[n], encoding="utf-8")

assert len(list(OUT.glob("ch*.md"))) == 26
assert "developing themes" not in selected[281]
assert "river did not reward us" not in selected[297]
print("materialized Round 09 reconciled chapters 279-304")
