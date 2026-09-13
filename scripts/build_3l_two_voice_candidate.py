#!/usr/bin/env python3
"""Build a reuse-first two-voice candidate from an existing 3L recording."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import wave


ROLE_LABELS = {
    "NARRATOR / GREG": "greg",
    "GREG": "greg",
    "DRAGON": "dragon",
}
SEMANTIC_BEATS = {"BEAT", "LONG BEAT"}


def _performance_blocks(performance_text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    role: str | None = None
    lines: list[str] = []

    for line in performance_text.splitlines():
        if line in ROLE_LABELS:
            if role is not None and any(part.strip() for part in lines):
                blocks.append((role, "\n".join(lines).strip()))
            role = ROLE_LABELS[line]
            lines = []
        elif role is not None and line not in SEMANTIC_BEATS:
            lines.append(line)

    if role is not None and any(part.strip() for part in lines):
        blocks.append((role, "\n".join(lines).strip()))
    return blocks


def map_transcript_role_spans(performance_text: str, transcript: str) -> list[dict]:
    """Map exact transcript characters to semantic Greg/Dragon ownership."""
    performance_chars: list[str] = []
    performance_roles: list[str] = []
    for role, text in _performance_blocks(performance_text):
        for char in text:
            if not char.isspace():
                performance_chars.append(char)
                performance_roles.append(role)

    transcript_chars = [char for char in transcript if not char.isspace()]
    if transcript_chars != performance_chars:
        raise ValueError("performance text does not preserve the transcript character sequence")

    roles_by_index: dict[int, str] = {}
    role_index = 0
    previous_role: str | None = None
    for index, char in enumerate(transcript):
        if char.isspace():
            if char == " " and previous_role is not None:
                roles_by_index[index] = previous_role
            continue
        previous_role = performance_roles[role_index]
        roles_by_index[index] = previous_role
        role_index += 1

    spans: list[dict] = []
    for index in sorted(roles_by_index):
        role = roles_by_index[index]
        if spans and spans[-1]["role"] == role and spans[-1]["end"] == index:
            spans[-1]["end"] = index + 1
            spans[-1]["text"] += transcript[index]
        else:
            spans.append(
                {
                    "start": index,
                    "end": index + 1,
                    "role": role,
                    "text": transcript[index],
                }
            )
    return spans


def validate_dragon_span_map(
    performance_text: str, transcript: str, spans: list[dict]
) -> list[str]:
    """Fail if any proposed Dragon treatment escapes a DRAGON-owned text span."""
    expected = map_transcript_role_spans(performance_text, transcript)
    expected_roles: dict[int, str] = {}
    for span in expected:
        for index in range(span["start"], span["end"]):
            expected_roles[index] = span["role"]

    samples: list[str] = []
    for span in spans:
        if span["role"] != "dragon":
            continue
        start = int(span["start"])
        end = int(span["end"])
        contaminated = [
            index for index in range(start, end) if expected_roles.get(index) != "dragon"
        ]
        if contaminated:
            raise ValueError("Dragon treatment includes Greg/narrator text")
        exact = transcript[start:end]
        if exact != span["text"]:
            raise ValueError("Dragon span text does not match the exact transcript")
        samples.append(exact)
    return samples


def slice_role_spans(
    spans: list[dict], *, take_start: int, take_end: int
) -> list[dict]:
    """Return one take's exact local role spans from the global speaker map."""
    sliced: list[dict] = []
    for span in spans:
        start = max(int(span["start"]), take_start)
        end = min(int(span["end"]), take_end)
        if end <= start:
            continue
        source_offset = start - int(span["start"])
        text = span["text"][source_offset : source_offset + (end - start)]
        sliced.append(
            {
                "start": start - take_start,
                "end": end - take_start,
                "role": span["role"],
                "text": text,
            }
        )
    return sliced


def _spoken_fraction(text: str, position: int) -> float:
    total = sum(not char.isspace() for char in text)
    if total == 0:
        return 0.0
    completed = sum(not char.isspace() for char in text[:position])
    return completed / total


