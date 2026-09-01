import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'scripts' / 'generate_illustrated.py'


def markdown_range(start: int, end: int, *, label: str) -> str:
    chunks = []
    for number in range(start, end + 1):
        if number == 232:
            chunks.append(
                '## Chapter 232 — THE COUNTERSIGN\n\n'
                'Exact countersign prose.\n'
            )
        else:
            chunks.append(
                f'# CHAPTER {number}\n\n'
                f'## THE {label} {number}\n\n'
                f'Exact {label.lower()} prose {number}.\n'
            )
    return '\n'.join(chunks)


CH155 = '''<!doctype html><html><body><header class="site-head"><a href="../index.html">PEG-LEG GREG</a></header><main class="chapter-shell"><header class="chapter-title"><div class="number">CHAPTER 155</div><h1>THE LEAK</h1></header><article class="prose"><p>Existing chapter 155 prose.</p></article><nav aria-label="Chapter navigation" class="chapter-nav"><a href="154.html">← Previous</a><a class="toclink" href="../index.html">Table of Contents</a></nav></main></body></html>'''


class IllustratedGeneratorTests(unittest.TestCase):
    def make_root(self, td: str) -> Path:
        root = Path(td)
        (root / 'state/manuscript').mkdir(parents=True)
        (root / 'chapters').mkdir()
        (root / 'chapters/155.html').write_text(CH155, encoding='utf-8')
        (root / 'state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md').write_text(
            markdown_range(156, 219, label='RECOVERED'), encoding='utf-8'
        )
        (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(
            markdown_range(220, 237, label='CURRENT'), encoding='utf-8'
        )
        return root

    def run_generator(self, root: Path):
        return subprocess.run(
            [sys.executable, str(GENERATOR), '156-235'],
            cwd=root,
            text=True,
            capture_output=True,
        )

    def test_generates_exact_normal_reader_pages_without_spilling_past_235(self):
        with tempfile.TemporaryDirectory() as td:
            root = self.make_root(td)
            result = self.run_generator(root)
            self.assertEqual(result.returncode, 0, result.stderr)

            for number in (156, 219, 220, 232, 235):
                self.assertTrue((root / f'chapters/{number:03d}.html').exists(), number)
            self.assertFalse((root / 'chapters/236.html').exists())
            self.assertFalse((root / 'chapters/237.html').exists())

            ch156 = (root / 'chapters/156.html').read_text(encoding='utf-8')
            self.assertIn('<div class="number">CHAPTER 156</div>', ch156)
            self.assertIn('<h1>THE RECOVERED 156</h1>', ch156)
            self.assertIn('<p>Exact recovered prose 156.</p>', ch156)
            self.assertIn('rel="prev" href="155.html"', ch156)
            self.assertIn('rel="next" href="157.html"', ch156)
            self.assertIn('href="../light/156.html"', ch156)
            self.assertNotIn('<img', ch156)
            self.assertNotIn('Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md', ch156)

            ch219 = (root / 'chapters/219.html').read_text(encoding='utf-8')
            self.assertIn('rel="next" href="220.html"', ch219)
            ch220 = (root / 'chapters/220.html').read_text(encoding='utf-8')
            self.assertIn('rel="prev" href="219.html"', ch220)

            ch232 = (root / 'chapters/232.html').read_text(encoding='utf-8')
            self.assertIn('<h1>THE COUNTERSIGN</h1>', ch232)
            self.assertIn('<p>Exact countersign prose.</p>', ch232)

            ch235 = (root / 'chapters/235.html').read_text(encoding='utf-8')
            self.assertIn('rel="prev" href="234.html"', ch235)
            self.assertNotIn('rel="next"', ch235)

            ch155 = (root / 'chapters/155.html').read_text(encoding='utf-8')
            self.assertIn('href="156.html"', ch155)

    def test_regeneration_preserves_promoted_figure_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = self.make_root(td)
            first = self.run_generator(root)
            self.assertEqual(first.returncode, 0, first.stderr)

            path = root / 'chapters/156.html'
            text = path.read_text(encoding='utf-8')
            figure = '<figure class="chapter-art scene-illustration"><img src="../visual/chapter_art/156/test.jpg" alt="Test art"/></figure>'
            text = text.replace(
                '<p>Exact recovered prose 156.</p>',
                figure + '<p>Exact recovered prose 156.</p>',
                1,
            )
            path.write_text(text, encoding='utf-8')

            second = self.run_generator(root)
            self.assertEqual(second.returncode, 0, second.stderr)
            regenerated = path.read_text(encoding='utf-8')
            self.assertIn(figure, regenerated)
            self.assertEqual(regenerated.count(figure), 1)


if __name__ == '__main__':
    unittest.main()
