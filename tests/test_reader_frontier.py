import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from verify_reader_frontier import discover_published_chapters, verify_reader_frontier


class ReaderFrontierTests(unittest.TestCase):
    def test_discovers_contiguous_published_chapter_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / 'chapters'
            chapters.mkdir()
            for number in range(1, 5):
                (chapters / f'{number:03d}.html').write_text('chapter', encoding='utf-8')
            self.assertEqual(discover_published_chapters(root), [1, 2, 3, 4])

    def test_rejects_a_gap_in_published_chapters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / 'chapters'
            chapters.mkdir()
            for number in (1, 2, 4):
                (chapters / f'{number:03d}.html').write_text('chapter', encoding='utf-8')
            with self.assertRaisesRegex(AssertionError, 'missing published chapter 3'):
                discover_published_chapters(root)

    def test_public_indexes_must_match_latest_published_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'chapters').mkdir()
            (root / 'light').mkdir()
            for number in range(1, 353):
                (root / 'chapters' / f'{number:03d}.html').write_text('chapter', encoding='utf-8')
            (root / 'light' / '352.html').write_text('text chapter', encoding='utf-8')
            (root / 'index.html').write_text(
                'BOOK IV Chapters 321–352 ACT II · Chapters 331–352 href="chapters/352.html"',
                encoding='utf-8',
            )
            (root / 'light' / 'index.html').write_text(
                'BOOK IV Chapters 321–352 ACT II · Chapters 331–352 href="352.html">Read newest · Chapter 352',
                encoding='utf-8',
            )
            self.assertEqual(verify_reader_frontier(root), 352)


if __name__ == '__main__':
    unittest.main()
