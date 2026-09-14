import unittest

from scripts.build_3l_short_dual_audio import (
    choose_role_segments,
    collapse_role_spans,
    expected_capture_keys,
    validate_verified_capture_receipt,
)


class ShortDualAudioTests(unittest.TestCase):
    def setUp(self):
        self.plan = {
            "record": "002",
            "chunks": [
                {"index": 1, "transcript": "Narration only.", "required_voices": ["deep"]},
                {"index": 2, "transcript": "Greg.Dragon.", "required_voices": ["deep", "normal"]},
            ],
        }

    def verified_receipt(self):
        return {
            "record": "002",
            "verified_capture_count": 3,
            "planned_capture_count": 3,
            "complete": True,
            "missing": [],
            "captures": [
                {"chunk": 1, "voice": "deep", "preview_url": "https://example.test/1.mp3", "sha256": "a" * 64, "status": "verified"},
                {"chunk": 2, "voice": "deep", "preview_url": "https://example.test/2d.mp3", "sha256": "b" * 64, "status": "verified"},
                {"chunk": 2, "voice": "normal", "preview_url": "https://example.test/2n.mp3", "sha256": "c" * 64, "status": "verified"},
            ],
        }

    def test_expected_capture_keys_follow_required_voices(self):
        self.assertEqual(expected_capture_keys(self.plan), [(1, "deep"), (2, "deep"), (2, "normal")])

    def test_verified_receipt_indexes_every_planned_capture(self):
        indexed = validate_verified_capture_receipt(self.plan, self.verified_receipt())
        self.assertEqual(sorted(indexed), [(1, "deep"), (2, "deep"), (2, "normal")])

    def test_verified_receipt_rejects_incomplete_source_set(self):
        receipt = self.verified_receipt()
        receipt["complete"] = False
        receipt["missing"] = [{"chunk": 2, "voice": "normal"}]
        receipt["captures"] = receipt["captures"][:-1]
        with self.assertRaisesRegex(ValueError, "verification receipt is incomplete"):
            validate_verified_capture_receipt(self.plan, receipt)

    def test_verified_receipt_rejects_duplicate_capture(self):
        receipt = self.verified_receipt()
        receipt["captures"].append(dict(receipt["captures"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate verified capture"):
            validate_verified_capture_receipt(self.plan, receipt)

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
        self.assertEqual(
            choose_role_segments(semantic, timed_by_voice),
            [
                {"role": "greg", "voice": "deep", "start_seconds": 0.0, "end_seconds": 1.2},
                {"role": "dragon", "voice": "normal", "start_seconds": 1.0, "end_seconds": 2.8},
            ],
        )

    def test_collapse_role_spans_keeps_only_true_speaker_transitions(self):
        transcript = "One.Two.Dragon.Greg."
        semantic = [
            {"start": 0, "end": 4, "role": "greg", "text": "One."},
            {"start": 4, "end": 8, "role": "greg", "text": "Two."},
            {"start": 8, "end": 15, "role": "dragon", "text": "Dragon."},
            {"start": 15, "end": 20, "role": "greg", "text": "Greg."},
        ]
        self.assertEqual(
            collapse_role_spans(transcript, semantic),
            [
                {"start": 0, "end": 8, "role": "greg", "text": "One.Two."},
                {"start": 8, "end": 15, "role": "dragon", "text": "Dragon."},
                {"start": 15, "end": 20, "role": "greg", "text": "Greg."},
            ],
        )


if __name__ == "__main__":
    unittest.main()
