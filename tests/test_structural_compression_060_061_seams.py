import unittest

from scripts.repair_structural_compression_060_061 import repair_paragraph


class RoadCompressionSeamTest(unittest.TestCase):
    def test_repairs_dangling_boundary_tails_without_losing_next_scene(self):
        ch60 = (
            "That was dangerous phrasing. Did I? I understood what he wanted. "
            "Not necessarily what he needed. Pessa said, ‘Next.’ We left. No repair. "
            "The farmer remained dissatisfied. The road remained functional. Good. "
            "Second site was not on the complaint list. Pessa stopped the wagon herself. "
            "I had been looking at a fence. Bad. Dorn had been looking at the road. Better."
        )
        ch61 = (
            "Good. Bounded. We marked it. No repair. Moved. "
            "The paired culvert from yesterday had changed more. One opening still flowed. "
            "The buried opening still did not."
        )

        fixed60 = repair_paragraph(60, ch60)
        fixed61 = repair_paragraph(61, ch61)

        self.assertEqual(
            fixed60,
            "Second site was not on the complaint list. Pessa stopped the wagon herself. "
            "I had been looking at a fence. Bad. Dorn had been looking at the road. Better.",
        )
        self.assertEqual(
            fixed61,
            "The paired culvert from yesterday had changed more. One opening still flowed. "
            "The buried opening still did not.",
        )
        self.assertEqual(repair_paragraph(60, fixed60), fixed60)
        self.assertEqual(repair_paragraph(61, fixed61), fixed61)


if __name__ == "__main__":
    unittest.main()
