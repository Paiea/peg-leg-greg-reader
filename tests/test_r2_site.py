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
        self.assertEqual(project['chapters'], [f'r2-ch{i:03d}' for i in range(1, 227)])
        self.assertEqual(project['current_chapter'], 'r2-ch226')

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
        self.assertTrue(pipeline['rules']['do_not_optimize_away_processing_time'])
        self.assertEqual(
            pipeline['rules']['processing_space_may_use'],
            ['pause', 'repetition', 'reset', 'self_correction', 'connective_thought', 'tiny_reaction'],
        )

        contract = (R2 / 'PIPELINE.md').read_text(encoding='utf-8')
        self.assertIn('Clean performance residue. Do not clean away cognition.', contract)
        self.assertIn('Greg may own the linguistic surface.', contract)
        self.assertIn('DO NOT OPTIMIZE AWAY PROCESSING TIME.', contract)
        self.assertIn('Smoothness is not automatically clarity.', contract)
        self.assertIn('Audio Finish', contract)
        self.assertIn('Written Finish', contract)

        readme = (R2 / 'README.md').read_text(encoding='utf-8')
        self.assertIn('PIPELINE.md', readme)
        self.assertIn('Shared Greg Surface', readme)
        self.assertIn('medium-specific finish', readme)

    def test_written_frontier_is_public_through_chapter_two_hundred_twenty_six(self):
        for number in range(1, 227):
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
                None if number == 226 else f'r2-ch{number + 1:03d}',
            )

    def test_selected_written_chapters_publish_directly_to_r2_reader(self):
        pipeline = json.loads((R2 / 'data/rendering-pipeline.json').read_text(encoding='utf-8'))
        publication = pipeline['publication']
        self.assertEqual(publication['selected_verified_written_default'], 'publish_to_live_r2_reader')
        self.assertFalse(publication['requires_audio_or_images'])
        self.assertFalse(publication['implies_immutable_canon'])

        policy = (R2 / 'WRITTEN_PRODUCTION.md').read_text(encoding='utf-8')
        self.assertIn('SELECTED + VERIFIED WRITTEN CHAPTERS PUBLISH TO THE R2 SITE BY DEFAULT.', policy)
        self.assertIn('WHAT SHOULD ACTUALLY HAPPEN NEXT?', policy)

    def test_chapter_twenty_public_copy_excludes_internal_experiment_prelude(self):
        prose = (R2 / 'assets/written/ch020.md').read_text(encoding='utf-8')
        self.assertNotIn('Status: **EXPERIMENTAL', prose)
        self.assertNotIn('Story search:', prose)
        self.assertTrue(prose.startswith('# Chapter 20: Ward Hand\n\n---\n'))

    def test_chapter_twenty_one_public_copy_excludes_internal_experiment_prelude(self):
        prose = (R2 / 'assets/written/ch021.md').read_text(encoding='utf-8')
        self.assertNotIn('Status: **EXPERIMENTAL', prose)
        self.assertNotIn('Story search:', prose)
        self.assertNotIn('Relationship rehearsal:', prose)
        self.assertTrue(prose.startswith('# Chapter 21: The Reply\n\n---\n'))

    def test_chapter_twenty_one_uses_public_role_title(self):
        chapter = json.loads((R2 / 'data/chapters/ch021.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['title'], 'The Letter Writer')

    def test_chapter_twenty_two_public_copy_excludes_internal_experiment_prelude(self):
        prose = (R2 / 'assets/written/ch022.md').read_text(encoding='utf-8')
        self.assertNotIn('Status: **EXPERIMENTAL', prose)
        self.assertNotIn('Story search:', prose)
        self.assertTrue(prose.startswith('# Chapter 22: The Neighbor\n\n---\n'))

    def test_chapter_twenty_two_title_names_what_greg_embodies(self):
        chapter = json.loads((R2 / 'data/chapters/ch022.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['title'], 'The Neighbor')

    def test_chapter_twenty_three_public_copy_excludes_internal_experiment_prelude(self):
        prose = (R2 / 'assets/written/ch023.md').read_text(encoding='utf-8')
        self.assertNotIn('Status: **EXPERIMENTAL', prose)
        self.assertNotIn('Story search:', prose)
        self.assertTrue(prose.startswith('# Chapter 23: The Adventurer\n\n---\n'))

    def test_chapter_twenty_three_title_names_what_greg_embodies(self):
        chapter = json.loads((R2 / 'data/chapters/ch023.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['title'], 'The Adventurer')

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
        self.assertEqual(chapter['title'], 'The Novice')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../greg-again/audio/assets/chapter-002.mp3')
        self.assertEqual(chapter['written']['status'], 'published')
        self.assertEqual(chapter['navigation']['previous'], 'r2-ch001')

    def test_chapter_three_reuses_published_audio(self):
        chapter = json.loads((R2 / 'data/chapters/ch003.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['title'], 'The Borrower')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../greg-again/audio/assets/chapter-003.mp3')

    def test_homepage_presents_clean_cover_entry_and_links_run_one(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('PEG-LEG GREG', html)
        self.assertIn('A second life. A second run.', html)
        self.assertIn('Peg-Leg Greg was written once already', html)
        self.assertIn('href="../index.html"', html)
        self.assertIn('Start Listening', html)
        self.assertIn('Start Reading', html)
        self.assertIn('Chapters', html)

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
        self.assertNotIn('renditions catch up', public_copy)
        self.assertNotIn('machinery broke', public_copy)
        self.assertNotIn('production pipelines worked', public_copy)
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

    def test_cover_asset_is_referenced_without_becoming_chapter_canon(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('assets/images/r2-cover-wide.webp', html)
        self.assertIn('assets/images/r2-cover-portrait.webp', html)
        chapter = json.loads((R2 / 'data/chapters/ch001.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['images'], [])

    def test_image_worker_is_source_grounded_and_scene_batched(self):
        worker = (R2 / 'IMAGE_WORKER.md').read_text(encoding='utf-8')
        system = (R2 / 'IMAGE_SYSTEM.md').read_text(encoding='utf-8')
        packet = (R2 / 'image-packets/TEMPLATE.md').read_text(encoding='utf-8')

        self.assertIn('CHAPTER TITLE IS METADATA, NOT IMAGE SOURCE.', worker)
        self.assertIn('READ THE CHAPTER', worker)
        self.assertIn('about five visually distinct moments', worker)
        self.assertIn('up to five scene-specific generated images', worker)
        self.assertIn('STORY SOURCE FIRST. TITLE LAST.', system)
        self.assertIn('source_excerpt', system)
        self.assertIn('not_grounded_in_source', system)
        self.assertIn('chapter_read_complete', packet)
        self.assertIn('Scene shortlist', packet)
        self.assertIn('could this image have been generated from title alone', packet)


if __name__ == '__main__':
    unittest.main()
