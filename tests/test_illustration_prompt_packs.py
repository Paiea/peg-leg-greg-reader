import unittest

from scripts.build_prompt_packs import prompt_pack_filename, render_prompt_pack


class IllustrationPromptPackTests(unittest.TestCase):
    def candidate(self, characters=None):
        return {
            "id": "ch090-chair-floor",
            "chapter": 90,
            "chapter_title": "The Example",
            "scene_summary": "Greg negotiates around a stubborn chair in a cramped shop.",
            "visual_hook": "A chair blocks the doorway while bodies angle around it.",
            "characters": characters or [],
            "location": "cramped shop",
            "mood": "dryly comic",
            "priority": "high",
            "kind": "chapter_illustration",
            "fit_target": "close_enough",
            "spoiler_level": "low",
            "status": "candidate",
            "paragraph_anchor": "Chair can stay today.",
        }

    def test_prompt_pack_contains_visual_bible_prompt_components(self):
        text = render_prompt_pack(self.candidate(["Greg"]))
        for fragment in (
            "SUBJECT + ACTION",
            "CAMERA",
            "FOREGROUND",
            "ENVIRONMENTAL MOVEMENT",
            "EYE PATH",
            "MANUSCRIPT DETAILS",
            "CONTINUITY",
            "SKETCH + INK + PAINT",
            "close_enough",
            "A chair blocks the doorway",
        ):
            self.assertIn(fragment, text)

    def test_greg_continuity_is_included_when_greg_is_present(self):
        text = render_prompt_pack(self.candidate(["Greg"]))
        self.assertIn("permanent LEFT BKA", text)
        self.assertIn("two crutches", text)

    def test_greg_continuity_is_not_forced_when_greg_is_absent(self):
        text = render_prompt_pack(self.candidate(["Lyssa"]))
        self.assertNotIn("permanent LEFT BKA", text)

    def test_lyssa_continuity_is_included_when_lyssa_is_present(self):
        text = render_prompt_pack(self.candidate(["Lyssa"]))
        self.assertIn("Black woman", text)
        self.assertIn("Afro-textured hair", text)

    def test_prompt_pack_filename_is_deterministic(self):
        self.assertEqual(prompt_pack_filename(self.candidate()), "ch090-chair-floor.md")


if __name__ == "__main__":
    unittest.main()
