import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'
AUDIO_MANIFEST = ROOT / 'greg-again' / 'audio' / 'manifest.json'
SYNC_SCRIPT = ROOT / 'scripts' / 'sync_r2_role_titles.py'
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

    def test_reconciler_promotes_approved_audit_then_changes_only_title_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'r2' / 'assets' / 'written').mkdir(parents=True)
            (root / 'r2' / 'data' / 'chapters').mkdir(parents=True)
            (root / 'greg-again' / 'audio').mkdir(parents=True)

            original_body = '\n\n---\n\nBody stays exactly here.\n'
            (root / 'r2' / 'assets' / 'written' / 'ch001.md').write_text(
                '# Chapter 1: Two Things' + original_body,
                encoding='utf-8',
            )
            (root / 'r2' / 'TITLE_ROLE_AUDIT.md').write_text(
                '# Audit\n\n## Approved title map\n\n```text\n001 The Novice\n```\n',
                encoding='utf-8',
            )
            (root / 'r2' / 'data' / 'project.json').write_text(
                json.dumps({'chapters': ['r2-ch001']}, indent=2) + '\n', encoding='utf-8'
            )
            public = {
                'chapter_id': 'r2-ch001',
                'display_number': 1,
                'title': 'Two Things',
                'audio': {'status': 'published', 'path': '../greg-again/audio/assets/chapter-001.mp3'},
                'written': {'status': 'published', 'path': 'assets/written/ch001.md'},
                'navigation': {'previous': None, 'next': None},
            }
            (root / 'r2' / 'data' / 'chapters' / 'ch001.json').write_text(
                json.dumps(public, indent=2) + '\n', encoding='utf-8'
            )
            registry = {
                'project_id': 'r2',
                'current_chapter': 'r2-ch001',
                'chapters': {
                    'r2-ch001': {
                        'display_number': 1,
                        'title': 'Two Things',
                        'pipeline': {'audio': 'published', 'written': 'published'},
                    }
                },
            }
            (root / 'r2' / 'data' / 'chapter-registry.json').write_text(
                json.dumps(registry, indent=2) + '\n', encoding='utf-8'
            )
            audio = {
                'series': 'Greg, Again',
                'chapters': [
                    {
                        'chapter_id': 'ga-001',
                        'number': 1,
                        'title': 'Two Things',
                        'audio_src': 'assets/chapter-001.mp3',
                        'take_count': 12,
                    }
                ],
            }
            (root / 'greg-again' / 'audio' / 'manifest.json').write_text(
                json.dumps(audio, indent=2) + '\n', encoding='utf-8'
            )

            result = subprocess.run(
                [sys.executable, str(SYNC_SCRIPT), '--root', str(root), '--promote-audit'],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            updated_public = json.loads(
                (root / 'r2' / 'data' / 'chapters' / 'ch001.json').read_text(encoding='utf-8')
            )
            updated_registry = json.loads(
                (root / 'r2' / 'data' / 'chapter-registry.json').read_text(encoding='utf-8')
            )
            updated_audio = json.loads(
                (root / 'greg-again' / 'audio' / 'manifest.json').read_text(encoding='utf-8')
            )
            selected = (root / 'r2' / 'assets' / 'written' / 'ch001.md').read_text(encoding='utf-8')

            self.assertEqual(selected, '# Chapter 1: The Novice' + original_body)
            self.assertEqual(updated_public['title'], 'The Novice')
            self.assertEqual(updated_public['chapter_id'], 'r2-ch001')
            self.assertEqual(updated_public['audio']['path'], '../greg-again/audio/assets/chapter-001.mp3')
            self.assertEqual(updated_registry['chapters']['r2-ch001']['title'], 'The Novice')
            self.assertEqual(updated_registry['chapters']['r2-ch001']['pipeline']['audio'], 'published')
            self.assertEqual(updated_audio['chapters'][0]['title'], 'The Novice')
            self.assertEqual(updated_audio['chapters'][0]['chapter_id'], 'ga-001')
            self.assertEqual(updated_audio['chapters'][0]['take_count'], 12)

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
