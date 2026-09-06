from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from scripts.build_generation_queue import build_generation_queue
from scripts.intake_generated_illustrations import intake_generated_assets
from scripts.apply_illustration_approvals import apply_approvals


class GenerationQueueTests(unittest.TestCase):
    def candidate(self):
        return {
            "id": "ch392-glass-mice",
            "chapter": 392,
            "chapter_title": "THE CAMPER",
            "scene_summary": "Glass mice investigate the food box.",
            "visual_hook": "Blue-white teeth in low firelight.",
            "characters": ["Greg"],
            "location": "Camp",
            "mood": "quiet",
            "priority": "high",
            "kind": "chapter_illustration",
            "fit_target": "exact",
            "spoiler_level": "low",
            "status": "prompt_ready",
            "paragraph_anchor": "Glass mice.",
        }

    def test_prompt_ready_candidate_gets_deterministic_generation_target(self):
        queue = build_generation_queue([self.candidate()], [])
        self.assertEqual(len(queue), 1)
        record = queue[0]
        self.assertEqual(record["candidate_id"], "ch392-glass-mice")
        self.assertEqual(record["prompt_pack"], "state/visual/prompt-packs/ch392-glass-mice.md")
        self.assertEqual(record["target_asset"], "visual/chapter_art/392/ch392-glass-mice-v1.webp")
        self.assertEqual(record["status"], "generation_ready")

    def test_live_registry_record_removes_candidate_from_generation_queue(self):
        registry = [{"candidate_id": "ch392-glass-mice", "status": "live"}]
        self.assertEqual(build_generation_queue([self.candidate()], registry), [])


class GeneratedAssetIntakeTests(unittest.TestCase):
    def queue_record(self):
        return {
            "candidate_id": "ch392-glass-mice",
            "chapter": 392,
            "kind": "chapter_illustration",
            "fit_target": "exact",
            "prompt_pack": "state/visual/prompt-packs/ch392-glass-mice.md",
            "paragraph_anchor": "Glass mice.",
            "target_asset": "visual/chapter_art/392/ch392-glass-mice-v1.webp",
            "status": "generation_ready",
        }

    def test_existing_target_asset_enters_registry_as_generated_not_live(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            asset = root / self.queue_record()["target_asset"]
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"RIFFxxxxWEBP")
            registry, changed = intake_generated_assets(root, [self.queue_record()], [])
            self.assertEqual(changed, 1)
            self.assertEqual(registry[0]["status"], "generated")
            self.assertEqual(registry[0]["candidate_id"], "ch392-glass-mice")
            self.assertEqual(registry[0]["source_asset"], self.queue_record()["target_asset"])
            self.assertEqual(registry[0]["live_asset"], "")

    def test_missing_target_asset_does_nothing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            registry, changed = intake_generated_assets(Path(temp_dir), [self.queue_record()], [])
            self.assertEqual(registry, [])
            self.assertEqual(changed, 0)


class IllustrationApprovalLedgerTests(unittest.TestCase):
    def generated_record(self):
        return {
            "id": "ch392-glass-mice-v1",
            "candidate_id": "ch392-glass-mice",
            "chapter": 392,
            "kind": "chapter_illustration",
            "status": "generated",
            "style_family": "sketch-ink-paint",
            "source_asset": "visual/chapter_art/392/ch392-glass-mice-v1.webp",
            "live_asset": "",
            "caption": "",
            "alt_text": "",
            "approved_fit": "exact",
            "prompt_pack": "state/visual/prompt-packs/ch392-glass-mice.md",
            "paragraph_anchor": "Glass mice.",
        }

    def test_explicit_approval_promotes_generated_record_to_approved_only(self):
        approval = {
            "candidate_id": "ch392-glass-mice",
            "asset": "visual/chapter_art/392/ch392-glass-mice-v1.webp",
            "approved_fit": "exact",
            "alt_text": "Tiny gray glass mice with faint blue-white teeth investigate a camp food box while Greg watches.",
            "caption": "Glass mice test the camp food box.",
        }
        updated, changed = apply_approvals([self.generated_record()], [approval])
        self.assertEqual(changed, 1)
        self.assertEqual(updated[0]["status"], "approved")
        self.assertEqual(updated[0]["live_asset"], approval["asset"])
        self.assertEqual(updated[0]["alt_text"], approval["alt_text"])
        self.assertEqual(updated[0]["caption"], approval["caption"])

    def test_approval_refuses_asset_mismatch(self):
        approval = {
            "candidate_id": "ch392-glass-mice",
            "asset": "visual/chapter_art/392/not-the-generated-file.webp",
            "approved_fit": "exact",
            "alt_text": "Something.",
            "caption": "",
        }
        with self.assertRaisesRegex(ValueError, "does not match generated asset"):
            apply_approvals([self.generated_record()], [approval])


if __name__ == "__main__":
    unittest.main()
