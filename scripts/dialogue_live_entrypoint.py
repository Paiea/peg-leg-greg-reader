#!/usr/bin/env python3
"""Stable entrypoint for incremental dialogue live integration."""

from __future__ import annotations

import re
import sys

import run_dialogue_live_integration as impl


def _candidate_lt(self, other):
    if not isinstance(other, impl.Candidate):
        return NotImplemented
    return (
        self.paragraph_index,
        self.start,
        self.end,
        self.penalty,
    ) < (
        other.paragraph_index,
        other.start,
        other.end,
        other.penalty,
    )


def _arg_int(name: str, default: int) -> int:
    try:
        index = sys.argv.index(name)
    except ValueError:
        return default
    try:
        return int(sys.argv[index + 1])
    except (IndexError, ValueError) as exc:
        raise SystemExit(f"{name} requires an integer") from exc


def _modern_batch_to_legacy(content: str) -> str:
    """Normalize accepted newer patch-note syntax for the strict legacy parser."""
    lines: list[str] = []
    for raw in content.splitlines():
        line = re.sub(r"^### Patch\b", "### Fix", raw, flags=re.IGNORECASE)
        if line.startswith("> "):
            value = line[2:].replace("`", "\\`")
            line = f"`{value}`"
        elif line.strip() == ">":
            line = ""
        lines.append(line)
    return "\n".join(lines)


_original_parse_batch = impl.base._parse_batch


def _parse_batch_compat(content: str, source_file: str, min_chapter: int, max_chapter: int):
    return _original_parse_batch(
        _modern_batch_to_legacy(content), source_file, min_chapter, max_chapter
    )


impl.Candidate.__lt__ = _candidate_lt
impl.base._parse_batch = _parse_batch_compat

# The override ledger contains reviewed drift exceptions from earlier publish
# increments. A later increment should require only overrides inside its own
# chapter range instead of failing because historical overrides are unused.
_original_load_overrides = impl._load_overrides


def _load_scoped_overrides():
    data = _original_load_overrides()
    min_chapter = _arg_int("--min-chapter", 6)
    max_chapter = _arg_int("--max-chapter", 80)
    scoped = {}
    for key, value in data.items():
        try:
            chapter = int(key.split("|", 1)[0])
        except (ValueError, IndexError) as exc:
            raise RuntimeError(f"invalid dialogue live override key: {key}") from exc
        if min_chapter <= chapter <= max_chapter:
            scoped[key] = value
    return scoped


impl._load_overrides = _load_scoped_overrides


if __name__ == "__main__":
    raise SystemExit(impl.main())
