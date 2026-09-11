from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

REQUIRED_AUTHORITY = "derived_editorial_reference"


def _require_text(record: dict, field: str, label: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} requires non-empty {field}")
    return value.strip()


def validate_visual_timeline(records: list[dict]) -> None:
    seen_ids: set[tuple[str, str]] = set()
    by_character: dict[str, list[tuple[int, int | None, str]]] = {}

    for record in records:
        character = _require_text(record, "character", "character visual state")
        state_id = _require_text(record, "state_id", f"character visual state {character}")
        key = (character, state_id)
        if key in seen_ids:
            raise ValueError(f"duplicate character visual state: {character} / {state_id}")
        seen_ids.add(key)

        start = record.get("chapter_start")
        end = record.get("chapter_end")
        if not isinstance(start, int) or start < 1:
            raise ValueError(f"character visual state {state_id} requires positive integer chapter_start")
        if end is not None and (not isinstance(end, int) or end < start):
            raise ValueError(f"character visual state {state_id} has invalid chapter_end")
        if record.get("authority") != REQUIRED_AUTHORITY:
            raise ValueError(f"character visual state {state_id} must use {REQUIRED_AUTHORITY} authority")
        if record.get("canon_authority") is not False:
            raise ValueError(f"character visual state {state_id} must set canon_authority false")

        evidence = record.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
            raise ValueError(f"character visual state {state_id} requires non-empty evidence list")
        for field in ("appearance", "body_state", "mobility_state"):
            value = record.get(field)
            if not isinstance(value, dict):
                raise ValueError(f"character visual state {state_id} {field} must be an object")
        for field in ("must_show", "must_not_show"):
            if field in record:
                value = record[field]
                if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                    raise ValueError(f"character visual state {state_id} {field} must be a list of text")

        by_character.setdefault(character, []).append((start, end, state_id))

    for character, intervals in by_character.items():
        intervals.sort(key=lambda item: item[0])
        for previous, current in zip(intervals, intervals[1:]):
            previous_start, previous_end, previous_id = previous
            current_start, _, current_id = current
            if previous_end is None or current_start <= previous_end:
                raise ValueError(
                    f"character visual timeline overlap for {character}: {previous_id} and {current_id}"
                )


def load_visual_timeline(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not all(isinstance(record, dict) for record in data):
        raise ValueError("character visual timeline must be a JSON list of objects")
    validate_visual_timeline(data)
    return data


def resolve_character_visual_state(records: Iterable[dict], character: str, chapter: int) -> dict | None:
    if not isinstance(chapter, int) or chapter < 1:
        raise ValueError("chapter must be a positive integer")
    for record in records:
        if record.get("character") != character:
            continue
        start = record.get("chapter_start")
        end = record.get("chapter_end")
        if isinstance(start, int) and start <= chapter and (end is None or chapter <= end):
            return {
                key: (dict(value) if isinstance(value, dict) else list(value) if isinstance(value, list) else value)
                for key, value in record.items()
            }
    return None


def resolve_scene_character_states(records: Iterable[dict], characters: Iterable[str], chapter: int) -> dict[str, dict]:
    resolved: dict[str, dict] = {}
    for character in characters:
        state = resolve_character_visual_state(records, character, chapter)
        if state is not None:
            resolved[character] = state
    return resolved
