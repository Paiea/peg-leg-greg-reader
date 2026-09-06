import subprocess
import sys
from pathlib import Path
import unittest

from scripts.build_illustration_backlog import build_backlog, render_backlog

ROOT = Path(__file__).resolve().parents[1]


class IllustrationBacklogTests(unittest.TestCase):
    def candidate(self, candidate_id, chapter, priority="medium", status="candidate", kind="chapter_illustration"):
        return {
            "id": candidate_id,
            "chapter": chapter,
            "chapter_title": f"Chapter {chapter}",
            "scene_summary": "A useful visual moment.",
            "visual_hook": f"Visual hook for {candidate_id}",
            "characters": [],
            "location": "",
            "mood": "",
            "priority": priority,
            "kind": kind,
            "fit_target": "close_enough",
            "spoiler_level": "low",
            "status": status,
        }

    def test_zero_art_chapter_ranks_ahead_of_one_art_chapter(self):
        candidates = [
            self.candidate("one-art", 10, priority="high"),
            self.candidate("zero-art", 11, priority="medium"),
        ]
        backlog = build_backlog(candidates, [], {10: 1, 11: 0})
        self.assertEqual([item["id"] for item in backlog], ["zero-art", "one-art"])

    def test_priority_breaks_ties_at_equal_coverage(self):
        candidates = [
            self.candidate("medium", 20, priority="medium"),
            self.candidate("high", 21, priority="high"),
        ]
        backlog = build_backlog(candidates, [], {20: 0, 21: 0})
        self.assertEqual([item["id"] for item in backlog], ["high", "medium"])

    def test_live_and_rejected_candidates_are_excluded(self):
        candidates = [
            self.candidate("candidate", 30),
            self.candidate("live", 31, status="live"),
            self.candidate("rejected", 32, status="rejected"),
        ]
        backlog = build_backlog(candidates, [], {})
        self.assertEqual([item["id"] for item in backlog], ["candidate"])

    def test_registered_live_candidate_is_excluded_even_if_candidate_state_is_stale(self):
        candidates = [self.candidate("stale-candidate", 40)]
        registry = [{"candidate_id": "stale-candidate", "status": "live"}]
        self.assertEqual(build_backlog(candidates, registry, {40: 0}), [])

    def test_card_kinds_rank_ahead_of_chapter_illustrations(self):
        candidates = [
            self.candidate("chapter", 50, kind="chapter_illustration"),
            self.candidate("book", 50, kind="book_card"),
            self.candidate("act", 50, kind="act_card"),
            self.candidate("role", 50, kind="role_card"),
        ]
        backlog = build_backlog(candidates, [], {50: 0})
        self.assertEqual([item["kind"] for item in backlog], ["book_card", "act_card", "role_card", "chapter_illustration"])

    def test_rendered_backlog_contains_operational_fields(self):
        backlog = build_backlog([self.candidate("scene-a", 60, priority="high")], [], {60: 0})
        text = render_backlog(backlog)
        for fragment in ("scene-a", "Chapter 60", "high", "close_enough", "0 image"):
            self.assertIn(fragment, text)

    def test_illustration_scripts_run_as_direct_cli_entry_points(self):
        for relative_path in (
            "scripts/build_illustration_backlog.py",
            "scripts/build_prompt_packs.py",
            "scripts/report_illustration_coverage.py",
        ):
            with self.subTest(script=relative_path):
                result = subprocess.run(
                    [sys.executable, relative_path],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, msg=result.stderr)


if __name__ == "__main__":
    unittest.main()
