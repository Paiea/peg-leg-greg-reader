import unittest

from scripts.apply_structural_compression_183_184 import transform_paragraphs


class WorkerRunnerCompressionTest(unittest.TestCase):
    def test_cuts_repeated_magic_and_errand_procedure_but_preserves_role_changes(self):
        ch183 = [
            "I woke up looking at the corner of a piece of paper.",
            "OLD_HOME_MAGIC_LOOP",
            "At East Market Hall, Pell was waiting for me beside the repaired latch.",
            "OLD_MAGIC_QUESTION_LOOP",
            "That was how my first established external magical effect entered the theatre.",
            "OLD_DOOR_REPAIR_LOOP",
            "The afternoon audience began arriving before we were ready.",
            "The afternoon problem was not the children.",
            "It was the lamp.",
            "The piece ran with a plain lamp.",
            "The Miller's Son was next.",
        ]
        ch184 = [
            "Lyssa asked me for a favor before I had finished chewing.",
            "OLD_BREAKFAST_AND_PARCEL_LOOP",
            "That was my second warning.",
            "Marra's was not on the way to East Market Hall.",
            "OLD_MARRA_SEN_MARRA_LOOP",
            "By the time I reached East Market Hall, my palm hurt",
            "OLD_WRONG_HOOKS_LOOP",
            "Teren was onstage.",
            "The Petition ran that afternoon.",
            "OLD_FAMILIAR_SHOW_LOOP",
            "For almost an hour, I forgot I had any.",
            "I left for the south market after my piece.",
        ]

        out183 = "\n".join(transform_paragraphs(183, ch183))
        out184 = "\n".join(transform_paragraphs(184, ch184))

        for marker in ("OLD_HOME_MAGIC_LOOP", "OLD_MAGIC_QUESTION_LOOP", "OLD_DOOR_REPAIR_LOOP"):
            self.assertNotIn(marker, out183)
        self.assertIn("first established external magical effect entered the theatre", out183)
        self.assertIn("The afternoon problem was not the children.", out183)
        self.assertIn("The Miller's Son was next.", out183)

        for marker in (
            "OLD_BREAKFAST_AND_PARCEL_LOOP",
            "OLD_MARRA_SEN_MARRA_LOOP",
            "OLD_WRONG_HOOKS_LOOP",
            "OLD_FAMILIAR_SHOW_LOOP",
        ):
            self.assertNotIn(marker, out184)
        self.assertIn("Lyssa asked me for a favor", out184)
        self.assertIn("By the time I reached East Market Hall", out184)
        self.assertIn("The Petition ran that afternoon", out184)
        self.assertIn("For almost an hour, I forgot I had any", out184)
        self.assertIn("I left for the south market after my piece.", out184)
        self.assertEqual(out184.count("That was my second warning."), 1)


if __name__ == "__main__":
    unittest.main()
