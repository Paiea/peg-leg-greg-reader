#!/usr/bin/env python3
from __future__ import annotations


def next_visible_chapters(
    manifest: dict,
    *,
    after_chapter: int,
    count: int,
    max_chapter: int,
) -> list[int]:
    """Return the next visible canon chapters in numeric order."""
    default_visible = manifest.get("default", "visible") == "visible"
    overrides = manifest.get("chapters", {})
    selected: list[int] = []

    for chapter in range(after_chapter + 1, max_chapter + 1):
        chapter_state = overrides.get(str(chapter), {})
        visible = chapter_state.get("showcase", default_visible)
        if not visible:
            continue
        selected.append(chapter)
        if len(selected) == count:
            break

    return selected
