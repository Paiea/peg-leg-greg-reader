from __future__ import annotations

import unittest

from scripts.audit_character_references import audit_character_references
from scripts.build_generation_packet import render_generation_packet
from scripts.build_generation_queue import build_generation_queue
from scripts.promote_character_references import promote_character_references
from scripts.score_character_references import score_reference, select_character_references


class ReferenceQualityScoringTests(unittest.TestCase):
    def test_live_exact_above_waist_greg_reference_outranks_lower_body_close_enough(self):
        strong = {
            "asset": "visual/greg-strong.webp",
            "status": "live",
            "approved_fit": "exact",
            "style_family": "sketch-ink-paint",
            "tags": ["above_waist", "strong_face"],
        }
        weak = {
            "asset": "visual/greg-weak.webp",
            "status": "approved",
            "approved_fit": "close_enough",
            "style_family": "legacy-import",
            "tags": ["full_body", "lower_body_visible"],
        }
        strong_score = score_reference(strong, "Greg", framing_preference="above_waist")
        weak_score = score_reference(weak, "Greg", framing_preference="above_waist")
        self.assertGreater(strong_score["score"], weak_score["score"])
        self.assertIn("above-waist Greg continuity", strong_score["reasons"])
        self.assertIn("lower-body mismatch", weak_score["penalties"])

    def test_selector_returns_top_scored_references_per_character(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "references": [
                    {"asset": "visual/greg-low.webp", "status": "approved", "approved_fit": "close_enough", "tags": ["full_body"]},
                    {"asset": "visual/greg-high.webp", "status": "live", "approved_fit": "exact", "style_family": "sketch-ink-paint", "tags": ["above_waist"]},
                ],
            }
        }
        selected = select_character_references(catalog, ["Greg"], framing_preference="above_waist", limit_per_character=1)
        self.assertEqual(selected[0]["asset"], "visual/greg-high.webp")
        self.assertEqual(selected[0]["character"], "Greg")
        self.assertGreater(selected[0]["score"], 0)


class ReferencePromotionTests(unittest.TestCase):
    def test_promotes_strong_live_registry_art_without_duplication(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "reference_assets": ["visual/manual-greg.webp"],
                "references": [],
            }
        }
        registry = [
            {
                "id": "greg-live-v1",
                "candidate_id": "ch020-greg",
                "chapter": 20,
                "status": "live",
                "approved_fit": "exact",
                "style_family": "sketch-ink-paint",
                "live_asset": "visual/chapter_art/020/greg-live-v1.webp",
                "alt_text": "Greg studies a blade at the bench.",
                "characters": ["Greg"],
                "framing_preference": "above_waist",
            }
        ]
        updated, promoted = promote_character_references(catalog, registry)
        self.assertEqual(promoted, 1)
        refs = updated["Greg"]["references"]
        self.assertEqual(refs[0]["registry_id"], "greg-live-v1")
        self.assertIn("above_waist", refs[0]["tags"])
        updated_again, promoted_again = promote_character_references(updated, registry)
        self.assertEqual(promoted_again, 0)
        self.assertEqual(len(updated_again["Greg"]["references"]), 1)


class ReferenceAuditTests(unittest.TestCase):
    def test_audit_flags_missing_duplicate_and_rejected_references(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "reference_assets": ["visual/missing.webp", "visual/duplicate.webp"],
                "references": [
                    {"asset": "visual/duplicate.webp", "registry_id": "bad-v1", "tags": ["lower_body_visible"]}
                ],
            }
        }
        registry = [{"id": "bad-v1", "status": "rejected"}]
        issues = audit_character_references(catalog, registry, available_assets={"visual/duplicate.webp"})
        codes = {issue["code"] for issue in issues}
        self.assertIn("missing_asset", codes)
        self.assertIn("duplicate_asset", codes)
        self.assertIn("bad_registry_status", codes)
        self.assertIn("greg_lower_body_risk", codes)


class QueueReferenceSelectionTests(unittest.TestCase):
    def candidate(self) -> dict:
        return {
            "id": "ch020-greg-lyssa",
            "chapter": 20,
            "chapter_title": "THE VOLUNTEER",
            "scene_summary": "Greg and Lyssa speak over a work table.",
            "visual_hook": "Hands, tools, cloth, and a conversational glance.",
            "characters": ["Greg", "Lyssa"],
            "location": "Carrow work room",
            "mood": "warm, practical",
            "priority": "high",
            "kind": "chapter_illustration",
            "fit_target": "close_enough",
            "spoiler_level": "low",
            "status": "prompt_ready",
            "paragraph_anchor": "Lyssa looked over the cloth.",
        }

    def test_queue_uses_strongest_references_and_carries_selection_rationale(self):
        references = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "references": [
                    {"asset": "visual/greg-low.webp", "status": "approved", "approved_fit": "close_enough", "tags": ["full_body"]},
                    {"asset": "visual/greg-high.webp", "status": "live", "approved_fit": "exact", "style_family": "sketch-ink-paint", "tags": ["above_waist", "strong_face"]},
                ],
            },
            "Lyssa": {
                "appearance_notes": "Black woman; tall relative to Greg; thin/lithe; natural Afro-textured hair.",
                "reference_assets": [],
            },
        }
        queue = build_generation_queue([self.candidate()], [], chapter_image_counts={20: 0}, character_references=references)
        record = queue[0]
        self.assertEqual(record["framing_preference"], "above_waist")
        self.assertEqual(record["character_reference_assets"][0], "visual/greg-high.webp")
        self.assertEqual(record["selected_character_references"][0]["character"], "Greg")
        self.assertIn("live", record["reference_selection_notes"])
        packet = render_generation_packet([record])
        self.assertIn("Reference selection rationale:", packet)
        self.assertIn("visual/greg-high.webp", packet)
        self.assertIn("above-waist Greg continuity", packet)


if __name__ == "__main__":
    unittest.main()
