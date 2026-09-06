from __future__ import annotations

import unittest

from scripts.review_bounded_production import review_bounded_batch
from scripts.seed_older_coverage_wave import apply_seed_wave
from scripts.tag_registry_characters import detect_characters
from scripts.validate_paragraph_anchors import validate_candidate_anchors
from scripts.promote_character_references import promote_character_references


class BoundedProductionReviewTests(unittest.TestCase):
    def test_review_routes_ready_generated_live_and_rejected_retryable_states(self):
        queue = [{
            "chapter": 156,
            "candidate_id": "ready",
            "status": "generation_ready",
            "target_asset": "visual/chapter_art/156/ready-v1.webp",
            "prompt_pack": "state/visual/prompt-packs/ready.md",
            "paragraph_anchor": "A distinctive placement sentence with useful context.",
            "selected_character_references": [{"character": "Greg", "asset": "greg.webp"}],
            "reference_selection_notes": "Greg anchor",
        }]
        registry = [
            {"candidate_id": "generated", "chapter": 157, "status": "generated", "source_asset": "g.webp"},
            {"candidate_id": "live", "chapter": 158, "status": "live", "live_asset": "l.webp"},
            {"candidate_id": "rejected", "chapter": 159, "status": "rejected", "source_asset": "r.webp"},
        ]
        candidates = [
            {"id": "ready", "chapter": 156, "anchor_status": "valid", "anchor_quality_status": "strong"},
            {"id": "generated", "chapter": 157, "anchor_status": "valid", "anchor_quality_status": "strong"},
            {"id": "live", "chapter": 158, "anchor_status": "valid", "anchor_quality_status": "strong"},
            {"id": "rejected", "chapter": 159, "anchor_status": "valid", "anchor_quality_status": "strong", "status": "prompt_ready"},
        ]
        rows = review_bounded_batch(queue, registry, candidates, 156, 160)
        by_id = {row["candidate_id"]: row for row in rows}
        self.assertEqual(by_id["ready"]["production_state"], "ready_to_generate")
        self.assertEqual(by_id["generated"]["production_state"], "generated_awaiting_approval")
        self.assertEqual(by_id["live"]["production_state"], "live")
        self.assertEqual(by_id["rejected"]["production_state"], "rejected_retryable")


class CharacterTagUnionTests(unittest.TestCase):
    def test_existing_greg_tag_does_not_hide_named_theatre_character(self):
        catalog = {"Greg": {}, "Pell": {}}
        record = {
            "characters": ["Greg"],
            "alt_text": "Pell and Greg watching a prop test backstage.",
        }
        characters, source = detect_characters(record, catalog)
        self.assertEqual(characters, ["Greg", "Pell"])
        self.assertIn("text_metadata", source)

    def test_identity_explicit_legacy_art_can_clear_promotion_threshold(self):
        catalog = {"Pell": {"appearance_notes": "Pell", "reference_assets": [], "references": []}}
        registry = [{
            "id": "pell-live",
            "status": "live",
            "live_asset": "visual/chapter_art/120/pell.webp",
            "approved_fit": "close_enough",
            "style_family": "legacy-import",
            "characters": ["Pell"],
            "alt_text": "Pell working backstage with a prop in his hands.",
            "scene_tags": ["backstage", "work"],
        }]
        updated, promoted = promote_character_references(catalog, registry)
        self.assertEqual(promoted, 1)
        self.assertEqual(updated["Pell"]["references"][0]["asset"], "visual/chapter_art/120/pell.webp")
        self.assertIn("identity_explicit", updated["Pell"]["references"][0]["tags"])


class AnchorQualityTests(unittest.TestCase):
    def test_short_pronoun_anchor_is_quality_blocked_when_backfill_quality_is_enforced(self):
        candidates = [{
            "id": "weak",
            "chapter": 159,
            "paragraph_anchor": "He was under the stage.",
            "status": "prompt_ready",
            "anchor_quality_enforced": True,
        }]
        report = validate_candidate_anchors(candidates, {159: "Before. He was under the stage. After."})
        self.assertEqual(report[0]["anchor_status"], "valid")
        self.assertEqual(report[0]["anchor_quality_status"], "weak")
        self.assertTrue(report[0]["anchor_quality_enforced"])
        self.assertTrue(report[0]["should_block"])

    def test_distinctive_anchor_passes_enforced_quality_gate(self):
        anchor = "We found the fish wedged behind a support where someone had pushed it with a boot."
        report = validate_candidate_anchors(
            [{
                "id": "strong",
                "chapter": 159,
                "paragraph_anchor": anchor,
                "status": "prompt_ready",
                "anchor_quality_enforced": True,
            }],
            {159: f"Before. {anchor} After."},
        )
        self.assertEqual(report[0]["anchor_quality_status"], "strong")
        self.assertFalse(report[0]["should_block"])


class OlderCoverageSeedTests(unittest.TestCase):
    def test_seed_repairs_weak_legacy_anchors_and_adds_166_through_170(self):
        existing = [
            {"id": "ch158-letter-lyssa", "chapter": 158, "paragraph_anchor": "I bought paper.", "status": "prompt_ready"},
            {"id": "ch159-fish-rescue", "chapter": 159, "paragraph_anchor": "He was under the stage.", "status": "prompt_ready"},
        ]
        updated, changed = apply_seed_wave(existing)
        by_id = {row["id"]: row for row in updated}
        self.assertGreater(changed, 0)
        self.assertNotEqual(by_id["ch158-letter-lyssa"]["paragraph_anchor"], "I bought paper.")
        self.assertNotEqual(by_id["ch159-fish-rescue"]["paragraph_anchor"], "He was under the stage.")
        self.assertTrue(by_id["ch158-letter-lyssa"]["anchor_quality_enforced"])
        self.assertTrue(by_id["ch159-fish-rescue"]["anchor_quality_enforced"])
        self.assertEqual(
            sorted(row["chapter"] for row in updated if 166 <= row.get("chapter", 0) <= 170),
            [166, 167, 168, 169, 170],
        )
        for row in updated:
            if 166 <= row.get("chapter", 0) <= 170:
                self.assertTrue(row.get("anchor_quality_enforced"))
            if 166 <= row.get("chapter", 0) <= 170 and "Greg" in row.get("characters", []):
                self.assertEqual(row.get("framing_preference"), "above_waist")


if __name__ == "__main__":
    unittest.main()
