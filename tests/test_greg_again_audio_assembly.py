import tempfile
import unittest
import wave
from pathlib import Path

from scripts.greg_again_audio_assembly import assemble_pcm_wav, inspect_wav


def write_silence(path: Path, *, frames: int, rate: int = 24000, channels: int = 1, width: int = 2) -> Path:
    with wave.open(str(path), "wb") as fh:
        fh.setnchannels(channels)
        fh.setsampwidth(width)
        fh.setframerate(rate)
        fh.writeframes(b"\x00" * frames * channels * width)
    return path


class GregAgainAudioAssemblyTests(unittest.TestCase):
    def test_inspect_wav_reports_pcm_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_silence(Path(tmp) / "a.wav", frames=2400)
            info = inspect_wav(path)
            self.assertEqual({"channels": 1, "sample_width": 2, "sample_rate": 24000, "frames": 2400}, info)

    def test_assemble_pcm_wav_preserves_block_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = write_silence(root / "a.wav", frames=2400, rate=24000)
            b = write_silence(root / "b.wav", frames=4800, rate=24000)
            duration = assemble_pcm_wav([a, b], root / "chapter.wav")
            self.assertAlmostEqual(0.3, duration)
            with wave.open(str(root / "chapter.wav"), "rb") as fh:
                self.assertEqual(7200, fh.getnframes())
                self.assertEqual(24000, fh.getframerate())
                self.assertEqual(1, fh.getnchannels())
                self.assertEqual(2, fh.getsampwidth())

    def test_assemble_pcm_wav_rejects_incompatible_sample_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = write_silence(root / "a.wav", frames=2400, rate=24000)
            b = write_silence(root / "b.wav", frames=2400, rate=22050)
            with self.assertRaisesRegex(ValueError, "incompatible WAV"):
                assemble_pcm_wav([a, b], root / "chapter.wav")


if __name__ == "__main__":
    unittest.main()