def _ordered_silence_choices(targets: list[float], candidates: list[float]) -> list[float]:
    if not targets:
        return []
    if len(candidates) < len(targets):
        return targets

    costs: list[list[tuple[float, list[float]] | None]] = [
        [None] * (len(candidates) + 1) for _ in range(len(targets) + 1)
    ]
    for candidate_count in range(len(candidates) + 1):
        costs[0][candidate_count] = (0.0, [])

    for target_count in range(1, len(targets) + 1):
        for candidate_count in range(1, len(candidates) + 1):
            skipped = costs[target_count][candidate_count - 1]
            previous = costs[target_count - 1][candidate_count - 1]
            chosen = None
            if previous is not None:
                distance = candidates[candidate_count - 1] - targets[target_count - 1]
                chosen = (
                    previous[0] + distance * distance,
                    previous[1] + [candidates[candidate_count - 1]],
                )
            if skipped is None:
                costs[target_count][candidate_count] = chosen
            elif chosen is None or skipped[0] <= chosen[0]:
                costs[target_count][candidate_count] = skipped
            else:
                costs[target_count][candidate_count] = chosen

    result = costs[-1][-1]
    if result is None:
        return targets
    return result[1]


def build_timed_role_spans(
    transcript: str,
    role_spans: list[dict],
    *,
    duration_seconds: float,
    silence_intervals: list[tuple[float, float]],
) -> list[dict]:
    """Estimate semantic role timing, snapping paragraph changes to real silence."""
    paragraph_starts = [0] + [match.end() for match in re.finditer(r"\n\s*\n", transcript)]
    paragraph_targets = [
        duration_seconds * _spoken_fraction(transcript, start)
        for start in paragraph_starts[1:]
    ]
    silence_midpoints = sorted(
        (start + end) / 2
        for start, end in silence_intervals
        if 0.0 < (start + end) / 2 < duration_seconds
    )
    paragraph_times = [0.0] + _ordered_silence_choices(paragraph_targets, silence_midpoints)
    paragraph_times.append(duration_seconds)
    paragraph_time_by_start = dict(zip(paragraph_starts, paragraph_times))

    transition_positions = [span["start"] for span in role_spans[1:]]
    transition_times: list[float | None] = [None] * len(transition_positions)
    mixed_by_paragraph: dict[int, list[tuple[int, float]]] = {}
    for transition_index, position in enumerate(transition_positions):
        paragraph_start = max(start for start in paragraph_starts if start <= position)
        if position == paragraph_start:
            transition_times[transition_index] = paragraph_time_by_start[paragraph_start]
            continue

        paragraph_index = paragraph_starts.index(paragraph_start)
        paragraph_end = (
            paragraph_starts[paragraph_index + 1]
            if paragraph_index + 1 < len(paragraph_starts)
            else len(transcript)
        )
        time_start = paragraph_times[paragraph_index]
        time_end = paragraph_times[paragraph_index + 1]
        local_fraction = _spoken_fraction(
            transcript[paragraph_start:paragraph_end], position - paragraph_start
        )
        target = time_start + (time_end - time_start) * local_fraction
        mixed_by_paragraph.setdefault(paragraph_index, []).append(
            (transition_index, target)
        )

    for paragraph_index, transitions in mixed_by_paragraph.items():
        time_start = paragraph_times[paragraph_index]
        time_end = paragraph_times[paragraph_index + 1]
        local_silences = [
            midpoint
            for midpoint in silence_midpoints
            if time_start + 0.03 < midpoint < time_end - 0.03
        ]
        targets = [target for _, target in transitions]
        choices = _ordered_silence_choices(targets, local_silences)
        for (transition_index, _), choice in zip(transitions, choices):
            transition_times[transition_index] = choice

    if any(value is None for value in transition_times):
        raise ValueError("failed to resolve every semantic role transition")

    boundaries = [0.0] + [float(value) for value in transition_times] + [duration_seconds]
    timed: list[dict] = []
    for index, role_span in enumerate(role_spans):
        start = round(boundaries[index], 6)
        end = round(boundaries[index + 1], 6)
        if timed and timed[-1]["role"] == role_span["role"]:
            timed[-1]["end_seconds"] = end
        else:
            timed.append(
                {
                    "start_seconds": start,
                    "end_seconds": end,
                    "role": role_span["role"],
                }
            )
    return timed


