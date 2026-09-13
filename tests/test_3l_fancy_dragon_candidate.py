import unittest

from scripts.build_3l_fancy_dragon_candidate import choose_take_boundaries


class FancyDragonCandidateTests(unittest.TestCase):
    def test_take_boundaries_follow_ordered_silences(self):
        takes = [
            {"source_transcript": "one two"},
            {"source_transcript": "three four"},
            {"source_transcript": "five six"},
        ]
        boundaries = choose_take_boundaries(
            takes,
            duration_seconds=6.0,
            silence_intervals=[(1.9, 2.1), (3.9, 4.1)],
        )
        self.assertEqual(boundaries, [0.0, 2.0, 4.0, 6.0])

    def test_take_boundaries_are_strictly_increasing(self):
        takes = [
            {"source_transcript": "one"},
            {"source_transcript": "two"},
        ]
        boundaries = choose_take_boundaries(
            takes,
            duration_seconds=2.0,
            silence_intervals=[(0.9, 1.1)],
        )
        self.assertLess(boundaries[0], boundaries[1])
        self.assertLess(boundaries[1], boundaries[2])


if __name__ == "__main__":
    unittest.main()
