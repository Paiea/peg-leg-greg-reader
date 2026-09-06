import unittest

from scripts.apply_structural_compression_075_076 import transform_chapter_paragraphs


class IndependenceCompressionTest(unittest.TestCase):
    def test_preserves_two_independence_milestones_while_cutting_repeated_instruction(self):
        ch75 = [
            "The rail was finished before I was.",
            "No job today. Sera looked at the wound.",
            "OLD WOUND INVENTORY AND SEVEN STEP DRILL",
            "At the Guild desk, the clerk had a note for me.",
            "Jorren arrived after fourth bell with ink on his thumb.",
            "Hessa showed him. Not by making me climb.",
            "OLD SPOTTER INSTRUCTION LOOP",
            "Ready? Hessa asked. No.",
            "I put one crutch aside.",
            "Top. I was upstairs.",
            "My room. Same bed. Same washbasin.",
        ]
        ch76 = [
            "The chamber pot had become personal.",
            "Nerin arrived with a satchel and used the new rail.",
            "OLD WOUND INVENTORY AND SPOTTER OPTIONS",
            "Jorren could not come.",
            "The keeper volunteered.",
            "OLD KEEPER SPOTTER INSTRUCTION LOOP",
            "Fine. I stood at the top.",
            "The phantom left foot was already on the first lower step.",
            "I sat on step nine.",
            "Ground floor. Kitchen.",
            "I can use the privy.",
            "The storage room no longer felt like the only place I could exist.",
        ]

        out75 = transform_chapter_paragraphs(75, ch75)
        out76 = transform_chapter_paragraphs(76, ch76)
        text75 = "\n".join(out75)
        text76 = "\n".join(out76)

        self.assertNotIn("OLD WOUND INVENTORY AND SEVEN STEP DRILL", text75)
        self.assertNotIn("OLD SPOTTER INSTRUCTION LOOP", text75)
        self.assertIn("At the Guild desk, the clerk had a note for me.", text75)
        self.assertIn("Top. I was upstairs.", text75)
        self.assertIn("My room. Same bed. Same washbasin.", text75)

        self.assertNotIn("OLD WOUND INVENTORY AND SPOTTER OPTIONS", text76)
        self.assertNotIn("OLD KEEPER SPOTTER INSTRUCTION LOOP", text76)
        self.assertIn("The phantom left foot was already on the first lower step.", text76)
        self.assertIn("I can use the privy.", text76)
        self.assertIn("The storage room no longer felt like the only place I could exist.", text76)

        self.assertNotEqual(out75, out76)


if __name__ == "__main__":
    unittest.main()
