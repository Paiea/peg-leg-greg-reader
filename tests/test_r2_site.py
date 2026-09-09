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
        self.assertEqual(project['chapters'], [f'r2-ch{i:03d}' for i in range(1, 18)])
        self.assertEqual(project['current_chapter'], 'r2-ch017')

    def test_r2_declares_shared_greg_surface_pipeline(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['rendering_pipeline'], 'data/rendering-pipeline.json')

        pipeline = json.loads((R2 / 'data/rendering-pipeline.json').read_text(encoding='utf-8'))
        self.assertEqual(pipeline['schema'], 'r2_rendering_pipeline/v1')
        self.assertEqual(
            pipeline['shared_flow'],
            ['story_state_or_performance', 'greg_experience', 'shared_greg_surface'],
        )
        self.assertEqual(pipeline['renderers']['audio']['input'], 'shared_greg_surface')
        self.assertEqual(pipeline['renderers']['written']['input'], 'shared_greg_surface')
        self.assertEqual(
            pipeline['feedback_classes'],
            ['shared_greg_experience', 'audio_only', 'written_only'],
        )

        contract = (R2 / 'PIPELINE.md').read_text(encoding='utf-8')
        self.assertIn('Clean performance residue. Do not clean away cognition.', contract)
        self.assertIn('Greg may own the linguistic surface.', contract)
        self.assertIn('Audio Finish', contract)
        self.assertIn('Written Finish', contract)

        readme = (R2 / 'README.md').read_text(encoding='utf-8')
        self.assertIn('PIPELINE.md', readme)
        self.assertIn('Shared Greg Surface', readme)
        self.assertIn('medium-specific finish', readme)

    def test_written_frontier_is_public_through_chapter_seventeen(self):
        for number in range(1, 18):
            chapter_id = f'r2-ch{number:03d}'
            manifest_path = R2 / f'data/chapters/ch{number:03d}.json'
            self.assertTrue(manifest_path.exists(), chapter_id)
            chapter = json.loads(manifest_path.read_text(encoding='utf-8'))
            self.assertEqual(chapter['chapter_id'], chapter_id)
            self.assertEqual(chapter['display_number'], number)
            self.assertEqual(chapter['written']['status'], 'published')
            self.assertEqual(chapter['written']['path'], f'assets/written/ch{number:03d}.md')
            self.assertTrue((R2 / f'assets/written/ch{number:03d}.md').exists(), chapter_id)
            self.assertEqual(
                chapter['navigation']['previous'],
                None if number == 1 else f'r2-ch{number - 1:03d}',
            )
            self.assertEqual(
                chapter['navigation']['next'],
                None if number == 17 else f'r2-ch{number + 1:03d}',
            )

    def test_written_renderer_hides_internal_experiment_prelude(self):
        js = (R2 / 'assets/js/chapter.js').read_text(encoding='utf-8')
        self.assertIn('function stripInternalPrelude(markdown)', js)
        self.assertIn('stripInternalPrelude(await response.text())', js)

    def test_chapter_one_reuses_existing_audio_and_publishes_written(self):
        chapter = json.loads((R2 / 'data/chapters/ch001.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['chapter_id'], 'r2-ch001')
        self.assertEqual(chapter['title'], 'The Boy')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../greg-again/audio/assets/chapter-001.mp3')
        self.assertEqual(chapter['written']['status'], 'published')
        self.assertEqual(chapter['images'], [])

    def test_chapter_two_reuses_current_main_audio_and_publishes_written(self):
        chapter = json.loads((R2 / 'data/chapters/ch002.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['chapter_id'], 'r2-ch002')
        self.assertEqual(chapter['title'], 'Two Things')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../greg-again/audio/assets/chapter-002.mp3')
        self.assertEqual(chapter['written']['status'], 'published')
        self.assertEqual(chapter['navigation']['previous'], 'r2-ch001')

    def test_chapter_three_reuses_published_audio(self):
        chapter = json.loads((R2 / 'data/chapters/ch003.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['title'], 'The Borrower')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../greg-again/audio/assets/chapter-003.mp3')

    def test_homepage_presents_story_first_and_links_run_one(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('PEG-LEG GREG', html)
        self.assertIn('He remembers an entire life. He woke up nineteen.', html)
        self.assertIn('Peg-Leg Greg was written once already', html)
        self.assertIn('href="../index.html"', html)
        self.assertIn('Listen', html)
        self.assertIn('Read', html)
        self.assertIn('Chapters', html)

    def test_homepage_progress_is_manifest_aware(self):
        js = (R2 / 'assets/js/home.js').read_text(encoding='utf-8')
        self.assertIn('project.current_chapter', js)
        self.assertIn("chapter.written?.status === 'published'", js)
        self.assertIn("chapter.audio?.status === 'published'", js)
        self.assertIn('Read through Chapter', js)
        self.assertIn('Listen through Chapter', js)

    def test_public_copy_presents_r2_as_an_intentional_story(self):
        homepage = (R2 / 'index.html').read_text(encoding='utf-8')
        about = (R2 / 'about/index.html').read_text(encoding='utf-8')
        public_copy = f'{homepage}\n{about}'.lower()

        self.assertNotIn('experiment', public_copy)
        self.assertNotIn('renditions catch up', public_copy)
        self.assertNotIn('machinery broke', public_copy)
        self.assertNotIn('production pipelines worked', public_copy)
        self.assertIn('greg knows what he became. now he has to live his way there again.', public_copy)

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
        self.assertIn('assets/images/r2-hero-wide.webp', html)
        self.assertIn('assets/images/r2-hero-portrait.webp', html)
        chapter = json.loads((R2 / 'data/chapters/ch001.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['images'], [])


if __name__ == '__main__':
    unittest.main()
