import unittest

from scripts import story_sync_engine as sync


class StorySyncFeedbackTests(unittest.TestCase):
    def test_contradiction_evidence_does_not_help_promote_a_discovery(self):
        discovery = {
            "id": "d",
            "finding": "One narrow behavior repeats.",
            "evidence": [
                {"source_id": "a", "independent_group": "a", "kind": "support", "dramatic_uses": ["character"], "regions": ["act-i"]},
                {"source_id": "b", "independent_group": "b", "kind": "support", "dramatic_uses": ["character"], "regions": ["act-i"]},
                {"source_id": "against", "independent_group": "against", "kind": "contradiction", "dramatic_uses": ["plot", "world", "relationship"], "regions": ["act-iii"]},
            ],
        }
        self.assertEqual("repeated_signal", sync.classify_discovery(discovery))

    def test_unresolved_questions_survive_sync_without_becoming_assumptions(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.5,
            "possibilities": [],
            "discoveries": [],
            "contradictions": [],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
            "unresolved_questions": [
                {"id": "q1", "question": "What does the first dragon actually want?", "regions": ["act-i", "act-iii"], "importance": "high"}
            ],
        }
        report = sync.sync_story(state)
        self.assertEqual(state["unresolved_questions"], report["unresolved_questions"])
        self.assertEqual([], report["story_truths"])

    def test_book_shaping_strong_thread_without_challenge_returns_high_heat_rehearsal_target(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.6,
            "possibilities": [],
            "discoveries": [
                {
                    "id": "thread",
                    "finding": "A strong thread needs adversarial rehearsal before truth promotion.",
                    "book_shaping": True,
                    "evidence": [
                        {"source_id": "a", "independent_group": "a", "kind": "support", "dramatic_uses": ["plot", "character", "world"], "regions": ["act-i"]},
                        {"source_id": "b", "independent_group": "b", "kind": "support", "dramatic_uses": ["plot", "relationship", "setup_payoff"], "regions": ["act-iii"]},
                    ],
                }
            ],
            "contradictions": [],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
            "unresolved_questions": [],
        }
        report = sync.sync_story(state)
        target = report["rehearsal_targets"][0]
        self.assertEqual("thread", target["source_id"])
        self.assertEqual("high", target["heat"])
        self.assertEqual("challenge_strong_thread", target["purpose"])

    def test_high_severity_contradiction_returns_high_heat_divergent_rehearsal_target(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.6,
            "possibilities": [],
            "discoveries": [],
            "contradictions": [
                {"id": "ending", "members": ["ending-a", "ending-b"], "status": "unresolved", "severity": "high", "book_shaping": True}
            ],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
            "unresolved_questions": [],
        }
        report = sync.sync_story(state)
        target = report["rehearsal_targets"][0]
        self.assertEqual("ending", target["source_id"])
        self.assertEqual("high", target["heat"])
        self.assertEqual("compare_live_contradiction", target["purpose"])
        self.assertEqual(["ending-a", "ending-b"], target["members"])


if __name__ == "__main__":
    unittest.main()
