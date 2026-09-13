#!/usr/bin/env python3
"""Build Record 001 from existing Deep Greg spans plus Fancy Dragon take spans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from scripts.build_3l_two_voice_candidate import (
    _concatenate_wav_files,
    _detect_silences,
    _probe_duration,
    _sha256,
    build_timed_role_spans,
    map_transcript_role_spans,
    slice_role_spans,
    validate_dragon_span_map,
)


def render_piece(source: Path, output: Path, start: float, end: float, *, pitch_ratio: float | None = None) -> None:
    if end <= start:
        raise ValueError("piece must have positive duration")
    filters = [f"atrim=start={start:.6f}:end={end:.6f}", "asetpts=PTS-STARTPTS"]
    if pitch_ratio is not None:
        filters.append(
            f"rubberband=pitch={pitch_ratio:.12f}:tempo=1:formant=preserved:pitchq=quality"
        )
    filters += ["aresample=24000", "aformat=sample_fmts=s16:channel_layouts=mono"]
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(source), "-af", ",".join(filters),
         "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(output)],
        check=True,
    )


def build(*, performance: Path, take_map: Path, deep_map: Path, fancy_dir: Path,
          output: Path, verification: Path, pitch_ratio: float, pitch_semitones: float,
          tail_seconds: float = 2.0) -> dict:
    performance_text = performance.read_text(encoding="utf-8")
    takes = json.loads(take_map.read_text(encoding="utf-8"))["takes"]
    deep_takes = json.loads(deep_map.read_text(encoding="utf-8"))["takes"]
    if len(takes) != len(deep_takes):
        raise ValueError("take maps disagree")

    full_transcript = "\n\n".join(t["source_transcript"] for t in takes)
    global_roles = map_transcript_role_spans(performance_text, full_transcript)
    dragon_samples = validate_dragon_span_map(performance_text, full_transcript, global_roles)
    transcript_offset = 0
    pieces: list[Path] = []
    receipts: list[dict] = []
    fancy_used = 0

    with tempfile.TemporaryDirectory(prefix="3l-fancy-takes-") as td:
        temp = Path(td)
        for take, deep in zip(takes, deep_takes):
            order = int(take["order"])
            transcript = take["source_transcript"]
            take_start = transcript_offset
            take_end = take_start + len(transcript)
            local_roles = slice_role_spans(global_roles, take_start=take_start, take_end=take_end)
            deep_spans = deep["mapped_spans"]
            expected_roles = [s["role"] for s in deep_spans]
            has_dragon = "dragon" in expected_roles

            fancy_spans = None
            fancy_source = fancy_dir / f"{order:02d}.mp3"
            if has_dragon:
                if not fancy_source.exists():
                    raise FileNotFoundError(f"missing Fancy take {order:02d}")
                fancy_duration = _probe_duration(fancy_source)
                fancy_spans = build_timed_role_spans(
                    transcript, local_roles,
                    duration_seconds=fancy_duration,
                    silence_intervals=_detect_silences(fancy_source),
                )
                fancy_roles = [s["role"] for s in fancy_spans]
                if fancy_roles != expected_roles:
                    raise ValueError(f"take {order:02d} role mismatch: Deep {expected_roles}, Fancy {fancy_roles}")
                fancy_used += 1

            for idx, deep_span in enumerate(deep_spans, start=1):
                role = deep_span["role"]
                piece = temp / f"{order:02d}-{idx:02d}-{role}.wav"
                if role == "greg":
                    render_piece(
                        Path(deep["source"]), piece,
                        float(deep_span["start_seconds"]), float(deep_span["end_seconds"]),
                    )
                else:
                    assert fancy_spans is not None
                    fancy_span = fancy_spans[idx - 1]
                    render_piece(
                        fancy_source, piece,
                        float(fancy_span["start_seconds"]), float(fancy_span["end_seconds"]),
                        pitch_ratio=pitch_ratio,
                    )
                pieces.append(piece)

            receipts.append({
                "order": order,
                "role_pattern": expected_roles,
                "fancy_take_used": has_dragon,
                "dragon_span_count": sum(r == "dragon" for r in expected_roles),
            })
            transcript_offset = take_end + 2

        if sum(r["dragon_span_count"] for r in receipts) != len(dragon_samples):
            raise ValueError("Dragon span count no longer matches semantic authority")

        wav = temp / "assembled.wav"
        _concatenate_wav_files(pieces, wav, tail_seconds)
        output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav),
             "-c:a", "libmp3lame", "-b:a", "192k", str(output)],
            check=True,
        )

    receipt = {
        "record": 1,
        "status": "verified_unlistened_fancy_dragon_candidate",
        "assembly_mode": "existing_deep_greg_plus_fancy_take_semantic_swap",
        "source_take_count": len(takes),
        "fancy_take_count": fancy_used,
        "dragon_span_count": len(dragon_samples),
        "greg_source": "existing Deep Record 001 short takes",
        "dragon_source": "Fancy preview-safe takes",
        "dragon_pitch_semitones": pitch_semitones,
        "dragon_pitch_ratio": pitch_ratio,
        "dragon_tempo": 1.0,
        "dragon_formant": "preserved",
        "greg_or_narrator_voice_replacement_count": 0,
        "take_role_patterns_verified": True,
        "settling_tail_seconds": tail_seconds,
        "candidate_duration_seconds": round(_probe_duration(output), 6),
        "candidate_byte_size": output.stat().st_size,
        "candidate_sha256": _sha256(output),
        "takes": receipts,
    }
    verification.parent.mkdir(parents=True, exist_ok=True)
    verification.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--performance", type=Path, default=Path("3l/performance/record-001.performance.md"))
    p.add_argument("--take-map", type=Path, default=Path("3l/audio/record-001-short-takes.json"))
    p.add_argument("--deep-map", type=Path, default=Path("3l/audio/record-001-two-voice-map.json"))
    p.add_argument("--fancy-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("3l/assets/audio/record-001-fancy-dragon-minus3_25.mp3"))
    p.add_argument("--verification", type=Path, default=Path("3l/audio/verification/record-001-fancy-dragon-minus3_25.json"))
    p.add_argument("--pitch-ratio", type=float, default=0.8288406503840438)
    p.add_argument("--pitch-semitones", type=float, default=-3.25)
    a = p.parse_args()
    print(json.dumps(build(
        performance=a.performance, take_map=a.take_map, deep_map=a.deep_map,
        fancy_dir=a.fancy_dir, output=a.output, verification=a.verification,
        pitch_ratio=a.pitch_ratio, pitch_semitones=a.pitch_semitones,
    ), indent=2))


if __name__ == "__main__":
    main()
