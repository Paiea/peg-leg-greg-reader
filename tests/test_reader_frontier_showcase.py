import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from verify_reader_frontier import verify_reader_frontier


class ReaderFrontierShowcaseTests(unittest.TestCase):
    def test_frontier_keeps_canonical_file_edge_but_uses_showcase_public_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'chapters').mkdir()
            (root / 'light').mkdir()
            (root / 'publishing').mkdir()
            (root / 'publishing/showcase_chapters.json').write_text(json.dumps({
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'3': {'showcase': False, 'reason': 'pacing'}},
            }), encoding='utf-8')

            for number in range(1, 5):
                (root / 'chapters' / f'{number:03d}.html').write_text('canon archive', encoding='utf-8')

            (root / 'chapters/002.html').write_text(
                '<nav><a rel="next" href="004.html">Chapter 3 →</a></nav>', encoding='utf-8'
            )
            (root / 'light/002.html').write_text(
                '<nav><a rel="next" href="004.html">Chapter 3 →</a></nav>', encoding='utf-8'
            )
            (root / 'chapters/004.html').write_text(
                '<nav><a rel="prev" href="002.html">← Chapter 2</a><span>Next →</span></nav>'
                '<h1>THE FOURTH</h1><a href="../light/004.html">TEXT</a>', encoding='utf-8'
            )
            (root / 'light/004.html').write_text(
                '<nav><a rel="prev" href="002.html">← Chapter 2</a><span>Next →</span></nav>'
                '<h1>THE FOURTH</h1><a href="../chapters/004.html">Illustrated Reader</a>', encoding='utf-8'
            )
            (root / 'index.html').write_text(
                'BOOK I Chapters 1–3 ACT I · Chapters 1–3 THE SECOND LIFE href="chapters/004.html"',
                encoding='utf-8',
            )
            (root / 'light/index.html').write_text(
                'BOOK I Chapters 1–3 ACT I · Chapters 1–3 THE SECOND LIFE '
                'href="004.html">Read newest · Chapter 3', encoding='utf-8'
            )
            (root / 'latest.html').write_text(
                '<h1>Chapter 3</h1><h2>THE FOURTH</h2>'
                '<a href="light/004.html">Read Chapter 3</a>', encoding='utf-8'
            )
            (root / 'light/manifest.json').write_text(json.dumps({
                'latest': 4,
                'latest_showcase': 3,
                'chapters': [
                    {'number': 1, 'showcase_number': 1, 'title': 'ONE', 'path': '001.html'},
                    {'number': 2, 'showcase_number': 2, 'title': 'TWO', 'path': '002.html'},
                    {'number': 4, 'showcase_number': 3, 'title': 'THE FOURTH', 'path': '004.html'},
                ],
            }), encoding='utf-8')

            self.assertEqual(
                verify_reader_frontier(root, expected_latest=4, expected_title='THE FOURTH'),
                4,
            )


if __name__ == '__main__':
    unittest.main()
