import copy
import unittest

from scripts import story_sync_engine as sync


class CreatorTastePriorTests(unittest.TestCase):
    def _prior(self):
        return {
            "schema": sync.CREATOR_TASTE_SCHEMA,
            "preferences": [
                {
                    "id": "project.consequence-dense",
                    "scope": "project",
                    "statement": "Prefer consequences that connect several story dimensions rather than isolated novelty.",
                    "confidence": 0.8,
                    "tags": ["consequence-dense", "causal-reuse"],
                    "support": ["creator.choice.12", "creator.choice.19"],
                    "counterexamples": [],
                },
                {
                    "id": "cross.hidden-life",
                    "scope": "cross_project",
                    "statement": "Often values hidden canon that makes visible relationships feel accumulated.",
                    "confidence": 0.7,
                    "tags": ["hidden-canon", "accumulated-relationship"],
                    "support": ["creator.plg.hide-pass"],
                    "counterexamples": [],
                },
            ],
            "surprise_wins": [],
        }

    def _state(self):
        return {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.55,
            "possibilities": [
                {
                    "id": "likely",
                    "branch_group": "fork",
                    "region": "act-ii",
                    "status": "active",
                    "viability": "viable",
                    "taste_alignment": ["project.consequence-dense"],
                },
                {
                    "id": "surprise",
                    "branch_group": "fork",
                    "region": "act-ii",
                    "status": "active",
                    "viability": "viable",
                    "creator_surprise": True,
                    "surprise_reason": "Less creator-typical, but could create unusually strong relationship pressure.",
                },
            ],
            "discoveries": [
                {
                    "id": "thread",
                    "finding": "A supported thread.",
                    "evidence": [
                        {"source_id": "a", "independent_group": "a", "kind": "support", "dramatic_uses": ["plot"], "regions": ["act-i"]},
                        {"source_id": "b", "independent_group": "b", "kind": "support", "dramatic_uses": ["plot"], "regions": ["act-i"]},
                    ],
                }
            ],
            "contradictions": [],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
            "unresolved_questions": [],
            "creator_taste_prior": self._prior(),
        }

    def test_taste_prior_cannot_change_discovery_authority_or_branch_action(self):
        state = self._state()
        without = copy.deepcopy(state)
        without.pop("creator_taste_prior")

        report_with = sync.sync_story(state)
        report_without = sync.sync_story(without)

        self.assertEqual(report_without["discovery_levels"], report_with["discovery_levels"])
        self.assertEqual(report_without["branches_killed"], report_with["branches_killed"])
        self.assertEqual(report_without["branches_preserved"], report_with["branches_preserved"])
        self.assertEqual("heuristic_only_no_story_authority", report_with["creator_taste"]["authority_effect"])

    def test_project_specific_alignment_has_more_search_weight_than_cross_project(self):
        prior = self._prior()
        project = {"taste_alignment": ["project.consequence-dense"]}
        cross = {"taste_alignment": ["cross.hidden-life"]}
        self.assertGreater(
            sync.creator_taste_affinity(project, prior),
            sync.creator_taste_affinity(cross, prior),
        )

    def test_compare_phase_preserves_one_creator_surprise_rehearsal_target(self):
        report = sync.sync_story(self._state())
        targets = [item for item in report["rehearsal_targets"] if item.get("purpose") == "creator_surprise_probe"]
        self.assertEqual(1, len(targets))
        self.assertEqual("surprise", targets[0]["source_id"])

    def test_creator_likely_branch_is_a_rehearsal_hint_not_a_winner(self):
        report = sync.sync_story(self._state())
        likely = [item for item in report["rehearsal_targets"] if item.get("purpose") == "creator_likely_probe"]
        self.assertEqual(["likely"], [item["source_id"] for item in likely])
        self.assertNotIn("selected_branch", report)
        self.assertIn("surprise", report["branches_preserved"])

    def test_taste_pressure_does_not_increase_during_convergence(self):
        state = self._state()
        compare_report = sync.sync_story(state)
        state["story_confidence"] = 0.9
        converge_report = sync.sync_story(state)

        compare_hints = [item for item in compare_report["rehearsal_targets"] if item.get("source_type") == "creator_taste"]
        converge_hints = [item for item in converge_report["rehearsal_targets"] if item.get("source_type") == "creator_taste"]
        self.assertGreaterEqual(len(compare_hints), len(converge_hints))
        self.assertEqual([], converge_hints)

    def test_record_surprise_win_preserves_context_instead_of_flipping_absolute_preference(self):
        prior = self._prior()
        updated = sync.record_creator_surprise_win(
            prior,
            decision_id="creator.choice.27",
            chosen_branch="delayed-disclosure",
            predicted_branch="immediate-use",
            conditions=["secrecy strengthened the relationship arc", "delayed disclosure increased downstream consequence"],
        )
        self.assertEqual(prior["preferences"], updated["preferences"])
        self.assertEqual(1, len(updated["surprise_wins"]))
        self.assertEqual("delayed-disclosure", updated["surprise_wins"][0]["chosen_branch"])
        self.assertEqual(
            ["secrecy strengthened the relationship arc", "delayed disclosure increased downstream consequence"],
            updated["surprise_wins"][0]["conditions"],
        )

    def test_single_supporting_decision_cannot_create_high_confidence_preference(self):
        prior = {
            "schema": sync.CREATOR_TASTE_SCHEMA,
            "preferences": [
                {
                    "id": "too-certain",
                    "scope": "project",
                    "statement": "One choice becomes a rule.",
                    "confidence": 0.9,
                    "tags": ["x"],
                    "support": ["one-decision"],
                    "counterexamples": [],
                }
            ],
            "surprise_wins": [],
        }
        with self.assertRaisesRegex(ValueError, "multiple supporting decisions"):
            sync.validate_creator_taste_prior(prior)


if __name__ == "__main__":
    unittest.main()
