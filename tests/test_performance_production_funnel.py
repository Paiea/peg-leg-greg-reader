import unittest

from scripts import performance_production_funnel as funnel


class PerformanceProductionFunnelTests(unittest.TestCase):
    def test_next_visible_chapters_skip_hidden_canon(self):
        manifest = {
            "default": "visible",
            "chapters": {
                "3": {"showcase": False},
                "6": {"showcase": False},
                "8": {"showcase": False},
                "12": {"showcase": False},
                "20": {"showcase": False},
                "21": {"showcase": False},
                "33": {"showcase": False},
                "38": {"showcase": False},
                "43": {"showcase": False},
                "46": {"showcase": False},
                "48": {"showcase": False},
                "49": {"showcase": False},
                "57": {"showcase": False},
                "66": {"showcase": False},
                "73": {"showcase": False},
            },
        }
        expected = [
            27, 28, 29, 30, 31, 32, 34, 35, 36, 37,
            39, 40, 41, 42, 44, 45, 47, 50, 51, 52,
            53, 54, 55, 56, 58, 59, 60, 61, 62, 63,
            64, 65, 67, 68, 69, 70, 71, 72, 74, 75,
        ]
        self.assertEqual(
            expected,
            funnel.next_visible_chapters(manifest, after_chapter=26, count=40, max_chapter=75),
        )

    def test_source_win_record_stays_lightweight(self):
        record = {
            "chapter": 27,
            "verdict": "source_win",
            "screen": {
                "decision": "source_win",
                "signals": [],
                "reason": "The task already carries the exchange.",
            },
        }
        funnel.validate_record(record)

    def test_surviving_change_requires_deep_roundtrip_evidence(self):
        record = {
            "chapter": 28,
            "verdict": "change_survives",
            "screen": {
                "decision": "deep_review",
                "signals": ["verbalized_behavior"],
                "reason": "A spoken correction can become action.",
            },
            "patches": [],
        }
        with self.assertRaisesRegex(ValueError, "dramatic"):
            funnel.validate_record(record)

    def test_apply_record_replaces_exact_paragraph_span(self):
        page = (
            '<html><article class="prose">'
            '<p>Before.</p><p>Old first.</p><p>Old second.</p><p>After.</p>'
            '</article></html>'
        )
        record = {
            "chapter": 28,
            "verdict": "change_survives",
            "screen": {
                "decision": "deep_review",
                "signals": ["verbalized_behavior"],
                "reason": "Physical behavior is stronger.",
            },
            "dramatic": "A wants the answer; B controls the task.",
            "performance": "B answers by doing the task.",
            "screenplay": "B [moves object]: Again.",
            "comparison": "Candidate externalizes B's authority without changing the result.",
            "patches": [
                {
                    "start": "Old first.",
                    "end": "Old second.",
                    "replacement": ["New first.", 'B said, "Again."'],
                    "rationale": "Make task ownership physical.",
                }
            ],
        }
        funnel.validate_record(record)
        updated = funnel.apply_record(page, record)
        self.assertIn("<p>Before.</p><p>New first.</p><p>B said, &quot;Again.&quot;</p><p>After.</p>", updated)
        self.assertNotIn("Old first.", updated)

    def test_apply_record_fails_closed_on_ambiguous_anchor(self):
        page = (
            '<article class="prose">'
            '<p>Same.</p><p>Middle.</p><p>Same.</p>'
            '</article>'
        )
        record = {
            "chapter": 28,
            "verdict": "change_survives",
            "screen": {"decision": "deep_review", "signals": ["rhythm"], "reason": "Test."},
            "dramatic": "Test.",
            "performance": "Test.",
            "screenplay": "Test.",
            "comparison": "Test.",
            "patches": [
                {
                    "start": "Same.",
                    "end": "Middle.",
                    "replacement": ["Changed."],
                    "rationale": "Test.",
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "start boundary matched 2"):
            funnel.apply_record(page, record)

    def test_survivor_rejects_em_dash_in_new_prose(self):
        record = {
            "chapter": 28,
            "verdict": "change_survives",
            "screen": {"decision": "deep_review", "signals": ["rhythm"], "reason": "Test."},
            "dramatic": "Test.",
            "performance": "Test.",
            "screenplay": "Test.",
            "comparison": "Test.",
            "patches": [
                {
                    "start": "Old.",
                    "end": "Old.",
                    "replacement": ["No—new dash."],
                    "rationale": "Test.",
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "em dash"):
            funnel.validate_record(record)


if __name__ == "__main__":
    unittest.main()
