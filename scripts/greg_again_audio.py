from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any

SCORE_SCHEMA = "greg_again_audio_score/v1"
MANIFEST_SCHEMA = "greg_again_audio_manifest/v1"
RENDERER_STATES = {"qualified", "experimental", "failed_quality_gate", "unrendered"}
APPROVAL_STATES = {"experimental", "approved"}
_BLOCK_ID = re.compile(r"^ga-001-b\d{3}$")


def _nonempty(value: object, *, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} must be nonempty")
    return text


def validate_score(score: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(score, dict):
        raise ValueError("score must be an object")
    if score.get("schema") != SCORE_SCHEMA:
        raise ValueError("score schema mismatch")
    if score.get("run_id") != "greg-again":
        raise ValueError("run_id must be greg-again")
    _nonempty(score.get("chapter_id"), field="chapter_id")
    _nonempty(score.get("title"), field="title")
    revision = score.get("score_revision")
    if not isinstance(revision, int) or revision < 1:
        raise ValueError("score_revision must be a positive integer")
    blocks = score.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("blocks must be a nonempty list")
    seen: set[str] = set()
    for block in blocks:
        if not isinstance(block, dict):
            raise ValueError("each block must be an object")
        block_id = _nonempty(block.get("id"), field="block id")
        if not _BLOCK_ID.match(block_id):
            raise ValueError(f"unstable block id: {block_id}")
        if block_id in seen:
            raise ValueError(f"duplicate block id: {block_id}")
        seen.add(block_id)
        _nonempty(block.get("scene_id"), field="scene_id")
        _nonempty(block.get("spoken_text"), field="spoken_text")
        if not isinstance(block.get("direction"), dict):
            raise ValueError("direction must be an object")
    return deepcopy(score)


def validate_manifest(manifest: dict[str, Any], score: dict[str, Any]) -> dict[str, Any]:
    validate_score(score)
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be an object")
    if manifest.get("schema") != MANIFEST_SCHEMA:
        raise ValueError("manifest schema mismatch")
    if manifest.get("run_id") != "greg-again":
        raise ValueError("run_id must be greg-again")
    if manifest.get("chapter_id") != score.get("chapter_id"):
        raise ValueError("chapter_id must match score")
    if manifest.get("title") != score.get("title"):
        raise ValueError("title must match score")
    if manifest.get("score_revision") != score.get("score_revision"):
        raise ValueError("score_revision must match score")
    if manifest.get("renderer_status") not in RENDERER_STATES:
        raise ValueError("renderer_status must use an allowed state")
    if manifest.get("approval_state") not in APPROVAL_STATES:
        raise ValueError("approval_state must use an allowed state")

    expected = [block["id"] for block in score["blocks"]]
    if manifest.get("block_order") != expected:
        raise ValueError("block_order must exactly match score block ids")

    takes = manifest.get("takes", {})
    selected = manifest.get("selected_takes", {})
    if not isinstance(takes, dict) or not isinstance(selected, dict):
        raise ValueError("takes and selected_takes must be objects")
    known = set(expected)
    unknown_takes = set(takes) - known
    unknown_selected = set(selected) - known
    if unknown_takes or unknown_selected:
        raise ValueError("take keys must reference known block ids")
    for block_id, block_takes in takes.items():
        if not isinstance(block_takes, dict):
            raise ValueError(f"takes for {block_id} must be an object")
        for take_id, take in block_takes.items():
            _nonempty(take_id, field="take id")
            if not isinstance(take, dict):
                raise ValueError("take record must be an object")
            _nonempty(take.get("relative_path"), field="relative_path")
            if take.get("renderer_status") not in RENDERER_STATES:
                raise ValueError("take renderer_status must use an allowed state")
    for block_id, take_id in selected.items():
        if block_id not in takes or take_id not in takes[block_id]:
            raise ValueError(f"selected take not registered for {block_id}")
    return deepcopy(manifest)


def selected_take_paths(manifest: dict[str, Any], takes_root: Path) -> list[Path]:
    paths: list[Path] = []
    takes = manifest.get("takes", {})
    selected = manifest.get("selected_takes", {})
    for block_id in manifest.get("block_order", []):
        take_id = selected.get(block_id)
        if not take_id:
            raise ValueError(f"missing selected take for {block_id}")
        try:
            record = takes[block_id][take_id]
        except KeyError as exc:
            raise ValueError(f"selected take not registered for {block_id}") from exc
        if record.get("renderer_status") != "qualified":
            raise ValueError(f"selected take for {block_id} must be qualified")
        paths.append(takes_root / record["relative_path"])
    return paths


def build_public_metadata(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "chapter_id": manifest.get("chapter_id"),
        "title": manifest.get("title"),
        "status": manifest.get("approval_state"),
        "duration_seconds": manifest.get("duration_seconds"),
        "audio_src": manifest.get("assembled_asset"),
    }
