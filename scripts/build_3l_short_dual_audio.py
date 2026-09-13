#!/usr/bin/env python3
"""Assemble a verified 3L record from preview-safe short dual-render captures."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
from typing import Any

BITRATE = "192k"
SETTLING_TAIL_SECONDS = 2.0
ROLE_TO_VOICE = {"greg": "deep", "dragon": "normal"}


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _probe_duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def expected_capture_keys(plan: dict[str, Any]) -> list[tuple[int, str]]:
    return [
        (int(chunk["index"]), str(voice))
        for chunk in plan.get("chunks", [])
        for voice in chunk.get("required_voices", [])
    ]


def validate_verified_capture_receipt(
    plan: dict[str, Any], receipt: dict[str, Any]
) -> dict[tuple[int, str], dict[str, Any]]:
    expected = set(expected_capture_keys(plan))
    if receipt.get("record") != plan.get("record"):
        raise ValueError("verification receipt record does not match plan")
    if receipt.get("complete") is not True:
        raise ValueError("verification receipt is incomplete")
    if receipt.get("missing") not in ([], None):
        raise ValueError("verification receipt still reports missing captures")
    if int(receipt.get("planned_capture_count", -1)) != len(expected):
        raise ValueError("verification receipt planned capture count does not match plan")

    indexed: dict[tuple[int, str], dict[str, Any]] = {}
    for item in receipt.get("captures", []):
        key = (int(item["chunk"]), str(item["voice"]))
        if key in indexed:
            raise ValueError(f"duplicate verified capture {key}")
        if item.get("status") != "verified":
            raise ValueError(f"capture {key} is not verified")
        if not item.get("preview_url"):
            raise ValueError(f"capture {key} has no preview URL")
        if not item.get("sha256"):
            raise ValueError(f"capture {key} has no verified sha256")
        indexed[key] = item
    if set(indexed) != expected:
        missing = sorted(expected - set(indexed))
        extra = sorted(set(indexed) - expected)
        raise ValueError(f"verified capture coverage mismatch; missing={missing} extra={extra}")
    return indexed


def collapse_role_spans(transcript: str, spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse detailed semantic spans to true speaker-transition regions."""
    if not spans:
        raise ValueError("chunk has no semantic spans")
    ordered = sorted(spans, key=lambda item: int(item["start"]))
    cursor = 0
    collapsed: list[dict[str, Any]] = []
    for item in ordered:
        start = int(item["start"])
        end = int(item["end"])
        role = str(item["role"])
        if role not in ROLE_TO_VOICE:
            raise ValueError(f"unknown semantic role {role}")
        if start != cursor or end <= start or end > len(transcript):
            raise ValueError("semantic spans do not exactly cover transcript")
        text = transcript[start:end]
        if item.get("text") not in (None, text):
            raise ValueError("semantic span text does not match transcript")
        if collapsed and collapsed[-1]["role"] == role:
            collapsed[-1]["end"] = end
            collapsed[-1]["text"] += text
        else:
            collapsed.append({"start": start, "end": end, "role": role, "text": text})
        cursor = end
    if cursor != len(transcript):
        raise ValueError("semantic spans do not cover transcript end")
    return collapsed


def _detect_silences(path: Path, noise: str = "-38dB", minimum: float = 0.06) -> list[tuple[float, float]]:
    completed = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            f"silencedetect=noise={noise}:d={minimum}",
            "-f",
            "null",
            "-",
        ],
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=True,
    )
    starts: list[float] = []
    silences: list[tuple[float, float]] = []
    for line in completed.stderr.splitlines():
        if "silence_start:" in line:
            starts.append(float(line.split("silence_start:", 1)[1].strip().split()[0]))
        elif "silence_end:" in line and starts:
            end = float(line.split("silence_end:", 1)[1].strip().split()[0])
            silences.append((starts.pop(0), end))
    duration = _probe_duration(path)
    for start in starts:
        silences.append((start, duration))
    return silences


