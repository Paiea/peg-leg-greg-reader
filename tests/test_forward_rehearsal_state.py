import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ForwardRehearsalStateTests(unittest.TestCase):
    def test_open_threads_routes_to_current_endpoint(self):
        text = (ROOT / "state" / "OPEN_THREADS.md").read_text(encoding="utf-8")
        self.assertIn("Chapter 492 - **THE RESPONDENT**", text)
        self.assertNotIn("Current exact story endpoint: Chapter 320", text)
        self.assertIn("`MANUSCRIPT_STATE.md` owns the exact endpoint", text)

    def test_chapter_index_is_current_and_compact(self):
        text = (ROOT / "state" / "MANUSCRIPT_CHAPTER_INDEX.md").read_text(encoding="utf-8")
        self.assertIn("Chapter 492 - **THE RESPONDENT**", text)
        self.assertNotIn("**Current endpoint:** Chapter 248", text)
        self.assertIn("481. **THE SUBSTITUTE**", text)
        self.assertIn("492. **THE RESPONDENT**", text)
        self.assertIn("search the repository", text.lower())

    def test_forward_workflow_places_rehearsal_before_prose(self):
        text = (
            ROOT / "state" / "editorial" / "rehearsal" / "FORWARD_WORKFLOW.md"
        ).read_text(encoding="utf-8")
        core = "COMPETING POSSIBILITIES -> REHEARSAL DISCOVERIES -> OPTIONAL PERFORMANCE -> SELECTED SCENE PACKET -> PROSE"
        self.assertIn(core, text)
        self.assertIn("REHEARSAL happens before prose", text)
        self.assertIn("PERFORMANCE is optional", text)
        self.assertIn("REHEARSAL output should be compact enough to render from", text)

    def test_proving_run_covers_493_through_500(self):
        path = (
            ROOT
            / "state"
            / "editorial"
            / "rehearsal"
            / "forward"
            / "proving-run-493-500.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "forward_rehearsal_proving_run/v1")
        self.assertEqual(data["range"], {"start": 493, "end": 500})
        chapters = data["chapters"]
        self.assertEqual([row["chapter"] for row in chapters], list(range(493, 501)))
        self.assertTrue(all(row["status"] == "pending" for row in chapters))
        self.assertIn("performance", chapters[0])
        self.assertIn("evaluation", data)


if __name__ == "__main__":
    unittest.main()
