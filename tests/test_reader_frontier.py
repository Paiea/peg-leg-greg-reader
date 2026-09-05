import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from verify_reader_frontier import discover_published_chapters, verify_reader_frontier


class ReaderFrontierTests(unittest.TestCase):
    def write_frontier(
        self,
        root: Path,
        *,
        latest: int = 352,
        illustrated_title: str = 'THE COUNT',
        text_title: str = 'THE COUNT',
        illustrated_to_text: bool = True,
        text_to_illustrated: bool = True,
    ) -> None:
        (root / 'chapters').mkdir()
        (root / 'light').mkdir()
        for number in range(1, latest + 1):
            (root / 'chapters' / f'{number:03d}.html').write_text('chapter', encoding='utf-8')
        previous = latest - 1
        illustrated_mode_link = (
            f'<a href="../light/{latest:03d}.html">TEXT</a>' if illustrated_to_text else ''
        )
        text_mode_link = (
            f'<a class="mode-link" href="../chapters/{latest:03d}.html">Illustrated version</a>'
            if text_to_illustrated else ''
        )
        (root / 'chapters' / f'{latest:03d}.html').write_text(
            f'<nav><a rel="prev" href="{previous:03d}.html">← Chapter {previous}</a></nav>'
            f'<header class="chapter-title"><h1>{illustrated_title}</h1></header>'
            f'{illustrated_mode_link}',
            encoding='utf-8',
        )
        (root / 'light' / f'{latest:03d}.html').write_text(
            f'<nav><a rel="prev" href="{previous:03d}.html">← Chapter {previous}</a></nav>'
            f'<header class="light-chapter-title"><h1>{text_title}</h1></header>'
            f'{text_mode_link}',
            encoding='utf-8',
        )
        (root / 'index.html').write_text(
            f'BOOK IV Chapters 321–{latest} ACT II · Chapters 331–{latest} href="chapters/{latest:03d}.html"',
            encoding='utf-8',
        )
        (root / 'light' / 'index.html').write_text(
            f'BOOK IV Chapters 321–{latest} ACT II · Chapters 331–{latest} href="{latest:03d}.html">Read newest · Chapter {latest}',
            encoding='utf-8',
        )

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
            self.write_frontier(root)
            self.assertEqual(verify_reader_frontier(root), 352)

    def test_rejects_latest_illustrated_title_mismatch_with_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, illustrated_title='THE WRONG TITLE')
            with self.assertRaisesRegex(AssertionError, 'Illustrated title mismatch'):
                verify_reader_frontier(root, expected_title='THE COUNT')

    def test_rejects_latest_text_title_mismatch_with_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, text_title='THE WRONG TITLE')
            with self.assertRaisesRegex(AssertionError, 'Text title mismatch'):
                verify_reader_frontier(root, expected_title='THE COUNT')

    def test_rejects_missing_illustrated_to_text_frontier_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, illustrated_to_text=False)
            with self.assertRaisesRegex(AssertionError, 'Illustrated page does not link matching Text chapter'):
                verify_reader_frontier(root)

    def test_rejects_missing_text_to_illustrated_frontier_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, text_to_illustrated=False)
            with self.assertRaisesRegex(AssertionError, 'Text page does not link matching Illustrated chapter'):
                verify_reader_frontier(root)


if __name__ == '__main__':
    unittest.main()
