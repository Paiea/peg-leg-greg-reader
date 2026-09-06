from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.backfill_tagged_registry_metadata import backfill_tagged_registry_metadata
from scripts.build_bounded_generation_packet import select_bounded_generation_batch, render_bounded_generation_packet
from scripts.validate_paragraph_anchors import validate_candidate_anchors, apply_anchor_validation

ROOT = Path(__file__).resolve().parents[1]


class BoundedGenerationPacketTests(unittest.TestCase):
    def test_packet_selects_only_requested_chapter_band(self):
        queue = [
            {"chapter": 156, "candidate_id": "a", "status": "generation_ready", "target_asset": "a.webp", "prompt_pack": "a.md", "selected_character_references": [], "reference_selection_notes": "Greg anchor", "paragraph_anchor": "anchor a"},
            {"chapter": 160, "candidate_id": "b", "status": "generation_ready", "target_asset": "b.webp", "prompt_pack": "b.md", "selected_character_references": [], "reference_selection_notes": "Greg anchor", "paragraph_anchor": "anchor b"},
            {"chapter": 161, "candidate_id": "c", "status": "generation_ready", "target_asset": "c.webp", "prompt_pack": "c.md", "selected_character_references": [], "reference_selection_notes": "other", "paragraph_anchor": "anchor c"},
        ]
        selected = select_bounded_generation_batch(queue, 156, 160)
        self.assertEqual([record["chapter"] for record in selected], [156, 160])

    def test_packet_contains_deterministic_targets_reference_rationale_and_review_structure(self):
        records = [{
            "chapter": 156,
            "chapter_title": "THE ADVOCATE",
            "candidate_id": "ch156-order-coat",
            "status": "generation_ready",
            "target_asset": "visual/chapter_art/156/ch156-order-coat-v1.webp",
            "prompt_pack": "state/visual/prompt-packs/ch156-order-coat.md",
            "paragraph_anchor": "She came over, took the order, and shoved it inside the front of my Advocate coat.",
            "framing_preference": "above_waist",
            "selected_character_references": [{"character": "Greg", "asset": "greg.webp", "selection_score": 120}],
            "reference_selection_notes": "Greg: greg.webp won for above-waist continuity",
        }]
        text = render_bounded_generation_packet(records, 156, 160)
        self.assertIn("Chapters 156–160", text)
        self.assertIn("visual/chapter_art/156/ch156-order-coat-v1.webp", text)
        self.assertIn("Greg: greg.webp won", text)
        self.assertIn("Approval checklist", text)
        self.assertIn("Paragraph anchor", text)


class ParagraphAnchorValidationTests(unittest.TestCase):
    def test_validator_accepts_unique_anchor_and_blocks_missing_or_ambiguous_anchor(self):
        candidates = [
            {"id": "good", "chapter": 156, "paragraph_anchor": "unique text", "status": "prompt_ready"},
            {"id": "missing", "chapter": 157, "paragraph_anchor": "not there", "status": "prompt_ready"},
            {"id": "ambiguous", "chapter": 158, "paragraph_anchor": "repeat", "status": "prompt_ready"},
        ]
        chapter_text = {
            156: "before\nunique text\nafter",
            157: "different",
            158: "repeat\nother\nrepeat",
        }
        report = validate_candidate_anchors(candidates, chapter_text)
        by_id = {row["candidate_id"]: row for row in report}
        self.assertEqual(by_id["good"]["anchor_status"], "valid")
        self.assertEqual(by_id["missing"]["anchor_status"], "missing")
        self.assertEqual(by_id["ambiguous"]["anchor_status"], "ambiguous")

        updated, changed = apply_anchor_validation(candidates, report)
        by_id = {row["id"]: row for row in updated}
        self.assertEqual(by_id["good"]["status"], "prompt_ready")
        self.assertEqual(by_id["missing"]["status"], "candidate")
        self.assertEqual(by_id["ambiguous"]["status"], "candidate")
        self.assertTrue(by_id["missing"]["anchor_blocked"])
        self.assertGreaterEqual(changed, 2)


class TaggedRegistryMetadataBackfillTests(unittest.TestCase):
    def test_backfill_uses_strong_evidence_but_does_not_invent_metadata(self):
        registry = [
            {
                "id": "clear",
                "status": "live",
                "characters": ["Nessa"],
                "alt_text": "Nessa works backstage at the costume table in three-quarter view.",
                "scene_tags": [],
            },
            {
                "id": "weak",
                "status": "live",
                "characters": ["Marek"],
                "alt_text": "Marek on stage.",
            },
        ]
        updated, changed = backfill_tagged_registry_metadata(registry)
        by_id = {row["id"]: row for row in updated}
        self.assertEqual(by_id["clear"]["view_angle"], "three_quarter")
        self.assertEqual(by_id["clear"]["pose_family"], "working")
        self.assertIn("backstage", by_id["clear"]["scene_tags"])
        self.assertNotIn("view_angle", by_id["weak"])
        self.assertGreaterEqual(changed, 1)


class OlderCoverageWaveTests(unittest.TestCase):
    def test_actual_scene_ledger_contains_prompt_ready_161_through_165(self):
        candidates = json.loads((ROOT / "state" / "visual" / "SCENE_CANDIDATES.json").read_text(encoding="utf-8"))
        by_chapter = {record["chapter"]: record for record in candidates if 161 <= record.get("chapter", 0) <= 165}
        self.assertEqual(sorted(by_chapter), [161, 162, 163, 164, 165])
        for chapter, record in by_chapter.items():
            self.assertEqual(record["status"], "prompt_ready")
            self.assertTrue(record.get("paragraph_anchor"))
            if "Greg" in record.get("characters", []):
                self.assertEqual(record.get("framing_preference"), "above_waist")


class TheatreReferenceCatalogTests(unittest.TestCase):
    def test_catalog_expands_to_theatre_characters_needed_by_156_through_165(self):
        catalog = json.loads((ROOT / "state" / "visual" / "CHARACTER_VISUAL_REFERENCES.json").read_text(encoding="utf-8"))
        for character in ("Nessa", "Marek", "Serra", "Iven", "Pell"):
            self.assertIn(character, catalog)
            self.assertTrue(catalog[character].get("appearance_notes"))


if __name__ == "__main__":
    unittest.main()
