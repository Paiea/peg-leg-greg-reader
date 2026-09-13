#!/usr/bin/env python3
"""Assemble verified 3L short dual-render captures into chapter audio."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any

try:
    from scripts.build_3l_two_voice_candidate import (
        _detect_silences,
        _probe_duration,
        build_timed_role_spans,
    )
except ModuleNotFoundError:  # Direct execution: python scripts/build_3l_short_dual_audio.py
    from build_3l_two_voice_candidate import (  # type: ignore
        _detect_silences,
        _probe_duration,
        build_timed_role_spans,
    )


ROLE_TO_VOICE = {
    "greg": "deep",
    "dragon": "normal",
}
SAMPLE_RATE = 44100
CHANNELS = 1
BITRATE = "192k"
SETTLING_TAIL_SECONDS = 2.0


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

    The planner may annotate many adjacent pieces owned by the same role. Audio only
    needs a cut where ownership changes. Interstitial whitespace belongs to the role
    that precedes the transition, and the collapsed regions cover the full take.
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
    previous_start = int(ordered[0]["start"])

    for span in ordered[1:]:
        start = int(span["start"])
        role = str(span["role"])
        if start < previous_start:
            raise ValueError("semantic spans are not ordered")
        if role not in ROLE_TO_VOICE:
            raise ValueError(f"unknown semantic role {role}")
        if role != current_role:
            if start <= region_start or start > len(transcript):
                raise ValueError("invalid semantic role transition offset")
            collapsed.append({"start": region_start, "end": start, "role": current_role})
            region_start = start
            current_role = role
        previous_start = start

    collapsed.append({"start": region_start, "end": len(transcript), "role": current_role})
    return collapsed


def choose_role_segments(
    semantic_spans: list[dict[str, Any]],
    timed_by_voice: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Select each semantic region from the timing map for its assigned voice."""
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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _download_verified_capture(capture: dict[str, Any], output: Path) -> None:
    subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--retry",
            "3",
            "--retry-delay",
            "1",
            "-o",
            str(output),
            str(capture["preview_url"]),
        ],
        check=True,
    )
    actual_sha = _sha256(output)
    expected_sha = str(capture["sha256"]).lower()
    if actual_sha.lower() != expected_sha:
        raise ValueError(
            f"source sha256 drift for chunk {capture['chunk']} voice {capture['voice']}: "
            f"expected {expected_sha}, got {actual_sha}"
        )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"],
        check=True,
    )


def _render_wav_segment(
    source: Path,
    output: Path,
    *,
    start_seconds: float | None = None,
    end_seconds: float | None = None,
) -> None:
    filters: list[str] = []
    if start_seconds is not None or end_seconds is not None:
        start = 0.0 if start_seconds is None else float(start_seconds)
        end = _probe_duration(source) if end_seconds is None else float(end_seconds)
        if end - start <= 0.03:
            raise ValueError(f"non-positive or tiny audio segment: {start:.6f}-{end:.6f}")
        filters.append(f"atrim=start={start:.6f}:end={end:.6f}")
        filters.append("asetpts=PTS-STARTPTS")

    command = ["ffmpeg", "-loglevel", "error", "-y", "-i", str(source)]
    if filters:
        command.extend(["-af", ",".join(filters)])
    command.extend(
        [
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            str(CHANNELS),
            "-c:a",
            "pcm_s16le",
            str(output),
        ]
    )
    subprocess.run(command, check=True)


def _concat_wavs(paths: list[Path], output: Path) -> None:
    if not paths:
        raise ValueError("cannot concatenate an empty WAV list")
    concat_file = output.with_suffix(".concat.txt")
    concat_file.write_text(
        "".join(f"file '{path.resolve().as_posix()}'\n" for path in paths),
        encoding="utf-8",
    )
    subprocess.run(
        [
            "ffmpeg",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            str(CHANNELS),
            "-c:a",
            "pcm_s16le",
            str(output),
        ],
        check=True,
    )


def _encode_final_mp3(chapter_wav: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(chapter_wav),
            "-af",
            f"apad=pad_dur={SETTLING_TAIL_SECONDS:.3f}",
            "-c:a",
            "libmp3lame",
            "-b:a",
            BITRATE,
            str(output),
        ],
        check=True,
    )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"],
        check=True,
    )


def _source_timing_map(
    transcript: str,
    collapsed_roles: list[dict[str, Any]],
    source: Path,
) -> list[dict[str, Any]]:
    duration = _probe_duration(source)
    silences = _detect_silences(source)
    timed = build_timed_role_spans(
        transcript,
        collapsed_roles,
        duration_seconds=duration,
        silence_intervals=silences,
    )
    if len(timed) != len(collapsed_roles):
        raise ValueError("timing map changed speaker-transition geometry")
    return timed


