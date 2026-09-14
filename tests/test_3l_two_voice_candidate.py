import unittest
import json
import subprocess
import tempfile
from pathlib import Path


from scripts.build_3l_two_voice_candidate import (
    _concatenate_wav_files,
    build_timed_role_spans,
    map_transcript_role_spans,
    render_profiled_audio,
    slice_role_spans,
    validate_dragon_span_map,
)


class RecordTwoVoiceCandidateTests(unittest.TestCase):
    def test_maps_only_dragon_owned_words_inside_mixed_paragraph(self):
        performance = """# PERFORMANCE

NARRATOR / GREG

Then it says,

DRAGON

“Do you?”

NARRATOR / GREG

I wait.
"""
        transcript = "Then it says, “Do you?”\n\nI wait."

        spans = map_transcript_role_spans(performance, transcript)

        self.assertEqual(
            spans,
            [
                {"start": 0, "end": 14, "role": "greg", "text": "Then it says, "},
                {"start": 14, "end": 23, "role": "dragon", "text": "“Do you?”"},
                {"start": 25, "end": 32, "role": "greg", "text": "I wait."},
            ],
        )

    def test_renders_dragon_slower_without_retiming_greg(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "source.wav"
            output = Path(temporary_directory) / "candidate.wav"
            subprocess.run(
                [
                    "ffmpeg",
                    "-loglevel",
                    "error",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "sine=frequency=440:sample_rate=44100:duration=3",
                    str(source),
                ],
                check=True,
            )

            render_profiled_audio(
                source,
                output,
                [
                    {"start_seconds": 0.0, "end_seconds": 1.0, "role": "greg"},
                    {"start_seconds": 1.0, "end_seconds": 2.0, "role": "dragon"},
                    {"start_seconds": 2.0, "end_seconds": 3.0, "role": "greg"},
                ],
                dragon_tempo=0.88,
            )

            probe = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "json",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            duration = float(json.loads(probe.stdout)["format"]["duration"])
            self.assertGreater(duration, 3.11)
            self.assertLess(duration, 3.17)

    def test_snaps_role_changes_to_paragraph_silences(self):
        performance = """NARRATOR / GREG

Greg one.

DRAGON

Dragon two.

NARRATOR / GREG

Greg three.
"""
        transcript = "Greg one.\n\nDragon two.\n\nGreg three."
        role_spans = map_transcript_role_spans(performance, transcript)

        timed = build_timed_role_spans(
            transcript,
            role_spans,
            duration_seconds=4.0,
            silence_intervals=[(0.9, 1.1), (2.4, 2.6)],
        )

        self.assertEqual(
            timed,
            [
                {"start_seconds": 0.0, "end_seconds": 1.0, "role": "greg"},
                {"start_seconds": 1.0, "end_seconds": 2.5, "role": "dragon"},
                {"start_seconds": 2.5, "end_seconds": 4.0, "role": "greg"},
            ],
        )

    def test_rejects_dragon_span_that_contains_narrator_text(self):
        performance = """NARRATOR / GREG

Then it says,

DRAGON

“Do you?”
"""
        transcript = "Then it says, “Do you?”"
        spans = map_transcript_role_spans(performance, transcript)
        spans[0]["role"] = "dragon"

        with self.assertRaisesRegex(ValueError, "Greg/narrator text"):
            validate_dragon_span_map(performance, transcript, spans)

    def test_slices_global_role_map_to_one_take(self):
        spans = [
            {"start": 0, "end": 5, "role": "greg", "text": "Greg"},
            {"start": 7, "end": 13, "role": "dragon", "text": "Dragon"},
            {"start": 15, "end": 19, "role": "greg", "text": "Next"},
        ]

        sliced = slice_role_spans(spans, take_start=7, take_end=13)

        self.assertEqual(
            sliced,
            [{"start": 0, "end": 6, "role": "dragon", "text": "Dragon"}],
        )

    def test_keeps_multiple_mixed_paragraph_transitions_strictly_ordered(self):
        performance = """DRAGON

“To you,”

NARRATOR / GREG

it says.

DRAGON

“That is more useful.”
"""
        transcript = "“To you,” it says. “That is more useful.”"
        role_spans = map_transcript_role_spans(performance, transcript)

        timed = build_timed_role_spans(
            transcript,
            role_spans,
            duration_seconds=3.0,
            silence_intervals=[(1.0, 1.2)],
        )

        self.assertTrue(
            all(
                timed[index]["end_seconds"]
                <= timed[index + 1]["start_seconds"]
                for index in range(len(timed) - 1)
            )
        )
        self.assertTrue(
            all(span["end_seconds"] > span["start_seconds"] for span in timed)
        )

    def test_concatenates_same_format_wavs_with_different_lengths(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first = root / "first.wav"
            second = root / "second.wav"
            output = root / "combined.wav"
            for path, duration in ((first, 0.2), (second, 0.4)):
                subprocess.run(
                    [
                        "ffmpeg",
                        "-loglevel",
                        "error",
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        f"sine=frequency=440:sample_rate=24000:duration={duration}",
                        "-c:a",
                        "pcm_s16le",
                        str(path),
                    ],
                    check=True,
                )

            _concatenate_wav_files([first, second], output, tail_seconds=0.0)

            self.assertGreater(output.stat().st_size, first.stat().st_size)


if __name__ == "__main__":
    unittest.main()
