import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / 'r2'


class R2SiteTests(unittest.TestCase):
    def test_project_manifest_names_run_two_and_preserves_run_one(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['title'], 'Peg-Leg Greg R2')
        self.assertEqual(project['series_title'], 'Peg-Leg Greg')
        self.assertEqual(project['run_label'], 'R2')
        self.assertEqual(project['run_number'], 2)
        self.assertEqual(project['previous_run']['label'], 'Run 1')
        self.assertEqual(project['previous_run']['href'], '../')

    def test_public_frontier_is_character_rebuild_through_chapter_thirty_nine(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        registry = json.loads((R2 / 'data/chapter-registry.json').read_text(encoding='utf-8'))
        self.assertEqual(project['public_frontier_chapter'], 39)
        self.assertEqual(registry['current_chapter'], 'r2-ch039')
        self.assertEqual(list(registry['chapters'])[-1], 'r2-ch039')
        self.assertFalse((R2 / 'data/chapters/ch040.json').exists())

    def test_rebuild_titles_are_public(self):
        expected = {
            27: 'The Late Letter',
            28: 'Eventually',
            29: 'The Seven',
            30: 'The Workshop',
            31: 'The Next Road',
            32: 'Two Copper',
            33: 'Route Day',
            34: 'The Packet',
            35: 'The Ask',
            36: 'Four Nights',
            37: 'One Day Late',
            38: 'Two Keys',
            39: 'The East Desk',
        }
        for number, title in expected.items():
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['title'], title)
            self.assertEqual(chapter['images'], [])
            self.assertIn(chapter['audio']['status'], {'unavailable', 'published'})

    def test_registry_is_rerouted_and_legacy_registry_is_archived(self):
        registry = json.loads((R2 / 'data/chapter-registry.json').read_text(encoding='utf-8'))
        self.assertEqual(registry['current_chapter'], 'r2-ch039')
        self.assertEqual(list(registry['chapters'])[-1], 'r2-ch039')
        self.assertNotIn('r2-ch040', registry['chapters'])
        self.assertTrue((R2 / 'editorial/legacy-forward/chapter-registry-pre-character-rebuild.json').exists())
        authority = (R2 / 'PUBLIC_REBUILD_AUTHORITY.md').read_text(encoding='utf-8')
        self.assertIn('Chapter 39', authority)
        self.assertIn('40+', authority)

    def test_r2_declares_shared_greg_surface_pipeline(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['rendering_pipeline'], 'data/rendering-pipeline.json')

    def test_public_copy_presents_r2_as_an_intentional_story(self):
        index = (R2 / 'index.html').read_text(encoding='utf-8')
        about = (R2 / 'about/index.html').read_text(encoding='utf-8')
        self.assertIn('Peg-Leg Greg R2', index)
        self.assertIn('Run 2', about)
        self.assertNotIn('experimental rewrite', index.lower())
        self.assertNotIn('experimental rewrite', about.lower())

    def test_homepage_presents_clean_cover_entry_and_links_run_one(self):
        index = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('r2-cover-wide.webp', index)
        self.assertIn('Run 1', index)
        self.assertIn('../', index)

    def test_cover_asset_is_referenced_without_becoming_chapter_canon(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        self.assertIn('cover', project)
        self.assertEqual(project['cover']['asset'], 'assets/images/r2-cover-wide.webp')
        self.assertTrue((R2 / project['cover']['asset']).exists())
        self.assertNotIn('r2-cover-wide.webp', json.dumps(json.loads((R2 / 'data/chapter-registry.json').read_text(encoding='utf-8'))))

    def test_site_renderer_is_manifest_driven(self):
        app = (R2 / 'assets/js/app.js').read_text(encoding='utf-8')
        self.assertIn('data/project.json', app)
        self.assertIn('data/chapter-registry.json', app)

    def test_chapter_renderer_has_missing_media_fallbacks(self):
        app = (R2 / 'assets/js/app.js').read_text(encoding='utf-8')
        self.assertIn('Written rendition not published yet.', app)
        self.assertIn('Audio rendition not published yet.', app)

    def test_written_renderer_hides_internal_experiment_prelude(self):
        app = (R2 / 'assets/js/app.js').read_text(encoding='utf-8')
        self.assertIn("/^#\\s+Chapter\\s+\\d+:/i", app)

    def test_r2_css_is_responsive_and_audio_first(self):
        css = (R2 / 'assets/css/r2.css').read_text(encoding='utf-8')
        self.assertIn('.audio-player', css)
        self.assertIn('@media', css)

    def test_public_routes_exist(self):
        self.assertTrue((R2 / 'index.html').exists())
        self.assertTrue((R2 / 'chapters/index.html').exists())
        self.assertTrue((R2 / 'about/index.html').exists())

    def test_existing_audio_before_rebuild_is_preserved(self):
        for number in range(1, 27):
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            if chapter['audio']['status'] == 'published':
                self.assertTrue(chapter['audio']['path'].endswith(f'chapter-{number:03d}.mp3'))

    def test_existing_public_role_title_is_preserved(self):
        ch1 = json.loads((R2 / 'data/chapters/ch001.json').read_text(encoding='utf-8'))
        self.assertEqual(ch1['role_title'], 'THE BOY')

    def test_homepage_progress_is_manifest_aware(self):
        index = (R2 / 'index.html').read_text(encoding='utf-8')
        app = (R2 / 'assets/js/app.js').read_text(encoding='utf-8')
        self.assertIn('chapter-count', index)
        self.assertIn('audio-progress', index)
        self.assertIn('written-progress', index)
        self.assertIn('audio-progress', app)
        self.assertIn('written-progress', app)

    def test_selected_written_chapters_publish_directly_to_r2_reader(self):
        for number in (1, 8, 11, 16):
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['written']['status'], 'published')
            self.assertTrue(chapter['written']['path'].startswith('../assets/written/'))


if __name__ == '__main__':
    unittest.main()
