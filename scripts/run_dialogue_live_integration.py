#!/usr/bin/env python3
"""Run Book 1 dialogue integration with explicit current-main drift overrides.

The durable editorial batches remain the default authority. This wrapper applies
small, reviewed overrides only where current `main` contains preserved prose
beats that an editorial batch abbreviated. Overrides never enable fuzzy
matching: they replace one patch's exact current/replacement tuples and then the
strict base integrator still requires an exact unique match.
"""

from __future__ import annotations

import json
from pathlib import Path

import apply_dialogue_attribution_patches as base


OVERRIDES_PATH = Path("state/editorial/dialogue-live-overrides.json")


def _load_overrides() -> dict[str, dict[str, object]]:
    if not OVERRIDES_PATH.exists():
        return {}
    data = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"{OVERRIDES_PATH} must contain a JSON object")
    return data


def _values(raw: object, key: str) -> tuple[str, ...]:
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise RuntimeError(f"override {key} must be a list of strings")
    return tuple(base.GAP if item == "..." else item for item in raw)


def main() -> int:
    overrides = _load_overrides()
    original_load_patches = base.load_patches

    def load_patches_with_overrides(ref: str, min_chapter: int, max_chapter: int):
        patches = original_load_patches(ref, min_chapter, max_chapter)
        seen: set[str] = set()
        result: list[base.Patch] = []
        for patch in patches:
            key = f"{patch.chapter}|{patch.label}"
            override = overrides.get(key)
            if override is None:
                result.append(patch)
                continue
            if not isinstance(override, dict):
                raise RuntimeError(f"override {key} must be an object")
            current = _values(override.get("current"), f"{key}.current")
            replacement = _values(override.get("replacement"), f"{key}.replacement")
            result.append(
                base.Patch(
                    chapter=patch.chapter,
                    label=patch.label,
                    current=current,
                    replacement=replacement,
                    source_file=f"{OVERRIDES_PATH} overriding {patch.source_file}",
                )
            )
            seen.add(key)

        unused = sorted(set(overrides) - seen)
        if unused:
            raise RuntimeError(f"unused dialogue live overrides: {unused}")
        return result

    base.load_patches = load_patches_with_overrides
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
