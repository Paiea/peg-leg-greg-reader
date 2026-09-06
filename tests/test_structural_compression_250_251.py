import unittest

from scripts.apply_structural_compression_250_251 import transform_paragraphs


class UnderstudyCompressionTest(unittest.TestCase):
    def test_keeps_substitution_and_acting_progression_distinct(self):
        ch250 = [
            "The needle case did not become more important overnight.",
            "Lyssa was already dressed.",
            "OLD_HOUSEHOLD_INVENTORY_LOOP",
            "Instead someone knocked.",
            "Pell's sick.",
            "The theatre side door was already open.",
            "OLD_WALK_TO_THEATRE_LOOP",
            "Teren held out pages.",
            "Knowing a man's cup was not the same as knowing his lines.",
            "Jori came from the wing, looked once, and moved a narrow side stool",
        ]
        ch251 = [
            "I learned thirty-eight of the Uncle's forty-three lines before sleep.",
            "The first missing line was in scene one",
            "OLD_LINE_BY_LINE_MEMORIZATION_LOOP",
            "Forty-three lines. Probably.",
            "Lyssa gave the pages back.",
            "The walk gave me twenty minutes",
            "OLD_THEATRE_ARRIVAL_LOOP",
            "Teren arrived before I could answer.",
            "Knowing and playing were apparently separate industries.",
            "Because stopping is worse.",
            "We ran the whole piece.",
            "OLD_TIMING_REHEARSAL_LOOP",
            "By midday, I could get through the play without pages.",
            "Pell sounds angrier.",
            "One belonged to Pell.",
        ]
        out250 = "\n".join(transform_paragraphs(250, ch250))
        out251 = "\n".join(transform_paragraphs(251, ch251))

        self.assertNotIn("OLD_HOUSEHOLD_INVENTORY_LOOP", out250)
        self.assertNotIn("OLD_WALK_TO_THEATRE_LOOP", out250)
        self.assertIn("Pell's sick.", out250)
        self.assertIn("Knowing a man's cup was not the same as knowing his lines.", out250)
        self.assertIn("narrow side stool", out250)

        self.assertNotIn("OLD_LINE_BY_LINE_MEMORIZATION_LOOP", out251)
        self.assertNotIn("OLD_THEATRE_ARRIVAL_LOOP", out251)
        self.assertNotIn("OLD_TIMING_REHEARSAL_LOOP", out251)
        self.assertIn("Knowing and playing were apparently separate industries.", out251)
        self.assertIn("Because stopping is worse.", out251)
        self.assertIn("One belonged to Pell.", out251)


if __name__ == "__main__":
    unittest.main()
