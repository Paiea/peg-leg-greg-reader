import json
import tempfile
import unittest
from pathlib import Path

from scripts import rehearsal_engine as engine


def actor(actor_id="actor.nico.v1", role="Greg", actor_name="Nico"):
    return {
        "actor_id": actor_id,
        "actor_name": actor_name,
        "role": role,
        "status": "selected",
        "casting_authority": "Mana",
        "user_anchors": [{"value": "disheveled intensity", "provenance": "user_casting_anchor"}],
        "derived_interpretation": [{"value": "practical systems curiosity", "provenance": "character_bible"}],
        "visual": {"status": "candidate", "era_sensitive": True, "thumbnail_distinctness_required": True},
    }


def registry():
    return {"schema": engine.ACTOR_SCHEMA, "director": "Mana", "actors": [actor()]}


class RehearsalEngineTests(unittest.TestCase):
    def test_load_and_role_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "actors.json"
            path.write_text(json.dumps(registry()), encoding="utf-8")
            loaded = engine.load_actor_registry(path)
            self.assertEqual("Nico", engine.actor_for_role(loaded, "Greg")["actor_name"])

    def test_registry_rejects_duplicate_actor_id(self):
        value = registry()
        value["actors"].append(actor(actor_id="actor.nico.v1", role="Lyssa", actor_name="Imani"))
        with self.assertRaisesRegex(ValueError, "duplicate actor_id"):
            engine.validate_actor_registry(value)

    def test_registry_rejects_duplicate_role_binding(self):
        value = registry()
        value["actors"].append(actor(actor_id="actor.imani.v1", role="Greg", actor_name="Imani"))
        with self.assertRaisesRegex(ValueError, "duplicate role binding"):
            engine.validate_actor_registry(value)

    def test_registry_requires_user_anchor_provenance(self):
        value = registry()
        value["actors"][0]["user_anchors"][0]["provenance"] = "generated"
        with self.assertRaisesRegex(ValueError, "user_casting_anchor"):
            engine.validate_actor_registry(value)

    def test_actor_packet_keeps_user_anchor_and_scene_visual_override(self):
        packet = engine.compile_actor_packet(
            actor(),
            scene_id="007.s010",
            role_context={
                "objective": "get Antonius to answer",
                "visual_state": {"mobility": "left BKA, two crutches, no peg"},
            },
            promoted_tendencies=[{"value": "watches hands before faces", "source": "chapters/007.html"}],
        )
        self.assertEqual("disheveled intensity", packet["user_anchors"][0]["value"])
        self.assertEqual("left BKA, two crutches, no peg", packet["visual_state"]["mobility"])
        self.assertEqual("promoted_tendency", packet["promoted_tendencies"][0]["provenance"])
        self.assertNotIn("history", packet)

    def test_rehearsal_packet_requires_unique_role_ownership(self):
        packet = engine.compile_actor_packet(actor(), scene_id="007.s010", role_context={})
        with self.assertRaisesRegex(ValueError, "unique actor role ownership"):
            engine.build_rehearsal_packet({"scene_id": "007.s010"}, {}, [packet, packet])

    def test_rehearsal_packet_exposes_locked_and_unlocked_surfaces(self):
        packet = engine.compile_actor_packet(actor(), scene_id="007.s010", role_context={})
        rehearsal = engine.build_rehearsal_packet(
            {"scene_id": "007.s010", "source": {"hash": "abc"}},
            {"required_result": "Antonius keeps control of the task"},
            [packet],
        )
        self.assertIn("facts", rehearsal["freedom"]["locked"])
        self.assertIn("movement", rehearsal["freedom"]["unlocked"])
        self.assertEqual("Preserve canon truth, not source choreography.", rehearsal["director_instruction"])

    def test_discovery_validation_and_self_confirmation_filter(self):
        engine.validate_discovery({
            "scene_id": "007.s010",
            "kind": "movement",
            "finding": "Antonius can keep sorting while Greg talks.",
            "provenance_class": "rehearsal_hypothesis",
            "dramatic_lock_status": "preserved",
            "support": ["take-1"],
        })
        evidence = [
            {"type": "rehearsal", "source": "take-1"},
            {"type": "rehearsal", "source": "take-2"},
            {"type": "canon", "source": "chapters/007.html#p4"},
            {"type": "canon", "source": "chapters/007.html#p4"},
            {"type": "accepted_prose", "source": "chapters/022.html#p9"},
        ]
        self.assertEqual(2, engine.independent_support_count(evidence))

    def test_overtuned_calibration_policy_allows_scene_rebuilds_on_non_main_branch(self):
        policy = engine.editorial_return_policy("overtuned_calibration")
        self.assertTrue(policy["actor_preference_can_trigger_write"])
        self.assertTrue(policy["branch_canon_write_authorized"])
        self.assertEqual("scene_rebuild", policy["max_local_scope"])
        self.assertFalse(policy["production_safe"])
        self.assertIn("tone", policy["soft_surfaces"])
        self.assertIn("plot", policy["hard_surfaces"])

    def test_overtuned_auto_apply_requires_all_gates_and_soft_surfaces(self):
        policy = engine.editorial_return_policy("overtuned_calibration")
        candidate = {
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "source_match": True,
            "target_branch": "editor/rehearsal-simulation-engine",
            "changed_surfaces": ["movement", "dialogue", "tone", "paragraphing"],
        }
        self.assertTrue(engine.can_auto_apply_rehearsal_candidate(candidate, policy))
        self.assertFalse(engine.can_auto_apply_rehearsal_candidate(dict(candidate, changed_surfaces=["movement", "plot"]), policy))
        self.assertFalse(engine.can_auto_apply_rehearsal_candidate(dict(candidate, target_branch="main"), policy))
        self.assertFalse(engine.can_auto_apply_rehearsal_candidate(dict(candidate, reader_check="fail"), policy))

    def test_free_is_default_and_directed_requires_direction(self):
        packet = engine.compile_actor_packet(actor(), scene_id="007.s010", role_context={})
        rehearsal = engine.build_rehearsal_packet({"scene_id": "007.s010"}, {}, [packet])
        self.assertEqual("free", rehearsal["mode"])
        with self.assertRaisesRegex(ValueError, "direction"):
            engine.build_rehearsal_packet(
                {"scene_id": "007.s010"}, {}, [packet], mode="directed", take_id="directed-1"
            )

    def test_production_policy_keeps_high_authority_off_main(self):
        policy = engine.editorial_return_policy("production")
        candidate = {
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "source_match": True,
            "target_branch": "editor/rehearsal-simulation-engine",
            "changed_surfaces": ["movement", "dialogue", "tone", "paragraphing"],
        }
        self.assertTrue(policy["actor_preference_can_trigger_write"])
        self.assertEqual("scene_rebuild", policy["max_local_scope"])
        self.assertTrue(engine.can_auto_apply_rehearsal_candidate(candidate, policy))
        self.assertFalse(engine.can_auto_apply_rehearsal_candidate(dict(candidate, target_branch="main"), policy))

    def test_relationship_memory_is_directional_and_lane_separated(self):
        memory = {
            "schema": engine.RELATIONSHIP_MEMORY_SCHEMA,
            "relationships": {
                "Antonius::Greg": {
                    "supported": [
                        {"value": "waits Greg out", "source_type": "canon", "source": "chapters/005.html"}
                    ],
                    "hypothesis": [
                        {
                            "value": "privately amused by Greg's bluff",
                            "source_type": "rehearsal",
                            "source": "take-x",
                            "kind": "private_interpretation",
                        }
                    ],
                }
            },
        }
        engine.validate_relationship_memory_registry(memory)
        compiled = engine.relationship_memory_for(memory, "Antonius", ["Greg"])
        self.assertEqual("waits Greg out", compiled["supported"][0]["value"])
        self.assertEqual("privately amused by Greg's bluff", compiled["hypothesis"][0]["value"])
        self.assertEqual({}, engine.relationship_memory_for(memory, "Greg", ["Antonius"]))

    def test_synthetic_private_interpretation_cannot_enter_supported_memory(self):
        memory = {
            "schema": engine.RELATIONSHIP_MEMORY_SCHEMA,
            "relationships": {
                "Hessa::Greg": {
                    "supported": [
                        {
                            "value": "privately suspects Greg is hiding something",
                            "source_type": "rehearsal",
                            "source": "take-a",
                            "kind": "private_interpretation",
                        }
                    ],
                    "hypothesis": [],
                }
            },
        }
        with self.assertRaisesRegex(ValueError, "supported"):
            engine.validate_relationship_memory_registry(memory)

    def test_greg_and_non_greg_receive_distinct_private_channels(self):
        greg_packet = engine.compile_actor_packet(actor(), scene_id="005.s001", role_context={})
        hessa_packet = engine.compile_actor_packet(
            actor(actor_id="actor.mara.v1", role="Hessa", actor_name="Mara"),
            scene_id="018.s001",
            role_context={},
        )
        self.assertEqual(["body", "voice", "inner_voice"], greg_packet["performance_channels"])
        self.assertEqual(["body", "voice", "private_inner_voice"], hessa_packet["performance_channels"])

    def test_private_inner_performance_is_actor_interpretation_not_character_truth(self):
        output = {
            "actor_name": "Mara",
            "role": "Hessa",
            "body": [],
            "voice": [],
            "private_inner_voice": [
                {
                    "form": "wrong_inference",
                    "value": "Greg is hiding something.",
                    "authority": "performed_interpretation",
                }
            ],
        }
        engine.validate_performance_output(output)
        self.assertNotIn("character_thinks", output)

    def test_private_cognition_accepts_non_sentence_forms(self):
        output = {
            "actor_name": "Nico",
            "role": "Greg",
            "body": [],
            "voice": [],
            "inner_voice": [
                {"form": "image", "value": "ledger / red numbers", "authority": "performed_interpretation"},
                {"form": "memory_fragment", "value": "hand on table", "authority": "performed_interpretation"},
                {"form": "impulse", "value": "push", "authority": "performed_interpretation"},
                {"form": "calculation", "value": "today != total", "authority": "performed_interpretation"},
                {"form": "sensory_hook", "value": "broom bristles stop", "authority": "performed_interpretation"},
                {"form": "unfinished_thought", "value": "If he already...", "authority": "performed_interpretation"},
            ],
        }
        engine.validate_performance_output(output)

    def test_other_actor_cannot_observe_private_thought_and_novelizer_only_gets_greg_inner_voice(self):
        greg = {
            "actor_name": "Nico",
            "role": "Greg",
            "body": [{"kind": "hesitation", "value": "hand pauses"}],
            "voice": [{"value": "Same thing."}],
            "inner_voice": [
                {"form": "wrong_inference", "value": "He bought it.", "authority": "performed_interpretation"}
            ],
        }
        hessa = {
            "actor_name": "Mara",
            "role": "Hessa",
            "body": [{"kind": "touch", "value": "two fingers stay on wrist"}],
            "voice": [{"value": "No."}],
            "private_inner_voice": [
                {"form": "impulse", "value": "do not reward this", "authority": "performed_interpretation"}
            ],
        }
        antonius_view = engine.actor_observable_view(greg, observer_role="Antonius")
        self.assertIn("body", antonius_view)
        self.assertIn("voice", antonius_view)
        self.assertNotIn("inner_voice", antonius_view)
        self.assertNotIn("private_inner_voice", engine.actor_observable_view(hessa, observer_role="Greg"))
        self.assertIn("inner_voice", engine.novelizer_performance_view(greg))
        self.assertNotIn("private_inner_voice", engine.novelizer_performance_view(hessa))

    def test_private_thought_cannot_grant_unsupported_knowledge(self):
        hessa_packet = engine.compile_actor_packet(
            actor(actor_id="actor.mara.v1", role="Hessa", actor_name="Mara"),
            scene_id="018.s001",
            role_context={"knowledge": ["Greg is injured", "the bean exercise has a stop condition"]},
        )
        output = {
            "actor_name": "Mara",
            "role": "Hessa",
            "body": [],
            "voice": [],
            "private_inner_voice": [
                {
                    "form": "recognition",
                    "value": "Greg hid the missing coin in Antonius's roof.",
                    "authority": "performed_interpretation",
                    "uses_knowledge": ["Greg hid the missing coin in Antonius's roof"],
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "unsupported knowledge"):
            engine.validate_performance_output(output, actor_packet=hessa_packet)

    def test_observed_inputs_cannot_reference_another_actors_private_channel(self):
        output = {
            "actor_name": "Desmond",
            "role": "Antonius",
            "body": [],
            "voice": [],
            "private_inner_voice": [],
            "observed_inputs": [
                {"role": "Greg", "source_channel": "inner_voice", "value": "He bought it."}
            ],
        }
        with self.assertRaisesRegex(ValueError, "private channel"):
            engine.validate_performance_output(output)

    def test_variance_siblings_share_frozen_memory_and_cannot_see_each_other(self):
        takes = [
            engine.build_take_spec("free", take_id="free-a", memory_snapshot_id="mem-1", variance_group_id="v1"),
            engine.build_take_spec("free", take_id="free-b", memory_snapshot_id="mem-2", variance_group_id="v1"),
        ]
        with self.assertRaisesRegex(ValueError, "memory snapshot"):
            engine.validate_variance_group(takes)

        contaminated = [
            {
                "mode": "free",
                "take_id": "free-a",
                "variance_group_id": "v1",
                "memory_snapshot_id": "mem-1",
                "sibling_take_context": ["free-b"],
            }
        ]
        with self.assertRaisesRegex(ValueError, "sibling"):
            engine.validate_variance_group(contaminated)

    def test_variance_strengthens_observable_behavior_not_private_motive(self):
        takes = [
            {
                "mode": "free",
                "take_id": "free-a",
                "variance_group_id": "hessa-018",
                "memory_snapshot_id": "mem-hessa-018",
                "observable_findings": ["controls_lesson", "checks_wrist"],
                "private_interpretations": ["safety_responsibility"],
            },
            {
                "mode": "free",
                "take_id": "free-b",
                "variance_group_id": "hessa-018",
                "memory_snapshot_id": "mem-hessa-018",
                "observable_findings": ["controls_lesson", "checks_wrist"],
                "private_interpretations": ["suspicion_of_withholding"],
            },
        ]
        engine.validate_variance_group(takes)
        stable = engine.stable_variance_findings(takes)
        self.assertEqual(
            [
                {"finding": "checks_wrist", "support_count": 2, "authority": "rehearsal_evidence"},
                {"finding": "controls_lesson", "support_count": 2, "authority": "rehearsal_evidence"},
            ],
            stable,
        )
        self.assertNotIn("safety_responsibility", json.dumps(stable))
        self.assertNotIn("suspicion_of_withholding", json.dumps(stable))


if __name__ == "__main__":
    unittest.main()
