import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from update_home_contents import THIRD_LEG_HOME_LINK, upgrade_home_book_labels


class ProjectRouteTests(unittest.TestCase):
    def test_plg_home_generator_adds_one_3l_route(self):
        source = '<a class="tertiary-action" href="r2/">R2 · Run 2</a>'
        once = upgrade_home_book_labels(source)
        twice = upgrade_home_book_labels(once)

        self.assertIn(THIRD_LEG_HOME_LINK, once)
        self.assertEqual(1, twice.count(THIRD_LEG_HOME_LINK))

    def test_published_homepages_have_direct_project_routes(self):
        plg = (ROOT / "index.html").read_text(encoding="utf-8")
        r2 = (ROOT / "r2" / "index.html").read_text(encoding="utf-8")
        third_leg = (ROOT / "3l" / "index.html").read_text(encoding="utf-8")

        plg_hero = plg.split('</section>', 1)[0]
        r2_header = r2.split('</header>', 1)[0]
        third_leg_header = third_leg.split('</header>', 1)[0]

        self.assertIn('href="3l/">3L · The Third Leg</a>', plg_hero)
        self.assertIn('href="../3l/">3L</a>', r2_header)
        self.assertIn('href="../index.html">PLG</a>', third_leg_header)
        self.assertIn('href="../r2/">R2</a>', third_leg_header)


if __name__ == "__main__":
    unittest.main()
