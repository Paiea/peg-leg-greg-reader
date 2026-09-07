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

    def test_compact_rehearsal_evidence_can_close_directional_constraint(self):
        state = self._runtime()
        before = runtime.constraint_closure(state)
        self.assertEqual("untested", before["messages"][0]["closure_status"])

        evidence = {
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

        deltas = runtime.reduce_rehearsal_evidence(evidence)
        self.assertIn("constraint_response", {item["type"] for item in deltas})
        updated = runtime.integrate_deltas(state, deltas)
        after = runtime.constraint_closure(updated)
        self.assertEqual("supported", after["messages"][0]["closure_status"])
        self.assertLess(
            runtime.temporal_consistency(updated)["unresolved_message_count"],
            runtime.temporal_consistency(state)["unresolved_message_count"],
        )


if __name__ == "__main__":
    unittest.main()
