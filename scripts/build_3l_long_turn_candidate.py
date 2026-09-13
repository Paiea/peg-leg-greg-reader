#!/usr/bin/env python3
"""Assemble the speaker-pure long-turn Record 001 audio experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def duration(path: Path) -> float:
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(p.stdout.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=Path("3l/audio/experiments/record-001-long-turn-v3-captures.json"))
    ap.add_argument("--capture-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=Path("3l/assets/audio/record-001-long-turn-v3.mp3"))
    ap.add_argument("--receipt", type=Path, default=Path("3l/audio/verification/record-001-long-turn-v3.json"))
    a = ap.parse_args()

    manifest = json.loads(a.manifest.read_text(encoding="utf-8"))
    clips = manifest["clips"]
    contract = manifest["voice_contract"]
    assert len(clips) == 36, len(clips)
    assert len({row[1] for row in clips if row[2] == "dragon"}) == 12
    assert contract["dragon_pitch_semitones"] == -3.25
    assert contract["dragon_tempo"] == 1.0
    assert contract["mixed_speaker_splicing"] is False

    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.receipt.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="3l-long-turn-") as td:
        temp = Path(td)
        concat_entries: list[Path] = []
        rendered = []

        for index, row in enumerate(clips, start=1):
            clip_id, block, role, pause_ms, _url = row
            source = a.capture_dir / f"{clip_id}.mp3"
            if not source.exists():
                raise FileNotFoundError(source)

            wav = temp / f"{index:03d}-{clip_id}.wav"
            filters = []
            if role == "dragon":
                filters.append(
                    f"rubberband=pitch={contract['dragon_pitch_ratio']}:tempo=1:formant=preserved:pitchq=quality"
                )
            filters.extend(["aresample=24000", "aformat=sample_fmts=s16:channel_layouts=mono"])
            run("ffmpeg", "-loglevel", "error", "-y", "-i", str(source), "-af", ",".join(filters),
                "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(wav))
            concat_entries.append(wav)

            silence = temp / f"{index:03d}-{clip_id}-pause.wav"
            run("ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi",
                "-i", "anullsrc=r=24000:cl=mono", "-t", f"{pause_ms / 1000:.3f}",
                "-c:a", "pcm_s16le", str(silence))
            concat_entries.append(silence)

            rendered.append({
                "id": clip_id,
                "block": block,
                "role": role,
                "pause_after_ms": pause_ms,
                "source_duration_seconds": round(duration(source), 6),
                "rendered_duration_seconds": round(duration(wav), 6),
                "source_sha256": sha256(source),
            })

        concat_file = temp / "concat.txt"
        concat_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in concat_entries), encoding="utf-8")
        assembled = temp / "assembled.wav"
        run("ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-c:a", "pcm_s16le", str(assembled))
        run("ffmpeg", "-loglevel", "error", "-y", "-i", str(assembled),
            "-c:a", "libmp3lame", "-b:a", "192k", str(a.output))

    receipt = {
        "record": 1,
        "experiment": "long-turn-dragon-v3",
        "status": "verified_unlistened",
        "assembly_mode": "speaker_pure_clips_plus_explicit_pause_metadata",
        "clip_count": len(clips),
        "dramatic_block_count": len({row[1] for row in clips}),
        "dragon_turn_count": len({row[1] for row in clips if row[2] == "dragon"}),
        "dragon_clip_count": sum(row[2] == "dragon" for row in clips),
        "greg_clip_count": sum(row[2] == "greg" for row in clips),
        "mixed_speaker_clip_count": 0,
        "dragon_voice": contract["dragon_voice"],
        "dragon_pitch_semitones": contract["dragon_pitch_semitones"],
        "dragon_tempo": contract["dragon_tempo"],
        "dragon_formant": contract["dragon_formant"],
        "candidate_duration_seconds": round(duration(a.output), 6),
        "candidate_byte_size": a.output.stat().st_size,
        "candidate_sha256": sha256(a.output),
        "clips": rendered,
    }
    a.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in (
        "clip_count", "dramatic_block_count", "dragon_turn_count", "dragon_clip_count",
        "candidate_duration_seconds", "candidate_byte_size", "candidate_sha256"
    )}, indent=2))


if __name__ == "__main__":
    main()
