import unittest

from scripts.apply_image_batch import figure


class ImageMarkupTests(unittest.TestCase):
    def test_generated_figure_has_intrinsic_size_lazy_loading_and_async_decoding(self):
        item = {
            "role": "scene-illustration",
            "target": "visual/chapter_art/001/example.jpg",
            "alt": "Greg crosses the room.",
        }
        markup = figure(item, width=1200, height=800)
        self.assertIn('width="1200"', markup)
        self.assertIn('height="800"', markup)
        self.assertIn('loading="lazy"', markup)
        self.assertIn('decoding="async"', markup)


if __name__ == "__main__":
    unittest.main()
