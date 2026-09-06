import unittest

from scripts import apply_performance_novelization_experiment as exp
from scripts import clean_performance_novelization_seams as seams


class PerformanceNovelizationExperimentTests(unittest.TestCase):
    def test_only_three_surviving_source_files_are_mutated(self):
        self.assertEqual(
            {"chapters/007.html", "chapters/013.html", "chapters/018.html"},
            set(exp.TARGET_PATHS),
        )

    def test_mixed_lab_scenes_remain_explicit_source_wins(self):
        self.assertEqual({2, 16}, set(exp.SOURCE_WINS))

    def test_replacements_do_not_add_em_dashes(self):
        for patch in exp.PATCHES:
            self.assertNotIn("—", "\n".join(patch.replacement))

    def test_paragraph_span_replacement_is_exact_and_preserves_neighbors(self):
        page = '<article class="prose"><p>before</p><p>start</p><p>middle</p><p>end</p><p>after</p></article>'
        updated = exp.replace_paragraph_span(page, "start", "end", ("new one", "new two"))
        self.assertIn("<p>before</p>", updated)
        self.assertIn("<p>after</p>", updated)
        self.assertIn("<p>new one</p><p>new two</p>", updated)
        self.assertNotIn("<p>middle</p>", updated)

    def test_ambiguous_start_boundary_fails_closed(self):
        page = '<article class="prose"><p>start</p><p>end</p><p>start</p><p>end</p></article>'
        with self.assertRaisesRegex(AssertionError, "start boundary"):
            exp.replace_paragraph_span(page, "start", "end", ("new",))

    def test_showcase_borrower_to_expert_seam_reestablishes_hidden_shale_result(self):
        cleaner = getattr(seams, "clean_004", None)
        self.assertIsNotNone(cleaner, "clean_004 must repair the displayed 2 -> 3 seam")
        if cleaner is None:
            return
        source = (
            '<article class="prose"><p>before</p>'
            '<p>The room did not object. The shale project had become the most dangerous kind of thing: promising. Failure would have been cleaner. If Arlo had looked at the sixth disk and said no, useless, wrong, then the project could die with dignity. Instead we had a twenty-percent improvement, a path toward better tests, and no idea whether the final product would take two weeks or two years.</p>'
            '<p>after</p></article>'
        )
        updated = cleaner(source)
        self.assertIn(
            "The sixth disk had barely beaten the control; by the end of the night, Arlo's best result was closer to twenty percent.",
            updated,
        )
        self.assertIn("<p>before</p>", updated)
        self.assertIn("<p>after</p>", updated)
        self.assertNotIn("Instead we had a twenty-percent improvement", updated)


if __name__ == "__main__":
    unittest.main()
