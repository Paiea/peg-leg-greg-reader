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
        self.assertEqual(project['chapters'], [f'r2-ch{i:03d}' for i in range(1, 43)])
        self.assertEqual(project['current_chapter'], 'r2-ch042')

    def test_public_frontier_is_character_rebuild_through_chapter_forty_two(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        for number in range(1, 43):
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
            self.assertEqual(chapter['navigation']['next'], None if number == 42 else f'r2-ch{number + 1:03d}')
        self.assertNotIn('r2-ch043', project['chapters'])
        self.assertTrue((R2 / 'assets/written/ch043.md').exists())

    def test_rebuild_titles_are_public(self):
        expected = {27:'The Late Letter',28:'Eventually',29:'The Seven',30:'The Workshop',31:'The Next Road',32:'Two Copper',33:'Route Day',34:'The Packet',35:'The Ask',36:'Four Nights',37:'One Day Late',38:'Two Keys',39:'The East Desk',40:'Not Early',41:'The Second Chair',42:'Tax Clerk'}
        for number, title in expected.items():
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['title'], title)
            self.assertEqual(chapter['images'], [])
            self.assertNotEqual(chapter['audio']['status'], 'published')

    def test_registry_is_rerouted_and_legacy_registry_is_archived(self):
        registry = json.loads((R2 / 'data/chapter-registry.json').read_text(encoding='utf-8'))
        self.assertEqual(registry['current_chapter'], 'r2-ch042')
        self.assertEqual(list(registry['chapters'])[-1], 'r2-ch042')
        self.assertNotIn('r2-ch043', registry['chapters'])
        self.assertTrue((R2 / 'editorial/legacy-forward/chapter-registry-pre-character-rebuild.json').exists())
        authority = (R2 / 'PUBLIC_REBUILD_AUTHORITY.md').read_text(encoding='utf-8')
        self.assertIn('Chapter 42', authority)
        self.assertIn('43+', authority)

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

    def test_existing_audio_before_rebuild_is_preserved(self):
        for number in (1,2,3,21,26):
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['audio']['status'], 'published')
            self.assertTrue(chapter['audio']['path'])

    def test_public_copy_presents_r2_as_an_intentional_story(self):
        homepage = (R2 / 'index.html').read_text(encoding='utf-8')
        about = (R2 / 'about/index.html').read_text(encoding='utf-8')
        public_copy = f'{homepage}\n{about}'.lower()
        self.assertNotIn('experiment', public_copy)
        self.assertIn('the story has lived once already. this is the second run.', public_copy)

    def test_public_routes_exist(self):
        for path in ['about/index.html','chapters/index.html','gallery/index.html','chapter.html']:
            self.assertTrue((R2 / path).exists(), path)


if __name__ == '__main__':
    unittest.main()
