from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
import json
from typing import Any

from scripts.greg_again_audio import RENDERER_STATES


@dataclass(frozen=True)
class RendererRequest:
    block_id: str
    spoken_text: str
    narrator_brief: str
    performance_context: dict[str, Any]
    prior_block_text: str | None = None
    pronunciation_notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RendererResult:
    take_id: str
    relative_path: str
    adapter: str
    model: str | None
    voice: str | None
    renderer_status: str
    generation_note: str | None = None


def build_renderer_request(
    block: dict[str, Any],
    narrator_text: str,
    *,
    prior_block_text: str | None = None,
) -> RendererRequest:
    return RendererRequest(
        block_id=str(block["id"]),
        spoken_text=str(block["spoken_text"]),
        narrator_brief=narrator_text,
        performance_context=deepcopy(block.get("direction", {})),
        prior_block_text=prior_block_text,
        pronunciation_notes=tuple(block.get("pronunciation_notes", [])),
    )


def export_bootstrap_bundle(score: dict[str, Any], narrator_text: str, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    previous: str | None = None
    index: list[dict[str, str]] = []
    for block in score.get("blocks", []):
        request = build_renderer_request(block, narrator_text, prior_block_text=previous)
        payload = asdict(request)
        payload["pronunciation_notes"] = list(request.pronunciation_notes)
        path = output_dir / f"{request.block_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        paths.append(path)
        index.append({"block_id": request.block_id, "path": path.name})
        previous = request.spoken_text
    (output_dir / "index.json").write_text(
        json.dumps({
            "chapter_id": score.get("chapter_id"),
            "score_revision": score.get("score_revision"),
            "blocks": index,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    return paths


def register_take(
    manifest: dict[str, Any],
    *,
    block_id: str,
    take_id: str,
    relative_path: str,
    adapter: str,
    model: str | None,
    voice: str | None,
    renderer_status: str,
    generation_note: str | None = None,
) -> dict[str, Any]:
    if renderer_status not in RENDERER_STATES:
        raise ValueError("renderer_status must use an allowed state")
    updated = deepcopy(manifest)
    updated.setdefault("takes", {})
    updated.setdefault("selected_takes", {})
    updated["takes"].setdefault(block_id, {})
    updated["takes"][block_id][take_id] = {
        "relative_path": relative_path,
        "adapter": adapter,
        "model": model,
        "voice": voice,
        "renderer_status": renderer_status,
        "generation_note": generation_note,
    }
    return updated
