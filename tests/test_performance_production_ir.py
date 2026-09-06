import unittest

from scripts import performance_production_funnel as funnel


class PerformanceProductionIRTests(unittest.TestCase):
    def _scene(self):
        return {
            "scene_id": "214.s010",
            "source": {
                "hash": "source-a",
                "chapter": 214,
                "paragraph_span": [10, 14],
                "start_anchor": "Greg lifted the box.",
                "end_anchor": "Antonius returned to the broom.",
                "paragraphs": ["SECRET SOURCE PAYLOAD"],
            },
            "mechanical": {
                "dialogue_turns": 8,
                "dialogue_ratio": 0.55,
                "question_count": 3,
                "money_mentions": ["five silver"],
                "capitalized_tokens": ["Antonius", "Greg"],
                "action_word_hits": 5,
            },
            "dependencies": {},
        }

    def test_validate_claim_requires_epistemic_kind(self):
        with self.assertRaisesRegex(ValueError, "kind"):
            funnel.validate_claim({"value": "recover leverage"})
        with self.assertRaisesRegex(ValueError, "kind"):
            funnel.validate_claim({"value": "recover leverage", "kind": "canon"})

    def test_inferred_claim_requires_valid_confidence_and_compiler(self):
        with self.assertRaisesRegex(ValueError, "confidence"):
            funnel.validate_claim({"value": "recover leverage", "kind": "inferred", "compiler": "scene-semantic/v1"})
        with self.assertRaisesRegex(ValueError, "compiler"):
            funnel.validate_claim({"value": "recover leverage", "kind": "inferred", "confidence": 0.8})
        funnel.validate_claim({"value": "recover leverage", "kind": "inferred", "confidence": 0.8, "compiler": "scene-semantic/v1"})

    def test_locked_derived_claim_is_not_silently_overwritten(self):
        scene = self._scene()
        scene["semantic"] = {
            "goal": {
                "value": "finish cleanup",
                "kind": "locked_derived",
                "compiler": "roundtrip/archive-v1",
                "provenance": "performance-roundtrip/007",
            }
        }
        updated = funnel.merge_derived_layer(
            scene,
            "semantic",
            {
                "goal": {
                    "value": "maximize sale value",
                    "kind": "inferred",
                    "confidence": 0.83,
                    "compiler": "scene-semantic/v1",
                }
            },
            compiler="scene-semantic/v1",
            dependency_hash="dep-1",
        )
        self.assertEqual("finish cleanup", updated["semantic"]["goal"]["value"])
        self.assertEqual("semantic.goal", updated["semantic_conflicts"][0]["field"])
        self.assertEqual("maximize sale value", updated["semantic_conflicts"][0]["candidate"]["value"])

    def test_material_inferred_disagreement_is_preserved_as_conflict(self):
        scene = self._scene()
        scene["semantic"] = {
            "relationship_pressure": {
                "value": "buyer-specific value",
                "kind": "inferred",
                "confidence": 0.72,
                "compiler": "scene-semantic/v1",
            }
        }
        updated = funnel.merge_derived_layer(
            scene,
            "semantic",
            {
                "relationship_pressure": {
                    "value": "cleanup impatience",
                    "kind": "inferred",
                    "confidence": 0.75,
                    "compiler": "scene-semantic/v1",
                }
            },
            compiler="scene-semantic/v1",
            dependency_hash="dep-2",
        )
        self.assertEqual("buyer-specific value", updated["semantic"]["relationship_pressure"]["value"])
        self.assertEqual(1, len(updated["semantic_conflicts"]))

    def test_task_views_are_narrow_and_never_copy_full_source_paragraphs(self):
        scene = self._scene()
        scene["semantic"] = {
            "active_task": {"value": "storeroom sorting", "kind": "inferred", "confidence": 0.95, "compiler": "scene-semantic/v1"},
            "relationship_pressure": {"value": "Greg reveals buyer-specific value", "kind": "inferred", "confidence": 0.9, "compiler": "scene-semantic/v1"},
            "required_outcome": {"value": ["item retained", "price rises"], "kind": "locked_derived", "compiler": "roundtrip/archive-v1"},
            "continuity": {"value": {"money": ["five silver"]}, "kind": "inferred", "confidence": 0.8, "compiler": "scene-semantic/v1"},
            "location": {"value": "storeroom", "kind": "inferred", "confidence": 0.9, "compiler": "scene-semantic/v1"},
            "objects": {"value": ["box", "broom"], "kind": "observed"},
        }
        scene["performance"] = {
            "greg": {"value": {"stance": "recover leverage"}, "kind": "inferred", "confidence": 0.9, "compiler": "performance/v1"}
        }

        for view_name in ("performance", "dialogue", "continuity", "illustration", "comparison"):
            view = funnel.render_scene_view(scene, view_name)
            self.assertEqual("214.s010", view["scene_id"])
            self.assertNotIn("paragraphs", str(view))
            self.assertNotIn("SECRET SOURCE PAYLOAD", str(view))
            self.assertLess(len(str(view)), len(str(scene)))

        performance = funnel.render_scene_view(scene, "performance")
        self.assertIn("performance", performance)
        self.assertIn("relationship_pressure", performance["semantic"])

        dialogue = funnel.render_scene_view(scene, "dialogue")
        self.assertIn("dialogue_turns", dialogue["mechanical"])
        self.assertNotIn("money_mentions", dialogue["mechanical"])

        continuity = funnel.render_scene_view(scene, "continuity")
        self.assertIn("money_mentions", continuity["mechanical"])
        self.assertIn("continuity", continuity["semantic"])

        illustration = funnel.render_scene_view(scene, "illustration")
        self.assertIn("location", illustration["semantic"])
        self.assertIn("objects", illustration["semantic"])

    def test_unknown_view_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown scene view"):
            funnel.render_scene_view(self._scene(), "everything")


if __name__ == "__main__":
    unittest.main()
