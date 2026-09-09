import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'


class R2SiteTests(unittest.TestCase):
    def test_project_manifest_names_run_two_and_preserves_run_one(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['project_id'], 'r2')
        self.assertEqual(project['title'], 'R2')
        self.assertIn('two lives', project['tagline'].lower())
        self.assertEqual(project['run1_href'], '../index.html')
        self.assertEqual(project['chapters'], ['r2-ch001', 'r2-ch002'])
        self.assertEqual(project['current_chapter'], 'r2-ch002')

    def test_chapter_one_reuses_existing_audio_without_claiming_missing_prose(self):
        chapter = json.loads((R2 / 'data/chapters/ch001.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['chapter_id'], 'r2-ch001')
        self.assertEqual(chapter['title'], 'The Boy')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../greg-again/audio/assets/chapter-001.mp3')
        self.assertEqual(chapter['written']['status'], 'unavailable')
        self.assertEqual(chapter['images'], [])

    def test_chapter_two_reuses_current_main_audio(self):
        chapter = json.loads((R2 / 'data/chapters/ch002.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['chapter_id'], 'r2-ch002')
        self.assertEqual(chapter['title'], 'Two Things')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../greg-again/audio/assets/chapter-002.mp3')
        self.assertEqual(chapter['written']['status'], 'unavailable')
        self.assertEqual(chapter['navigation']['previous'], 'r2-ch001')

    def test_homepage_explains_run_two_and_links_run_one(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('Greg has had two lives so far. So has his story.', html)
        self.assertIn('Peg-Leg Greg was written once already', html)
        self.assertIn('href="../index.html"', html)
        self.assertIn('Listen', html)
        self.assertIn('Read', html)
        self.assertIn('Look', html)

    def test_public_routes_exist(self):
        for path in ['about/index.html', 'chapters/index.html', 'gallery/index.html', 'chapter.html']:
            self.assertTrue((R2 / path).exists(), path)

    def test_chapter_renderer_has_missing_media_fallbacks(self):
        js = (R2 / 'assets/js/chapter.js').read_text(encoding='utf-8')
        self.assertIn('Written rendition coming soon.', js)
        self.assertIn('Audio version coming soon.', js)
        self.assertIn('new URLSearchParams', js)
        self.assertIn("document.createElement('audio')", js)
        self.assertIn('chapter.images', js)

    def test_site_renderer_is_manifest_driven(self):
        js = (R2 / 'assets/js/site.js').read_text(encoding='utf-8')
        self.assertIn('data/project.json', js)
        self.assertIn('data/chapters/', js)
        self.assertIn('chapter.html?id=', js)

    def test_r2_css_is_responsive_and_audio_first(self):
        css = (R2 / 'assets/css/r2.css').read_text(encoding='utf-8')
        self.assertIn('.audio-panel', css)
        self.assertIn('.reading-copy', css)
        self.assertIn('min-height: 44px', css)
        self.assertIn('@media (max-width: 760px)', css)
        self.assertNotIn('animation:', css)

    def test_hero_asset_is_referenced_without_becoming_chapter_canon(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('assets/images/r2-harbor-hero.webp', html)
        chapter = json.loads((R2 / 'data/chapters/ch001.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['images'], [])


if __name__ == '__main__':
    unittest.main()
