import re
import unittest

from scripts.recompose_forward_markdown import recompose_body


class ForwardProseRecomposeTests(unittest.TestCase):
    def test_merges_fragmented_narrative_without_crossing_dialogue(self):
        source = 'The room changed.\n\nNot metaphorically.\n\nBoxes everywhere.\n\n"Move."\n\nI moved.\n\nToo fast.'
        result = recompose_body(source)
        self.assertIn('The room changed. Not metaphorically. Boxes everywhere.', result)
        self.assertIn('\n\n"Move."\n\n', result)
        self.assertIn('I moved. Too fast.', result)

    def test_preserves_the_complete_word_and_punctuation_stream(self):
        source = 'Rain.\n\nCold stone.\n\n"Again," Hessa said.\n\nGreg moved.'
        result = recompose_body(source)
        normalize = lambda text: re.sub(r'\s+', ' ', text).strip()
        self.assertEqual(normalize(result), normalize(source))


if __name__ == "__main__":
    unittest.main()
