import json
import unittest
from pathlib import Path

from scripts import story_sync_engine as sync


ROOT = Path(__file__).resolve().parents[1]
TRIAL_ROOT = ROOT / "state" / "experiments" / "dragon-spotter" / "story-sync"


class DragonSpotterStorySyncTrialTests(unittest.TestCase):
    def test_bounded_trial_finds_threads_without_premature_story_truth(self):
        state = json.loads((TRIAL_ROOT / "trial-input.json").read_text(encoding="utf-8"))
        expected = json.loads((TRIAL_ROOT / "trial-report.json").read_text(encoding="utf-8"))
        report = sync.sync_story(state)

        self.assertEqual(expected, report)
        self.assertEqual("compare", report["phase"])
        self.assertEqual(
            ["gift-reciprocity", "improvisation-is-competence-path"],
            report["strong_threads"],
        )
        self.assertEqual(
            ["heat-through-competence", "mutual-indispensability"],
            report["repeated_signals"],
        )
        self.assertEqual([], report["story_truths"])

    def test_trial_preserves_meaningful_divergence_and_kills_only_redundant_branch(self):
        state = json.loads((TRIAL_ROOT / "trial-input.json").read_text(encoding="utf-8"))
        report = sync.sync_story(state)
        self.assertEqual(["conflict.hidden-conspiracy"], report["branches_killed"])
        for branch in ("gift.coin", "gift.scale-token", "ending.crown-spotter", "ending.dragon-envoy", "romance.clean-rivals"):
            self.assertIn(branch, report["branches_preserved"])
        self.assertEqual(["first-gift-form", "ending-office-role"], report["contradictions_alive"])

    def test_trial_demonstrates_bidirectional_and_event_driven_sync(self):
        state = json.loads((TRIAL_ROOT / "trial-input.json").read_text(encoding="utf-8"))
        report = sync.sync_story(state)
        directions = {item["direction"] for item in report["propagation"]}
        self.assertEqual({"backward", "forward"}, directions)
        self.assertIn("gift-reciprocity", report["immediate_sync_discoveries"])
        self.assertIn("improvisation-is-competence-path", report["immediate_sync_discoveries"])
        self.assertEqual(["ending-office-role"], report["immediate_sync_contradictions"])
        self.assertTrue(report["sync_required"])

    def test_trial_keeps_hidden_canon_distinct_and_detects_reader_gap(self):
        state = json.loads((TRIAL_ROOT / "trial-input.json").read_text(encoding="utf-8"))
        report = sync.sync_story(state)
        self.assertEqual(["training-week-hidden", "scholar-briefings-hidden"], report["hidden_canon"])
        self.assertEqual(["earned-competence-legibility"], [item["id"] for item in report["reader_gaps"]])
        self.assertEqual("derived_only_no_canon_mutation", report["authority_effect"])


if __name__ == "__main__":
    unittest.main()
