#!/usr/bin/env python3
"""Assemble 3L short dual-render captures using locked semantic speaker plans."""

from __future__ import annotations

from typing import Any


ROLE_TO_VOICE = {
    "greg": "deep",
    "dragon": "normal",
}


def expected_capture_keys(plan: dict[str, Any]) -> list[tuple[int, str]]:
    """Return every required (chunk, voice) capture in deterministic order."""
    keys: list[tuple[int, str]] = []
    for chunk in plan.get("chunks", []):
        index = int(chunk["index"])
        for voice in chunk.get("required_voices", []):
            keys.append((index, str(voice)))
    return keys


def validate_capture_manifest(
    plan: dict[str, Any], manifest: dict[str, Any]
) -> dict[tuple[int, str], dict[str, Any]]:
    """Require one exact preview capture for every voice the plan needs."""
    if str(manifest.get("record")) != str(plan.get("record")):
        raise ValueError("record mismatch between plan and capture manifest")

    chunk_by_index = {int(chunk["index"]): chunk for chunk in plan.get("chunks", [])}
    indexed: dict[tuple[int, str], dict[str, Any]] = {}

    for capture in manifest.get("captures", []):
        key = (int(capture["chunk"]), str(capture["voice"]))
        if key in indexed:
            raise ValueError(f"duplicate capture for chunk {key[0]} voice {key[1]}")
        chunk = chunk_by_index.get(key[0])
        if chunk is None or key[1] not in chunk.get("required_voices", []):
            raise ValueError(f"unexpected capture for chunk {key[0]} voice {key[1]}")
        if capture.get("transcript") != chunk.get("transcript"):
            raise ValueError(f"transcript mismatch for chunk {key[0]} voice {key[1]}")
        preview_url = capture.get("preview_url")
        if not isinstance(preview_url, str) or not preview_url.startswith(("http://", "https://")):
            raise ValueError(f"missing preview_url for chunk {key[0]} voice {key[1]}")
        indexed[key] = capture

    expected = set(expected_capture_keys(plan))
    actual = set(indexed)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise ValueError(f"missing captures: {missing}")
    if extra:
        raise ValueError(f"unexpected captures: {extra}")
    return indexed


def choose_role_segments(
    semantic_spans: list[dict[str, Any]],
    timed_by_voice: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Select each semantic span from the timing map for its assigned voice."""
    cursors = {voice: 0 for voice in timed_by_voice}
    chosen: list[dict[str, Any]] = []

    for semantic in semantic_spans:
        role = str(semantic["role"])
        voice = ROLE_TO_VOICE[role]
        candidates = timed_by_voice.get(voice)
        if candidates is None:
            raise ValueError(f"missing timing source for voice {voice}")

        cursor = cursors[voice]
        while cursor < len(candidates) and candidates[cursor].get("role") != role:
            cursor += 1
        if cursor >= len(candidates):
            raise ValueError(f"could not align {role} span to {voice} source")

        timed = candidates[cursor]
        chosen.append(
            {
                "role": role,
                "voice": voice,
                "start_seconds": float(timed["start_seconds"]),
                "end_seconds": float(timed["end_seconds"]),
            }
        )
        cursors[voice] = cursor + 1

    return chosen
