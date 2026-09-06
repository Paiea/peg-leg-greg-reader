import unittest

from scripts import performance_production_funnel as funnel


class PerformanceProductionFunnelTests(unittest.TestCase):
    def test_next_visible_chapters_skip_hidden_canon(self):
        manifest = {
            "default": "visible",
            "chapters": {
                "3": {"showcase": False},
                "6": {"showcase": False},
                "8": {"showcase": False},
                "12": {"showcase": False},
                "20": {"showcase": False},
                "21": {"showcase": False},
                "33": {"showcase": False},
                "38": {"showcase": False},
                "43": {"showcase": False},
                "46": {"showcase": False},
                "48": {"showcase": False},
                "49": {"showcase": False},
                "57": {"showcase": False},
                "66": {"showcase": False},
                "73": {"showcase": False},
            },
        }
        expected = [
            27, 28, 29, 30, 31, 32, 34, 35, 36, 37,
            39, 40, 41, 42, 44, 45, 47, 50, 51, 52,
            53, 54, 55, 56, 58, 59, 60, 61, 62, 63,
            64, 65, 67, 68, 69, 70, 71, 72, 74, 75,
        ]
        self.assertEqual(
            expected,
            funnel.next_visible_chapters(manifest, after_chapter=26, count=40, max_chapter=75),
        )


if __name__ == "__main__":
    unittest.main()
