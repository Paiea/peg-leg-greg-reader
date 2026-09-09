#!/usr/bin/env python3
"""Register conventionally named R2 listening-shelf art in presentation.json."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "greg-again" / "audio"
ART_DIR = AUDIO_DIR / "assets" / "art"
MANIFEST_PATH = AUDIO_DIR / "manifest.json"
PRESENTATION_PATH = AUDIO_DIR / "presentation.json"
ART_RE = re.compile(r"^chapter-(\d{3})\.webp$")
STABLE_ID_RE = re.compile(r"^ga-\d{3}$")


def sync_presentation(manifest: dict, presentation: dict, filenames: Iterable[str]) -> dict:
    """Return presentation data with known chapter-NNN.webp files registered.

    Existing presentation metadata is preserved. Files that do not match a
    published audio chapter are ignored rather than inventing new identities.
    """

    result = copy.deepcopy(presentation)
    result.setdefault("version", 1)
    entries = result.setdefault("chapters", {})

    by_number = {}
    for chapter in manifest.get("chapters", []):
        try:
            number = int(chapter["number"])
            stable_id = str(chapter["chapter_id"])
        except (KeyError, TypeError, ValueError):
            continue
        if STABLE_ID_RE.fullmatch(stable_id):
            by_number[number] = chapter

    for filename in sorted(set(filenames)):
        match = ART_RE.fullmatch(filename)
        if not match:
            continue

        number = int(match.group(1))
        chapter = by_number.get(number)
        if not chapter:
            continue

        stable_id = str(chapter["chapter_id"])
        entry = dict(entries.get(stable_id) or {})
        entry["image_src"] = f"assets/art/{filename}"
        entry.setdefault(
            "alt",
            f"Chapter {number}: {chapter.get('title', 'Peg-Leg Greg R2')} illustration.",
        )
        entries[stable_id] = entry

    return result


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    presentation = json.loads(PRESENTATION_PATH.read_text(encoding="utf-8"))
    filenames = [path.name for path in ART_DIR.glob("chapter-*.webp")]

    updated = sync_presentation(manifest, presentation, filenames)
    if updated != presentation:
        PRESENTATION_PATH.write_text(
            json.dumps(updated, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    registered = sum(
        1
        for metadata in updated.get("chapters", {}).values()
        if metadata.get("image_src")
    )
    print(f"R2 listening art registered: {registered}")


if __name__ == "__main__":
    main()
