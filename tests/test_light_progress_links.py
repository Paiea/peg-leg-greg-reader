import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from generate_light import Chapter, render_index


class LightProgressLinkTests(unittest.TestCase):
    def test_continue_reading_uses_compatibility_router_for_any_saved_chapter(self):
        script = (ROOT / 'assets/light-progress.js').read_text(encoding='utf-8')
        self.assertIn("../light.html?chapter=${chapter}", script)
        self.assertNotIn("${String(chapter).padStart(3, '0')}.html", script)

    def test_progress_script_has_no_homepage_repair_layer(self):
        script = (ROOT / 'assets/light-progress.js').read_text(encoding='utf-8')
        self.assertNotIn("main.home", script)
        self.assertNotIn("#chapters", script)
        self.assertNotIn("contents.id = 'books'", script)
        self.assertNotIn("Illustrated Reader", script)

    def test_progress_script_requires_a_strict_integer_saved_chapter(self):
        script = (ROOT / 'assets/light-progress.js').read_text(encoding='utf-8')
        self.assertIn("Number(localStorage.getItem('plg:lastLightChapter') || '')", script)
        self.assertIn('Number.isInteger(chapter)', script)
        self.assertNotIn('Number.parseInt', script)

    def test_progress_script_rejects_saved_chapters_beyond_current_frontier(self):
        script = (ROOT / 'assets/light-progress.js').read_text(encoding='utf-8')
        self.assertIn('target.dataset.latestChapter', script)
        self.assertIn('Number.isInteger(latest)', script)
        self.assertIn('chapter > latest', script)

    def test_text_reader_index_exposes_latest_chapter_to_progress_script(self):
        chapters = {
            n: Chapter(n, f'THE CHAPTER {n}', '<p>Body</p>', 'test')
            for n in range(1, 243)
        }
        rendered = render_index(chapters, set(chapters))
        self.assertIn(
            '<p class="light-continue" data-light-continue data-latest-chapter="242" hidden>',
            rendered,
        )

    def test_workflow_guards_progress_asset_against_legacy_chapters_anchor(self):
        workflow = (ROOT / '.github/workflows/light-edition.yml').read_text(encoding='utf-8')
        self.assertIn(
            "if grep -R '#chapters' light/*.html light.html latest.html index.html assets/light-progress.js; then",
            workflow,
        )


if __name__ == '__main__':
    unittest.main()
