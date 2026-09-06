from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.build_generation_queue import build_generation_queue
from scripts.performance_roundtrip_references import (
    load_reference,
    load_visual_reference,
    validate_reference,
)


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = ROOT / "state" / "editorial" / "performance-roundtrip"
CHAPTER_ROOT = ROOT / "chapters"


class PerformanceRoundtripReferenceTests(unittest.TestCase):
    def _write_fixture(self, root: Path, *, anchor: str = "Antonius picked up the broom.") -> tuple[Path, Path]:
        archive_root = root / "archive"
        chapter_root = root / "chapters"
        reference_dir = archive_root / "007"
        reference_dir.mkdir(parents=True)
        chapter_root.mkdir(parents=True)
        (reference_dir / "source.lock.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "authority": "derived_editorial_reference",
                    "canon_authority": False,
                    "canon_chapter": 7,
                    "source_path": "chapters/007.html",
                    "source_chapter_blob": "historical-blob",
                    "source_authority_commit": "historical-commit",
                    "displayed_showcase_chapter": 5,
                    "performance_lab_commit": "historical-lab",
                    "resulting_canon_commit": "result-commit",
                    "result_scene_anchors": [anchor],
                    "visual_reference": {
                        "characters": ["Greg", "Antonius"],
                        "location": "Antonius storeroom",
                        "active_task": "Sort the storeroom.",
                        "props": ["broom"],
                        "physical_beats": ["Antonius returns to the broom."],
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        for name in ("dramatic.md", "performance.md", "screenplay.md", "comparison.md"):
            (reference_dir / name).write_text(f"# {name}\n", encoding="utf-8")
        (chapter_root / "007.html").write_text(
            "<html><body><article class=\"prose\"><p>Greg watched.</p>"
            f"<p>{anchor}</p></article></body></html>",
            encoding="utf-8",
        )
        return archive_root, chapter_root

    def _candidate(self) -> dict:
        return {
            "id": "ch007-performance-test",
            "chapter": 7,
            "chapter_title": "The Buyer",
            "kind": "chapter_illustration",
            "priority": "medium",
            "fit_target": "exact",
            "spoiler_level": "low",
            "scene_summary": "Antonius ends a negotiation by returning to work.",
            "visual_hook": "The broom becomes the physical final word.",
            "characters": ["Greg", "Antonius"],
            "location": "storeroom",
            "mood": "dry practical tension",
            "scene_tags": ["storeroom", "work"],
            "paragraph_anchor": "Antonius picked up the broom.",
            "status": "prompt_ready",
        }

    def test_missing_reference_is_optional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertIsNone(load_reference(999, archive_root=root / "archive", chapter_root=root / "chapters"))
            self.assertIsNone(load_visual_reference(999, archive_root=root / "archive", chapter_root=root / "chapters"))

    def test_fresh_reference_requires_derived_authority_and_unique_scene_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive_root, chapter_root = self._write_fixture(Path(tmp))
            result = validate_reference(7, archive_root=archive_root, chapter_root=chapter_root)
            self.assertEqual(result["status"], "fresh")
            reference = load_reference(7, archive_root=archive_root, chapter_root=chapter_root)
            self.assertIsNotNone(reference)
            assert reference is not None
            self.assertEqual(reference["authority"], "derived_editorial_reference")
            self.assertFalse(reference["canon_authority"])

    def test_material_scene_change_marks_reference_stale_and_visual_consumer_ignores_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive_root, chapter_root = self._write_fixture(Path(tmp))
            (chapter_root / "007.html").write_text(
                "<html><body><article class=\"prose\"><p>Greg watched.</p>"
                "<p>Antonius left the broom where it was.</p></article></body></html>",
                encoding="utf-8",
            )
            result = validate_reference(7, archive_root=archive_root, chapter_root=chapter_root)
            self.assertEqual(result["status"], "stale")
            self.assertTrue(any("anchor" in reason for reason in result["reasons"]))
            self.assertIsNone(load_visual_reference(7, archive_root=archive_root, chapter_root=chapter_root))

    def test_non_prose_html_changes_do_not_make_reference_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive_root, chapter_root = self._write_fixture(Path(tmp))
            chapter = chapter_root / "007.html"
            text = chapter.read_text(encoding="utf-8")
            text = text.replace(
                '<article class="prose">',
                '<figure><img src="new-art.webp"/></figure><article class="prose">',
            )
            chapter.write_text(text, encoding="utf-8")
            self.assertEqual(
                validate_reference(7, archive_root=archive_root, chapter_root=chapter_root)["status"],
                "fresh",
            )

    def test_committed_successful_backfills_are_complete_fresh_and_noncanonical(self) -> None:
        expected = {
            7: (5, "70f79b2b11940cbadeb970c1e8cf39c7294fdb66"),
            13: (9, "181a2b52326c3b190aa5ae6f9ee8967e4d206715"),
            18: (14, "30538e320c31db744212e4c22922b0f0fe860975"),
        }
        required = {"source.lock.json", "dramatic.md", "performance.md", "screenplay.md", "comparison.md"}
        for chapter, (displayed, source_blob) in expected.items():
            with self.subTest(chapter=chapter):
                directory = ARCHIVE_ROOT / f"{chapter:03d}"
                self.assertEqual({path.name for path in directory.iterdir()}, required)
                lock = json.loads((directory / "source.lock.json").read_text(encoding="utf-8"))
                self.assertEqual(lock["source_chapter_blob"], source_blob)
                self.assertEqual(lock["source_authority_commit"], "35055180a116cf7a0dfd4a1fa94704c2c5b0bd40")
                self.assertEqual(lock["performance_lab_commit"], "48bf312924c5d1d6836587e9cb3e21f3944a4d43")
                self.assertEqual(lock["resulting_canon_commit"], "fb703c47db1e682ea32f45da5e5bb89b319c4c93")
                self.assertEqual(lock["displayed_showcase_chapter"], displayed)
                self.assertEqual(lock["authority"], "derived_editorial_reference")
                self.assertFalse(lock["canon_authority"])
                self.assertGreaterEqual(len(lock["result_scene_anchors"]), 3)
                self.assertEqual(
                    validate_reference(chapter, archive_root=ARCHIVE_ROOT, chapter_root=CHAPTER_ROOT)["status"],
                    "fresh",
                )

    def test_source_wins_do_not_get_heavy_archive_by_default(self) -> None:
        self.assertFalse((ARCHIVE_ROOT / "002").exists())
        self.assertFalse((ARCHIVE_ROOT / "016").exists())

    def test_generation_queue_can_carry_fresh_performance_reference_without_changing_candidate_authority(self) -> None:
        fresh = load_visual_reference(7, archive_root=ARCHIVE_ROOT, chapter_root=CHAPTER_ROOT)
        self.assertIsNotNone(fresh)
        assert fresh is not None
        self.assertIn("Antonius picked up the broom.", fresh["scene_anchors"])
        queue = build_generation_queue(
            [self._candidate()],
            [],
            chapter_image_counts={7: 0},
            character_references={},
            performance_references={7: fresh},
        )
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["performance_reference"], fresh)
        self.assertEqual(queue[0]["characters"], ["Greg", "Antonius"])
        self.assertEqual(queue[0]["paragraph_anchor"], "Antonius picked up the broom.")
        self.assertEqual(queue[0]["status"], "generation_ready")

    def test_generation_queue_does_not_attach_same_chapter_reference_to_unrelated_scene(self) -> None:
        fresh = load_visual_reference(7, archive_root=ARCHIVE_ROOT, chapter_root=CHAPTER_ROOT)
        self.assertIsNotNone(fresh)
        candidate = self._candidate()
        candidate["id"] = "ch007-red-scarf"
        candidate["scene_summary"] = "Greg finds a red scarf after the storeroom negotiation."
        candidate["visual_hook"] = "A quiet memory beat around a worthless object."
        candidate["paragraph_anchor"] = "At the bottom of the last crate I found a small red scarf."
        queue = build_generation_queue(
            [candidate],
            [],
            chapter_image_counts={7: 0},
            character_references={},
            performance_references={7: fresh},
        )
        self.assertEqual(len(queue), 1)
        self.assertNotIn("performance_reference", queue[0])
        self.assertEqual(queue[0]["status"], "generation_ready")

    def test_generation_queue_remains_independent_when_performance_reference_is_missing(self) -> None:
        queue = build_generation_queue(
            [self._candidate()],
            [],
            chapter_image_counts={7: 0},
            character_references={},
            performance_references={},
        )
        self.assertEqual(len(queue), 1)
        self.assertNotIn("performance_reference", queue[0])
        self.assertEqual(queue[0]["status"], "generation_ready")


if __name__ == "__main__":
    unittest.main()
