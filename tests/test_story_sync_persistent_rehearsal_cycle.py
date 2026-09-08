import copy
import unittest

from scripts import persistent_act_runtime as runtime


class PersistentRehearsalCycleTests(unittest.TestCase):
    def _boundary(self, boundary_id, dimension, value, confidence=0.6):
        return {
            "id": boundary_id,
            "dimension": dimension,
            "value": value,
            "confidence": confidence,
            "provenance": [f"seed:{boundary_id}"],
        }

    def _runtime(self):
        return {
            "schema": runtime.RUNTIME_SCHEMA,
            "story_id": "test-story",
            "acts": {
                "act-i": {
                    "state_in": [self._boundary("a1-in-role", "professional_role", "fraud")],
                    "local_state": {
                        "possibilities": [
                            {"id": "land", "status": "active", "viability": "viable"},
                            {"id": "protocol-only", "status": "active", "viability": "weak"},
                        ],
                        "discoveries": [],
                        "unresolved_questions": ["What does the first bargain actually require?"],
                        "constraint_responses": [],
                    },
                    "state_out": [self._boundary("a1-out-role", "professional_role", "useful-fraud")],
                },
                "act-ii": {
                    "state_in": [self._boundary("a2-in-role", "professional_role", "useful-fraud")],
                    "local_state": {
                        "possibilities": [],
                        "discoveries": [],
                        "unresolved_questions": [],
                        "constraint_responses": [],
                    },
                    "state_out": [
                        self._boundary("a2-out-role", "professional_role", "political-liability"),
                        self._boundary("a2-out-trust", "romantic_trust", "guarded"),
                    ],
                },
                "act-iii": {
                    "state_in": [
                        self._boundary("a3-in-role", "professional_role", "needed-envoy"),
                        self._boundary("a3-in-trust", "romantic_trust", "intimate-team"),
                    ],
                    "local_state": {
                        "possibilities": [],
                        "discoveries": [],
                        "unresolved_questions": [],
                        "constraint_responses": [],
                    },
                    "state_out": [self._boundary("a3-out-role", "professional_role", "public-envoy")],
                },
                "act-iv": {
                    "state_in": [self._boundary("a4-in-role", "professional_role", "public-envoy")],
                    "local_state": {
                        "possibilities": [],
                        "discoveries": [],
                        "unresolved_questions": [],
                        "constraint_responses": [],
                    },
                    "state_out": [self._boundary("a4-out-role", "professional_role", "dragon-recognized-envoy")],
                },
            },
            "shared_story_state": {
                "sync_state": {
                    "schema": "story_sync_state/v1",
                    "story_confidence": 0.5,
                    "possibilities": [],
                    "discoveries": [],
                    "contradictions": [],
                    "canon_events": [],
                    "reader_requirements": [],
                    "assumptions": [],
                    "unresolved_questions": [],
                },
                "forward_consequences": [
                    {
                        "id": "forward-recognition",
                        "kind": "forward_consequence",
                        "source_act": "act-i",
                        "target_act": "act-iv",
                        "statement": "A reciprocal first bargain makes later dragons test whether humans honor obligations.",
                        "confidence": 0.6,
                        "provenance": ["rehearsal:first-bargain"],
                        "status": "open",
                        "thread_key": "reciprocal-obligation",
                    }
                ],
                "backward_requirements": [
                    {
                        "id": "backward-earned-envoy",
                        "kind": "backward_requirement",
                        "source_act": "act-iv",
                        "target_act": "act-i",
                        "statement": "A dragon-recognized envoy ending needs an early reason dragons value his responsiveness rather than credentials.",
                        "confidence": 0.6,
                        "provenance": ["act-iv:ending-hypothesis"],
                        "status": "open",
                        "thread_key": "earned-recognition",
                    }
                ],
                "cross_direction_agreements": [
                    {
                        "id": "recognition-agreement",
                        "acts": ["act-i", "act-iv"],
                        "statement": "Early responsiveness and late dragon recognition may describe one earned identity thread.",
                        "confidence": 0.55,
                        "provenance": ["act-i:first-bargain", "act-iv:ending-hypothesis"],
                    }
                ],
                "contradictions": [],
            },
        }

    def test_rehearsal_targets_use_declared_experiment_modes_and_fidelity(self):
        targets = runtime.compile_rehearsal_targets(self._runtime())
        self.assertTrue(targets)
        for target in targets:
            self.assertEqual(runtime.REHEARSAL_TARGET_SCHEMA, target["schema"])
            self.assertIn(target["experiment_mode"], runtime.EXPERIMENT_MODES)
            self.assertIn(target["fidelity"], runtime.FIDELITY_LEVELS)
            self.assertEqual("derived_only_no_story_authority", target["authority_effect"])

    def test_structural_boundary_mismatch_does_not_default_to_performance(self):
        targets = runtime.compile_rehearsal_targets(self._runtime())
        structural = [item for item in targets if item.get("dimension") == "professional_role"]
        self.assertTrue(structural)
        self.assertTrue(all(item["experiment_mode"] == "state_transition_test" for item in structural))
        self.assertTrue(all(item["fidelity"] == "development" for item in structural))

    def test_embodied_relationship_boundary_can_escalate_to_high_heat_performance(self):
        targets = runtime.compile_rehearsal_targets(self._runtime())
        relationship = [item for item in targets if item.get("dimension") == "romantic_trust"]
        self.assertEqual(1, len(relationship))
        self.assertEqual("performance", relationship[0]["experiment_mode"])
        self.assertEqual("high_heat", relationship[0]["fidelity"])

    def test_directional_messages_get_direction_specific_cheap_tests(self):
        targets = runtime.compile_rehearsal_targets(self._runtime())
        by_source = {item["source_id"]: item for item in targets}
        self.assertEqual("forward_consequence_test", by_source["forward-recognition"]["experiment_mode"])
        self.assertEqual("probe", by_source["forward-recognition"]["fidelity"])
        self.assertEqual("backward_prerequisite_test", by_source["backward-earned-envoy"]["experiment_mode"])
        self.assertEqual("probe", by_source["backward-earned-envoy"]["fidelity"])

    def test_compact_rehearsal_evidence_reduces_to_forward_backward_and_local_deltas(self):
        evidence = {
            "schema": runtime.REHEARSAL_EVIDENCE_SCHEMA,
            "id": "evidence:first-bargain",
            "target_id": "question:act-i:0",
            "source_act": "act-i",
            "experiment_mode": "performance",
            "fidelity": "high_heat",
            "finding": "Responsiveness plus domain constraint is more useful than protocol or improvisation alone.",
            "confidence": 0.75,
            "provenance": "state/experiments/example.json",
            "local_discoveries": [
                {"id": "pair-competence", "finding": "Observation and doctrine are mutually constraining."}
            ],
            "forward_consequences": [
                {
                    "id": "future-obligation",
                    "target_act": "act-iii",
                    "statement": "Reciprocal bargains create obligations later actors can call in.",
                    "confidence": 0.7,
                    "thread_key": "reciprocal-obligation",
                }
            ],
            "backward_requirements": [
                {
                    "id": "earlier-recognition",
                    "target_act": "act-i",
                    "statement": "Later recognition requires early evidence that responsiveness matters.",
                    "confidence": 0.65,
                    "thread_key": "earned-recognition",
                }
            ],
            "branch_updates": [],
            "story_sync_discoveries": [],
        }
        deltas = runtime.reduce_rehearsal_evidence(evidence)
        self.assertEqual(
            {"local_discovery", "forward_consequence", "backward_requirement"},
            {item["type"] for item in deltas},
        )

    def test_branch_updates_can_reduce_local_entropy_without_promoting_truth(self):
        state = self._runtime()
        before = runtime.branch_entropy(state)
        evidence = {
            "schema": runtime.REHEARSAL_EVIDENCE_SCHEMA,
            "id": "evidence:protocol-challenge",
            "target_id": "question:act-i:0",
            "source_act": "act-i",
            "experiment_mode": "counterfactual_branch_comparison",
            "fidelity": "development",
            "finding": "Protocol-only survives as safety scaffolding but fails as the main competence path.",
            "confidence": 0.8,
            "provenance": "rehearsal:protocol-challenge",
            "local_discoveries": [],
            "forward_consequences": [],
            "backward_requirements": [],
            "branch_updates": [
                {
                    "possibility_id": "protocol-only",
                    "status": "superseded",
                    "viability": "redundant",
                    "reason": "challenge evidence rejects protocol-only as the lead competence branch",
                }
            ],
            "story_sync_discoveries": [],
        }
        updated = runtime.integrate_deltas(state, runtime.reduce_rehearsal_evidence(evidence))
        after = runtime.branch_entropy(updated)
        self.assertLess(after["open_branch_count"], before["open_branch_count"])
        self.assertEqual([], runtime.sync_shared_story(updated)["story_truths"])

    def test_cycle_preserves_four_persistent_packets_and_reports_entropy_change(self):
        state = self._runtime()
        result = runtime.run_rehearsal_cycle(state)
        self.assertEqual(set(runtime.ACT_IDS), set(result["act_packets"]))
        self.assertEqual(4, len([item for item in result["schedule"] if item["kind"] == "baseline_local_search"]))
        self.assertIn("rehearsal_targets", result)
        self.assertIn("branch_entropy", result)
        self.assertEqual("derived_only_no_canon_mutation", result["authority_effect"])


if __name__ == "__main__":
    unittest.main()
