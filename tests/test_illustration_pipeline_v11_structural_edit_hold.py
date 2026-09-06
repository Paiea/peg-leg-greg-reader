from __future__ import annotations

import unittest

from scripts.build_generation_queue import build_generation_queue
from scripts.illustration_edit_hold import edit_hold_active, reconcile_candidates


class StructuralEditHoldTests(unittest.TestCase):
    def test_active_structural_edit_hold_stops_generation_queue_without_mutating_candidates(self):
        candidates = [{
            "id": "ch156-order-coat",
            "chapter": 156,
            "chapter_title": "THE ADVOCATE",
            "kind": "chapter_illustration",
            "priority": "high",
            "fit_target": "exact",
            "spoiler_level": "low",
            "scene_summary": "Nessa stuffs the order into Greg's coat while his hands are occupied.",
            "visual_hook": "workplace comedy and physical constraint",
            "characters": ["Greg", "Nessa"],
            "status": "prompt_ready",
            "paragraph_anchor": "She came over, took the order, and shoved it inside the front of my Advocate coat.",
        }]
        hold = {
            "active": True,
            "mode": "structural_edit_hold",
            "generation_allowed": False,
        }

        self.assertTrue(edit_hold_active(hold))
        queue = build_generation_queue(candidates, [], production_hold=hold)
        self.assertEqual(queue, [])
        self.assertEqual(candidates[0]["status"], "prompt_ready")
        self.assertEqual(candidates[0]["chapter"], 156)

    def test_inactive_hold_does_not_block_generation(self):
        candidates = [{
            "id": "candidate",
            "chapter": 10,
            "chapter_title": "TEST",
            "kind": "chapter_illustration",
            "priority": "medium",
            "fit_target": "close_enough",
            "spoiler_level": "low",
            "scene_summary": "A visual moment.",
            "visual_hook": "clear action",
            "characters": [],
            "status": "prompt_ready",
        }]
        queue = build_generation_queue(
            candidates,
            [],
            chapter_image_counts={10: 0},
            production_hold={"active": False, "mode": "structural_edit_hold", "generation_allowed": False},
        )
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["candidate_id"], "candidate")


class CandidateReconciliationTests(unittest.TestCase):
    def test_reconciliation_preserves_semantic_candidate_identity_when_anchor_drifts(self):
        candidate = {
            "id": "ch159-fish-rescue",
            "chapter": 159,
            "chapter_title": "THE PRIVATE PLAYER",
            "scene_summary": "Greg and Pell recover the wooden fish from under the stage.",
            "visual_hook": "prop rescue under the stage",
            "paragraph_anchor": "We found the fish wedged behind a support where someone had pushed it with a boot.",
        }
        rows = reconcile_candidates([candidate], {159: "The scene was substantially compressed and the old sentence is gone."})
        self.assertEqual(rows[0]["candidate_id"], "ch159-fish-rescue")
        self.assertEqual(rows[0]["source_chapter"], 159)
        self.assertEqual(rows[0]["reconciliation_status"], "anchor_drift")
        self.assertEqual(rows[0]["scene_summary"], candidate["scene_summary"])
        self.assertEqual(rows[0]["visual_hook"], candidate["visual_hook"])

    def test_reconciliation_distinguishes_stable_ambiguous_and_missing_chapter(self):
        candidates = [
            {"id": "stable", "chapter": 1, "paragraph_anchor": "A distinctive sentence remains intact."},
            {"id": "ambiguous", "chapter": 2, "paragraph_anchor": "Repeated line."},
            {"id": "missing", "chapter": 3, "paragraph_anchor": "Old chapter line."},
        ]
        rows = reconcile_candidates(
            candidates,
            {
                1: "Before. A distinctive sentence remains intact. After.",
                2: "Repeated line. Something. Repeated line.",
            },
        )
        by_id = {row["candidate_id"]: row for row in rows}
        self.assertEqual(by_id["stable"]["reconciliation_status"], "stable")
        self.assertEqual(by_id["ambiguous"]["reconciliation_status"], "anchor_ambiguous")
        self.assertEqual(by_id["missing"]["reconciliation_status"], "chapter_missing")

    def test_reconciliation_never_auto_reassigns_a_candidate_to_a_different_chapter(self):
        candidate = {
            "id": "moved-scene",
            "chapter": 5,
            "scene_summary": "A scene that may survive a chapter merge.",
            "visual_hook": "strong visual beat",
            "paragraph_anchor": "This exact scene text moved.",
        }
        rows = reconcile_candidates(
            [candidate],
            {
                5: "The old chapter no longer contains it.",
                6: "This exact scene text moved.",
            },
        )
        self.assertEqual(rows[0]["source_chapter"], 5)
        self.assertEqual(rows[0]["reconciliation_status"], "anchor_drift")
        self.assertNotIn("new_chapter", rows[0])


if __name__ == "__main__":
    unittest.main()
