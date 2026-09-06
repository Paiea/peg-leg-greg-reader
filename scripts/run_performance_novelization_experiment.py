#!/usr/bin/env python3
from dataclasses import replace

import apply_performance_novelization_experiment as exp


fixed = []
for patch in exp.PATCHES:
    if patch.patch_id != "007-valuation-exit":
        fixed.append(patch)
        continue
    replacement = tuple(
        '"Five silver."' if line == '"Five silver. End of week."' else line
        for line in patch.replacement
    )
    fixed.append(replace(patch, end="His mouth twitched.", replacement=replacement))

exp.PATCHES = tuple(fixed)


if __name__ == "__main__":
    raise SystemExit(exp.main())
