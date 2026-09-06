import unittest

from scripts import apply_performance_novelization_experiment as exp


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


if __name__ == "__main__":
    unittest.main()
