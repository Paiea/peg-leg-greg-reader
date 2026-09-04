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

# The legacy applicator uses --canonicalize-from as both the first chapter looped
# and the Book I name-map threshold. For Book II increments we need the full
# requested loop without applying the Book I Pell/Arlo map. A threshold above
# max-chapter is the explicit sentinel for that mode.
_requested_canonicalize_from = _arg_int("--canonicalize-from", 1)
_min_chapter = _arg_int("--min-chapter", 6)
_max_chapter = _arg_int("--max-chapter", 80)
_disable_canonicalize = _requested_canonicalize_from > _max_chapter
if _disable_canonicalize and "--canonicalize-from" in sys.argv:
    sys.argv[sys.argv.index("--canonicalize-from") + 1] = str(_min_chapter)

_original_apply_to_chapter = impl.base.apply_to_chapter


def _apply_with_scope(path, patches, canonicalize):
    return _original_apply_to_chapter(
        path, patches, canonicalize=False if _disable_canonicalize else canonicalize
    )


impl.base.apply_to_chapter = _apply_with_scope


if __name__ == "__main__":
    raise SystemExit(impl.main())