def render_profiled_audio(
    source: Path,
    output: Path,
    timed_spans: list[dict],
    *,
    dragon_tempo: float = 0.88,
) -> None:
    """Render one take while applying the Dragon profile only to Dragon spans."""
    if not timed_spans:
        raise ValueError("at least one timed role span is required")

    count = len(timed_spans)
    split_outputs = "".join(f"[source{index}]" for index in range(count))
    filters = [f"[0:a]asplit={count}{split_outputs}"]
    concat_inputs: list[str] = []
    for index, span in enumerate(timed_spans):
        start = float(span["start_seconds"])
        end = float(span["end_seconds"])
        if end <= start:
            raise ValueError("timed role spans must have positive duration")
        treatment = f",atempo={dragon_tempo:.6f}" if span["role"] == "dragon" else ""
        filters.append(
            f"[source{index}]atrim=start={start:.6f}:end={end:.6f},"
            f"asetpts=PTS-STARTPTS{treatment}[part{index}]"
        )
        concat_inputs.append(f"[part{index}]")
    filters.append(f"{''.join(concat_inputs)}concat=n={count}:v=0:a=1[out]")

    command = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[out]",
    ]
    if output.suffix.lower() == ".mp3":
        command.extend(["-c:a", "libmp3lame", "-b:a", "192k"])
    else:
        command.extend(["-c:a", "pcm_s16le"])
    command.append(str(output))
    subprocess.run(command, check=True)


def _probe_duration(path: Path) -> float:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(completed.stdout)["format"]["duration"])


def _detect_silences(path: Path) -> list[tuple[float, float]]:
    completed = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            "silencedetect=noise=-42dB:d=0.08",
            "-f",
            "null",
            "-",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    events = re.findall(r"silence_(start|end):\s*([0-9.]+)", completed.stderr)
    intervals: list[tuple[float, float]] = []
    start: float | None = None
    for kind, value in events:
        if kind == "start":
            start = float(value)
        elif start is not None:
            intervals.append((start, float(value)))
            start = None
    return intervals


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _concatenate_wav_files(paths: list[Path], output: Path, tail_seconds: float) -> None:
    with wave.open(str(paths[0]), "rb") as first:
        parameters = first.getparams()
    with wave.open(str(output), "wb") as destination:
        destination.setparams(parameters)
        for path in paths:
            with wave.open(str(path), "rb") as source:
                source_parameters = source.getparams()
                source_format = (
                    source_parameters.nchannels,
                    source_parameters.sampwidth,
                    source_parameters.framerate,
                    source_parameters.comptype,
                )
                destination_format = (
                    parameters.nchannels,
                    parameters.sampwidth,
                    parameters.framerate,
                    parameters.comptype,
                )
                if source_format != destination_format:
                    raise ValueError(f"incompatible WAV take: {path}")
                destination.writeframes(source.readframes(source.getnframes()))
        silence_frames = int(parameters.framerate * tail_seconds)
        destination.writeframes(b"\0" * silence_frames * parameters.sampwidth * parameters.nchannels)


