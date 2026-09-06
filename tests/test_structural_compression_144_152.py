import unittest

from scripts.apply_structural_compression_144_152 import (
    apply_transformations,
    replace_between,
)


class StructuralCompressionHelpersTest(unittest.TestCase):
    def test_replace_between_replaces_inclusive_markers(self):
        text = "aaa START old material END zzz"
        self.assertEqual(
            replace_between(text, "START", "END", "NEW"),
            "aaa NEW zzz",
        )

    def test_replace_between_requires_unique_markers(self):
        with self.assertRaises(ValueError):
            replace_between("nothing here", "START", "END", "NEW")

    def test_wave_one_is_idempotent_and_skips_legacy_150(self):
        docs = {
            149: (
                '<a rel="next" href="150.html">Chapter 150</a>'
                '<article class="prose"><p>We went opposite directions. That felt appropriate. OLD</p>'
                '<p>I went to the wing. The house had grown. Maybe forty now. People entered without ceremony. Some paid something at the front. Some apparently did not. A woman came in, saw someone she knew, crossed two rows to sit beside her, and immediately began talking. This was not an audience. It was a town temporarily facing the same direction.</p>'
                '</article>'
            ),
            150: '<article class="prose"><p>River House had six rooms</p></article>',
            151: (
                '<a rel="prev" href="150.html">Chapter 150</a>'
                '<article class="prose"><p>The rest of the show happened around me. OLD</p>'
                '<p>A local worker dragged the broken pieces off during the next entrance. No one mentioned it again.</p>'
                '</article>'
            ),
            152: (
                '<article class="prose"><p>Pell was under a table. I found his boots first.</p>'
                '<p>OLD RESET</p><p>Then Teren called him and he got up. I stayed.</p>'
                '<p>Doors in one hour.</p></article>'
            ),
        }
        once = apply_transformations(docs)
        twice = apply_transformations(once)
        self.assertEqual(once, twice)
        self.assertIn('href="151.html"', once[149])
        self.assertIn('href="149.html"', once[151])
        self.assertIn('data-structural-status="merged"', once[150])
        self.assertIn("That's the work.", once[149])
        self.assertIn("Don't do the dead uncle.", once[152])
        self.assertNotIn("OLD RESET", once[152])


if __name__ == "__main__":
    unittest.main()
