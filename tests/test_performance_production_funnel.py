import json
import tempfile
import unittest
from pathlib import Path

from scripts import performance_production_funnel as funnel


class PerformanceProductionFunnelTests(unittest.TestCase):
    def test_next_visible_chapters_skip_hidden_canon(self):
        manifest = {
            "default": "visible",
            "chapters": {
                "3": {"showcase": False}, "6": {"showcase": False}, "8": {"showcase": False},
                "12": {"showcase": False}, "20": {"showcase": False}, "21": {"showcase": False},
                "33": {"showcase": False}, "38": {"showcase": False}, "43": {"showcase": False},
                "46": {"showcase": False}, "48": {"showcase": False}, "49": {"showcase": False},
                "57": {"showcase": False}, "66": {"showcase": False}, "73": {"showcase": False},
            },
        }
        expected = [27,28,29,30,31,32,34,35,36,37,39,40,41,42,44,45,47,50,51,52,53,54,55,56,58,59,60,61,62,63,64,65,67,68,69,70,71,72,74,75]
        self.assertEqual(expected, funnel.next_visible_chapters(manifest, after_chapter=26, count=40, max_chapter=75))

    def test_source_win_record_stays_lightweight(self):
        funnel.validate_record({"chapter":27,"verdict":"source_win","screen":{"decision":"source_win","signals":[],"reason":"The task already carries the exchange."}})

    def test_deep_review_can_still_end_in_source_win(self):
        funnel.validate_record({"chapter":28,"verdict":"source_win","screen":{"decision":"deep_review","signals":["rhythm"],"reason":"The exchange looked too polished on the cheap screen."},"comparison":"The source already resolves the pressure through the active task, so the candidate adds staging without improving the scene."})

    def test_deep_review_source_win_requires_comparison(self):
        record={"chapter":28,"verdict":"source_win","screen":{"decision":"deep_review","signals":["rhythm"],"reason":"The exchange looked too polished on the cheap screen."}}
        with self.assertRaisesRegex(ValueError,"comparison"): funnel.validate_record(record)

    def test_surviving_change_requires_deep_roundtrip_evidence(self):
        record={"chapter":28,"verdict":"change_survives","screen":{"decision":"deep_review","signals":["verbalized_behavior"],"reason":"A spoken correction can become action."},"patches":[]}
        with self.assertRaisesRegex(ValueError,"dramatic"): funnel.validate_record(record)

    def test_validate_batch_requires_exact_scope_coverage_once(self):
        batch={"schema":"performance_production_batch/v1","source_authority":"abc123","scope":[27,28],"records":[{"chapter":27,"verdict":"source_win","screen":{"decision":"source_win","signals":[],"reason":"Healthy."}},{"chapter":28,"verdict":"source_win","screen":{"decision":"source_win","signals":[],"reason":"Healthy."}}]}
        funnel.validate_batch(batch)
        with self.assertRaisesRegex(ValueError,"coverage"): funnel.validate_batch({**batch,"records":batch["records"][:1]})
        with self.assertRaisesRegex(ValueError,"coverage"): funnel.validate_batch({**batch,"records":[batch["records"][0],batch["records"][0]]})

    def _survivor(self, chapter=28):
        return {"chapter":chapter,"verdict":"change_survives","screen":{"decision":"deep_review","signals":["verbalized_behavior"],"reason":"Physical behavior is stronger."},"dramatic":"A wants the answer; B controls the task.","performance":"B answers by doing the task.","screenplay":"B [moves object]: Again.","comparison":"Candidate externalizes B's authority without changing the result.","patches":[{"start":"Old first.","end":"Old second.","replacement":["New first.",'B said, "Again."'],"rationale":"Make task ownership physical."}]}

    def test_apply_record_replaces_exact_paragraph_span(self):
        page='<html><article class="prose"><p>Before.</p><p>Old first.</p><p>Old second.</p><p>After.</p></article></html>'
        record=self._survivor()
        funnel.validate_record(record)
        updated=funnel.apply_record(page,record)
        self.assertIn("<p>Before.</p><p>New first.</p><p>B said, &quot;Again.&quot;</p><p>After.</p>",updated)
        self.assertNotIn("Old first.",updated)

    def test_apply_record_fails_closed_on_ambiguous_anchor(self):
        page='<article class="prose"><p>Same.</p><p>Middle.</p><p>Same.</p></article>'
        record=self._survivor()
        record["patches"]=[{"start":"Same.","end":"Middle.","replacement":["Changed."],"rationale":"Test."}]
        with self.assertRaisesRegex(ValueError,"start boundary matched 2"): funnel.apply_record(page,record)

    def test_survivor_rejects_em_dash_in_new_prose(self):
        record=self._survivor()
        record["patches"]=[{"start":"Old.","end":"Old.","replacement":["No—new dash."],"rationale":"Test."}]
        with self.assertRaisesRegex(ValueError,"em dash"): funnel.validate_record(record)

    def test_apply_batch_to_root_changes_only_survivors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"027.html").write_text('<article class="prose"><p>Keep.</p></article>',encoding="utf-8")
            (root/"028.html").write_text('<article class="prose"><p>Old first.</p><p>Old second.</p></article>',encoding="utf-8")
            batch={"schema":"performance_production_batch/v1","source_authority":"abc123","scope":[27,28],"records":[{"chapter":27,"verdict":"source_win","screen":{"decision":"source_win","signals":[],"reason":"Healthy."}},self._survivor(28)]}
            changed=funnel.apply_batch_to_root(batch,root)
            self.assertEqual([root/"028.html"],changed)
            self.assertEqual('<article class="prose"><p>Keep.</p></article>',(root/"027.html").read_text(encoding="utf-8"))
            self.assertIn("New first.",(root/"028.html").read_text(encoding="utf-8"))

    def test_segment_chapter_splits_explicit_hr_and_uses_spaced_scene_ids(self):
        page = '<article class="prose"><p>Greg lifted the box.</p><p>"Five silver?" Antonius asked.</p><hr><p>Later, Hessa moved the tray.</p></article>'
        scenes = funnel.segment_chapter(page, 214)
        self.assertEqual(["214.s010", "214.s020"], [scene["scene_id"] for scene in scenes])
        self.assertEqual(2, scenes[0]["mechanical"]["paragraph_count"])
        self.assertEqual(1, scenes[0]["mechanical"]["dialogue_turns"])
        self.assertIn("five silver", scenes[0]["mechanical"]["money_mentions"])
        self.assertTrue(scenes[0]["source"]["hash"])

    def test_segment_chapter_falls_back_to_one_scene_without_explicit_break(self):
        page = '<article class="prose"><p>Greg lifted the box.</p><p>Antonius watched.</p></article>'
        scenes = funnel.segment_chapter(page, 7)
        self.assertEqual(["007.s010"], [scene["scene_id"] for scene in scenes])
        self.assertEqual(["Greg lifted the box.", "Antonius watched."], scenes[0]["source"]["paragraphs"])

    def test_mechanical_ir_collects_reusable_cheap_signals_without_semantic_claims(self):
        scene = {
            "scene_id": "007.s010",
            "source": {"paragraphs": ["Greg lifted the box.", '"Five silver?" Antonius asked.', "Antonius turned and opened the door."]},
        }
        mechanical = funnel.build_mechanical_ir(scene)
        self.assertEqual(3, mechanical["paragraph_count"])
        self.assertEqual(1, mechanical["question_count"])
        self.assertEqual(1, mechanical["dialogue_turns"])
        self.assertIn("five silver", mechanical["money_mentions"])
        self.assertIn("Greg", mechanical["capitalized_tokens"])
        self.assertGreaterEqual(mechanical["action_word_hits"], 3)
        self.assertNotIn("goal", mechanical)

    def test_dependency_fingerprint_is_canonical_and_sensitive(self):
        left = funnel.dependency_fingerprint({"b": 2, "a": 1}, ["x"])
        right = funnel.dependency_fingerprint({"a": 1, "b": 2}, ["x"])
        self.assertEqual(left, right)
        self.assertNotEqual(left, funnel.dependency_fingerprint({"a": 1, "b": 3}, ["x"]))

    def test_chapter_manifest_stays_small_and_routes_to_scene_records(self):
        page = '<article class="prose"><p>A.</p><hr><p>B.</p></article>'
        scenes = funnel.segment_chapter(page, 214)
        manifest = funnel.build_chapter_manifest(214, "chapters/214.html", scenes, funnel.COMPILER_VERSIONS)
        self.assertEqual("performance_chapter_manifest/v1", manifest["schema"])
        self.assertEqual(["214.s010", "214.s020"], manifest["scene_order"])
        self.assertEqual(scenes[0]["source"]["hash"], manifest["scenes"]["214.s010"]["source_hash"])
        self.assertNotIn("mechanical", manifest["scenes"]["214.s010"])

    def test_scene_ids_survive_inserting_a_new_scene_between_unchanged_scenes(self):
        before = '<article class="prose"><p>Alpha stays.</p><hr><p>Omega stays.</p></article>'
        old_scenes = funnel.segment_chapter(before, 214)
        previous = funnel.build_chapter_manifest(214, "chapters/214.html", old_scenes, funnel.COMPILER_VERSIONS)
        after = '<article class="prose"><p>Alpha stays.</p><hr><p>Inserted middle.</p><hr><p>Omega stays.</p></article>'
        new_scenes = funnel.segment_chapter(after, 214, previous_manifest=previous)
        self.assertEqual(["214.s010", "214.s015", "214.s020"], [scene["scene_id"] for scene in new_scenes])

    def test_cache_status_invalidates_only_layers_whose_dependencies_changed(self):
        record = {
            "source": {"hash": "source-a"},
            "dependencies": {
                "semantic": {"source_hash": "source-a", "compiler": "scene-semantic/v1"},
                "performance": {"source_hash": "source-a", "compiler": "performance/v1"},
            },
        }
        fresh = funnel.cache_status(record, source_hash="source-a", semantic_version="scene-semantic/v1", performance_version="performance/v1")
        self.assertEqual({"mechanical_valid": True, "semantic_valid": True, "performance_valid": True}, fresh)
        stale = funnel.cache_status(record, source_hash="source-b", semantic_version="scene-semantic/v1", performance_version="performance/v1")
        self.assertEqual({"mechanical_valid": False, "semantic_valid": False, "performance_valid": False}, stale)

    def test_write_compiled_chapter_writes_manifest_and_small_scene_files(self):
        page = '<article class="prose"><p>Alpha.</p><hr><p>Beta.</p></article>'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            written = funnel.write_compiled_chapter(7, page, root)
            chapter_root = root / "007"
            self.assertEqual({chapter_root / "manifest.json", chapter_root / "s010.json", chapter_root / "s020.json"}, set(written))
            manifest = json.loads((chapter_root / "manifest.json").read_text(encoding="utf-8"))
            scene = json.loads((chapter_root / "s010.json").read_text(encoding="utf-8"))
            self.assertEqual(["007.s010", "007.s020"], manifest["scene_order"])
            self.assertIn("mechanical", scene)
            self.assertNotIn("paragraphs", manifest["scenes"]["007.s010"])


if __name__ == "__main__": unittest.main()
