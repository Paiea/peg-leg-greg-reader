import unittest

from scripts.apply_chapter_role_titles import (
    clean_markdown_cell,
    parse_audit_table,
    update_html_text,
    update_markdown_text,
)


class ChapterRoleTitleIntegrationTests(unittest.TestCase):
    def test_parse_audit_table_keeps_only_rename_rows(self):
        text = """
| Ch | Current title | Decision | Proposed title | Confidence | Note |
| ---: | --- | --- | --- | --- | --- |
| 331 | The Marker Field | RENAME | The Surveyor | high | role |
| 332 | The Client | KEEP |  | high | role |
| 150 | The Work | RETIRED ADDRESS |  | high | retired |
"""
        self.assertEqual(parse_audit_table(text), {331: ("The Marker Field", "The Surveyor")})

    def test_clean_markdown_cell_removes_display_markup(self):
        self.assertEqual(clean_markdown_cell(" **The Surveyor** "), "The Surveyor")
        self.assertEqual(clean_markdown_cell(" `The Surveyor` "), "The Surveyor")

    def test_markdown_title_change_preserves_prose_exactly(self):
        source = "# CHAPTER 331\n\n## THE MARKER FIELD\n\nFirst paragraph.\n\nSecond paragraph.\n"
        updated, changed = update_markdown_text(
            source,
            {331: ("The Marker Field", "The Surveyor")},
        )
        self.assertEqual(changed, {331})
        self.assertIn("## THE SURVEYOR", updated)
        self.assertEqual(
            updated.split("## THE SURVEYOR", 1)[1],
            source.split("## THE MARKER FIELD", 1)[1],
        )

    def test_html_title_change_preserves_article_prose_exactly(self):
        source = (
            '<meta name="description" content="Peg-Leg Greg Chapter 331: The Marker Field."/>'
            '<title>Chapter 331: The Marker Field — Peg-Leg Greg</title>'
            '<h1>THE MARKER FIELD</h1>'
            '<article class="prose"><p>The marker field itself stays prose.</p></article>'
        )
        updated, changed = update_html_text(
            source,
            331,
            "The Marker Field",
            "The Surveyor",
        )
        self.assertTrue(changed)
        self.assertIn("Chapter 331: The Surveyor", updated)
        self.assertIn("<h1>THE SURVEYOR</h1>", updated)
        self.assertEqual(
            updated.split('<article class="prose">', 1)[1],
            source.split('<article class="prose">', 1)[1],
        )

    def test_html_update_is_idempotent_when_already_applied(self):
        source = '<title>Chapter 331: The Surveyor — Peg-Leg Greg</title><h1>THE SURVEYOR</h1>'
        updated, changed = update_html_text(source, 331, "The Marker Field", "The Surveyor")
        self.assertFalse(changed)
        self.assertEqual(updated, source)


if __name__ == "__main__":
    unittest.main()
