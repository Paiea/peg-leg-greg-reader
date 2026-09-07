import copy
import unittest

from scripts import creator_taste_prior as taste
from scripts import plg_ai_tools
from scripts import story_sync_engine as sync


class CreatorTastePriorityTests(unittest.TestCase):
    def _context(self):
        prior = {
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
        overlay = {
            "schema": taste.PROJECT_TASTE_OVERLAY_SCHEMA,
            "project": "dragon-spotter",
            "signals": [
                {
                    "id": "competence_as_romantic_pressure",
                    "scope": "project",
                    "direction": "explore",
                    "confidence": 0.81,
                    "summary": "Competence and professional conflict are useful sources of attraction here.",
                }
            ],
        }
        return taste.compile_taste_context(prior, overlay)

    def _state(self, *, confidence=0.55):
        return {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": confidence,
            "possibilities": [
                {
                    "id": "creator-likely",
                    "branch_group": "fork",
                    "region": "act-ii",
                    "status": "active",
                    "viability": "viable",
                    "creator_prior_match": "high",
                    "creator_surprise": "low",
                },
                {
                    "id": "creator-surprise",
                    "branch_group": "fork",
                    "region": "act-ii",
                    "status": "active",
                    "viability": "viable",
                    "creator_prior_match": "low",
                    "creator_surprise": "high",
                    "surprise_reason": "Less predicted by creator history but may create stronger emotional pressure.",
                },
                {
                    "id": "invalidated-but-likely",
                    "branch_group": "fork",
                    "region": "act-ii",
                    "status": "active",
                    "viability": "invalidated",
                    "creator_prior_match": "high",
                    "creator_surprise": "low",
                },
            ],
            "discoveries": [],
            "contradictions": [],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
            "unresolved_questions": [],
        }

    def test_creator_match_changes_search_priority_not_branch_authority(self):
        self.assertEqual("medium", taste.branch_search_priority(self._state()["possibilities"][0], phase="compare"))
        self.assertEqual("none", taste.branch_search_priority(self._state()["possibilities"][2], phase="compare"))

        state = self._state()
        core = sync.sync_story(copy.deepcopy(state))
        report = taste.augment_sync_report(state, core, creator_taste=self._context())
        self.assertIn("invalidated-but-likely", report["branches_killed"])
        invalidated = next(item for item in report["branch_decisions"] if item["id"] == "invalidated-but-likely")
        self.assertEqual("none", invalidated["creator_search_priority"])

    def test_creator_surprise_remains_rehearsal_eligible_in_compare(self):
        state = self._state()
        report = taste.augment_sync_report(state, sync.sync_story(copy.deepcopy(state)), creator_taste=self._context())
        targets = [item for item in report["rehearsal_targets"] if item.get("source_type") == "creator_taste"]
        self.assertIn("creator-likely", [item["source_id"] for item in targets])
        self.assertIn("creator-surprise", [item["source_id"] for item in targets])
        surprise = next(item for item in targets if item["source_id"] == "creator-surprise")
        self.assertEqual("creator_surprise_probe", surprise["purpose"])

    def test_convergence_does_not_upgrade_creator_taste_authority(self):
        state = self._state(confidence=0.9)
        report = taste.augment_sync_report(state, sync.sync_story(copy.deepcopy(state)), creator_taste=self._context())
        self.assertEqual("converge", report["phase"])
        self.assertEqual([], [item for item in report["rehearsal_targets"] if item.get("source_type") == "creator_taste"])
        self.assertEqual("heuristic_only_no_story_authority", report["creator_taste"]["authority_effect"])

    def test_runtime_context_is_inspectable_but_never_selects_a_branch(self):
        state = self._state()
        report = taste.augment_sync_report(state, sync.sync_story(copy.deepcopy(state)), creator_taste=self._context())
        self.assertEqual("dragon-spotter", report["creator_taste"]["project"])
        self.assertEqual(["consequence_over_explanation"], [item["id"] for item in report["creator_taste"]["cross_project_signals"]])
        self.assertEqual(["competence_as_romantic_pressure"], [item["id"] for item in report["creator_taste"]["project_signals"]])
        self.assertNotIn("selected_branch", report)


if __name__ == "__main__":
    unittest.main()
