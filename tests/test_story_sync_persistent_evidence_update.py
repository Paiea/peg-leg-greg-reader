import unittest

from scripts import persistent_act_runtime as runtime


class SharedDiscoveryEvidenceUpdateTests(unittest.TestCase):
    def _boundary(self, boundary_id, dimension, value):
        return {"id": boundary_id, "dimension": dimension, "value": value, "confidence": 0.6, "provenance": ["seed"]}

    def _runtime(self):
        acts = {}
        for index, act_id in enumerate(runtime.ACT_IDS):
            acts[act_id] = {
                "state_in": [self._boundary(f"{act_id}-in", "phase", index)],
                "local_state": {"possibilities": [], "discoveries": [], "unresolved_questions": [], "constraint_responses": []},
                "state_out": [self._boundary(f"{act_id}-out", "phase", index + 1)],
            }
        return {
            "schema": runtime.RUNTIME_SCHEMA,
            "story_id": "test",
            "acts": acts,
            "shared_story_state": {
                "sync_state": {
                    "schema": "story_sync_state/v1",
                    "story_confidence": 0.55,
                    "possibilities": [],
                    "discoveries": [
                        {
                            "id": "mutual-indispensability",
                            "finding": "Neither lead cleanly replaces the other.",
                            "confidence": "repeated_signal",
                            "evidence": [
                                {"source_id": "briefing", "independent_group": "act-i-briefing", "kind": "support", "dramatic_uses": ["relationship", "character"], "regions": ["act-i"]},
                                {"source_id": "fieldwork", "independent_group": "act-ii-fieldwork", "kind": "support", "dramatic_uses": ["relationship", "character"], "regions": ["act-ii"]},
                            ],
                        }
                    ],
                    "contradictions": [],
                    "canon_events": [],
                    "reader_requirements": [],
                    "assumptions": [],
                    "unresolved_questions": [],
                },
                "forward_consequences": [],
                "backward_requirements": [],
                "cross_direction_agreements": [],
                "contradictions": [],
            },
        }

    def test_rehearsal_can_append_bounded_evidence_to_existing_discovery_then_story_sync_reclassifies(self):
        state = self._runtime()
        before = runtime.sync_shared_story(state)
        self.assertEqual("repeated_signal", before["discovery_levels"]["mutual-indispensability"])
        evidence = {
            "schema": runtime.REHEARSAL_EVIDENCE_SCHEMA,
            "id": "first-bargain-high-heat",
            "target_id": "target:first-bargain",
            "source_act": "act-i",
            "experiment_mode": "performance",
            "fidelity": "high_heat",
            "finding": "The pair becomes useful by correcting each other's failure modes in live negotiation.",
            "confidence": 0.8,
            "provenance": "dragon-spotter:first-bargain",
            "local_discoveries": [],
            "forward_consequences": [],
            "backward_requirements": [],
            "branch_updates": [],
            "story_sync_discoveries": [],
            "story_sync_evidence_updates": [
                {
                    "discovery_id": "mutual-indispensability",
                    "evidence": {
                        "source_id": "rehearsal:first-bargain-high-heat:relationship_behavior",
                        "independent_group": "first-bargain-high-heat",
                        "kind": "support",
                        "dramatic_uses": ["plot"],
                        "regions": ["act-i"],
                    },
                }
            ],
        }
        deltas = runtime.reduce_rehearsal_evidence(evidence)
        self.assertIn("shared_discovery_evidence", {item["type"] for item in deltas})
        updated = runtime.integrate_deltas(state, deltas)
        after = runtime.sync_shared_story(updated)
        self.assertEqual("strong_thread", after["discovery_levels"]["mutual-indispensability"])
        self.assertNotIn("mutual-indispensability", after["story_truths"])


if __name__ == "__main__":
    unittest.main()
