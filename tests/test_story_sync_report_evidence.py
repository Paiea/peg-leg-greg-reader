import unittest

from scripts import story_sync_engine as sync


class StorySyncReportEvidenceTests(unittest.TestCase):
    def test_report_preserves_promotion_evidence_summary(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.55,
            "possibilities": [],
            "discoveries": [
                {
                    "id": "gift-obligation",
                    "finding": "Dragon treasure functions as reciprocal diplomatic obligation.",
                    "evidence": [
                        {"source_id": "a", "independent_group": "a", "kind": "support", "dramatic_uses": ["plot", "world", "character"], "regions": ["act-i"]},
                        {"source_id": "b", "independent_group": "b", "kind": "support", "dramatic_uses": ["plot", "relationship", "setup_payoff"], "regions": ["act-iii"]},
                    ],
                }
            ],
            "contradictions": [],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
        }
        report = sync.sync_story(state)
        record = report["discovery_records"]["gift-obligation"]
        self.assertEqual("strong_thread", record["confidence"])
        self.assertEqual(2, record["evidence_summary"]["independent_support_count"])
        self.assertIn("setup_payoff", record["evidence_summary"]["dramatic_uses"])

    def test_branch_kill_preserves_reason_and_evidence(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.6,
            "possibilities": [
                {
                    "id": "generic-conspiracy",
                    "branch_group": "central-conflict",
                    "region": "act-iii",
                    "status": "active",
                    "viability": "redundant",
                    "sync_reason": "Adds a second hidden-villain engine where dragon treaty consequences already supply the same pressure.",
                    "evidence": ["compare.central-conflict.2"],
                }
            ],
            "discoveries": [],
            "contradictions": [],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
        }
        report = sync.sync_story(state)
        decision = report["branch_decisions"][0]
        self.assertEqual("kill", decision["action"])
        self.assertEqual("redundant", decision["viability"])
        self.assertIn("treaty consequences", decision["reason"])
        self.assertEqual(["compare.central-conflict.2"], decision["evidence"])


if __name__ == "__main__":
    unittest.main()
