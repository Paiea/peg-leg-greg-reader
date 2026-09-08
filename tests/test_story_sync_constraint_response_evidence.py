import unittest

from scripts import persistent_act_runtime as runtime


class RehearsalConstraintResponseEvidenceTests(unittest.TestCase):
    def _boundary(self, boundary_id, value):
        return {
            "id": boundary_id,
            "dimension": "phase",
            "value": value,
            "confidence": 0.6,
            "provenance": ["seed"],
        }

    def _runtime(self):
        acts = {}
        for index, act_id in enumerate(runtime.ACT_IDS):
            acts[act_id] = {
                "state_in": [self._boundary(f"{act_id}-in", index)],
                "local_state": {
                    "possibilities": [],
                    "discoveries": [],
                    "unresolved_questions": [],
                    "constraint_responses": [],
                },
                "state_out": [self._boundary(f"{act_id}-out", index + 1)],
            }
        return {
            "schema": runtime.RUNTIME_SCHEMA,
            "story_id": "test",
            "acts": acts,
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
                        "id": "forward-test",
                        "kind": "forward_consequence",
                        "source_act": "act-i",
                        "target_act": "act-ii",
                        "statement": "Act II must test whether the Act I consequence survives.",
                        "confidence": 0.6,
                        "provenance": ["seed"],
                        "status": "open",
                    }
                ],
                "backward_requirements": [],
                "cross_direction_agreements": [],
                "contradictions": [],
            },
        }

    def _support_evidence(self):
        return {
            "schema": runtime.REHEARSAL_EVIDENCE_SCHEMA,
            "id": "evidence:forward-test",
            "target_id": "target:message:forward-test",
            "source_act": "act-ii",
            "experiment_mode": "forward_consequence_test",
            "fidelity": "probe",
            "finding": "The consequence remains causally alive in Act II.",
            "confidence": 0.8,
            "provenance": "rehearsal:forward-test",
            "local_discoveries": [],
            "forward_consequences": [],
            "backward_requirements": [],
            "branch_updates": [],
            "story_sync_discoveries": [],
            "story_sync_evidence_updates": [],
            "constraint_responses": [
                {
                    "message_id": "forward-test",
                    "response": "supported",
                    "reason": "The tested Act II state naturally preserves the earlier consequence."
                }
            ],
        }

    def _boundary_evidence(self, boundary_id):
        return {
            "schema": runtime.REHEARSAL_EVIDENCE_SCHEMA,
            "id": "evidence:boundary-test",
            "target_id": f"target:{boundary_id}",
            "source_act": "act-ii",
            "experiment_mode": "performance",
            "fidelity": "high_heat",
            "finding": "The performed bridge reaches a narrower downstream state than the original hypothesis.",
            "confidence": 0.84,
            "provenance": "rehearsal:boundary-test",
            "local_discoveries": [],
            "forward_consequences": [],
            "backward_requirements": [],
            "branch_updates": [],
            "story_sync_discoveries": [],
            "story_sync_evidence_updates": [],
            "constraint_responses": [],
            "boundary_updates": [
                {
                    "act_id": "act-ii",
                    "boundary_side": "state_in",
                    "boundary_id": "act-ii-in",
                    "value": "earned-but-guarded",
                    "confidence": 0.72,
                    "reason": "Observed behavior narrows the downstream hypothesis without turning it into canon."
                }
            ],
            "boundary_responses": [
                {
                    "boundary_id": boundary_id,
                    "target_act": "act-ii",
                    "response": "supported",
                    "reason": "The mismatch is an evidence-backed transition rather than an unresolved interpolation gap."
                }
            ],
        }

    def test_compact_rehearsal_evidence_can_close_directional_constraint(self):
        state = self._runtime()
        before = runtime.constraint_closure(state)
        self.assertEqual("untested", before["messages"][0]["closure_status"])

        deltas = runtime.reduce_rehearsal_evidence(self._support_evidence())
        self.assertIn("constraint_response", {item["type"] for item in deltas})
        updated = runtime.integrate_deltas(state, deltas)
        after = runtime.constraint_closure(updated)
        self.assertEqual("supported", after["messages"][0]["closure_status"])
        self.assertLess(
            runtime.temporal_consistency(updated)["unresolved_message_count"],
            runtime.temporal_consistency(state)["unresolved_message_count"],
        )

    def test_supported_directional_constraint_retires_identical_probe_target(self):
        state = self._runtime()
        before = runtime.compile_rehearsal_targets(state)
        self.assertTrue(any(item["source_id"] == "forward-test" and item["experiment_mode"] == "forward_consequence_test" for item in before))

        updated = runtime.integrate_deltas(state, runtime.reduce_rehearsal_evidence(self._support_evidence()))
        after = runtime.compile_rehearsal_targets(updated)
        self.assertFalse(any(item["source_id"] == "forward-test" and item["experiment_mode"] == "forward_consequence_test" for item in after))

    def test_boundary_evidence_can_revise_derived_hypothesis_and_retire_supported_bridge(self):
        state = self._runtime()
        state["acts"]["act-i"]["state_out"][0]["value"] = "guarded-respect"
        state["acts"]["act-ii"]["state_in"][0]["value"] = "mutual-reliance"
        boundary_id = "boundary:act-i:act-ii:phase:act-i-out:act-ii-in"

        before = runtime.boundary_contradictions(state)
        self.assertEqual([boundary_id], [item["id"] for item in before])

        deltas = runtime.reduce_rehearsal_evidence(self._boundary_evidence(boundary_id))
        self.assertIn("state_boundary_update", {item["type"] for item in deltas})
        self.assertIn("boundary_response", {item["type"] for item in deltas})
        updated = runtime.integrate_deltas(state, deltas)

        target = updated["acts"]["act-ii"]["state_in"][0]
        self.assertEqual("earned-but-guarded", target["value"])
        self.assertEqual("mutual-reliance", target["history"][-1]["value"])
        self.assertEqual([], runtime.boundary_contradictions(updated))
        self.assertFalse(any(item["source_id"] == boundary_id for item in runtime.compile_rehearsal_targets(updated)))


if __name__ == "__main__":
    unittest.main()
