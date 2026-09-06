from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.backfill_character_reference_metadata import backfill_reference_metadata
from scripts.build_character_continuity_report import summarize_character_continuity, render_character_continuity_report
from scripts.build_generation_queue import build_generation_queue
from scripts.build_prompt_packs import render_prompt_pack
from scripts.score_character_references import select_character_references

ROOT = Path(__file__).resolve().parents[1]


class ReferenceMetadataBackfillTests(unittest.TestCase):
    def test_backfill_adds_conservative_metadata_to_existing_greg_anchors(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "reference_assets": [
                    "visual/homepage/peg-leg-greg-homepage-frontispiece.png",
                    "assets/book-role-cards/book-ii-stagehand-177.webp",
                ],
                "references": [],
            }
        }
        updated, changed = backfill_reference_metadata(catalog)
        self.assertEqual(changed, 2)
        metadata = updated["Greg"]["reference_metadata"]
        self.assertEqual(metadata["assets/book-role-cards/book-ii-stagehand-177.webp"]["framing"], "above_waist")
        self.assertIn("backstage", metadata["assets/book-role-cards/book-ii-stagehand-177.webp"]["scene_tags"])
        self.assertTrue(metadata["visual/homepage/peg-leg-greg-homepage-frontispiece.png"]["pose_family"])

    def test_manual_reference_selection_uses_backfilled_metadata(self):
        catalog = {
            "Greg": {
                "reference_assets": ["assets/book-role-cards/book-ii-stagehand-177.webp"],
                "reference_metadata": {
                    "assets/book-role-cards/book-ii-stagehand-177.webp": {
                        "framing": "above_waist",
                        "view_angle": "three_quarter",
                        "pose_family": "working",
                        "scene_tags": ["backstage", "theatre", "work"],
                        "tags": ["above_waist", "strong_face", "style_anchor"],
                        "style_family": "sketch-ink-paint",
                    }
                },
            }
        }
        selected = select_character_references(
            catalog,
            ["Greg"],
            framing_preference="above_waist",
            scene_context={"scene_tags": ["backstage", "work"]},
            limit_per_character=1,
        )
        self.assertEqual(selected[0]["view_angle"], "three_quarter")
        self.assertIn("scene context match", selected[0]["reasons"])
        self.assertIn("above-waist Greg continuity", selected[0]["reasons"])


class ContinuityRoutingTests(unittest.TestCase):
    def test_report_routes_high_value_metadata_gaps_and_uncataloged_recurring_characters(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "reference_assets": ["visual/greg.webp"],
                "references": [],
            },
            "Lyssa": {
                "appearance_notes": "Lyssa notes.",
                "reference_assets": [],
                "references": [],
            },
        }
        candidates = [
            {"characters": ["Greg", "Lyssa", "Nessa"]},
            {"characters": ["Greg", "Nessa"]},
            {"characters": ["Greg"]},
        ]
        summary = summarize_character_continuity(catalog, [], candidates=candidates, registry=[])
        text = render_character_continuity_report(summary)
        self.assertEqual(summary["top_metadata_fix_targets"][0]["character"], "Greg")
        self.assertIn("Nessa", summary["uncataloged_recurring_characters"])
        self.assertIn("Top metadata repair targets", text)
        self.assertIn("Uncataloged recurring characters", text)


class PromptMetadataContractTests(unittest.TestCase):
    def test_prompt_pack_declares_generation_metadata_up_front(self):
        candidate = {
            "id": "ch156-order-coat",
            "chapter": 156,
            "chapter_title": "THE ADVOCATE",
            "scene_summary": "Nessa secures the forged order inside Greg's coat.",
            "visual_hook": "Hands, coat, paper, and crutches.",
            "characters": ["Greg", "Nessa"],
            "location": "theatre backstage",
            "mood": "practical, dryly comic",
            "priority": "high",
            "kind": "chapter_illustration",
            "fit_target": "exact",
            "spoiler_level": "low",
            "status": "prompt_ready",
            "paragraph_anchor": "She came over, took the order, and shoved it inside the front of my Advocate coat.",
            "framing_preference": "above_waist",
            "view_angle": "three_quarter",
            "pose_family": "working_handoff",
            "scene_tags": ["backstage", "theatre", "work", "prop"],
        }
        text = render_prompt_pack(candidate)
        self.assertIn("### GENERATION METADATA", text)
        self.assertIn("Framing: `above_waist`", text)
        self.assertIn("View angle: `three_quarter`", text)
        self.assertIn("Pose family: `working_handoff`", text)
        self.assertIn("backstage, theatre, work, prop", text)


class OlderCoverageBackfillTests(unittest.TestCase):
    def test_actual_scene_ledger_contains_prompt_ready_156_through_160(self):
        candidates = json.loads((ROOT / "state" / "visual" / "SCENE_CANDIDATES.json").read_text(encoding="utf-8"))
        by_id = {record["id"]: record for record in candidates}
        expected = {
            "ch156-order-coat": 156,
            "ch157-two-swords": 157,
            "ch158-letter-lyssa": 158,
            "ch159-fish-rescue": 159,
            "ch160-fish-twitch": 160,
        }
        for candidate_id, chapter in expected.items():
            self.assertEqual(by_id[candidate_id]["chapter"], chapter)
            self.assertEqual(by_id[candidate_id]["status"], "prompt_ready")
            if "Greg" in by_id[candidate_id]["characters"]:
                self.assertEqual(by_id[candidate_id]["framing_preference"], "above_waist")

    def test_old_zero_art_candidates_sort_before_newer_zero_art_candidates(self):
        candidates = [
            {
                "id": "ch390-new",
                "chapter": 390,
                "chapter_title": "NEW",
                "scene_summary": "new",
                "visual_hook": "new",
                "characters": ["Greg"],
                "location": "new",
                "mood": "new",
                "priority": "high",
                "kind": "chapter_illustration",
                "fit_target": "exact",
                "spoiler_level": "low",
                "status": "prompt_ready",
                "paragraph_anchor": "new",
            },
            {
                "id": "ch156-old",
                "chapter": 156,
                "chapter_title": "OLD",
                "scene_summary": "old",
                "visual_hook": "old",
                "characters": ["Greg"],
                "location": "old",
                "mood": "old",
                "priority": "high",
                "kind": "chapter_illustration",
                "fit_target": "exact",
                "spoiler_level": "low",
                "status": "prompt_ready",
                "paragraph_anchor": "old",
            },
        ]
        queue = build_generation_queue(candidates, [], chapter_image_counts={156: 0, 390: 0}, character_references={})
        self.assertEqual([record["chapter"] for record in queue], [156, 390])


if __name__ == "__main__":
    unittest.main()
