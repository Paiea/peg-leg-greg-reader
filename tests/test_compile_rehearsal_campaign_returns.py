import tempfile
import unittest
from pathlib import Path

from scripts import compile_rehearsal_campaign_returns as compiler


class RehearsalCampaignReturnCompilerTests(unittest.TestCase):
    def worker_result(self, candidates=None):
        return {
            "schema": "rehearsal_campaign_worker_result/v1",
            "batch": {"start": 61, "end": 70, "source_authority": "abc123"},
            "chapters": [
                {"chapter": n, "disposition": "source_win", "discoveries": [], "rejected_hot": []}
                for n in range(61, 71)
            ],
            "candidates": candidates or [],
        }

    def candidate(self, **overrides):
        base = {
            "id": "c061-test-01",
            "chapter": 61,
            "actor": "Actor",
            "role": "Role",
            "supporting_actors": ["Nico as Greg"],
            "take_id": "061-free-a",
            "variance_group_id": None,
            "actor_prefers": True,
            "dramatic_lock_status": "preserved",
            "reader_check": "pass",
            "changed_surfaces": ["dialogue", "movement"],
            "before": "<p>Original line.</p>",
            "after": "<p>Performed line.</p>",
            "reason": "performed specificity",
        }
        base.update(overrides)
        return base

    def test_zero_candidates_returns_source_win(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = compiler.compile_worker_result(Path(tmp), self.worker_result())
        self.assertEqual("source_win", result["result"])
        self.assertIsNone(result["manifest"])

    def test_candidate_must_match_literal_current_html_exactly_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "chapters").mkdir()
            (root / "chapters" / "061.html").write_text("<article><p>Original line.</p></article>", encoding="utf-8")
            result = compiler.compile_worker_result(root, self.worker_result([self.candidate()]))
        self.assertEqual("returns", result["result"])
        self.assertEqual("free_production", result["manifest"]["mode"])
        self.assertEqual(1, len(result["manifest"]["patches"]))

    def test_rendered_boundary_hallucination_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "chapters").mkdir()
            (root / "chapters" / "061.html").write_text("<article><p>Lead. Original line.</p></article>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "literal exact source"):
                compiler.compile_worker_result(root, self.worker_result([self.candidate()]))

    def test_candidate_cannot_escape_claimed_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "claimed batch"):
                compiler.compile_worker_result(Path(tmp), self.worker_result([self.candidate(chapter=71)]))

    def test_discovery_only_surfaces_are_not_writable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "chapters").mkdir()
            (root / "chapters" / "061.html").write_text("<p>Original line.</p>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "writable surface"):
                compiler.compile_worker_result(
                    root,
                    self.worker_result([self.candidate(changed_surfaces=["relationship_behavior"])]),
                )

    def test_hard_surfaces_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "chapters").mkdir()
            (root / "chapters" / "061.html").write_text("<p>Original line.</p>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hard surface"):
                compiler.compile_worker_result(
                    root,
                    self.worker_result([self.candidate(changed_surfaces=["plot"])]),
                )


if __name__ == "__main__":
    unittest.main()
