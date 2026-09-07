import tempfile
import unittest
from pathlib import Path

from scripts import apply_rehearsal_overtuned_calibration as calibration


class OvertunedCalibrationTests(unittest.TestCase):
    def test_applies_exact_soft_surface_scene_rebuild_and_records_provenance(self):
        text = '<article class="prose"><p>Old line.</p><p>Old movement.</p></article>'
        patch = {
            "id": "demo-1",
            "actor": "Desmond",
            "role": "Antonius",
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "changed_surfaces": ["dialogue", "movement", "tone", "paragraphing"],
            "before": '<p>Old line.</p><p>Old movement.</p>',
            "after": '<p>New line.</p><p>New movement.</p>',
        }
        updated, record = calibration.apply_patch_to_text(
            text,
            patch,
            target_branch="editor/rehearsal-simulation-engine",
        )
        self.assertIn('<p>New line.</p><p>New movement.</p>', updated)
        self.assertEqual("demo-1", record["patch_id"])
        self.assertEqual("Desmond", record["actor"])
        self.assertEqual("scene_rebuild", record["policy_scope"])

    def test_rejects_non_exact_source_and_hard_surface_or_main_writes(self):
        text = '<article class="prose"><p>Old line.</p></article>'
        base = {
            "id": "demo-2",
            "actor": "Nico",
            "role": "Greg",
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "changed_surfaces": ["dialogue"],
            "before": '<p>Missing line.</p>',
            "after": '<p>Replacement.</p>',
        }
        with self.assertRaisesRegex(ValueError, "exact source"):
            calibration.apply_patch_to_text(text, base, target_branch="editor/rehearsal-simulation-engine")

        hard = dict(base, before='<p>Old line.</p>', changed_surfaces=["dialogue", "plot"])
        with self.assertRaisesRegex(ValueError, "write gate"):
            calibration.apply_patch_to_text(text, hard, target_branch="editor/rehearsal-simulation-engine")

        safe = dict(base, before='<p>Old line.</p>')
        with self.assertRaisesRegex(ValueError, "write gate"):
            calibration.apply_patch_to_text(text, safe, target_branch="main")

    def test_apply_manifest_writes_only_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            chapter = chapters / "005.html"
            chapter.write_text('<article class="prose"><p>Old.</p></article>', encoding="utf-8")
            manifest = {
                "mode": "overtuned_calibration",
                "target_branch": "editor/rehearsal-simulation-engine",
                "patches": [{
                    "id": "demo-3",
                    "chapter": 5,
                    "actor": "Nico",
                    "role": "Greg",
                    "actor_prefers": True,
                    "dramatic_lock_status": "preserved",
                    "reader_check": "pass",
                    "changed_surfaces": ["tone"],
                    "before": '<p>Old.</p>',
                    "after": '<p>New.</p>',
                }],
            }
            report = calibration.apply_manifest(root, manifest, write=False)
            self.assertEqual(1, report["patches_ready"])
            self.assertIn('<p>Old.</p>', chapter.read_text(encoding="utf-8"))

            report = calibration.apply_manifest(root, manifest, write=True)
            self.assertEqual(1, report["patches_applied"])
            self.assertIn('<p>New.</p>', chapter.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
