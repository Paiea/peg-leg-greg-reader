import json
import tempfile
import unittest
from pathlib import Path

from scripts import rehearsal_engine as engine


def actor(actor_id="actor.nico.v1", role="Greg"):
    return {
        "actor_id": actor_id,
        "actor_name": "Nico",
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
        value["actors"].append(actor(actor_id="actor.nico.v1", role="Lyssa"))
        with self.assertRaisesRegex(ValueError, "duplicate actor_id"):
            engine.validate_actor_registry(value)

    def test_registry_rejects_duplicate_role_binding(self):
        value = registry()
        second = actor(actor_id="actor.imani.v1", role="Greg")
        second["actor_name"] = "Imani"
        value["actors"].append(second)
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

        hard_change = dict(candidate, changed_surfaces=["movement", "plot"])
        self.assertFalse(engine.can_auto_apply_rehearsal_candidate(hard_change, policy))

        main_write = dict(candidate, target_branch="main")
        self.assertFalse(engine.can_auto_apply_rehearsal_candidate(main_write, policy))

        failed_reader = dict(candidate, reader_check="fail")
        self.assertFalse(engine.can_auto_apply_rehearsal_candidate(failed_reader, policy))


if __name__ == "__main__":
    unittest.main()
