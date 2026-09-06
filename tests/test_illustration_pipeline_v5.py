from __future__ import annotations

import unittest

from scripts.build_approval_packet import generated_records_for_review, render_approval_packet
from scripts.build_generation_packet import render_generation_packet, select_generation_batch
from scripts.build_generation_queue import build_generation_queue
from scripts.report_illustration_coverage import summarize_coverage
from scripts.sync_scene_candidate_status import sync_candidate_statuses


class GenerationPacketTests(unittest.TestCase):
    def test_generation_packet_exports_top_ready_batch_with_continuity_context(self):
        queue = [
            {
                "candidate_id": "ch010-a",
                "chapter": 10,
                "chapter_title": "THE APPRAISER",
                "priority": "high",
                "visual_hook": "Greg studies a worked blade at the bench.",
                "prompt_pack": "state/visual/prompt-packs/ch010-a.md",
                "target_asset": "visual/chapter_art/010/ch010-a-v1.webp",
                "coverage_before": 0,
                "style_family": "sketch-ink-paint",
                "framing_preference": "above_waist",
                "character_reference_assets": ["assets/book-role-cards/book-ii-stagehand-177.webp"],
                "character_appearance_notes": {"Greg": "Young man; keep face and build consistent with accepted Greg art."},
                "status": "generation_ready",
            },
            {
                "candidate_id": "ch011-b",
                "chapter": 11,
                "chapter_title": "THE MAGE",
                "priority": "high",
                "visual_hook": "A narrow spell test.",
                "prompt_pack": "state/visual/prompt-packs/ch011-b.md",
                "target_asset": "visual/chapter_art/011/ch011-b-v1.webp",
                "coverage_before": 0,
                "status": "generation_ready",
            },
        ]
        selected = select_generation_batch(queue, limit=1)
        self.assertEqual([item["candidate_id"] for item in selected], ["ch010-a"])
        packet = render_generation_packet(selected)
        self.assertIn("# PEG-LEG GREG — GENERATION PACKET", packet)
        self.assertIn("Framing preference: above_waist", packet)
        self.assertIn("assets/book-role-cards/book-ii-stagehand-177.webp", packet)
        self.assertIn("Young man; keep face and build consistent", packet)


class ApprovalPacketTests(unittest.TestCase):
    def test_approval_packet_surfaces_generated_assets_only(self):
        registry = [
            {
                "id": "ch010-a-v1",
                "candidate_id": "ch010-a",
                "chapter": 10,
                "status": "generated",
                "source_asset": "visual/chapter_art/010/ch010-a-v1.webp",
                "prompt_pack": "state/visual/prompt-packs/ch010-a.md",
                "approved_fit": "exact",
            },
            {
                "id": "ch011-b-v1",
                "candidate_id": "ch011-b",
                "chapter": 11,
                "status": "approved",
                "source_asset": "visual/chapter_art/011/ch011-b-v1.webp",
                "prompt_pack": "state/visual/prompt-packs/ch011-b.md",
                "approved_fit": "exact",
            },
        ]
        generated = generated_records_for_review(registry)
        self.assertEqual([item["candidate_id"] for item in generated], ["ch010-a"])
        packet = render_approval_packet(generated)
        self.assertIn('"decision": "approve"', packet)
        self.assertIn('"decision": "reject"', packet)
        self.assertIn("visual/chapter_art/010/ch010-a-v1.webp", packet)


class CandidateStatusSyncTests(unittest.TestCase):
    def test_candidate_status_tracks_progress_but_rejected_attempt_stays_retryable(self):
        candidates = [
            {"id": "a", "status": "prompt_ready"},
            {"id": "b", "status": "prompt_ready"},
        ]
        registry = [
            {"candidate_id": "a", "status": "generated"},
            {"candidate_id": "a", "status": "approved"},
            {"candidate_id": "b", "status": "rejected"},
        ]
        synced, changed = sync_candidate_statuses(candidates, registry)
        self.assertEqual(changed, 2)
        self.assertEqual(synced[0]["status"], "approved")
        self.assertEqual(synced[1]["status"], "prompt_ready")
        self.assertEqual(synced[1]["latest_generation_status"], "rejected")


class CoverageActionPreviewTests(unittest.TestCase):
    def test_summary_exposes_actionable_chapter_previews(self):
        summary = summarize_coverage(
            {1: 0, 2: 0, 3: 1, 4: 0, 5: 0},
            [
                {"id": "ch001-a", "chapter": 1, "status": "candidate"},
                {"id": "ch002-a", "chapter": 2, "status": "prompt_ready"},
            ],
            [
                {"candidate_id": "ch004-a", "chapter": 4, "status": "generated"},
                {"candidate_id": "live-3", "chapter": 3, "status": "live"},
            ],
        )
        self.assertEqual(summary["top_zero_art_without_candidate"], [5])
        self.assertEqual(summary["top_prompt_ready_chapters"], [2])
        self.assertEqual(summary["top_generated_waiting_chapters"], [4])


class ContinuityMetadataTests(unittest.TestCase):
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

    def test_queue_adds_default_greg_framing_and_character_reference_metadata(self):
        references = {
            "Greg": {
                "appearance_notes": "Young man; match accepted Greg face/build and current-period grooming.",
                "reference_assets": [
                    "visual/homepage/peg-leg-greg-homepage-frontispiece.png",
                    "assets/book-role-cards/book-ii-stagehand-177.webp",
                ],
            },
            "Lyssa": {
                "appearance_notes": "Black woman, tall relative to Greg, thin/lithe, natural Afro-textured hair.",
                "reference_assets": [],
            },
        }
        queue = build_generation_queue(
            [self.candidate()],
            [],
            chapter_image_counts={20: 0},
            character_references=references,
        )
        record = queue[0]
        self.assertEqual(record["framing_preference"], "above_waist")
        self.assertEqual(record["style_family"], "sketch-ink-paint")
        self.assertIn("assets/book-role-cards/book-ii-stagehand-177.webp", record["character_reference_assets"])
        self.assertIn("Lyssa", record["character_appearance_notes"])
        self.assertIn("avoid unnecessary lower-body visibility", record["continuity_notes"])


if __name__ == "__main__":
    unittest.main()
