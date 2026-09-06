import unittest

from scripts.apply_structural_compression_144_152 import (
    apply_transformations,
    replace_between,
    replace_paragraph_range,
)

# This focused suite is also the execution trigger for the first compression wave.


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

    def test_replace_paragraph_range_uses_unique_cues_not_full_paragraph_bytes(self):
        text = (
            '<article class="prose">'
            '<p>Before.</p>'
            '<p>Start cue. Extra wording that may drift.</p>'
            '<figure>art may disappear</figure>'
            '<p>Middle material.</p>'
            '<p>More drift. End cue.</p>'
            '<p>After.</p>'
            '</article>'
        )
        self.assertEqual(
            replace_paragraph_range(text, "Start cue.", "End cue.", "<p>Compressed.</p>"),
            '<article class="prose"><p>Before.</p><p>Compressed.</p><p>After.</p></article>',
        )
        with self.assertRaises(ValueError):
            replace_paragraph_range(
                '<p>Start cue.</p><p>Start cue. Again.</p><p>End cue.</p>',
                "Start cue.",
                "End cue.",
                "X",
            )

    def test_wave_one_is_idempotent_and_skips_legacy_150(self):
        docs = {
            149: (
                '<a rel="next" href="150.html">Chapter 150</a>'
                '<article class="prose"><p>We went opposite directions. That felt appropriate. OLD</p>'
                '<p>I went to the wing. The house had grown. Maybe forty now. People entered without ceremony. '
                'Some paid something at the front. Some apparently did not. A woman came in, saw someone she knew, '
                'crossed two rows to sit beside her, and immediately began talking. This was not an audience. '
                'It was a town temporarily facing the same direction. Teren stood in the center aisle.</p>'
                '<p>"Start with the road scene."</p>'
                '</article>'
            ),
            150: '<article class="prose"><p>River House had six rooms</p></article>',
            151: (
                '<a rel="prev" href="150.html">Chapter 150</a>'
                '<article class="prose"><p>Then listened. Serra\'s line came. Not the line I expected. OLD OPENING</p>'
                '<p>The rest of the show happened around me. Not to me. That was different. OLD</p>'
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
        self.assertIn("I listened.", once[151])


if __name__ == "__main__":
    unittest.main()
