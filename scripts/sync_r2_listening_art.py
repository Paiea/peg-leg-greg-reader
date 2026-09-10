#!/usr/bin/env python3
"""Register conventionally named R2 listening-shelf art in presentation.json."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "greg-again" / "audio"
ART_DIR = AUDIO_DIR / "assets" / "art"
MANIFEST_PATH = AUDIO_DIR / "manifest.json"
PRESENTATION_PATH = AUDIO_DIR / "presentation.json"
ART_RE = re.compile(r"^chapter-(\d{3})\.webp$")
ART_PATH_RE = re.compile(r"^assets/art/(chapter-\d{3}\.webp)$")
STABLE_ID_RE = re.compile(r"^ga-\d{3}$")


def sync_presentation(manifest: dict, presentation: dict, filenames: Iterable[str]) -> dict:
    """Return presentation data synchronized with conventional chapter art.

    Existing editorial metadata is preserved. Conventional image registrations
    are added or removed to match files currently present in the art folder.
    Nonconventional manual image mappings are left untouched.
    """

    result = copy.deepcopy(presentation)
    result.setdefault("version", 1)
    entries = result.setdefault("chapters", {})
    present_filenames = set(filenames)

    by_number = {}
    for chapter in manifest.get("chapters", []):
        try:
            number = int(chapter["number"])
            stable_id = str(chapter["chapter_id"])
        except (KeyError, TypeError, ValueError):
            continue
        if STABLE_ID_RE.fullmatch(stable_id):
            by_number[number] = chapter

    for stable_id, metadata in list(entries.items()):
        entry = dict(metadata or {})
        image_src = entry.get("image_src")
        path_match = ART_PATH_RE.fullmatch(str(image_src)) if image_src else None
        if path_match and path_match.group(1) not in present_filenames:
            entry.pop("image_src", None)
            entries[stable_id] = entry

    for filename in sorted(present_filenames):
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit nonzero if presentation.json is not synchronized; do not write changes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    presentation = json.loads(PRESENTATION_PATH.read_text(encoding="utf-8"))
    filenames = [path.name for path in ART_DIR.glob("chapter-*.webp")]

    updated = sync_presentation(manifest, presentation, filenames)
    if args.check:
        if updated != presentation:
            print("R2 listening art presentation is out of sync.")
            return 1
        print("R2 listening art presentation is in sync.")
        return 0

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