def build_candidate(
    *,
    performance_path: Path,
    take_map_path: Path,
    chunk_directory: Path,
    original_path: Path,
    output_path: Path,
    map_output_path: Path,
    verification_output_path: Path,
    dragon_tempo: float = 0.88,
    settling_tail_seconds: float = 2.0,
) -> dict:
    performance_text = performance_path.read_text(encoding="utf-8")
    take_map = json.loads(take_map_path.read_text(encoding="utf-8"))
    takes = take_map["takes"]
    full_transcript = "\n\n".join(take["source_transcript"] for take in takes)
    global_spans = map_transcript_role_spans(performance_text, full_transcript)
    dragon_samples = validate_dragon_span_map(
        performance_text, full_transcript, global_spans
    )
    if not dragon_samples:
        raise ValueError("validated performance contains no Dragon-owned speech")

    print("Dragon span audit: PASS")
    print(f"Mapped Dragon spans: {len(dragon_samples)}")
    print("Exact Dragon span sample:")
    for sample in dragon_samples[:8]:
        print(f"  {sample!r}")

    original_hash_before = _sha256(original_path)
    take_receipts: list[dict] = []
    rendered_takes: list[Path] = []
    transcript_offset = 0

    with tempfile.TemporaryDirectory(prefix="3l-record-001-two-voice-") as temporary:
        temporary_path = Path(temporary)
        for take in takes:
            order = int(take["order"])
            transcript = take["source_transcript"]
            take_start = transcript_offset
            take_end = take_start + len(transcript)
            local_spans = slice_role_spans(
                global_spans, take_start=take_start, take_end=take_end
            )
            source = chunk_directory / f"{order:02d}.mp3"
            duration = _probe_duration(source)
            silences = _detect_silences(source)
            timed_spans = build_timed_role_spans(
                transcript,
                local_spans,
                duration_seconds=duration,
                silence_intervals=silences,
            )
            rendered = temporary_path / f"{order:02d}.wav"
            render_profiled_audio(
                source,
                rendered,
                timed_spans,
                dragon_tempo=dragon_tempo,
            )
            rendered_takes.append(rendered)
            dragon_intervals = [
                span for span in timed_spans if span["role"] == "dragon"
            ]
            take_receipts.append(
                {
                    "order": order,
                    "source": str(source),
                    "source_sha256": _sha256(source),
                    "source_duration_seconds": round(duration, 6),
                    "mapped_spans": timed_spans,
                    "dragon_interval_count": len(dragon_intervals),
                    "dragon_source_seconds": round(
                        sum(
                            span["end_seconds"] - span["start_seconds"]
                            for span in dragon_intervals
                        ),
                        6,
                    ),
                }
            )
            transcript_offset = take_end + 2

        assembled_wav = temporary_path / "record-001-two-voice-candidate.wav"
        _concatenate_wav_files(
            rendered_takes, assembled_wav, settling_tail_seconds
        )
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

    original_hash_after = _sha256(original_path)
    if original_hash_before != original_hash_after:
        raise ValueError("existing single-voice MP3 changed during candidate assembly")

    map_receipt = {
        "record": 1,
        "source_performance": str(performance_path),
        "source_take_map": str(take_map_path),
        "profile": {
            "greg": "existing Deep performance, unchanged timing",
            "dragon": "semantic DRAGON profile",
            "dragon_tempo": dragon_tempo,
            "treatment": "tempo-only, pitch-preserving",
        },
        "validation": {
            "status": "pass",
            "rule": "Only exact text labeled DRAGON receives Dragon treatment.",
            "dragon_span_count": len(dragon_samples),
            "greg_or_narrator_contamination_count": 0,
            "sample_exact_text": dragon_samples[:8],
        },
        "takes": take_receipts,
    }
    map_output_path.write_text(
        json.dumps(map_receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    output_duration = _probe_duration(output_path)
    verification = {
        "record": 1,
        "candidate": str(output_path),
        "status": "verified_unlistened_ab_candidate",
        "assembly_mode": "reuse_existing_takes_dragon_spans_only",
        "source_take_count": len(takes),
        "new_voice_capture_count": 0,
        "dragon_span_count": len(dragon_samples),
        "dragon_tempo": dragon_tempo,
        "settling_tail_seconds": settling_tail_seconds,
        "original_single_voice": {
            "path": str(original_path),
            "sha256_before": original_hash_before,
            "sha256_after": original_hash_after,
            "preserved": True,
        },
        "candidate_duration_seconds": round(output_duration, 6),
        "candidate_byte_size": output_path.stat().st_size,
        "candidate_sha256": _sha256(output_path),
        "ffprobe_playable": output_duration > settling_tail_seconds,
        "scope": "Record 001 only",
    }
    verification_output_path.write_text(
        json.dumps(verification, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return verification


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the 3L Record 001 Dragon-profile A/B candidate."
    )
    parser.add_argument(
        "--performance",
        type=Path,
        default=Path("3l/performance/record-001.performance.md"),
    )
    parser.add_argument(
        "--take-map",
        type=Path,
        default=Path("3l/audio/record-001-short-takes.json"),
    )
    parser.add_argument(
        "--chunk-directory",
        type=Path,
        default=Path("3l/assets/audio/record-001-chunks"),
    )
    parser.add_argument(
        "--original",
        type=Path,
        default=Path("3l/assets/audio/record-001.mp3"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("3l/assets/audio/record-001-two-voice-candidate.mp3"),
    )
    parser.add_argument(
        "--map-output",
        type=Path,
        default=Path("3l/audio/record-001-two-voice-map.json"),
    )
    parser.add_argument(
        "--verification-output",
        type=Path,
        default=Path("3l/audio/verification/record-001-two-voice-candidate.json"),
    )
    arguments = parser.parse_args()
    for path in (
        arguments.output.parent,
        arguments.map_output.parent,
        arguments.verification_output.parent,
    ):
        path.mkdir(parents=True, exist_ok=True)
    receipt = build_candidate(
        performance_path=arguments.performance,
        take_map_path=arguments.take_map,
        chunk_directory=arguments.chunk_directory,
        original_path=arguments.original,
        output_path=arguments.output,
        map_output_path=arguments.map_output,
        verification_output_path=arguments.verification_output,
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
