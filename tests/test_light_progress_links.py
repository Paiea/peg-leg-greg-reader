import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LightProgressLinkTests(unittest.TestCase):
    def test_continue_reading_uses_compatibility_router_for_any_saved_chapter(self):
        script = (ROOT / 'assets/light-progress.js').read_text(encoding='utf-8')
        self.assertIn("../light.html?chapter=${chapter}", script)
        self.assertNotIn("${String(chapter).padStart(3, '0')}.html", script)


if __name__ == '__main__':
    unittest.main()
