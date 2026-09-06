from __future__ import annotations

import unittest

from scripts.apply_illustration_approvals import apply_approvals
from scripts.build_generation_queue import build_generation_queue
from scripts.promote_illustrations import promote_html
from scripts.report_illustration_coverage import summarize_coverage


class GenerationQueueCoveragePriorityTests(unittest.TestCase):
    def candidate(self, chapter: int, candidate_id: str, priority: str = "high") -> dict:
        return {
            "id": candidate_id,
            "chapter": chapter,
            "chapter_title": f"CHAPTER {chapter}",
            "scene_summary": f"Scene summary for {chapter}.",
            "visual_hook": f"Visual hook for {chapter}.",
            "characters": ["Greg"],
            "location": "Carrow",
            "mood": "working",
            "priority": priority,
            "kind": "chapter_illustration",
            "fit_target": "exact",
            "spoiler_level": "low",
            "status": "prompt_ready",
            "paragraph_anchor": f"Anchor {chapter}.",
        }

    def test_zero_art_chapters_sort_ahead_of_one_art_chapters(self):
        candidates = [
            self.candidate(10, "ch010-one-art"),
            self.candidate(20, "ch020-zero-art"),
        ]
        queue = build_generation_queue(candidates, [], chapter_image_counts={10: 1, 20: 0})
        self.assertEqual([item["candidate_id"] for item in queue], ["ch020-zero-art", "ch010-one-art"])
        self.assertEqual(queue[0]["coverage_before"], 0)
        self.assertEqual(queue[1]["coverage_before"], 1)

    def test_queue_carries_generation_context_without_reopening_candidate_source(self):
        queue = build_generation_queue([self.candidate(20, "ch020-context")], [], chapter_image_counts={20: 0})
        record = queue[0]
        self.assertEqual(record["scene_summary"], "Scene summary for 20.")
        self.assertEqual(record["visual_hook"], "Visual hook for 20.")
        self.assertEqual(record["characters"], ["Greg"])
        self.assertEqual(record["location"], "Carrow")
        self.assertEqual(record["mood"], "working")
        self.assertEqual(record["spoiler_level"], "low")


class ApprovalDecisionTests(unittest.TestCase):
    def generated_record(self) -> dict:
        return {
            "id": "ch020-context-v1",
            "candidate_id": "ch020-context",
            "chapter": 20,
            "kind": "chapter_illustration",
            "status": "generated",
            "style_family": "sketch-ink-paint",
            "source_asset": "visual/chapter_art/020/ch020-context-v1.webp",
            "live_asset": "",
            "caption": "",
            "alt_text": "",
            "approved_fit": "exact",
            "prompt_pack": "state/visual/prompt-packs/ch020-context.md",
            "paragraph_anchor": "Anchor 20.",
        }

    def test_reject_decision_marks_generated_asset_rejected_without_requiring_alt_text(self):
        decision = {
            "candidate_id": "ch020-context",
            "asset": "visual/chapter_art/020/ch020-context-v1.webp",
            "decision": "reject",
            "reason": "Greg has the wrong leg anatomy.",
        }
        updated, changed = apply_approvals([self.generated_record()], [decision])
        self.assertEqual(changed, 1)
        self.assertEqual(updated[0]["status"], "rejected")
        self.assertEqual(updated[0]["notes"], "Rejected: Greg has the wrong leg anatomy.")
        self.assertEqual(updated[0]["live_asset"], "")


class PlacementToleranceTests(unittest.TestCase):
    def approved_record(self) -> dict:
        return {
            "id": "ch020-context-v1",
            "candidate_id": "ch020-context",
            "chapter": 20,
            "kind": "chapter_illustration",
            "status": "approved",
            "source_asset": "visual/chapter_art/020/ch020-context-v1.webp",
            "live_asset": "visual/chapter_art/020/ch020-context-v1.webp",
            "alt_text": "Greg works beside a cart.",
            "caption": "",
            "paragraph_anchor": "Greg worked beside the cart.",
        }

    def test_promote_html_matches_anchor_despite_html_whitespace_drift(self):
        source = "<p>Before.</p>\n<p>  Greg worked beside the cart.  </p>\n<p>After.</p>"
        promoted = promote_html(source, self.approved_record())
        self.assertIn("Greg worked beside the cart.  </p>\n<figure", promoted)


class CoverageIntelligenceTests(unittest.TestCase):
    def test_summary_distinguishes_pipeline_stage_and_zero_art_without_candidates(self):
        image_counts = {1: 0, 2: 0, 3: 1, 4: 0}
        candidates = [
            {"id": "ch001-a", "chapter": 1, "status": "prompt_ready"},
            {"id": "ch003-a", "chapter": 3, "status": "candidate"},
        ]
        registry = [
            {"candidate_id": "ch004-a", "chapter": 4, "status": "generated"},
            {"candidate_id": "legacy-live", "chapter": 3, "status": "live"},
        ]
        summary = summarize_coverage(image_counts, candidates, registry)
        self.assertEqual(summary["prompt_ready"], 1)
        self.assertEqual(summary["generated_awaiting_approval"], 1)
        self.assertEqual(summary["zero_art_without_candidate"], 1)


if __name__ == "__main__":
    unittest.main()
