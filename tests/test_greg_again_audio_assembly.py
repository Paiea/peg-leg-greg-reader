from pathlib import Path
import wave
import pytest

from scripts.greg_again_audio_assembly import assemble_pcm_wav, inspect_wav


def write_silence(path: Path, *, frames: int, rate: int = 24000, channels: int = 1, width: int = 2) -> Path:
    with wave.open(str(path), "wb") as fh:
        fh.setnchannels(channels)
        fh.setsampwidth(width)
        fh.setframerate(rate)
        fh.writeframes(b"\x00" * frames * channels * width)
    return path


def test_inspect_wav_reports_pcm_shape(tmp_path):
    path = write_silence(tmp_path / "a.wav", frames=2400)
    info = inspect_wav(path)
    assert info == {"channels": 1, "sample_width": 2, "sample_rate": 24000, "frames": 2400}


def test_assemble_pcm_wav_preserves_block_order(tmp_path):
    a = write_silence(tmp_path / "a.wav", frames=2400, rate=24000)
    b = write_silence(tmp_path / "b.wav", frames=4800, rate=24000)
    duration = assemble_pcm_wav([a, b], tmp_path / "chapter.wav")
    assert duration == pytest.approx(0.3)
    with wave.open(str(tmp_path / "chapter.wav"), "rb") as fh:
        assert fh.getnframes() == 7200
        assert fh.getframerate() == 24000
        assert fh.getnchannels() == 1
        assert fh.getsampwidth() == 2


def test_assemble_pcm_wav_rejects_incompatible_sample_rate(tmp_path):
    a = write_silence(tmp_path / "a.wav", frames=2400, rate=24000)
    b = write_silence(tmp_path / "b.wav", frames=2400, rate=22050)
    with pytest.raises(ValueError, match="incompatible WAV"):
        assemble_pcm_wav([a, b], tmp_path / "chapter.wav")
