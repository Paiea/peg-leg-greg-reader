#!/usr/bin/env python3
"""Assemble Record 001 with existing Deep Greg and a Fancy Dragon master."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from scripts.build_3l_two_voice_candidate import (
    _concatenate_wav_files,
    _detect_silences,
    _ordered_silence_choices,
    _probe_duration,
    _sha256,
    build_timed_role_spans,
    map_transcript_role_spans,
    slice_role_spans,
    validate_dragon_span_map,
)


def _spoken_count(text: str) -> int:
    return sum(not char.isspace() for char in text)


def choose_take_boundaries(
    takes: list[dict], *, duration_seconds: float, silence_intervals: list[tuple[float, float]]
) -> list[float]:
    """Map the 36 source-take boundaries onto a second full-length performance."""
    spoken_counts = [_spoken_count(take["source_transcript"]) for take in takes]
    total = sum(spoken_counts)
    if total <= 0:
        raise ValueError("take transcripts contain no spoken text")

    cumulative = 0
    targets: list[float] = []
    for count in spoken_counts[:-1]:
        cumulative += count
        targets.append(duration_seconds * cumulative / total)

    candidates = sorted(
        (start + end) / 2
        for start, end in silence_intervals
        if 0.0 < (start + end) / 2 < duration_seconds
    )
    choices = _ordered_silence_choices(targets, candidates)
    if len(choices) != len(targets):
        raise ValueError("could not resolve every Fancy take boundary")
    boundaries = [0.0, *choices, duration_seconds]
    if any(right <= left for left, right in zip(boundaries, boundaries[1:])):
        raise ValueError("Fancy take boundaries are not strictly increasing")
    return boundaries


def _render_piece(
    source: Path,
    output: Path,
    *,
    start: float,
    end: float,
    pitch_ratio: float | None = None,
) -> None:
    if end <= start:
        raise ValueError("audio piece must have positive duration")
    filters = [
        f"atrim=start={start:.6f}:end={end:.6f}",
        "asetpts=PTS-STARTPTS",
    ]
    if pitch_ratio is not None:
        filters.append(
            f"rubberband=pitch={pitch_ratio:.12f}:tempo=1:formant=preserved:pitchq=quality"
        )
    filters.extend(["aresample=24000", "aformat=sample_fmts=s16:channel_layouts=mono"])
    subprocess.run(
        [
            "ffmpeg",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-af",
            ",".join(filters),
            "-ac",
            "1",
            "-ar",
            "24000",
            "-c:a",
            "pcm_s16le",
            str(output),
        ],
        check=True,
    )


def build_candidate(
    *,
    performance_path: Path,
    take_map_path: Path,
    deep_map_path: Path,
    fancy_master_path: Path,
    output_path: Path,
    verification_path: Path,
    pitch_ratio: float,
    pitch_semitones: float,
    tail_seconds: float = 2.0,
) -> dict:
    performance_text = performance_path.read_text(encoding="utf-8")
    take_map = json.loads(take_map_path.read_text(encoding="utf-8"))
    deep_map = json.loads(deep_map_path.read_text(encoding="utf-8"))
    takes = take_map["takes"]
    deep_takes = deep_map["takes"]
    if len(takes) != len(deep_takes):
        raise ValueError("source take map and Deep timing map disagree on take count")

    full_transcript = "\n\n".join(take["source_transcript"] for take in takes)
    global_roles = map_transcript_role_spans(performance_text, full_transcript)
    dragon_samples = validate_dragon_span_map(performance_text, full_transcript, global_roles)

    fancy_duration = _probe_duration(fancy_master_path)
    fancy_silences = _detect_silences(fancy_master_path)
    take_boundaries = choose_take_boundaries(
        takes,
        duration_seconds=fancy_duration,
        silence_intervals=fancy_silences,
    )

    rendered_pieces: list[Path] = []
    take_receipts: list[dict] = []
    transcript_offset = 0
    fancy_dragon_count = 0
    deep_dragon_count = 0

    with tempfile.TemporaryDirectory(prefix="3l-fancy-dragon-") as temporary:
        temp = Path(temporary)
        for index, (take, deep_take) in enumerate(zip(takes, deep_takes), start=1):
            transcript = take["source_transcript"]
            take_start = transcript_offset
            take_end = take_start + len(transcript)
            local_roles = slice_role_spans(global_roles, take_start=take_start, take_end=take_end)

            fancy_take = temp / f"fancy-take-{index:02d}.wav"
            _render_piece(
                fancy_master_path,
                fancy_take,
                start=take_boundaries[index - 1],
                end=take_boundaries[index],
            )
            local_fancy_timing = build_timed_role_spans(
                transcript,
                local_roles,
                duration_seconds=_probe_duration(fancy_take),
                silence_intervals=_detect_silences(fancy_take),
            )
            deep_timing = deep_take["mapped_spans"]
            deep_roles = [span["role"] for span in deep_timing]
            fancy_roles = [span["role"] for span in local_fancy_timing]
            if deep_roles != fancy_roles:
                raise ValueError(
                    f"take {index:02d} role pattern mismatch: Deep {deep_roles} vs Fancy {fancy_roles}"
                )

            deep_source = Path(deep_take["source"])
            for span_index, (deep_span, fancy_span) in enumerate(
                zip(deep_timing, local_fancy_timing), start=1
            ):
                role = deep_span["role"]
                piece = temp / f"piece-{index:02d}-{span_index:02d}-{role}.wav"
                if role == "greg":
                    _render_piece(
                        deep_source,
                        piece,
                        start=float(deep_span["start_seconds"]),
                        end=float(deep_span["end_seconds"]),
                    )
                elif role == "dragon":
                    deep_dragon_count += 1
                    fancy_dragon_count += 1
                    _render_piece(
                        fancy_take,
                        piece,
                        start=float(fancy_span["start_seconds"]),
                        end=float(fancy_span["end_seconds"]),
                        pitch_ratio=pitch_ratio,
                    )
                else:
                    raise ValueError(f"unexpected role {role!r}")
                rendered_pieces.append(piece)

            take_receipts.append(
                {
                    "order": index,
                    "deep_role_pattern": deep_roles,
                    "fancy_take_start_seconds": round(take_boundaries[index - 1], 6),
                    "fancy_take_end_seconds": round(take_boundaries[index], 6),
                    "dragon_span_count": sum(role == "dragon" for role in deep_roles),
                }
            )
            transcript_offset = take_end + 2

        if deep_dragon_count != len(dragon_samples):
            raise ValueError(
                f"Deep Dragon span count {deep_dragon_count} != semantic map {len(dragon_samples)}"
            )
        if fancy_dragon_count != deep_dragon_count:
            raise ValueError("Fancy and Deep Dragon span counts differ")

        assembled_wav = temp / "record-001-fancy-dragon.wav"
        _concatenate_wav_files(rendered_pieces, assembled_wav, tail_seconds=tail_seconds)
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(assembled_wav),
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                str(output_path),
            ],
            check=True,
        )

    output_duration = _probe_duration(output_path)
    receipt = {
        "record": 1,
        "status": "verified_unlistened_fancy_dragon_candidate",
        "assembly_mode": "existing_deep_greg_plus_full_fancy_master_semantic_swap",
        "source_take_count": len(takes),
        "dragon_span_count": deep_dragon_count,
        "greg_source": "existing Record 001 Deep short takes",
        "dragon_source": "Fancy full-scene master",
        "dragon_pitch_semitones": pitch_semitones,
        "dragon_pitch_ratio": pitch_ratio,
        "dragon_tempo": 1.0,
        "dragon_formant": "preserved",
        "settling_tail_seconds": tail_seconds,
        "fancy_master_duration_seconds": round(fancy_duration, 6),
        "candidate_duration_seconds": round(output_duration, 6),
        "candidate_byte_size": output_path.stat().st_size,
        "candidate_sha256": _sha256(output_path),
        "ffprobe_playable": output_duration > tail_seconds,
        "take_role_patterns_verified": True,
        "greg_or_narrator_voice_replacement_count": 0,
        "takes": take_receipts,
    }
    verification_path.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--performance", type=Path, default=Path("3l/performance/record-001.performance.md")
    )
    parser.add_argument(
        "--take-map", type=Path, default=Path("3l/audio/record-001-short-takes.json")
    )
    parser.add_argument(
        "--deep-map", type=Path, default=Path("3l/audio/record-001-two-voice-map.json")
    )
    parser.add_argument("--fancy-master", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("3l/assets/audio/record-001-fancy-dragon-minus3_25.mp3"),
    )
    parser.add_argument(
        "--verification",
        type=Path,
        default=Path("3l/audio/verification/record-001-fancy-dragon-minus3_25.json"),
    )
    parser.add_argument("--pitch-ratio", type=float, default=0.8288406503840438)
    parser.add_argument("--pitch-semitones", type=float, default=-3.25)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.verification.parent.mkdir(parents=True, exist_ok=True)
    receipt = build_candidate(
        performance_path=args.performance,
        take_map_path=args.take_map,
        deep_map_path=args.deep_map,
        fancy_master_path=args.fancy_master,
        output_path=args.output,
        verification_path=args.verification,
        pitch_ratio=args.pitch_ratio,
        pitch_semitones=args.pitch_semitones,
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
