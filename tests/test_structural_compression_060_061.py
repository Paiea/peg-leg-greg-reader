import unittest

from scripts.apply_structural_compression_060_061 import (
    transform_chapter_paragraphs,
)


class RoadCompressionTest(unittest.TestCase):
    def test_preserves_distinct_day_functions_while_cutting_repeated_procedure(self):
        ch60 = [
            "Pessa's wagon had one wheel that squeaked every seventh turn.",
            "The farmer was waiting. Of course.",
            "You see it.",
            "OLD FARMER ARGUMENT LOOP",
            "Second site was not on the complaint list.",
            "There. Field systems. Maps remembered one version. Ground remembered more.",
            "At the third site, the complaint said standing water.",
            "OLD PRIVATE DRAIN PROCEDURE LOOP",
            "We ate beside a low wall near noon.",
            "Not severity. Consequence plus change.",
            "After lunch came the narrow stone bridge.",
            "Roads don't care about narrative.",
            "The next farm spur was where I became useful.",
            "Stop.",
            "Later, at a culvert half blocked with reeds, I used magic.",
        ]
        ch61 = [
            "It rained enough to make Pessa change the route.",
            "The old drainage cut did not look the same.",
            "The wheel track was still clear.",
            "OLD REPROBE TRAFFIC CONTROL LOOP",
            "No repair. Moved.",
            "The paired culvert from yesterday had changed more.",
            "Yesterday, clearing the mouth had looked like the obvious repair.",
            "DO NOT CLEAR WITHOUT OPENING / ASSESSING STRUCTURE",
            "Near noon we reached a long downhill section",
            "OLD SECOND CONSEQUENCE PLUS CHANGE LESSON",
            "Dorn said, Drink.",
            "Before the upper loop, I was wrong about a culvert.",
            "Pond overflow",
            "Then we finished the upper loop.",
        ]

        out60 = transform_chapter_paragraphs(60, ch60)
        out61 = transform_chapter_paragraphs(61, ch61)
        text60 = "\n".join(out60)
        text61 = "\n".join(out61)

        self.assertNotIn("OLD FARMER ARGUMENT LOOP", text60)
        self.assertNotIn("OLD PRIVATE DRAIN PROCEDURE LOOP", text60)
        self.assertIn("Maps remembered one version. Ground remembered more.", text60)
        self.assertIn("Roads don't care about narrative.", text60)
        self.assertIn("The next farm spur was where I became useful.", text60)

        self.assertNotIn("OLD REPROBE TRAFFIC CONTROL LOOP", text61)
        self.assertNotIn("OLD SECOND CONSEQUENCE PLUS CHANGE LESSON", text61)
        self.assertIn("The paired culvert from yesterday had changed more.", text61)
        self.assertIn("DO NOT CLEAR WITHOUT OPENING / ASSESSING STRUCTURE", text61)
        self.assertIn("Pond overflow", text61)

        self.assertNotEqual(out60, out61)


if __name__ == "__main__":
    unittest.main()
