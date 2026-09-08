#!/usr/bin/env python3
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path

from scripts.greg_again_audio import build_public_metadata, selected_take_paths, validate_manifest, validate_score
from scripts.greg_again_audio_assembly import assemble_pcm_wav
from scripts.greg_again_audio_render import export_bootstrap_bundle

ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "state/experiments/greg-again/audio"
CHAPTER_ROOT = AUDIO_ROOT / "chapters/001"
SCORE_PATH = CHAPTER_ROOT / "score.json"
MANIFEST_PATH = CHAPTER_ROOT / "manifest.json"
NARRATOR_PATH = AUDIO_ROOT / "narrator.md"
PUBLIC_ROOT = ROOT / "greg-again/audio"
PUBLIC_MANIFEST_PATH = PUBLIC_ROOT / "manifest.json"
PUBLIC_AUDIO_PATH = PUBLIC_ROOT / "assets/chapter-001.wav"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_state() -> tuple[dict, dict]:
    score = validate_score(_read_json(SCORE_PATH))
    manifest = validate_manifest(_read_json(MANIFEST_PATH), score)
    return score, manifest


def select_take(block_id: str, take_id: str) -> dict:
    score, manifest = validate_state()
    takes = manifest.get("takes", {})
    if block_id not in takes or take_id not in takes[block_id]:
        raise ValueError(f"take {take_id} is not registered for {block_id}")
    updated = deepcopy(manifest)
    updated.setdefault("selected_takes", {})[block_id] = take_id
    validate_manifest(updated, score)
    _write_json(MANIFEST_PATH, updated)
    return updated


def assemble() -> dict:
    score, manifest = validate_state()
    paths = selected_take_paths(manifest, CHAPTER_ROOT)
    duration = assemble_pcm_wav(paths, PUBLIC_AUDIO_PATH)
    updated = deepcopy(manifest)
    updated["assembled_asset"] = "assets/chapter-001.wav"
    updated["duration_seconds"] = round(duration, 3)
    if all(
        updated["takes"][block_id][updated["selected_takes"][block_id]]["renderer_status"] == "qualified"
        for block_id in updated["block_order"]
    ):
        updated["renderer_status"] = "qualified"
    validate_manifest(updated, score)
    _write_json(MANIFEST_PATH, updated)
    return updated


def publish_metadata() -> dict:
    _, manifest = validate_state()
    public = build_public_metadata(manifest)
    _write_json(PUBLIC_MANIFEST_PATH, public)
    return public


def main() -> None:
    parser = argparse.ArgumentParser(description="Greg, Again Chapter 1 Audio OS")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    export = sub.add_parser("export-bootstrap")
    export.add_argument("--output-dir", type=Path, default=CHAPTER_ROOT / "bootstrap")
    select = sub.add_parser("select-take")
    select.add_argument("--block-id", required=True)
    select.add_argument("--take-id", required=True)
    sub.add_parser("assemble")
    sub.add_parser("publish-metadata")
    args = parser.parse_args()

    if args.command == "validate":
        score, manifest = validate_state()
        print(json.dumps({"chapter_id": score["chapter_id"], "renderer_status": manifest["renderer_status"]}))
    elif args.command == "export-bootstrap":
        score, _ = validate_state()
        paths = export_bootstrap_bundle(score, NARRATOR_PATH.read_text(encoding="utf-8"), args.output_dir)
        print(json.dumps({"exported_blocks": len(paths), "output_dir": str(args.output_dir)}))
    elif args.command == "select-take":
        updated = select_take(args.block_id, args.take_id)
        print(json.dumps({"selected": updated["selected_takes"][args.block_id]}))
    elif args.command == "assemble":
        updated = assemble()
        print(json.dumps({"assembled_asset": updated["assembled_asset"], "duration_seconds": updated["duration_seconds"]}))
    elif args.command == "publish-metadata":
        print(json.dumps(publish_metadata()))


if __name__ == "__main__":
    main()
