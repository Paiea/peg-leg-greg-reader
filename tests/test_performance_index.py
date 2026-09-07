import json
import tempfile
import unittest
from pathlib import Path

from scripts import performance_index


class PerformanceIndexTests(unittest.TestCase):
    def _compiled_root(self, root: Path) -> Path:
        compiled = root / "compiled"
        chapter = compiled / "214"
        chapter.mkdir(parents=True)
        scene_a = {
            "scene_id": "214.s010",
            "source": {
                "chapter": 214,
                "hash": "hash-a",
                "paragraph_span": [1, 2],
                "start_anchor": "Greg lifted the gray frame.",
                "end_anchor": "Antonius asked for five silver.",
                "paragraphs": ["Greg lifted the gray frame.", "Antonius asked for five silver."],
            },
            "mechanical": {
                "capitalized_tokens": ["Greg", "Antonius"],
                "money_mentions": ["five silver"],
                "dialogue_turns": 1,
                "dialogue_ratio": 0.25,
                "question_count": 0,
                "action_word_hits": 1,
            },
            "semantic": {
                "characters": {"value": ["Greg", "Antonius"], "kind": "inferred", "confidence": 0.9, "compiler": "scene-semantic/v1"},
                "location": {"value": "storeroom", "kind": "inferred", "confidence": 0.8, "compiler": "scene-semantic/v1"},
            },
            "comparison": {"verdict": "performance_candidate", "possible_wins": [{"surface": "dialogue", "problem": "repetition", "performed_advantage": "physical turn", "source_span": ["Greg lifted the gray frame.", "Antonius asked for five silver."]}]},
            "dependencies": {"mechanical": {"compiler": "mechanical/v1"}},
        }
        scene_b = {
            "scene_id": "214.s020",
            "source": {
                "chapter": 214,
                "hash": "hash-b",
                "paragraph_span": [3, 3],
                "start_anchor": "Hessa closed the door.",
                "end_anchor": "Hessa closed the door.",
                "paragraphs": ["Hessa closed the door."],
            },
            "mechanical": {
                "capitalized_tokens": ["Hessa"],
                "money_mentions": [],
                "dialogue_turns": 0,
                "dialogue_ratio": 0.0,
                "question_count": 0,
                "action_word_hits": 1,
            },
            "dependencies": {"mechanical": {"compiler": "mechanical/v1"}},
        }
        (chapter / "s010.json").write_text(json.dumps(scene_a), encoding="utf-8")
        (chapter / "s020.json").write_text(json.dumps(scene_b), encoding="utf-8")
        return compiled

    def test_rebuild_and_exact_scene_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            compiled = self._compiled_root(root)
            db = root / "project-index.sqlite"
            summary = performance_index.rebuild_index(compiled, db)
            self.assertEqual(2, summary["scene_count"])
            rows = performance_index.query_scenes(db, scene_id="214.s010")
            self.assertEqual(["214.s010"], [row["scene_id"] for row in rows])
            self.assertNotIn("source_text", rows[0])

    def test_fts_and_structured_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            compiled = self._compiled_root(root)
            db = root / "project-index.sqlite"
            performance_index.rebuild_index(compiled, db)
            self.assertEqual(["214.s010"], [r["scene_id"] for r in performance_index.query_scenes(db, query="gray frame")])
            self.assertEqual(["214.s010"], [r["scene_id"] for r in performance_index.query_scenes(db, token="Greg")])
            self.assertEqual(["214.s010"], [r["scene_id"] for r in performance_index.query_scenes(db, money="silver")])
            self.assertEqual(["214.s010"], [r["scene_id"] for r in performance_index.query_scenes(db, verdict="performance_candidate")])
            self.assertEqual(2, len(performance_index.query_scenes(db, chapter_start=214, chapter_end=214)))

    def test_index_is_rebuildable_with_equivalent_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            compiled = self._compiled_root(root)
            db = root / "project-index.sqlite"
            performance_index.rebuild_index(compiled, db)
            before = performance_index.query_scenes(db, query="door")
            db.unlink()
            performance_index.rebuild_index(compiled, db)
            after = performance_index.query_scenes(db, query="door")
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
