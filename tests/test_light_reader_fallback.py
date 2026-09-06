import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LightReaderFallbackTests(unittest.TestCase):
    def script(self) -> str:
        return (ROOT / 'assets/light-reader.js').read_text(encoding='utf-8')

    def test_fallback_discovers_chapters_from_books_homepage(self):
        script = self.script()
        self.assertIn("doc.querySelectorAll('#books a[href*=\"chapters/\"]')", script)
        self.assertNotIn("doc.querySelectorAll('#chapters", script)

    def test_fallback_query_parameter_requires_strict_integer(self):
        script = self.script()
        self.assertIn("const requested = Number(params.get('chapter') || '');", script)
        self.assertIn('Number.isInteger(requested)', script)
        self.assertNotIn("Number.parseInt(params.get('chapter')", script)

    def test_fallback_jump_input_requires_strict_integer(self):
        script = self.script()
        self.assertIn('const number = Number(jumpInput.value);', script)
        self.assertIn('Number.isInteger(number)', script)
        self.assertNotIn('Number.parseInt(jumpInput.value', script)

    def test_fallback_uses_text_reader_public_vocabulary(self):
        script = self.script()
        self.assertIn('TEXT READER', script)
        self.assertIn('Peg-Leg Greg Text Reader', script)
        self.assertIn('Text Reader chapter list', script)
        self.assertNotIn('LIGHT EDITION', script)
        self.assertNotIn('Peg-Leg Greg Light', script)
        self.assertNotIn(' · LIGHT', script)

    def test_workflow_guards_fallback_asset_from_legacy_vocabulary(self):
        workflow = (ROOT / '.github/workflows/light-edition.yml').read_text(encoding='utf-8')
        self.assertIn('assets/light-reader.js', workflow)
        self.assertIn(
            "if grep -R '#chapters' light/*.html light.html latest.html index.html assets/light-progress.js assets/light-reader.js; then",
            workflow,
        )
        self.assertIn(
            "if grep -R 'Light Edition' light/*.html light.html latest.html index.html assets/light-reader.js; then",
            workflow,
        )


if __name__ == '__main__':
    unittest.main()
