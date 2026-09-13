import unittest

from scripts.build_3l_short_dual_audio import (
    expected_capture_keys,
    validate_capture_manifest,
    choose_role_segments,
)


class ShortDualAudioTests(unittest.TestCase):
    def setUp(self):
        self.plan = {
            "record": "002",
            "chunks": [
                {
                    "index": 1,
                    "transcript": "Narration only.",
                    "required_voices": ["deep"],
                    "semantic_spans": [
                        {"start": 0, "end": 15, "role": "greg", "text": "Narration only."}
                    ],
                },
                {
                    "index": 2,
                    "transcript": "Greg.\n\nDragon.",
                    "required_voices": ["deep", "normal"],
                    "semantic_spans": [
                        {"start": 0, "end": 5, "role": "greg", "text": "Greg."},
                        {"start": 7, "end": 14, "role": "dragon", "text": "Dragon."},
                    ],
                },
            ],
        }

    def test_expected_capture_keys_follow_required_voices(self):
        self.assertEqual(
            expected_capture_keys(self.plan),
            [(1, "deep"), (2, "deep"), (2, "normal")],
        )

    def test_manifest_must_cover_every_required_capture_exactly(self):
        manifest = {
            "record": "002",
            "captures": [
                {"chunk": 1, "voice": "deep", "transcript": "Narration only.", "preview_url": "https://example.test/1.mp3"},
                {"chunk": 2, "voice": "deep", "transcript": "Greg.\n\nDragon.", "preview_url": "https://example.test/2d.mp3"},
                {"chunk": 2, "voice": "normal", "transcript": "Greg.\n\nDragon.", "preview_url": "https://example.test/2n.mp3"},
            ],
        }
        indexed = validate_capture_manifest(self.plan, manifest)
        self.assertEqual(sorted(indexed), [(1, "deep"), (2, "deep"), (2, "normal")])

    def test_manifest_rejects_transcript_mismatch(self):
        manifest = {
            "record": "002",
            "captures": [
                {"chunk": 1, "voice": "deep", "transcript": "WRONG", "preview_url": "https://example.test/1.mp3"},
                {"chunk": 2, "voice": "deep", "transcript": "Greg.\n\nDragon.", "preview_url": "https://example.test/2d.mp3"},
                {"chunk": 2, "voice": "normal", "transcript": "Greg.\n\nDragon.", "preview_url": "https://example.test/2n.mp3"},
            ],
        }
        with self.assertRaisesRegex(ValueError, "transcript mismatch"):
            validate_capture_manifest(self.plan, manifest)

    def test_choose_role_segments_uses_role_specific_source_timing(self):
        semantic = [
            {"role": "greg", "text": "Greg."},
            {"role": "dragon", "text": "Dragon."},
        ]
        timed_by_voice = {
            "deep": [
                {"role": "greg", "start_seconds": 0.0, "end_seconds": 1.2},
                {"role": "dragon", "start_seconds": 1.2, "end_seconds": 2.5},
            ],
            "normal": [
                {"role": "greg", "start_seconds": 0.0, "end_seconds": 1.0},
                {"role": "dragon", "start_seconds": 1.0, "end_seconds": 2.8},
            ],
        }
        chosen = choose_role_segments(semantic, timed_by_voice)
        self.assertEqual(
            chosen,
            [
                {"role": "greg", "voice": "deep", "start_seconds": 0.0, "end_seconds": 1.2},
                {"role": "dragon", "voice": "normal", "start_seconds": 1.0, "end_seconds": 2.8},
            ],
        )


if __name__ == "__main__":
    unittest.main()
