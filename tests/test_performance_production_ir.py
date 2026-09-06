import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

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

    def test_every_scene_can_carry_screenplay_without_a_screen_gate(self):
        scene = self._scene()
        updated = funnel.set_screenplay_result(
            scene,
            "GREG: Five silver?\nANTONIUS [returns to broom]: End of week.",
            compiler="screenplay/v1",
            dependency_hash="perf-dep",
        )
        self.assertEqual("generated_output", updated["screenplay"]["kind"])
        self.assertIn("GREG: Five silver?", updated["screenplay"]["content"])
        self.assertEqual("screenplay/v1", updated["dependencies"]["screenplay"]["compiler"])
        self.assertNotIn("screen", updated)
        funnel.validate_scene_record(updated)

    def test_source_win_is_valid_after_screenplay_generation(self):
        scene = funnel.set_screenplay_result(
            self._scene(),
            "GREG: Five silver?",
            compiler="screenplay/v1",
            dependency_hash="perf-dep",
        )
        updated = funnel.set_comparison_result(
            scene,
            {"verdict": "source_win", "reason": "The source already performs the negotiation through action."},
            compiler="comparison/v1",
            dependency_hash="screenplay-dep",
        )
        self.assertEqual("source_win", updated["comparison"]["verdict"])
        funnel.validate_scene_record(updated)

    def test_performance_candidate_requires_bounded_possible_win(self):
        with self.assertRaisesRegex(ValueError, "possible_wins"):
            funnel.set_comparison_result(
                self._scene(),
                {"verdict": "performance_candidate", "possible_wins": []},
                compiler="comparison/v1",
                dependency_hash="dep",
            )
        candidate = funnel.set_comparison_result(
            self._scene(),
            {
                "verdict": "performance_candidate",
                "possible_wins": [{
                    "surface": "dialogue",
                    "problem": "repeated verbal confirmation",
                    "performed_advantage": "physical action carries the distinction",
                    "source_span": ["Greg lifted the box.", "Antonius returned to the broom."],
                }],
            },
            compiler="comparison/v1",
            dependency_hash="dep",
        )
        self.assertEqual("performance_candidate", candidate["comparison"]["verdict"])

    def test_comparison_rejects_unknown_verdict(self):
        with self.assertRaisesRegex(ValueError, "verdict"):
            funnel.set_comparison_result(
                self._scene(),
                {"verdict": "rewrite_everything"},
                compiler="comparison/v1",
                dependency_hash="dep",
            )

    def test_recompile_unchanged_scene_preserves_valid_expensive_layers(self):
        page = '<article class="prose"><p>Greg lifted the box.</p></article>'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            funnel.write_compiled_chapter(7, page, root)
            scene_path = root / "007" / "s010.json"
            scene = json.loads(scene_path.read_text(encoding="utf-8"))
            scene["semantic"] = {
                "active_task": {"value": "sort the storeroom", "kind": "inferred", "confidence": 0.9, "compiler": "scene-semantic/v1"}
            }
            scene["screenplay"] = {"kind": "generated_output", "content": "GREG [lifts box].", "compiler": "screenplay/v1"}
            scene["dependencies"]["semantic"] = {"source_hash": scene["source"]["hash"], "compiler": "scene-semantic/v1"}
            scene["dependencies"]["screenplay"] = {"dependency_hash": "screenplay-dep", "compiler": "screenplay/v1"}
            scene_path.write_text(json.dumps(scene), encoding="utf-8")

            funnel.write_compiled_chapter(7, page, root)
            rebuilt = json.loads(scene_path.read_text(encoding="utf-8"))
            self.assertIn("semantic", rebuilt)
            self.assertIn("screenplay", rebuilt)
            self.assertEqual("sort the storeroom", rebuilt["semantic"]["active_task"]["value"])

    def test_recompile_changed_scene_drops_stale_expensive_layers(self):
        first = '<article class="prose"><p>Greg lifted the box.</p></article>'
        changed = '<article class="prose"><p>Greg dropped the box.</p></article>'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            funnel.write_compiled_chapter(7, first, root)
            scene_path = root / "007" / "s010.json"
            scene = json.loads(scene_path.read_text(encoding="utf-8"))
            scene["semantic"] = {"active_task": {"value": "lift box", "kind": "inferred", "confidence": 0.9, "compiler": "scene-semantic/v1"}}
            scene_path.write_text(json.dumps(scene), encoding="utf-8")

            funnel.write_compiled_chapter(7, changed, root)
            rebuilt = json.loads(scene_path.read_text(encoding="utf-8"))
            self.assertNotIn("semantic", rebuilt)

    def test_compile_chapter_cli_writes_deterministic_scene_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            chapter_root = tmp_root / "chapters"
            output_root = tmp_root / "compiled"
            chapter_root.mkdir()
            (chapter_root / "007.html").write_text('<article class="prose"><p>Greg lifted the box.</p></article>', encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                result = funnel.main([
                    "--compile-chapter", "7",
                    "--chapter-root", str(chapter_root),
                    "--output-root", str(output_root),
                ])
            self.assertEqual(0, result)
            self.assertTrue((output_root / "007" / "manifest.json").exists())
            payload = json.loads(stdout.getvalue())
            self.assertEqual(1, payload["scene_count"])

    def test_view_cli_emits_narrow_ai_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp)
            page = '<article class="prose"><p>Greg lifted the box.</p></article>'
            funnel.write_compiled_chapter(7, page, output_root)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                result = funnel.main([
                    "--view", "dialogue",
                    "--scene", "007.s010",
                    "--output-root", str(output_root),
                ])
            self.assertEqual(0, result)
            payload = json.loads(stdout.getvalue())
            self.assertEqual("007.s010", payload["scene_id"])
            self.assertNotIn("paragraphs", str(payload))

    def test_successful_roundtrip_anchors_are_addressable_in_compiled_scenes(self):
        for chapter in (7, 13, 18):
            page = (funnel.ROOT / "chapters" / f"{chapter:03d}.html").read_text(encoding="utf-8")
            lock = json.loads((funnel.ROOT / "state" / "editorial" / "performance-roundtrip" / f"{chapter:03d}" / "source.lock.json").read_text(encoding="utf-8"))
            scenes = funnel.segment_chapter(page, chapter)
            scene_texts = [" ".join(scene["source"]["paragraphs"]) for scene in scenes]
            for anchor in lock["result_scene_anchors"]:
                matches = [text for text in scene_texts if anchor in text]
                self.assertEqual(1, len(matches), f"chapter {chapter} anchor should resolve to one compiled scene")


if __name__ == "__main__":
    unittest.main()
