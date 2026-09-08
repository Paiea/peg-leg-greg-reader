from __future__ import annotations

import json
from pathlib import Path

SCENE_PRIORITIES = {"high", "medium", "low"}
SCENE_KINDS = {"chapter_illustration", "role_card", "act_card", "book_card"}
FIT_TARGETS = {"exact", "close_enough"}
SPOILER_LEVELS = {"low", "medium", "high"}
SCENE_STATUSES = {"candidate", "prompt_ready", "generated", "approved", "live", "rejected"}
REGISTRY_STATUSES = {"queued", "generated", "approved", "live", "rejected"}
PRESENTATION_ROLES = {"sketch-beat", "scene-illustration", "feature-illustration", "feature-portrait"}


def _load_json_list(path: Path, label: str) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{label} must be a JSON list")
    if not all(isinstance(record, dict) for record in data):
        raise ValueError(f"{label} entries must be JSON objects")
    return data


def _require_text(record: dict, field: str, label: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} requires non-empty {field}")
    return value.strip()


def _require_enum(record: dict, field: str, allowed: set[str], label: str) -> str:
    value = record.get(field)
    if value not in allowed:
        raise ValueError(f"{label} has invalid {field}: {value!r}")
    return value


def load_scene_candidates(path: Path) -> list[dict]:
    records = _load_json_list(path, "scene candidates")
    validate_scene_candidates(records)
    return records


def validate_scene_candidates(records: list[dict]) -> None:
    seen: set[str] = set()
    for record in records:
        candidate_id = _require_text(record, "id", "scene candidate")
        if candidate_id in seen:
            raise ValueError(f"duplicate scene candidate id: {candidate_id}")
        seen.add(candidate_id)

        chapter = record.get("chapter")
        if not isinstance(chapter, int) or chapter < 1:
            raise ValueError(f"scene candidate {candidate_id} requires positive integer chapter")

        _require_text(record, "chapter_title", f"scene candidate {candidate_id}")
        _require_text(record, "scene_summary", f"scene candidate {candidate_id}")
        _require_text(record, "visual_hook", f"scene candidate {candidate_id}")
        _require_enum(record, "priority", SCENE_PRIORITIES, f"scene candidate {candidate_id}")
        _require_enum(record, "kind", SCENE_KINDS, f"scene candidate {candidate_id}")
        _require_enum(record, "fit_target", FIT_TARGETS, f"scene candidate {candidate_id}")
        _require_enum(record, "spoiler_level", SPOILER_LEVELS, f"scene candidate {candidate_id}")
        _require_enum(record, "status", SCENE_STATUSES, f"scene candidate {candidate_id}")

        characters = record.get("characters")
        if not isinstance(characters, list) or not all(isinstance(name, str) and name.strip() for name in characters):
            raise ValueError(f"scene candidate {candidate_id} requires characters list")

        for field in ("location", "mood"):
            if field in record and not isinstance(record[field], str):
                raise ValueError(f"scene candidate {candidate_id} {field} must be text")


def load_registry(path: Path, root: Path | None = None) -> list[dict]:
    records = _load_json_list(path, "illustration registry")
    validate_registry(records, root=root)
    return records


def validate_registry(records: list[dict], root: Path | None = None) -> None:
    seen: set[str] = set()
    for record in records:
        art_id = _require_text(record, "id", "illustration")
        if art_id in seen:
            raise ValueError(f"duplicate illustration id: {art_id}")
        seen.add(art_id)

        _require_text(record, "candidate_id", f"illustration {art_id}")
        chapter = record.get("chapter")
        if not isinstance(chapter, int) or chapter < 1:
            raise ValueError(f"illustration {art_id} requires positive integer chapter")
        _require_enum(record, "kind", SCENE_KINDS, f"illustration {art_id}")
        status = _require_enum(record, "status", REGISTRY_STATUSES, f"illustration {art_id}")
        _require_enum(record, "approved_fit", FIT_TARGETS, f"illustration {art_id}")
        _require_text(record, "style_family", f"illustration {art_id}")
        _require_text(record, "prompt_pack", f"illustration {art_id}")

        for field in ("source_asset", "live_asset", "caption", "alt_text"):
            value = record.get(field, "")
            if not isinstance(value, str):
                raise ValueError(f"illustration {art_id} {field} must be text")

        if "presentation_role" in record:
            _require_enum(record, "presentation_role", PRESENTATION_ROLES, f"illustration {art_id}")
        if "editorial_purpose" in record:
            _require_text(record, "editorial_purpose", f"illustration {art_id}")
        if "editorial_note" in record and not isinstance(record.get("editorial_note"), str):
            raise ValueError(f"illustration {art_id} editorial_note must be text")

        if status in {"approved", "live"}:
            _require_text(record, "alt_text", f"illustration {art_id}")

        if status == "live":
            live_asset = _require_text(record, "live_asset", f"illustration {art_id}")
            if root is not None and not (root / live_asset).is_file():
                raise ValueError(f"illustration {art_id} live_asset does not exist: {live_asset}")
