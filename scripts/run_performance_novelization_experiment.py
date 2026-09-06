#!/usr/bin/env python3
from dataclasses import replace

import apply_performance_novelization_experiment as exp


ARLO_END = (
    "He laughed despite himself. I looked around the workshop. The roof still sagged. "
    "The shelves still held too many half-finished jobs. A cracked crucible sat beside a bucket. "
    "There was clay under Arlo's fingernails and a burn on one thumb. Nothing had transformed. "
    "That mattered. I had been expecting breakthroughs to arrive with visible grandeur because I remembered the future result."
)
ARLO_TEXTURE = (
    "I looked around the workshop. The roof still sagged. The shelves still held too many half-finished jobs. "
    "A cracked crucible sat beside a bucket. There was clay under Arlo's fingernails and a burn on one thumb. "
    "Nothing had transformed. That mattered. I had been expecting breakthroughs to arrive with visible grandeur because I remembered the future result."
)

fixed = []
for patch in exp.PATCHES:
    if patch.patch_id == "007-valuation-exit":
        replacement = tuple(
            '"Five silver."' if line == '"Five silver. End of week."' else line
            for line in patch.replacement
        )
        fixed.append(replace(patch, end="His mouth twitched.", replacement=replacement))
        continue
    if patch.patch_id == "013-process-ownership":
        fixed.append(replace(patch, end=ARLO_END, replacement=patch.replacement + (ARLO_TEXTURE,)))
        continue
    fixed.append(patch)

exp.PATCHES = tuple(fixed)


if __name__ == "__main__":
    raise SystemExit(exp.main())