def _silence_midpoints(path: Path) -> list[float]:
    return [(start + end) / 2 for start, end in _detect_silences(path)]


def _snap_to_silence(expected: float, candidates: list[float], radius: float) -> float:
    nearby = [value for value in candidates if abs(value - expected) <= radius]
    return min(nearby, key=lambda value: abs(value - expected)) if nearby else expected


def _source_timing_map(
    transcript: str,
    regions: list[dict[str, Any]],
    source_path: Path,
) -> list[dict[str, Any]]:
    duration = _probe_duration(source_path)
    boundaries = [int(region["end"]) for region in regions[:-1]]
    silences = _silence_midpoints(source_path)
    snapped: list[float] = []
    previous = 0.0
    for char_end in boundaries:
        expected = duration * (char_end / max(len(transcript), 1))
        radius = max(0.28, min(1.2, duration * 0.035))
        value = _snap_to_silence(expected, silences, radius)
        value = max(previous + 0.02, min(value, duration - 0.02))
        snapped.append(value)
        previous = value
    times = [0.0, *snapped, duration]
    return [
        {
            "role": region["role"],
            "start_seconds": times[index],
            "end_seconds": times[index + 1],
        }
        for index, region in enumerate(regions)
    ]


def choose_role_segments(
    regions: list[dict[str, Any]],
    timed_by_voice: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for index, region in enumerate(regions):
        voice = ROLE_TO_VOICE[str(region["role"])]
        source_regions = timed_by_voice[voice]
        selected.append(
            {
                "role": region["role"],
                "voice": voice,
                "start_seconds": float(source_regions[index]["start_seconds"]),
                "end_seconds": float(source_regions[index]["end_seconds"]),
            }
        )
    return selected


def _download_verified_capture(item: dict[str, Any], target: Path) -> None:
    _run(
        [
            "curl",
            "-L",
            "--fail",
            "--retry",
            "3",
            "--retry-delay",
            "1",
            "-o",
            str(target),
            str(item["preview_url"]),
        ]
    )
    _run(["ffmpeg", "-v", "error", "-i", str(target), "-f", "null", "-"])
    digest = _sha256(target)
    if digest != item["sha256"]:
        raise ValueError(f"downloaded capture sha mismatch for chunk {item['chunk']} {item['voice']}")


def _render_wav_segment(
    source: Path,
    target: Path,
    start_seconds: float | None = None,
    end_seconds: float | None = None,
) -> None:
    command = ["ffmpeg", "-y", "-v", "error"]
    if start_seconds is not None:
        command += ["-ss", f"{start_seconds:.6f}"]
    command += ["-i", str(source)]
    if end_seconds is not None:
        duration = max(0.02, end_seconds - (start_seconds or 0.0))
        command += ["-t", f"{duration:.6f}"]
    command += ["-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(target)]
    _run(command)


def _concat_wavs(parts: list[Path], target: Path) -> None:
    if not parts:
        raise ValueError("cannot concatenate zero WAV parts")
    if len(parts) == 1:
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(parts[0]), "-c:a", "pcm_s16le", str(target)])
        return
    list_path = target.with_suffix(".concat.txt")
    list_path.write_text("".join(f"file '{path.as_posix()}'\n" for path in parts), encoding="utf-8")
    _run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c:a",
            "pcm_s16le",
            str(target),
        ]
    )


def _encode_final_mp3(source_wav: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    _run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(source_wav),
            "-af",
            f"apad=pad_dur={SETTLING_TAIL_SECONDS}",
            "-t",
            f"{_probe_duration(source_wav) + SETTLING_TAIL_SECONDS:.6f}",
            "-b:a",
            BITRATE,
            str(target),
        ]
    )
    _run(["ffmpeg", "-v", "error", "-i", str(target), "-f", "null", "-"])


def build_record(record: str, root: Path | None = None) -> dict[str, Any]:
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
        "plan_sha256": _sha256(plan_path),
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