def build_record(record: str, *, root: Path | None = None) -> dict[str, Any]:
    """Build one verified short-dual 3L chapter and return its audit receipt."""
    if not record.isdigit() or len(record) != 3:
        raise ValueError("record must be a zero-padded three-digit number")
    root = root or Path(__file__).resolve().parents[1]

    plan_path = root / f"3l/audio/record-{record}-short-dual-plan.json"
    source_receipt_path = root / f"3l/audio/verification/record-{record}-short-captures.json"
    output_path = root / f"3l/assets/audio/record-{record}.mp3"
    verification_path = root / f"3l/audio/verification/record-{record}-short-dual-audio.json"

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    source_receipt = json.loads(source_receipt_path.read_text(encoding="utf-8"))
    indexed = validate_verified_capture_receipt(plan, source_receipt)

    chunk_receipts: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix=f"3l-record-{record}-short-dual-") as temp_name:
        temp = Path(temp_name)
        source_paths: dict[tuple[int, str], Path] = {}

        for key in expected_capture_keys(plan):
            capture = indexed[key]
            source_path = temp / f"chunk-{key[0]:03d}-{key[1]}.mp3"
            _download_verified_capture(capture, source_path)
            source_paths[key] = source_path

        chunk_wavs: list[Path] = []
        for chunk in plan.get("chunks", []):
            chunk_index = int(chunk["index"])
            transcript = str(chunk["transcript"])
            collapsed = collapse_role_spans(transcript, list(chunk.get("semantic_spans", [])))
            required_voices = [str(voice) for voice in chunk.get("required_voices", [])]
            chunk_wav = temp / f"chunk-{chunk_index:03d}-assembled.wav"
            selected_segments: list[dict[str, Any]] = []

            if len(collapsed) == 1:
                role = str(collapsed[0]["role"])
                voice = ROLE_TO_VOICE[role]
                if voice not in required_voices:
                    raise ValueError(f"chunk {chunk_index}: role {role} requires absent voice {voice}")
                source = source_paths[(chunk_index, voice)]
                _render_wav_segment(source, chunk_wav)
                selected_segments.append(
                    {
                        "role": role,
                        "voice": voice,
                        "start_seconds": 0.0,
                        "end_seconds": round(_probe_duration(source), 6),
                    }
                )
            else:
                timed_by_voice: dict[str, list[dict[str, Any]]] = {}
                for voice in required_voices:
                    source = source_paths[(chunk_index, voice)]
                    timed_by_voice[voice] = _source_timing_map(transcript, collapsed, source)

                selected_segments = choose_role_segments(collapsed, timed_by_voice)
                part_wavs: list[Path] = []
                for part_index, segment in enumerate(selected_segments, start=1):
                    source = source_paths[(chunk_index, str(segment["voice"]))]
                    part = temp / f"chunk-{chunk_index:03d}-part-{part_index:02d}.wav"
                    _render_wav_segment(
                        source,
                        part,
                        start_seconds=float(segment["start_seconds"]),
                        end_seconds=float(segment["end_seconds"]),
                    )
                    part_wavs.append(part)
                _concat_wavs(part_wavs, chunk_wav)

            chunk_wavs.append(chunk_wav)
            chunk_receipts.append(
                {
                    "chunk": chunk_index,
                    "required_voices": required_voices,
                    "speaker_regions": collapsed,
                    "selected_segments": selected_segments,
                    "assembled_duration_seconds": round(_probe_duration(chunk_wav), 6),
                }
            )

        chapter_wav = temp / f"record-{record}-assembled.wav"
        _concat_wavs(chunk_wavs, chapter_wav)
        _encode_final_mp3(chapter_wav, output_path)

    duration = _probe_duration(output_path)
    if duration <= SETTLING_TAIL_SECONDS:
        raise ValueError("assembled chapter duration is suspiciously short")

    receipt: dict[str, Any] = {
        "record": record,
        "method": "verified-preview-safe-short-dual-semantic-splice",
        "plan": str(plan_path.relative_to(root)),
        "source_verification": str(source_receipt_path.relative_to(root)),
        "source_verification_sha256": _sha256(source_receipt_path),
        "voices": {"greg": "deep", "dragon": "normal"},
        "audio_processing": {
            "tempo": 1.0,
            "pitch_semitones": 0,
            "formant_shift": 0,
            "dragon_post_processing": False,
            "settling_tail_seconds": SETTLING_TAIL_SECONDS,
            "final_bitrate": BITRATE,
        },
        "planned_capture_count": len(expected_capture_keys(plan)),
        "chunk_count": len(chunk_receipts),
        "mixed_chunk_count": sum(len(item["required_voices"]) > 1 for item in chunk_receipts),
        "duration_seconds": round(duration, 6),
        "byte_size": output_path.stat().st_size,
        "sha256": _sha256(output_path),
        "status": "verified",
        "chunks": chunk_receipts,
    }
    verification_path.parent.mkdir(parents=True, exist_ok=True)
    verification_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        f"record {record}: built {output_path.relative_to(root)} "
        f"duration={duration:.3f}s sha256={receipt['sha256']}"
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", help="zero-padded record number, e.g. 002")
    args = parser.parse_args()
    build_record(args.record)


if __name__ == "__main__":
    main()
