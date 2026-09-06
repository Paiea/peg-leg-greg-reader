import unittest

from scripts.dialogue_ownership_engine import quoted_spans, split_paragraph
from scripts.apply_dialogue_ownership_novel import _transform_markdown_body


class DialogueOwnershipNovelTests(unittest.TestCase):
    def test_distinguishes_two_named_non_greg_owners(self):
        text = '"Enough," Antonius said. Jorren laughed. Antonius looked at Greg. "Again."'
        self.assertEqual(
            split_paragraph(text),
            [
                '"Enough," Antonius said.',
                'Jorren laughed.',
                'Antonius looked at Greg. "Again."',
            ],
        )

    def test_distinguishes_named_women(self):
        text = 'Sella folded her arms. "No." Hessa looked away. "Fine."'
        self.assertEqual(
            split_paragraph(text),
            ['Sella folded her arms. "No."', 'Hessa looked away. "Fine."'],
        )

    def test_keeps_unambiguous_same_owner_pronoun(self):
        text = '"Fine," Antonius said. He counted the silver.'
        self.assertEqual(split_paragraph(text), [text])

    def test_splits_greg_from_other_character_reaction(self):
        text = '"Fine," I said. He counted the silver.'
        self.assertEqual(
            split_paragraph(text),
            ['"Fine," I said.', 'He counted the silver.'],
        )

    def test_splits_greg_interior_from_named_speaker(self):
        text = '"Do I know you?" Sella asked. I knew her future immediately.'
        self.assertEqual(
            split_paragraph(text),
            ['"Do I know you?" Sella asked.', 'I knew her future immediately.'],
        )

    def test_distinguishes_descriptive_actor(self):
        text = '"How much?" Antonius asked. I named the offensive number. The man with the scar laughed. Antonius looked at my Bronze plate. "Collateral?"'
        self.assertEqual(
            split_paragraph(text),
            [
                '"How much?" Antonius asked.',
                'I named the offensive number.',
                'The man with the scar laughed.',
                'Antonius looked at my Bronze plate. "Collateral?"',
            ],
        )

    def test_leave_and_return_gets_three_owners(self):
        text = '"Fine," Sella said. The clerk smiled. Sella left.'
        self.assertEqual(
            split_paragraph(text),
            ['"Fine," Sella said.', 'The clerk smiled.', 'Sella left.'],
        )

    def test_quoted_dialogue_is_byte_for_byte_preserved(self):
        text = '"Enough," Antonius said. Jorren laughed. Antonius looked at Greg. "Again."'
        before = quoted_spans(text)
        after = quoted_spans(' '.join(split_paragraph(text)))
        self.assertEqual(after, before)

    def test_smart_quotes_are_recognized_as_dialogue(self):
        text = 'Alden eventually said, “You really were bad.” I looked at him.'
        self.assertEqual(
            split_paragraph(text),
            ['Alden eventually said, “You really were bad.”', 'I looked at him.'],
        )

    def test_smart_quote_dialogue_is_preserved_exactly(self):
        text = 'Sava said, “No.” Everyone looked at her. Sava pointed at Osric.'
        before = quoted_spans(text)
        after_parts = split_paragraph(text)
        self.assertEqual(after_parts, ['Sava said, “No.”', 'Everyone looked at her.', 'Sava pointed at Osric.'])
        self.assertEqual(quoted_spans(' '.join(after_parts)), before)

    def test_markdown_emphasis_block_is_not_rewritten(self):
        text = '**The theatre sent somebody by for you once. He said, "Again?" like this was my fault. I told him no. He left.**'
        transformed, splits = _transform_markdown_body(text)
        self.assertEqual(transformed, text)
        self.assertEqual(splits, 0)


if __name__ == '__main__':
    unittest.main()
