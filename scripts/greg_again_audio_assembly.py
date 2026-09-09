from __future__ import annotations

from pathlib import Path
import wave


def inspect_wav(path: Path) -> dict[str, int]:
    with wave.open(str(path), "rb") as fh:
        if fh.getcomptype() != "NONE":
            raise ValueError(f"compressed WAV not supported: {path}")
        return {
            "channels": fh.getnchannels(),
            "sample_width": fh.getsampwidth(),
            "sample_rate": fh.getframerate(),
            "frames": fh.getnframes(),
        }


def assemble_pcm_wav(paths: list[Path], output_path: Path) -> float:
    if not paths:
        raise ValueError("at least one WAV take is required")
    reference = inspect_wav(paths[0])
    chunks: list[bytes] = []
    total_frames = 0
    for path in paths:
        info = inspect_wav(path)
        for key in ("channels", "sample_width", "sample_rate"):
            if info[key] != reference[key]:
                raise ValueError(f"incompatible WAV {path}: {key} differs")
        with wave.open(str(path), "rb") as fh:
            chunks.append(fh.readframes(fh.getnframes()))
        total_frames += info["frames"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as out:
        out.setnchannels(reference["channels"])
        out.setsampwidth(reference["sample_width"])
        out.setframerate(reference["sample_rate"])
        for chunk in chunks:
            out.writeframes(chunk)
    return total_frames / reference["sample_rate"]
