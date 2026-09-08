import copy
import unittest

from scripts import persistent_act_runtime as runtime


class PersistentActRuntimeTests(unittest.TestCase):
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
            "story_id": "dragon-spotter",
            "acts": {
                "act-i": {
                    "state_in": [self._boundary("a1-in-role", "professional_role", "disgraced-spotter", 0.8)],
                    "local_state": {
                        "possibilities": [{"id": "a1-bargain-a", "status": "active"}],
                        "discoveries": [{"id": "a1-hide-attention", "finding": "Public attention makes concealment attractive."}],
                        "unresolved_questions": ["What does the first dragon concretely want?"],
                        "constraint_responses": [],
                    },
                    "state_out": [
                        self._boundary("a1-out-trust", "guild_trust", "conditional", 0.55),
                        self._boundary("a1-out-secret", "ability_visibility", "concealed", 0.5),
                    ],
                },
                "act-ii": {
                    "state_in": [self._boundary("a2-in-trust", "guild_trust", "conditional", 0.55)],
                    "local_state": {
                        "possibilities": [{"id": "a2-politics-a", "status": "active"}],
                        "discoveries": [],
                        "unresolved_questions": ["Who contests the bargain first?"],
                        "constraint_responses": [],
                    },
                    "state_out": [self._boundary("a2-out-trust", "guild_trust", "broken", 0.7)],
                },
                "act-iii": {
                    "state_in": [self._boundary("a3-in-trust", "guild_trust", "dependent", 0.7)],
                    "local_state": {
                        "possibilities": [{"id": "a3-alliance-a", "status": "active"}],
                        "discoveries": [],
                        "unresolved_questions": ["Can political reliance coexist with personal distrust?"],
                        "constraint_responses": [],
                    },
                    "state_out": [self._boundary("a3-out-partnership", "romantic_trust", "earned", 0.65)],
                },
                "act-iv": {
                    "state_in": [self._boundary("a4-in-partnership", "romantic_trust", "earned", 0.65)],
                    "local_state": {
                        "possibilities": [{"id": "a4-ending-reveal", "status": "active"}],
                        "discoveries": [{"id": "a4-late-reveal", "finding": "A concealed capability becomes publicly revealed."}],
                        "unresolved_questions": ["What ending identity survives the final bargain?"],
                        "constraint_responses": [],
                    },
                    "state_out": [self._boundary("a4-out-role", "professional_role", "dragon-recognized-envoy", 0.45)],
                },
            },
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
                "forward_consequences": [
                    {
                        "id": "a1-to-a4-secret",
                        "kind": "forward_consequence",
                        "source_act": "act-i",
                        "target_act": "act-iv",
                        "statement": "If concealment persists, public revelation remains available as a late consequence.",
                        "confidence": 0.55,
                        "provenance": ["act-i:a1-hide-attention"],
                        "status": "open",
                    }
                ],
                "backward_requirements": [
                    {
                        "id": "a4-to-a1-trust-fracture",
                        "kind": "backward_requirement",
                        "source_act": "act-iv",
                        "target_act": "act-i",
                        "statement": "A late public defense needs an earlier trust fracture worth repairing.",
                        "confidence": 0.6,
                        "provenance": ["act-iv:a4-ending-reveal"],
                        "status": "open",
                    }
                ],
                "cross_direction_agreements": [
                    {
                        "id": "concealment-reveal-agreement",
                        "acts": ["act-i", "act-iv"],
                        "statement": "Early concealment and late revelation independently support the same long-range thread.",
                        "confidence": 0.55,
                        "provenance": ["act-i:a1-hide-attention", "act-iv:a4-late-reveal"],
                    }
                ],
                "contradictions": [],
            },
        }

    def test_requires_exactly_four_persistent_temporal_slabs(self):
        state = self._runtime()
        runtime.validate_runtime(state)
        broken = copy.deepcopy(state)
        del broken["acts"]["act-iii"]
        with self.assertRaisesRegex(ValueError, "four persistent act channels"):
            runtime.validate_runtime(broken)

    def test_each_act_requires_state_in_local_search_and_state_out(self):
        state = self._runtime()
        broken = copy.deepcopy(state)
        del broken["acts"]["act-ii"]["state_out"]
        with self.assertRaisesRegex(ValueError, "state_out"):
            runtime.validate_runtime(broken)

    def test_local_beliefs_remain_local_and_do_not_become_shared_truth(self):
        state = self._runtime()
        packet = runtime.compile_act_packet(state, "act-i")
        self.assertEqual(["a1-bargain-a"], [item["id"] for item in packet["local_state"]["possibilities"]])
        self.assertNotIn("a1-bargain-a", packet["shared_story_truths"])
        self.assertNotIn("a1-hide-attention", packet["shared_story_truths"])

    def test_act_iv_backward_requirement_reaches_act_i_without_mutating_local_state(self):
        state = self._runtime()
        before = copy.deepcopy(state["acts"]["act-i"])
        packet = runtime.compile_act_packet(state, "act-i")
        self.assertEqual(["a4-to-a1-trust-fracture"], [item["id"] for item in packet["incoming_backward_requirements"]])
        self.assertEqual(before, state["acts"]["act-i"])

    def test_long_range_forward_consequence_can_skip_directly_from_act_i_to_act_iv(self):
        packet = runtime.compile_act_packet(self._runtime(), "act-iv")
        self.assertEqual(["a1-to-a4-secret"], [item["id"] for item in packet["incoming_forward_consequences"]])

    def test_adjacent_boundary_mismatch_surfaces_instead_of_being_smoothed(self):
        contradictions = runtime.boundary_contradictions(self._runtime())
        trust = [item for item in contradictions if item["dimension"] == "guild_trust"]
        self.assertEqual(1, len(trust))
        self.assertEqual("act-ii", trust[0]["source_act"])
        self.assertEqual("act-iii", trust[0]["target_act"])
        self.assertEqual("broken", trust[0]["source_value"])
        self.assertEqual("dependent", trust[0]["target_value"])

    def test_relationship_boundary_jump_becomes_rehearsal_target(self):
        state = self._runtime()
        state["acts"]["act-ii"]["state_out"].append(
            self._boundary("a2-out-romance", "romantic_trust", "distrust", 0.7)
        )
        state["acts"]["act-iii"]["state_in"].append(
            self._boundary("a3-in-romance", "romantic_trust", "intimate-team", 0.7)
        )
        closure = runtime.constraint_closure(state)
        targets = [item for item in closure["rehearsal_targets"] if item["kind"] == "behavioral_bridge"]
        self.assertTrue(any(item["dimension"] == "romantic_trust" for item in targets))

    def test_conflicting_constraint_response_stays_open_and_gets_extra_attention(self):
        state = self._runtime()
        state["acts"]["act-i"]["local_state"]["constraint_responses"].append(
            {
                "message_id": "a4-to-a1-trust-fracture",
                "response": "conflict",
                "reason": "Current Act I relationship trajectory does not naturally fracture trust yet.",
            }
        )
        closure = runtime.constraint_closure(state)
        collision_ids = [item["message_id"] for item in closure["constraint_collisions"]]
        self.assertIn("a4-to-a1-trust-fracture", collision_ids)
        schedule = runtime.schedule_work(state)
        extras = [item for item in schedule if item["kind"] == "constraint_collision"]
        self.assertTrue(any(item["act"] == "act-i" for item in extras))

    def test_cross_direction_agreement_increases_attention_without_promotion(self):
        state = self._runtime()
        schedule = runtime.schedule_work(state)
        agreement_work = [item for item in schedule if item["kind"] == "cross_direction_agreement"]
        self.assertTrue(agreement_work)
        report = runtime.sync_shared_story(state)
        self.assertNotIn("concealment-reveal-agreement", report["story_truths"])

    def test_scheduler_never_starves_an_act_even_during_convergence(self):
        state = self._runtime()
        state["shared_story_state"]["sync_state"]["story_confidence"] = 0.92
        schedule = runtime.schedule_work(state)
        baseline = [item for item in schedule if item["kind"] == "baseline_local_search"]
        self.assertEqual({"act-i", "act-ii", "act-iii", "act-iv"}, {item["act"] for item in baseline})
        self.assertTrue(all(item["budget"] > 0 for item in baseline))

    def test_sync_shared_story_delegates_discovery_maturity_to_story_sync(self):
        state = self._runtime()
        state["shared_story_state"]["sync_state"]["discoveries"] = [
            {
                "id": "shared-thread",
                "finding": "A reciprocal gift creates obligation.",
                "evidence": [
                    {"source_id": "a", "independent_group": "act-i", "kind": "support", "dramatic_uses": ["plot", "world", "character"], "regions": ["act-i"]},
                    {"source_id": "b", "independent_group": "act-iii", "kind": "support", "dramatic_uses": ["plot", "relationship", "setup_payoff"], "regions": ["act-iii"]},
                ],
            }
        ]
        report = runtime.sync_shared_story(state)
        self.assertEqual("strong_thread", report["discovery_levels"]["shared-thread"])

    def test_temporal_consistency_reports_open_boundary_and_long_range_work(self):
        report = runtime.temporal_consistency(self._runtime())
        self.assertEqual(3, report["adjacent_boundary_pairs"])
        self.assertGreaterEqual(report["boundary_contradiction_count"], 1)
        self.assertEqual(2, report["open_long_range_messages"])
        self.assertEqual("open", report["trajectory_status"])

    def test_temporal_consistency_improves_when_boundary_and_messages_close(self):
        state = self._runtime()
        before = runtime.temporal_consistency(state)
        state["acts"]["act-iii"]["state_in"] = [
            self._boundary("a3-in-trust-fixed", "guild_trust", "broken", 0.75)
        ]
        for collection in ("forward_consequences", "backward_requirements"):
            for item in state["shared_story_state"][collection]:
                item["status"] = "closed"
        after = runtime.temporal_consistency(state)
        self.assertLess(after["boundary_contradiction_count"], before["boundary_contradiction_count"])
        self.assertLess(after["open_long_range_messages"], before["open_long_range_messages"])


if __name__ == "__main__":
    unittest.main()
