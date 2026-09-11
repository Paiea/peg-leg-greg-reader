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
        self.assertEqual(project['chapters'], [f'r2-ch{i:03d}' for i in range(1, 119)])
        self.assertEqual(project['current_chapter'], 'r2-ch118')

    def test_public_frontier_runs_through_chapter_one_eighteen(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        for number in range(1, 119):
            chapter_id = f'r2-ch{number:03d}'
            manifest_path = R2 / f'data/chapters/ch{number:03d}.json'
            self.assertTrue(manifest_path.exists(), chapter_id)
            chapter = json.loads(manifest_path.read_text(encoding='utf-8'))
            self.assertEqual(chapter['chapter_id'], chapter_id)
            self.assertEqual(chapter['display_number'], number)
            self.assertEqual(chapter['written']['status'], 'published')
            self.assertEqual(chapter['written']['path'], f'assets/written/ch{number:03d}.md')
            self.assertTrue((R2 / f'assets/written/ch{number:03d}.md').exists(), chapter_id)
            self.assertEqual(chapter['navigation']['previous'], None if number == 1 else f'r2-ch{number - 1:03d}')
            self.assertEqual(chapter['navigation']['next'], None if number == 118 else f'r2-ch{number + 1:03d}')
        self.assertNotIn('r2-ch119', project['chapters'])

    def test_three_year_seam_landmarks_are_public(self):
        expected = {
            40: 'The Citizen',
            42: 'The Correspondent',
            43: 'The Date',
            50: 'Blackglass',
            62: 'Silver',
            75: 'Three Candidates',
            82: 'The Black Stair',
            83: 'Home Road',
            84: 'The Date',
            92: 'The Third Line',
            93: 'Brell Again',
            96: 'Below the Knee',
            110: 'Faultglass',
            113: 'Take',
            118: 'First Bell',
        }
        for number, title in expected.items():
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['title'], title)

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

    def test_public_authority_advances_while_legacy_registry_is_archived(self):
        registry = json.loads((R2 / 'data/chapter-registry.json').read_text(encoding='utf-8'))
        self.assertLessEqual(int(registry['current_chapter'].rsplit('ch', 1)[-1]), 118)
        self.assertTrue((R2 / 'editorial/legacy-forward/chapter-registry-pre-character-rebuild.json').exists())
        authority = (R2 / 'PUBLIC_REBUILD_AUTHORITY.md').read_text(encoding='utf-8')
        self.assertIn('Chapter 118', authority)
        self.assertIn('40+', authority)
        self.assertIn('three-year', authority.lower())

    def test_r2_declares_shared_greg_surface_pipeline(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['rendering_pipeline'], 'data/rendering-pipeline.json')
        pipeline = json.loads((R2 / 'data/rendering-pipeline.json').read_text(encoding='utf-8'))
        self.assertEqual(pipeline['schema'], 'r2_rendering_pipeline/v1')
        self.assertEqual(pipeline['shared_flow'], ['story_state_or_performance', 'greg_experience', 'shared_greg_surface'])
        self.assertEqual(pipeline['renderers']['audio']['input'], 'shared_greg_surface')
        self.assertEqual(pipeline['renderers']['written']['input'], 'shared_greg_surface')
        self.assertTrue(pipeline['rules']['do_not_optimize_away_processing_time'])
        contract = (R2 / 'PIPELINE.md').read_text(encoding='utf-8')
        self.assertIn('Clean performance residue. Do not clean away cognition.', contract)
        self.assertIn('Greg may own the linguistic surface.', contract)

    def test_selected_written_chapters_publish_directly_to_r2_reader(self):
        pipeline = json.loads((R2 / 'data/rendering-pipeline.json').read_text(encoding='utf-8'))
        publication = pipeline['publication']
        self.assertEqual(publication['selected_verified_written_default'], 'publish_to_live_r2_reader')
        self.assertFalse(publication['requires_audio_or_images'])
        policy = (R2 / 'WRITTEN_PRODUCTION.md').read_text(encoding='utf-8')
        self.assertIn('SELECTED + VERIFIED WRITTEN CHAPTERS PUBLISH TO THE R2 SITE BY DEFAULT.', policy)
        self.assertIn('WHAT SHOULD ACTUALLY HAPPEN NEXT?', policy)

    def test_written_renderer_hides_internal_experiment_prelude(self):
        js = (R2 / 'assets/js/chapter.js').read_text(encoding='utf-8')
        self.assertIn('function stripInternalPrelude(markdown)', js)
        self.assertIn('stripInternalPrelude(await response.text())', js)

    def test_existing_public_role_title_is_preserved(self):
        chapter = json.loads((R2 / 'data/chapters/ch021.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['title'], 'The Letter Writer')

    def test_existing_audio_before_rebuild_is_preserved(self):
        for number in (1, 2, 3, 21, 26):
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['audio']['status'], 'published')
            self.assertTrue(chapter['audio']['path'])

    def test_homepage_presents_clean_cover_entry_and_links_run_one(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('PEG-LEG GREG', html)
        self.assertIn('A second life. A second run.', html)
        self.assertIn('href="../index.html"', html)
        self.assertIn('Start Listening', html)
        self.assertIn('Start Reading', html)

    def test_homepage_progress_is_manifest_aware(self):
        js = (R2 / 'assets/js/home.js').read_text(encoding='utf-8')
        self.assertIn('project.current_chapter', js)
        self.assertIn('publishedWritten(chapter)', js)
        self.assertIn('publishedAudio(chapter)', js)
        self.assertIn('Read through Chapter', js)
        self.assertIn('Listen through Chapter', js)

    def test_public_copy_presents_r2_as_an_intentional_story(self):
        homepage = (R2 / 'index.html').read_text(encoding='utf-8')
        about = (R2 / 'about/index.html').read_text(encoding='utf-8')
        public_copy = f'{homepage}\n{about}'.lower()
        self.assertNotIn('experiment', public_copy)
        self.assertNotIn('machinery broke', public_copy)
        self.assertIn('the story has lived once already. this is the second run.', public_copy)

    def test_public_routes_exist(self):
        for path in ['about/index.html', 'chapters/index.html', 'gallery/index.html', 'chapter.html']:
            self.assertTrue((R2 / path).exists(), path)

    def test_chapter_renderer_has_missing_media_fallbacks(self):
        js = (R2 / 'assets/js/chapter.js').read_text(encoding='utf-8')
        self.assertIn('Written rendition coming soon.', js)
        self.assertIn('Audio version coming soon.', js)
        self.assertIn('new URLSearchParams', js)
        self.assertIn("document.createElement('audio')", js)

    def test_site_renderer_is_manifest_driven(self):
        js = (R2 / 'assets/js/site.js').read_text(encoding='utf-8')
        self.assertIn('data/project.json', js)
        self.assertIn('data/chapters/', js)
        self.assertIn('chapter.html?id=', js)

    def test_r2_css_is_responsive_and_audio_first(self):
        css = (R2 / 'assets/css/r2.css').read_text(encoding='utf-8')
        self.assertIn('.audio-panel', css)
        self.assertIn('.reading-copy', css)
        self.assertIn('@media (max-width: 760px)', css)
        self.assertNotIn('animation:', css)

    def test_cover_asset_is_referenced_without_becoming_chapter_canon(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('assets/images/r2-cover-wide.webp', html)
        self.assertIn('assets/images/r2-cover-portrait.webp', html)


if __name__ == '__main__':
    unittest.main()
