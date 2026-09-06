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

    def test_removes_generated_duplicate_hall_boundary(self):
        hall = "At the hall, Rinna was standing just inside the front doors with a small slate in one hand and a piece of chalk in the other."
        already_compressed = [
            "Lyssa was gone before I woke, but she had left me the larger piece of bread. I treated this as suspicious generosity, checked my wrist once, and discovered that once was enough. The wrist and shoulder were nearly boring again.",
            "Nothing new waited under the cup. I left it alone, ate the oversized bread, and went to work. On the way, three people were helping a cart out of a hole while four more explained why they were doing it wrong. Carrow remained fully staffed.",
            hall,
            hall,
            "Until the Guild sends for you, third bell.",
            "I had been scheduled.",
            "Inside, Pell and Davin were fixing a wobbling bench. Pell found the missing square nut under it; Davin put it back where it belonged. The repair required less philosophy than my inspection of it.",
            "The board initially gave me SET. Rinna pointed out that I was early only because I had arrived at my old time, which was exactly why she had made third bell official. The new schedule had survived several minutes before theatre began negotiating with it.",
            "Teren came through carrying pages, asked where everyone was, and found me before Rinna could finish proving the system worked.",
            "Teren looked directly at me.",
            "Good. Guard.",
            "The Guard had six lines until I found one about a chicken that no longer existed in the local version. Teren crossed it out. Five.",
            "Rehearsal took eleven minutes.",
        ]
        out = transform_paragraphs(198, already_compressed)
        self.assertEqual(out.count(hall), 1)


if __name__ == "__main__":
    unittest.main()
