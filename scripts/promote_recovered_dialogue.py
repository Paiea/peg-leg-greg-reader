#!/usr/bin/env python3
"""Promote accepted dialogue patches into recovered exact Markdown authority."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import apply_dialogue_attribution_patches as base
import dialogue_live_entrypoint  # installs modern batch compatibility parser


CHAPTER_BOUNDARY_RE = re.compile(r"^# CHAPTER (\d+)\s*$", re.MULTILINE)


def _chapter_spans(text: str) -> dict[int, tuple[int, int]]:
    matches = list(CHAPTER_BOUNDARY_RE.finditer(text))
    spans: dict[int, tuple[int, int]] = {}
    for index, match in enumerate(matches):
        number = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        spans[number] = (match.start(), end)
    return spans


def _paragraphs(chunk: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n+", chunk) if part.strip()]


def _replace_segment(chunk: str, current: tuple[str, ...], replacement: tuple[str, ...], label: str) -> tuple[str, str]:
    paragraphs = _paragraphs(chunk)
    width = len(current)
    replacement_width = len(replacement)
    current_hits = [
        i for i in range(len(paragraphs) - width + 1)
        if tuple(paragraphs[i:i + width]) == current
    ]
    replacement_hits = [
        i for i in range(len(paragraphs) - replacement_width + 1)
        if tuple(paragraphs[i:i + replacement_width]) == replacement
    ]
    if len(replacement_hits) == 1 and not current_hits:
        return chunk, "already"
    if len(current_hits) != 1:
        raise RuntimeError(f"{label}: expected current text exactly once, found {len(current_hits)}")

    start = current_hits[0]
    paragraphs[start:start + width] = list(replacement)
    return "\n\n".join(paragraphs) + "\n", "applied"


def _replace_patch(chunk: str, patch: base.Patch) -> tuple[str, str]:
    if base.GAP not in patch.current and base.GAP not in patch.replacement:
        return _replace_segment(chunk, patch.current, patch.replacement, patch.label)
    current_segments = base._split_gaps(patch.current)
    replacement_segments = base._split_gaps(patch.replacement)
    if len(current_segments) != len(replacement_segments):
        raise RuntimeError(f"{patch.label}: mismatched gapped patch segments")
    statuses: list[str] = []
    for index, (current, replacement) in enumerate(zip(current_segments, replacement_segments), start=1):
        chunk, status = _replace_segment(chunk, current, replacement, f"{patch.label} segment {index}")
        statuses.append(status)
    return chunk, "already" if all(status == "already" for status in statuses) else "applied"


def apply_patches_to_recovered(path: Path, patches: list[base.Patch], min_chapter: int, max_chapter: int) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original
    by_chapter: dict[int, list[base.Patch]] = {}
    for patch in patches:
        if min_chapter <= patch.chapter <= max_chapter:
            by_chapter.setdefault(patch.chapter, []).append(patch)

    for chapter in sorted(by_chapter, reverse=True):
        spans = _chapter_spans(text)
        if chapter not in spans:
            raise RuntimeError(f"missing recovered chapter {chapter}")
        start, end = spans[chapter]
        chunk = text[start:end]
        for patch in by_chapter[chapter]:
            if any("—" in value for value in patch.replacement if value != base.GAP):
                raise RuntimeError(f"{patch.label}: replacement introduces em dash")
            chunk, _ = _replace_patch(chunk, patch)
        text = text[:start] + chunk.rstrip() + "\n\n" + text[end:].lstrip("\n")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("range", help="N-N, for example 156-163")
    parser.add_argument("--patch-ref", default="origin/editor/voice-compression-pass")
    parser.add_argument("--source", type=Path, default=Path("state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md"))
    args = parser.parse_args()
    match = re.fullmatch(r"(\d+)-(\d+)", args.range)
    if not match:
        raise SystemExit("range must be N-N")
    start, end = map(int, match.groups())
    if start > end:
        start, end = end, start
    patches = base.load_patches(args.patch_ref, start, end)
    changed = apply_patches_to_recovered(args.source, patches, start, end)
    print(f"recovered dialogue promotion {start}-{end}: patches={len(patches)} changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
