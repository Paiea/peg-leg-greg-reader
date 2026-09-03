#!/usr/bin/env python3
"""Stable entrypoint for the Book 1 dialogue live integrator."""

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


impl.Candidate.__lt__ = _candidate_lt


if __name__ == "__main__":
    raise SystemExit(impl.main())
