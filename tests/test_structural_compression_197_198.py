import unittest

from scripts.apply_structural_compression_197_198 import transform_paragraphs


class TheatreRegularityCompressionTest(unittest.TestCase):
    def test_preserves_distinct_role_and_schedule_progression_while_cutting_repeated_procedure(self):
        ch197 = [
            "My wrist was stiff in the morning.",
            "OLD_MORNING_CHECK_LOOP",
            "At the hall, Rinna was counting tickets that did not yet belong to anyone.",
            "OLD_ROLE_INTERROGATION_LOOP",
            "I liked the petitioner.",
            "He had problems.",
            "Nobody respected them.",
            "OLD_REPAIR_AND_LUNCH_LOOP",
            "The afternoon changed something.",
        ]
        ch198 = [
            "Lyssa was gone before I woke.",
            "OLD_MORNING_AND_STREET_LOOP",
            "Until the Guild sends for you, third bell.",
            "I had been scheduled.",
            "OLD_BENCH_AND_BOARD_LOOP",
            "Teren looked directly at me.",
            "Good. Guard.",
            "OLD_GUARD_VERSION_AND_COSTUME_LOOP",
            "Rehearsal took eleven minutes.",
            "OLD_REHEARSAL_PROCEDURE_LOOP",
            "The guard worked.",
        ]

        out197 = "\n".join(transform_paragraphs(197, ch197))
        out198 = "\n".join(transform_paragraphs(198, ch198))

        self.assertNotIn("OLD_MORNING_CHECK_LOOP", out197)
        self.assertNotIn("OLD_ROLE_INTERROGATION_LOOP", out197)
        self.assertNotIn("OLD_REPAIR_AND_LUNCH_LOOP", out197)
        self.assertIn("I liked the petitioner.", out197)
        self.assertIn("Nobody respected them.", out197)

        self.assertNotIn("OLD_MORNING_AND_STREET_LOOP", out198)
        self.assertNotIn("OLD_BENCH_AND_BOARD_LOOP", out198)
        self.assertNotIn("OLD_GUARD_VERSION_AND_COSTUME_LOOP", out198)
        self.assertNotIn("OLD_REHEARSAL_PROCEDURE_LOOP", out198)
        self.assertIn("Until the Guild sends for you, third bell.", out198)
        self.assertIn("I had been scheduled.", out198)
        self.assertIn("Good. Guard.", out198)
        self.assertIn("The guard worked.", out198)


if __name__ == "__main__":
    unittest.main()
