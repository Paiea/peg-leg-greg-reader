import tempfile
import unittest
from pathlib import Path

from scripts import apply_rehearsal_returns as returns


class RehearsalReturnTests(unittest.TestCase):
    def test_applies_exact_free_production_return_and_records_take_provenance(self):
        text = '<article class="prose"><p>Old thought.</p><p>Old line.</p></article>'
        patch = {
            "id": "nico-005-1",
            "chapter": 5,
            "actor": "Nico",
            "role": "Greg",
            "take_id": "005-free-a",
            "variance_group_id": "005-v1",
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "changed_surfaces": ["internal_dialogue", "narration_rhythm", "dialogue"],
            "before": '<p>Old thought.</p><p>Old line.</p>',
            "after": '<p>New rhythm.</p><p>New line.</p>',
            "reason": "Nico live cognition improves timing without changing story truth.",
        }
        updated, record = returns.apply_patch_to_text(
            text,
            patch,
            target_branch="editor/rehearsal-simulation-engine",
        )
        self.assertIn('<p>New rhythm.</p><p>New line.</p>', updated)
        self.assertEqual("production", record["policy_mode"])
        self.assertEqual("005-free-a", record["take_id"])
        self.assertEqual("005-v1", record["variance_group_id"])
        self.assertEqual("scene_rebuild", record["policy_scope"])

    def test_rejects_main_hard_surface_and_non_exact_source(self):
        text = '<article class="prose"><p>Old.</p></article>'
        patch = {
            "id": "demo",
            "chapter": 5,
            "actor": "Mara",
            "role": "Hessa",
            "take_id": "018-free-a",
            "variance_group_id": "018-v1",
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "changed_surfaces": ["movement", "dialogue", "tone"],
            "before": '<p>Old.</p>',
            "after": '<p>New.</p>',
            "reason": "Private interpretation produces stronger visible control behavior.",
        }
        with self.assertRaisesRegex(ValueError, "write gate"):
            returns.apply_patch_to_text(text, patch, target_branch="main")

        hard = dict(patch, changed_surfaces=["dialogue", "knowledge"])
        with self.assertRaisesRegex(ValueError, "write gate"):
            returns.apply_patch_to_text(text, hard, target_branch="editor/rehearsal-simulation-engine")

        stale = dict(patch, before='<p>Missing.</p>')
        with self.assertRaisesRegex(ValueError, "exact source"):
            returns.apply_patch_to_text(text, stale, target_branch="editor/rehearsal-simulation-engine")

    def test_manifest_is_dry_run_by_default_and_declares_changed_chapters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            chapter = chapters / "005.html"
            chapter.write_text('<article class="prose"><p>Old.</p></article>', encoding="utf-8")
            manifest = {
                "schema": "rehearsal_free_returns/v1",
                "mode": "free_production",
                "target_branch": "editor/rehearsal-simulation-engine",
                "patches": [
                    {
                        "id": "demo-1",
                        "chapter": 5,
                        "actor": "Nico",
                        "role": "Greg",
                        "take_id": "005-free-a",
                        "variance_group_id": None,
                        "actor_prefers": True,
                        "dramatic_lock_status": "preserved",
                        "reader_check": "pass",
                        "changed_surfaces": ["attention_order", "sensory_emphasis"],
                        "before": '<p>Old.</p>',
                        "after": '<p>New.</p>',
                        "reason": "Sensory hook lands before analysis.",
                    }
                ],
            }
            report = returns.apply_manifest(root, manifest, write=False)
            self.assertEqual(1, report["patches_ready"])
            self.assertEqual([5], report["changed_chapters"])
            self.assertIn('<p>Old.</p>', chapter.read_text(encoding="utf-8"))

            report = returns.apply_manifest(root, manifest, write=True)
            self.assertEqual(1, report["patches_applied"])
            self.assertIn('<p>New.</p>', chapter.read_text(encoding="utf-8"))

    def test_private_inner_interpretation_is_provenance_not_canon_surface(self):
        text = '<article class="prose"><p>Hessa looked at me.</p></article>'
        patch = {
            "id": "hessa-018-1",
            "chapter": 18,
            "actor": "Mara",
            "role": "Hessa",
            "take_id": "018-free-a",
            "variance_group_id": "018-v1",
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "changed_surfaces": ["movement", "interaction_timing", "tone"],
            "before": '<p>Hessa looked at me.</p>',
            "after": '<p>Hessa kept two fingers on my wrist.</p>',
            "reason": "Hessa private interpretation generates stronger visible control behavior.",
            "performed_interpretation": {
                "authority": "rehearsal_hypothesis",
                "summary": "Responsibility for Greg's safety dominates this take.",
            },
        }
        _, record = returns.apply_patch_to_text(
            text,
            patch,
            target_branch="editor/rehearsal-simulation-engine",
        )
        self.assertEqual("rehearsal_hypothesis", record["performed_interpretation"]["authority"])
        self.assertNotIn("private_inner_voice", record["changed_surfaces"])


if __name__ == "__main__":
    unittest.main()
