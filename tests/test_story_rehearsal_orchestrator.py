import copy
import unittest

from scripts import persistent_act_runtime as runtime
from scripts import story_rehearsal_orchestrator as rehearsal


class StoryRehearsalOrchestratorTests(unittest.TestCase):
    def _boundary(self, item_id, dimension, value):
        return {"id": item_id, "dimension": dimension, "value": value, "confidence": 0.7, "provenance": ["test"]}

    def _state(self):
        acts = {}
        for act_id in runtime.ACT_IDS:
            acts[act_id] = {
                "state_in": [],
                "local_state": {
                    "possibilities": [],
                    "discoveries": [],
                    "unresolved_questions": [],
                    "constraint_responses": [],
                },
                "state_out": [],
            }
        acts["act-i"]["local_state"]["unresolved_questions"] = ["Could the first bargain work without treasure?"]
        acts["act-ii"]["state_out"] = [self._boundary("ii-trust", "romantic_trust", "distrust")]
        acts["act-iii"]["state_in"] = [self._boundary("iii-trust", "romantic_trust", "intimate_team")]
        return {
            "schema": runtime.RUNTIME_SCHEMA,
            "story_id": "dragon-spotter",
            "acts": acts,
            "shared_story_state": {
                "sync_state": {
                    "schema": "story_sync_state/v1",
                    "story_confidence": 0.55,
                    "possibilities": [],
                    "discoveries": [],
                    "contradictions": [],
                    "canon_events": [],
                    "reader_requirements": [],
                    "assumptions": [],
                    "unresolved_questions": [],
                },
                "forward_consequences": [{
                    "id": "gift-obligation",
                    "kind": "forward_consequence",
                    "source_act": "act-i",
                    "target_act": "act-iii",
                    "statement": "If he accepts dragon treasure, later human institutions may treat it as politically consequential.",
                    "confidence": 0.65,
                    "provenance": ["first-bargain"],
                    "status": "open",
                }],
                "backward_requirements": [{
                    "id": "ending-trust",
                    "kind": "backward_requirement",
                    "source_act": "act-iv",
                    "target_act": "act-ii",
                    "statement": "The ending partnership may require an earlier earned trust event.",
                    "confidence": 0.55,
                    "provenance": ["ending-probe"],
                    "status": "open",
                }],
                "cross_direction_agreements": [],
                "contradictions": [],
            },
        }

    def test_rehearsal_is_not_equated_with_performance(self):
        modes = rehearsal.REHEARSAL_EXPERIMENT_MODES
        self.assertIn("performance", modes)
        self.assertIn("plausibility_probe", modes)
        self.assertIn("state_transition_test", modes)
        self.assertIn("forward_consequence_test", modes)
        self.assertIn("backward_prerequisite_test", modes)
        self.assertGreater(len(modes), 4)

    def test_simple_unresolved_question_gets_cheap_probe_not_screenplay(self):
        targets = rehearsal.compile_rehearsal_targets(self._state())
        question = next(item for item in targets if item["source_type"] == "act_question")
        self.assertEqual("plausibility_probe", question["experiment_mode"])
        self.assertEqual("probe", question["heat"])
        self.assertNotEqual("performance", question["experiment_mode"])

    def test_relationship_boundary_jump_escalates_to_high_heat_performance(self):
        targets = rehearsal.compile_rehearsal_targets(self._state())
        target = next(item for item in targets if item["source_type"] == "boundary_contradiction")
        self.assertEqual("performance", target["experiment_mode"])
        self.assertEqual("high_heat", target["heat"])
        self.assertIn("romantic_trust", target["uncertainty"])

    def test_forward_and_backward_messages_use_directional_tests_before_performance(self):
        targets = rehearsal.compile_rehearsal_targets(self._state())
        forward = next(item for item in targets if item["source_id"] == "gift-obligation")
        backward = next(item for item in targets if item["source_id"] == "ending-trust")
        self.assertEqual("forward_consequence_test", forward["experiment_mode"])
        self.assertEqual("backward_prerequisite_test", backward["experiment_mode"])
        self.assertEqual("development", forward["heat"])
        self.assertEqual("development", backward["heat"])

    def test_target_does_not_prescribe_result_unless_explicitly_locked(self):
        target = rehearsal.build_rehearsal_target(
            target_id="probe-x",
            acts=["act-ii"],
            source_type="act_question",
            source_id="q-x",
            uncertainty="Will this pressure create cooperation or more distrust?",
            experiment_mode="state_transition_test",
            heat="development",
            provenance=["test"],
        )
        self.assertNotIn("required_result", target)
        locked = rehearsal.build_rehearsal_target(
            target_id="probe-y",
            acts=["act-ii"],
            source_type="locked_constraint",
            source_id="q-y",
            uncertainty="Can actors reach a canonically locked physical exit state?",
            experiment_mode="performance",
            heat="high_heat",
            provenance=["test"],
            required_result="Both leave the chamber alive.",
            result_locked=True,
        )
        self.assertEqual("Both leave the chamber alive.", locked["required_result"])

    def test_compact_result_reduction_drops_transcript_and_extracts_directional_deltas(self):
        result = {
            "schema": rehearsal.REHEARSAL_RESULT_SCHEMA,
            "target_id": "first-bargain-probe",
            "source_act": "act-i",
            "experiment_mode": "development_rehearsal",
            "heat": "development",
            "outcome": "support",
            "finding": "Accepting the gift behaves like accepting an obligation.",
            "confidence": 0.68,
            "independent_group": "first-bargain-variance-1",
            "dramatic_uses": ["plot", "world", "relationship"],
            "regions": ["act-i", "act-iii"],
            "provenance": "rehearsal:first-bargain:development-1",
            "transcript": "This should not remain in compact hot evidence.",
            "behavior_discovered": ["He asks what accepting the gift commits him to."],
            "relationship_movement": ["Scholar begins treating his observations as useful."],
            "forward_consequences": [{
                "id": "gift-obligation-later",
                "target_act": "act-iii",
                "statement": "The accepted gift should create a later institutional or dragon obligation to test.",
                "confidence": 0.62,
            }],
            "backward_requirements": [{
                "id": "reciprocity-setup",
                "target_act": "act-i",
                "statement": "The bargain needs enough reciprocal logic established for the gift not to read as random loot.",
                "confidence": 0.6,
            }],
            "unresolved_questions": ["What exact obligation attaches to the gift?"],
        }
        reduced = rehearsal.reduce_rehearsal_result(result)
        self.assertNotIn("transcript", reduced)
        self.assertEqual("Accepting the gift behaves like accepting an obligation.", reduced["finding"])
        self.assertEqual("support", reduced["story_sync_evidence"]["kind"])
        delta_types = [item["type"] for item in reduced["derived_deltas"]]
        self.assertIn("forward_consequence", delta_types)
        self.assertIn("backward_requirement", delta_types)
        self.assertIn("local_unresolved_question", delta_types)

    def test_challenging_result_becomes_contradiction_evidence_not_forced_success(self):
        result = {
            "schema": rehearsal.REHEARSAL_RESULT_SCHEMA,
            "target_id": "trust-bridge",
            "source_act": "act-ii",
            "experiment_mode": "performance",
            "heat": "high_heat",
            "outcome": "challenge",
            "finding": "Under the proposed pressure she trusts him less, not more.",
            "confidence": 0.76,
            "independent_group": "trust-bridge-challenge",
            "dramatic_uses": ["relationship", "character"],
            "regions": ["act-ii", "act-iii"],
            "provenance": "performance:trust-bridge:take-2",
            "behavior_discovered": ["She interprets his improvisation as concealment."],
            "relationship_movement": ["distrust deepens"],
            "forward_consequences": [],
            "backward_requirements": [],
            "unresolved_questions": ["Is the desired Act III intimacy boundary wrong?"],
        }
        reduced = rehearsal.reduce_rehearsal_result(result)
        self.assertEqual("contradiction", reduced["story_sync_evidence"]["kind"])
        self.assertEqual("challenge", reduced["outcome"])

    def test_temporal_distance_rehearsal_is_available_without_forcing_performance(self):
        target = rehearsal.build_rehearsal_target(
            target_id="worldline-romance",
            acts=["act-i", "act-iii", "act-iv"],
            source_type="trajectory_question",
            source_id="romance-worldline",
            uncertainty="Do early, middle, and late relationship states form one plausible worldline?",
            experiment_mode="temporal_distance_rehearsal",
            heat="development",
            provenance=["trajectory-compile"],
        )
        self.assertEqual("temporal_distance_rehearsal", target["experiment_mode"])
        self.assertEqual("development", target["heat"])


if __name__ == "__main__":
    unittest.main()
