import json
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
        illustrated_previous_ok: bool = True,
        text_previous_ok: bool = True,
        illustrated_future_link: bool = False,
        text_future_link: bool = False,
        illustrated_penultimate_forward_ok: bool = True,
        text_penultimate_forward_ok: bool = True,
        latest_landing_ok: bool = True,
        latest_landing_number_ok: bool = True,
        latest_landing_title_ok: bool = True,
        manifest_latest_ok: bool = True,
        manifest_entry_ok: bool = True,
        manifest_future_entry: bool = False,
    ) -> None:
        (root / 'chapters').mkdir()
        (root / 'light').mkdir()
        for number in range(1, latest + 1):
            (root / 'chapters' / f'{number:03d}.html').write_text('chapter', encoding='utf-8')
        previous = latest - 1
        illustrated_previous = previous if illustrated_previous_ok else previous - 1
        text_previous = previous if text_previous_ok else previous - 1
        illustrated_mode_link = (
            f'<a href="../light/{latest:03d}.html">TEXT</a>' if illustrated_to_text else ''
        )
        text_mode_link = (
            f'<a class="mode-link" href="../chapters/{latest:03d}.html">Illustrated version</a>'
            if text_to_illustrated else ''
        )
        illustrated_next = (
            f'<a rel="next" href="{latest + 1:03d}.html">Chapter {latest + 1} →</a>'
            if illustrated_future_link else '<span class="is-disabled">Next →</span>'
        )
        text_next = (
            f'<a rel="next" href="{latest + 1:03d}.html">Chapter {latest + 1} →</a>'
            if text_future_link else '<span class="is-disabled">Next →</span>'
        )
        illustrated_penultimate_target = latest if illustrated_penultimate_forward_ok else latest - 1
        text_penultimate_target = latest if text_penultimate_forward_ok else latest - 1
        (root / 'chapters' / f'{previous:03d}.html').write_text(
            f'<nav><a rel="next" href="{illustrated_penultimate_target:03d}.html">Chapter {illustrated_penultimate_target} →</a></nav>',
            encoding='utf-8',
        )
        (root / 'light' / f'{previous:03d}.html').write_text(
            f'<nav><a rel="next" href="{text_penultimate_target:03d}.html">Chapter {text_penultimate_target} →</a></nav>',
            encoding='utf-8',
        )
        (root / 'chapters' / f'{latest:03d}.html').write_text(
            f'<nav><a rel="prev" href="{illustrated_previous:03d}.html">← Chapter {illustrated_previous}</a>{illustrated_next}</nav>'
            f'<header class="chapter-title"><h1>{illustrated_title}</h1></header>'
            f'{illustrated_mode_link}',
            encoding='utf-8',
        )
        (root / 'light' / f'{latest:03d}.html').write_text(
            f'<nav><a rel="prev" href="{text_previous:03d}.html">← Chapter {text_previous}</a>{text_next}</nav>'
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
        latest_target = latest if latest_landing_ok else previous
        landing_number = latest if latest_landing_number_ok else previous
        landing_title = text_title if latest_landing_title_ok else 'THE WRONG TITLE'
        (root / 'latest.html').write_text(
            f'<h1>Chapter {landing_number}</h1><h2>{landing_title}</h2>'
            f'<a class="primary-action" href="light/{latest_target:03d}.html">Read Chapter {latest_target}</a>',
            encoding='utf-8',
        )
        manifest_latest = latest if manifest_latest_ok else previous
        manifest_entry = {
            'number': latest,
            'title': text_title if manifest_entry_ok else 'THE WRONG TITLE',
            'source': 'manuscript',
            'path': f'{latest:03d}.html' if manifest_entry_ok else f'{previous:03d}.html',
        }
        manifest_chapters = [manifest_entry]
        if manifest_future_entry:
            manifest_chapters.append({
                'number': latest + 1,
                'title': 'THE FUTURE',
                'source': 'manuscript',
                'path': f'{latest + 1:03d}.html',
            })
        (root / 'light' / 'manifest.json').write_text(
            json.dumps({'latest': manifest_latest, 'chapters': manifest_chapters}),
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

    def test_rejects_stale_previous_navigation_at_frontier(self):
        cases = (
            ('Illustrated', {'illustrated_previous_ok': False}, 'Illustrated latest previous link is stale'),
            ('Text', {'text_previous_ok': False}, 'Text latest previous link is stale'),
        )
        for mode, kwargs, message in cases:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_frontier(root, **kwargs)
                with self.assertRaisesRegex(AssertionError, message):
                    verify_reader_frontier(root)

    def test_rejects_future_link_on_latest_illustrated_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, illustrated_future_link=True)
            with self.assertRaisesRegex(AssertionError, 'Illustrated latest next link should be disabled'):
                verify_reader_frontier(root)

    def test_rejects_future_link_on_latest_text_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, text_future_link=True)
            with self.assertRaisesRegex(AssertionError, 'Text latest next link should be disabled'):
                verify_reader_frontier(root)

    def test_rejects_stale_illustrated_penultimate_forward_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, illustrated_penultimate_forward_ok=False)
            with self.assertRaisesRegex(AssertionError, 'Illustrated penultimate next link is stale'):
                verify_reader_frontier(root)

    def test_rejects_stale_text_penultimate_forward_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, text_penultimate_forward_ok=False)
            with self.assertRaisesRegex(AssertionError, 'Text penultimate next link is stale'):
                verify_reader_frontier(root)

    def test_rejects_stale_latest_landing_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, latest_landing_ok=False)
            with self.assertRaisesRegex(AssertionError, 'Latest landing page is stale'):
                verify_reader_frontier(root)

    def test_rejects_stale_latest_landing_chapter_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, latest_landing_number_ok=False)
            with self.assertRaisesRegex(AssertionError, 'Latest landing chapter number is stale'):
                verify_reader_frontier(root)

    def test_rejects_stale_latest_landing_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, latest_landing_title_ok=False)
            with self.assertRaisesRegex(AssertionError, 'Latest landing title is stale'):
                verify_reader_frontier(root, expected_title='THE COUNT')

    def test_rejects_stale_manifest_latest_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, manifest_latest_ok=False)
            with self.assertRaisesRegex(AssertionError, 'Text manifest latest field is stale'):
                verify_reader_frontier(root)

    def test_rejects_stale_manifest_frontier_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, manifest_entry_ok=False)
            with self.assertRaisesRegex(AssertionError, 'Text manifest frontier entry is stale'):
                verify_reader_frontier(root, expected_title='THE COUNT')

    def test_rejects_manifest_entry_beyond_published_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_frontier(root, manifest_future_entry=True)
            with self.assertRaisesRegex(AssertionError, 'Text manifest contains chapter beyond published frontier'):
                verify_reader_frontier(root)


if __name__ == '__main__':
    unittest.main()
