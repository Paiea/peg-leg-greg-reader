import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'
AUDIO_MANIFEST = ROOT / 'greg-again' / 'audio' / 'manifest.json'
HEADING_RE = re.compile(r'^# Chapter (?P<number>\d+): (?P<title>.+)$')

EXPECTED_TITLES = {
    1: 'The Boy',
    2: 'The Novice',
    3: 'The Borrower',
    4: 'The Contractor',
    5: 'The Partner',
    6: 'The Troubleshooter',
    7: 'The Extra Guard',
    8: 'The Defender',
    9: 'The Backstop',
    10: 'The Returner',
    11: 'The Gate Hand',
    12: 'The Stranger',
    13: 'The Fighter',
    14: 'The Helper',
    15: 'The Friend',
    16: 'The Investor',
    17: 'The Extra Hand',
    18: 'The Applicant',
    19: 'The Maintainer',
    20: 'Ward Hand',
    21: 'The Letter Writer',
    22: 'The Neighbor',
    23: 'The Adventurer',
    24: 'The Watchman',
    25: 'The Hired Sword',
    26: 'The Adventurer',
}


def selected_heading(number: int) -> tuple[int, str]:
    path = R2 / 'assets' / 'written' / f'ch{number:03d}.md'
    first_line = path.read_text(encoding='utf-8').splitlines()[0]
    match = HEADING_RE.fullmatch(first_line)
    if match is None:
        raise AssertionError(f'{path}: invalid chapter heading: {first_line!r}')
    return int(match.group('number')), match.group('title')


class R2RoleTitleTests(unittest.TestCase):
    def test_selected_written_headings_match_approved_role_titles(self):
        for number, expected_title in EXPECTED_TITLES.items():
            heading_number, title = selected_heading(number)
            self.assertEqual(heading_number, number)
            self.assertEqual(title, expected_title, f'Chapter {number}')

    def test_public_manifests_match_approved_role_titles_and_stable_identity(self):
        project = json.loads((R2 / 'data' / 'project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['chapters'], [f'r2-ch{i:03d}' for i in range(1, 27)])

        for number, expected_title in EXPECTED_TITLES.items():
            chapter = json.loads(
                (R2 / 'data' / 'chapters' / f'ch{number:03d}.json').read_text(encoding='utf-8')
            )
            self.assertEqual(chapter['chapter_id'], f'r2-ch{number:03d}')
            self.assertEqual(chapter['display_number'], number)
            self.assertEqual(chapter['title'], expected_title, f'Chapter {number}')
            self.assertEqual(chapter['written']['path'], f'assets/written/ch{number:03d}.md')
            if chapter['audio']['status'] == 'published':
                self.assertEqual(
                    chapter['audio']['path'],
                    f'../greg-again/audio/assets/chapter-{number:03d}.mp3',
                )

    def test_registry_titles_match_approved_role_titles_by_stable_id(self):
        registry = json.loads((R2 / 'data' / 'chapter-registry.json').read_text(encoding='utf-8'))
        for number, expected_title in EXPECTED_TITLES.items():
            chapter_id = f'r2-ch{number:03d}'
            self.assertIn(chapter_id, registry['chapters'])
            chapter = registry['chapters'][chapter_id]
            self.assertEqual(chapter['display_number'], number)
            self.assertEqual(chapter['title'], expected_title, f'Chapter {number}')

    def test_audio_manifest_titles_follow_r2_authority_by_number(self):
        manifest = json.loads(AUDIO_MANIFEST.read_text(encoding='utf-8'))
        for chapter in manifest['chapters']:
            number = chapter['number']
            if number not in EXPECTED_TITLES:
                continue
            self.assertEqual(chapter['chapter_id'], f'ga-{number:03d}')
            self.assertEqual(chapter['title'], EXPECTED_TITLES[number], f'ga-{number:03d}')
            self.assertEqual(chapter['audio_src'], f'assets/chapter-{number:03d}.mp3')

    def test_title_policy_keeps_identity_separate_from_title(self):
        policy = (R2 / 'TITLE_POLICY.md').read_text(encoding='utf-8')
        self.assertIn('Who is Greg in this chapter?', policy)
        self.assertIn('Title wording never owns chapter identity.', policy)
        self.assertIn('A title-only change must not imply that existing audio is missing', policy)
        self.assertNotIn('role":', policy)


if __name__ == '__main__':
    unittest.main()
