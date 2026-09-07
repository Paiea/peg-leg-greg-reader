import json
import tempfile
import unittest
from pathlib import Path

from scripts import creator_taste_prior as taste


class CreatorTastePriorTests(unittest.TestCase):
    def _prior(self):
        return {
            "schema": taste.CREATOR_TASTE_PRIOR_SCHEMA,
            "signals": [
                {
                    "id": "consequence_over_explanation",
                    "scope": "cross_project",
                    "direction": "prefer",
                    "confidence": 0.75,
                    "evidence_count": 2,
                    "counterexample_count": 0,
                    "summary": "Prefer mechanics that create visible human consequences.",
                    "last_evidence_reference": "ct-002",
                }
            ],
        }

    def _overlay(self):
        return {
            "schema": taste.PROJECT_TASTE_OVERLAY_SCHEMA,
            "project": "dragon-spotter",
            "signals": [
                {
                    "id": "competence_as_romantic_pressure",
                    "scope": "project",
                    "direction": "explore",
                    "confidence": 0.81,
                    "summary": "Competence and professional conflict are valuable sources of attraction in this project.",
                }
            ],
        }

    def _evidence(self, decision_id, *, effect="support", scope="cross_project", signal_id="consequence_over_explanation"):
        return {
            "schema": taste.CREATOR_TASTE_EVIDENCE_SCHEMA,
            "decision_id": decision_id,
            "project": "dragon-spotter",
            "context": "A system mechanic can remain explanatory or produce a social consequence.",
            "choice": "Use the consequence-bearing version.",
            "reason": "The consequence changes relationships and status.",
            "source_type": "human_editorial_decision",
            "signals": [
                {
                    "id": signal_id,
                    "scope": scope,
                    "direction": "prefer",
                    "summary": "Prefer mechanics that create visible human consequences.",
                    "effect": effect,
                }
            ],
        }

    def test_compact_runtime_context_keeps_cross_project_and_project_signals_separate(self):
        context = taste.compile_taste_context(self._prior(), self._overlay())
        self.assertEqual(taste.CREATOR_TASTE_CONTEXT_SCHEMA, context["schema"])
        self.assertEqual("dragon-spotter", context["project"])
        self.assertEqual(["consequence_over_explanation"], [item["id"] for item in context["cross_project_signals"]])
        self.assertEqual(["competence_as_romantic_pressure"], [item["id"] for item in context["project_signals"]])
        self.assertNotIn("evidence", context)
        self.assertNotIn("evidence_records", context)

    def test_invalid_prior_confidence_is_rejected(self):
        prior = self._prior()
        prior["signals"][0]["confidence"] = 1.2
        with self.assertRaisesRegex(ValueError, "confidence"):
            taste.validate_prior(prior)

    def test_append_evidence_is_append_only_and_duplicate_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.jsonl"
            first = self._evidence("ct-001")
            second = self._evidence("ct-002", effect="challenge")
            taste.append_evidence_record(path, first)
            taste.append_evidence_record(path, second)
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(["ct-001", "ct-002"], [item["decision_id"] for item in records])
            with self.assertRaisesRegex(ValueError, "duplicate decision_id"):
                taste.append_evidence_record(path, first)
            records_after = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(records, records_after)

    def test_rebuild_prior_preserves_counterexamples_without_erasing_supported_signal(self):
        records = [
            self._evidence("ct-001"),
            self._evidence("ct-002"),
            self._evidence("ct-003", effect="challenge"),
        ]
        prior = taste.rebuild_prior(records)
        self.assertEqual(taste.CREATOR_TASTE_PRIOR_SCHEMA, prior["schema"])
        signal = prior["signals"][0]
        self.assertEqual("consequence_over_explanation", signal["id"])
        self.assertEqual(3, signal["evidence_count"])
        self.assertEqual(1, signal["counterexample_count"])
        self.assertGreater(signal["confidence"], 0.5)
        self.assertLess(signal["confidence"], 0.75)
        self.assertEqual("ct-003", signal["last_evidence_reference"])

    def test_project_local_evidence_does_not_auto_promote_into_cross_project_prior(self):
        records = [
            self._evidence("ct-001"),
            self._evidence("ct-002", scope="project", signal_id="competence_as_romantic_pressure"),
        ]
        prior = taste.rebuild_prior(records)
        self.assertEqual(["consequence_over_explanation"], [item["id"] for item in prior["signals"]])

    def test_rebuild_prior_enforces_active_signal_cap(self):
        records = []
        for index in range(4):
            records.append(self._evidence(f"ct-{index}", signal_id=f"signal-{index}"))
        prior = taste.rebuild_prior(records, max_signals=2)
        self.assertEqual(2, len(prior["signals"]))
        with self.assertRaisesRegex(ValueError, "max_signals"):
            taste.rebuild_prior(records, max_signals=26)


if __name__ == "__main__":
    unittest.main()
