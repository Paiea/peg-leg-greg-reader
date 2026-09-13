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
        self.assertEqual(project['chapters'], [f'r2-ch{i:03d}' for i in range(1, 183)])
        self.assertEqual(project['current_chapter'], 'r2-ch182')
        self.assertIn('R2 COMPLETE', project['authority_note'])

    def test_public_frontier_runs_through_chapter_one_eighty_two(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        for number in range(1, 183):
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
            self.assertEqual(chapter['navigation']['next'], None if number == 182 else f'r2-ch{number + 1:03d}')
        self.assertNotIn('r2-ch183', project['chapters'])

    def test_post_first_bell_role_titles_are_greg_roles(self):
        expected = {
            119: 'The Planner', 120: 'The Customer', 121: 'The Troubleshooter', 122: 'The Specialist',
            123: 'The Contractor', 124: 'The Backstop', 125: 'The Coordinator', 126: 'The Investigator',
            127: 'The Patient', 128: 'The Fixed Point', 129: 'The Partner', 130: 'The Partner',
            131: 'The Helper', 132: 'The Responder', 133: 'The Tourist', 134: 'The Partner',
            135: 'The Hunter', 136: 'The Tenant', 137: 'The Passenger', 138: 'The Homecomer',
            139: 'The Tester', 140: 'The Friend', 141: 'The Entrant', 142: 'The Duelist',
            143: 'The Candidate', 144: 'The Teammate', 145: 'The Support', 146: 'The Experimenter',
            147: 'The Correspondent', 148: 'The Consultant', 149: 'The Recruiter', 150: 'The Specialist',
            151: 'The Explorer', 152: 'The Support', 153: 'The Observer', 154: 'The Survey Hand',
            155: 'The Collector', 156: 'The Troubleshooter', 157: 'The Surveyor', 158: 'The Follower',
            159: 'The Claimant', 160: 'The Cook', 161: 'The Evaluator', 162: 'The Surveyor',
            163: 'The Sponsor', 164: 'The Supervisor',
            165: 'The Contractor', 166: 'The Selector', 167: 'The Passenger', 168: 'The Brace',
            169: 'The Catcher', 170: 'The Camper', 171: 'The Counterweight', 172: 'The Customer',
            173: 'The Borrower', 174: 'The Reserve', 175: 'The Pacer', 176: 'The Escort',
            177: 'The Adviser', 178: 'The Setter', 179: 'The Router', 180: 'The Earner',
            181: 'The Visitor', 182: 'The Specialist',
        }
        for number, title in expected.items():
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['title'], title, number)

    def test_post_first_bell_public_prose_uses_selected_reperformance(self):
        chapter_119 = (R2 / 'assets/written/ch119.md').read_text(encoding='utf-8')
        chapter_164 = (R2 / 'assets/written/ch164.md').read_text(encoding='utf-8')
        chapter_182 = (R2 / 'assets/written/ch182.md').read_text(encoding='utf-8')
        self.assertIn('Second bell turned out to mean breakfast.', chapter_119)
        self.assertNotIn('The Trial Route', chapter_119)
        self.assertIn('Merek', chapter_164)
        self.assertTrue(chapter_182.startswith('# Chapter 182: The Specialist'))
        self.assertIn('Legal salvage.', chapter_182)

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
        self.assertLessEqual(int(registry['current_chapter'].rsplit('ch', 1)[-1]), 182)
        self.assertTrue((R2 / 'editorial/legacy-forward/chapter-registry-pre-character-rebuild.json').exists())
        authority = (R2 / 'PUBLIC_REBUILD_AUTHORITY.md').read_text(encoding='utf-8')
        self.assertIn('Chapter 182', authority)
        self.assertIn('R2 COMPLETE', authority)
        self.assertIn('Storm Road', authority)
        complete = (R2 / 'R2_COMPLETE.md').read_text(encoding='utf-8')
        self.assertIn('FROZEN WRITTEN RUN', complete)
        self.assertIn('182 - The Specialist', complete)
        self.assertIn('Chapter 183+', complete)

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
        self.assertIn('candidatePreludePattern', js)
        self.assertIn('Candidate Chapter', js)

    def test_existing_public_role_title_is_preserved(self):
        chapter = json.loads((R2 / 'data/chapters/ch021.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['title'], 'The Letter Writer')

    def test_existing_audio_before_rebuild_is_preserved(self):
        for number in (1, 2, 3, 21, 26):
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            self.assertEqual(chapter['audio']['status'], 'published')
            self.assertTrue(chapter['audio']['path'])

    def test_homepage_presents_listen_first_entry_and_links_run_one(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('PEG-LEG GREG', html)
        self.assertIn('A second life.', html)
        self.assertIn('A second run.', html)
        self.assertIn('href="../index.html"', html)
        self.assertIn('Start Listening', html)
        self.assertIn('Written rendition →', html)
        self.assertNotIn('Start Reading', html)

    def test_homepage_progress_is_manifest_aware(self):
        js = (R2 / 'assets/js/home.js').read_text(encoding='utf-8')
        self.assertIn('project.current_chapter', js)
        self.assertIn('publishedWritten(chapter)', js)
        self.assertIn('publishedAudio(chapter)', js)
        self.assertIn('Written through Chapter', js)
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

    def test_home_banner_uses_approved_high_res_site_art(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('assets/images/1.png', html)
        self.assertIn('width="1672"', html)
        self.assertIn('height="941"', html)
        self.assertNotIn('assets/images/Home.png', html)

    def test_chapter_art_routes_real_assets_through_chapter_thirty(self):
        art = json.loads((R2 / 'data/chapter-art.json').read_text(encoding='utf-8'))
        self.assertEqual(set(art), {f'r2-ch{i:03d}' for i in range(1, 31)})
        for number in range(1, 31):
            chapter_id = f'r2-ch{number:03d}'
            images = art[chapter_id]
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0]['role'], 'anchor')
            expected_path = f'assets/images/chapters/ch{number:03d}.png'
            self.assertEqual(images[0]['path'].split('?', 1)[0], expected_path)
            self.assertTrue((R2 / expected_path).exists(), chapter_id)


if __name__ == '__main__':
    unittest.main()
