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


def validate_verified_capture_receipt(
    plan: dict[str, Any], receipt: dict[str, Any]
) -> dict[tuple[int, str], dict[str, Any]]:
    """Validate the verifier's immutable source receipt before assembly."""
    if str(receipt.get("record")) != str(plan.get("record")):
        raise ValueError("record mismatch between plan and verified capture receipt")

    expected = set(expected_capture_keys(plan))
    planned_count = len(expected)
    if (
        receipt.get("complete") is not True
        or receipt.get("missing") not in ([], None)
        or int(receipt.get("verified_capture_count", -1)) != planned_count
        or int(receipt.get("planned_capture_count", -1)) != planned_count
    ):
        raise ValueError("incomplete verified capture receipt")

    indexed: dict[tuple[int, str], dict[str, Any]] = {}
    for capture in receipt.get("captures", []):
        key = (int(capture["chunk"]), str(capture["voice"]))
        if key in indexed:
            raise ValueError(f"duplicate verified capture for chunk {key[0]} voice {key[1]}")
        if key not in expected:
            raise ValueError(f"unexpected verified capture for chunk {key[0]} voice {key[1]}")
        if capture.get("status") != "verified":
            raise ValueError(f"unverified capture for chunk {key[0]} voice {key[1]}")
        preview_url = capture.get("preview_url")
        if not isinstance(preview_url, str) or not preview_url.startswith(("http://", "https://")):
            raise ValueError(f"missing preview_url for chunk {key[0]} voice {key[1]}")
        sha256 = capture.get("sha256")
        if (
            not isinstance(sha256, str)
            or len(sha256) != 64
            or any(char not in "0123456789abcdefABCDEF" for char in sha256)
        ):
            raise ValueError(f"invalid sha256 for chunk {key[0]} voice {key[1]}")
        indexed[key] = capture

    actual = set(indexed)
    if actual != expected:
        raise ValueError("incomplete verified capture receipt")
    return indexed


def collapse_role_spans(
    transcript: str, semantic_spans: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Collapse detailed annotations to the actual Greg/Dragon transition regions.

    The short-take planner may annotate many adjacent pieces owned by the same role.
    Audio only needs a cut where ownership changes. Whitespace between annotations is
    assigned to the preceding role so the collapsed spans cover the full transcript.
    """
    if not transcript:
        return []
    if not semantic_spans:
        raise ValueError("chunk has no semantic spans")

    ordered = sorted(semantic_spans, key=lambda span: (int(span["start"]), int(span["end"])))
    first_role = str(ordered[0]["role"])
    if first_role not in ROLE_TO_VOICE:
        raise ValueError(f"unknown semantic role {first_role}")

    collapsed: list[dict[str, Any]] = []
    current_role = first_role
    region_start = 0
    last_start = -1

    for span in ordered[1:]:
        start = int(span["start"])
        role = str(span["role"])
        if start < last_start:
            raise ValueError("semantic spans are not ordered")
        if role not in ROLE_TO_VOICE:
            raise ValueError(f"unknown semantic role {role}")
        if role != current_role:
            if start <= region_start or start > len(transcript):
                raise ValueError("invalid semantic role transition offset")
            collapsed.append({"start": region_start, "end": start, "role": current_role})
            region_start = start
            current_role = role
        last_start = start

    collapsed.append({"start": region_start, "end": len(transcript), "role": current_role})
    return collapsed


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
