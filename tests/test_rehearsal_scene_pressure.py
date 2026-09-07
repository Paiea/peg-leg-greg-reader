import unittest

from scripts import rehearsal_engine as engine


def actor(actor_id="actor.mara.v1", role="Hessa", actor_name="Mara"):
    return {
        "actor_id": actor_id,
        "actor_name": actor_name,
        "role": role,
        "status": "selected",
        "casting_authority": "Mana",
        "user_anchors": [],
        "derived_interpretation": [],
        "visual": {"status": "candidate", "era_sensitive": True, "thumbnail_distinctness_required": True},
    }


class ScenePressureTests(unittest.TestCase):
    def test_actor_packet_carries_compact_scene_pressure_context(self):
        packet = engine.compile_actor_packet(
            actor(),
            scene_id="018.s001",
            role_context={
                "knowledge": ["Greg is injured"],
                "pressure_context": {
                    "goal": "keep Greg from hurting himself",
                    "concealment": "do not show how worried she is",
                    "belief": "Greg is underestimating the risk",
                    "pressure": ["physical_safety", "time_pressure"],
                    "resources": ["procedure authority", "physical proximity"],
                    "observable_access": ["Greg's wrist", "Greg's speech", "Arlo's visible reaction"],
                },
            },
        )
        pressure = packet["scene"]["pressure_context"]
        self.assertEqual("keep Greg from hurting himself", pressure["goal"])
        self.assertEqual(["physical_safety", "time_pressure"], pressure["pressure"])
        self.assertLessEqual(len([key for key, value in pressure.items() if value not in (None, [], "")]), 6)

    def test_pressure_context_rejects_observable_access_to_private_channels(self):
        with self.assertRaisesRegex(ValueError, "observable"):
            engine.compile_actor_packet(
                actor(),
                scene_id="018.s001",
                role_context={
                    "pressure_context": {
                        "goal": "control the lesson",
                        "observable_access": ["Greg.inner_voice"],
                    }
                },
            )

    def test_behavioral_discovery_records_behavior_under_conditions_not_trait_only(self):
        discovery = engine.build_behavioral_discovery(
            source="chapters/018.html#bean-exercise",
            actor_name="Mara",
            role="Hessa",
            relationship="Hessa::Greg",
            pressure_tags=["physical_safety", "deflection"],
            observed_behavior="takes direct control of the task before explaining herself",
            take_id="018-free-a",
            support_count=1,
        )
        self.assertEqual("hypothesis", discovery["status"])
        self.assertEqual(["physical_safety", "deflection"], discovery["pressure_tags"])
        self.assertIn("direct control", discovery["observed_behavior"])
        self.assertNotIn("trait", discovery)

    def test_behavioral_discovery_requires_pressure_conditions(self):
        with self.assertRaisesRegex(ValueError, "pressure"):
            engine.build_behavioral_discovery(
                source="probe:hessa-dangerous-clever",
                actor_name="Mara",
                role="Hessa",
                relationship="Hessa::Greg",
                pressure_tags=[],
                observed_behavior="stops Greg physically",
                take_id="probe-free-a",
                support_count=1,
            )

    def test_character_probe_is_explicitly_non_authoritative(self):
        probe = engine.build_character_probe(
            probe_id="dangerous-clever-suggestion",
            premise="Greg proposes an obviously dangerous but technically clever shortcut.",
            actor_packets=[
                engine.compile_actor_packet(actor(), scene_id="probe.dangerous-clever", role_context={})
            ],
            memory_snapshot_id="probe-memory-1",
        )
        self.assertFalse(probe["authoritative"])
        self.assertEqual("character_probe", probe["kind"])
        self.assertEqual("free", probe["mode"])
        self.assertEqual("probe-memory-1", probe["memory_snapshot_id"])

    def test_probe_repetition_does_not_create_independent_support(self):
        evidence = [
            {"type": "probe", "source": "probe:hessa-dangerous-clever:a"},
            {"type": "probe", "source": "probe:hessa-dangerous-clever:b"},
            {"type": "rehearsal", "source": "take-018-a"},
        ]
        self.assertEqual(0, engine.independent_support_count(evidence))

    def test_survival_outcome_logs_why_rehearsal_reached_or_did_not_reach_prose(self):
        accepted = engine.build_rehearsal_outcome(
            source_id="018-free-a:hessa-control",
            chapter=18,
            role="Hessa",
            result="accepted",
            reasons=["behavioral_specificity", "physical_ownership", "subtext"],
        )
        rejected = engine.build_rehearsal_outcome(
            source_id="018-free-b:hessa-explains-too-much",
            chapter=18,
            role="Hessa",
            result="rejected",
            reasons=["rejected_overperformance"],
        )
        self.assertEqual("accepted", accepted["result"])
        self.assertIn("physical_ownership", accepted["reasons"])
        self.assertEqual(["rejected_overperformance"], rejected["reasons"])

    def test_outcome_reason_vocabulary_rejects_unknown_router_like_reason(self):
        with self.assertRaisesRegex(ValueError, "outcome reason"):
            engine.build_rehearsal_outcome(
                source_id="005-free-a",
                chapter=5,
                role="Greg",
                result="accepted",
                reasons=["auto_route_this_scene"],
            )


if __name__ == "__main__":
    unittest.main()
