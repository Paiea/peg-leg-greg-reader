import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import apply_dialogue_variance as adv


class DialogueVarianceIntegratorTests(unittest.TestCase):
    def test_parses_current_and_replace_patch(self):
        note = '''## Chapter 3 — THE INVESTOR
### Patch 3.V1 — example
Current:

`"Old."`

`"Still old."`

Replace with:

`"New."`

`"Still new."`

Reason: test
'''
        patches = adv.parse_batch(note)
        self.assertEqual(1, len(patches))
        self.assertEqual(3, patches[0].chapter)
        self.assertEqual(['"Old."', '"Still old."'], patches[0].current)
        self.assertEqual(['"New."', '"Still new."'], patches[0].replacement)

    def test_applies_patch_without_removing_figure_and_is_idempotent(self):
        html = '<article class="prose"><p>Before.</p><p>"Old."</p><figure><img src="x.png"/></figure><p>"Still old." After.</p></article>'
        patch = adv.Patch(3, '3.V1', ['"Old."', '"Still old."'], ['"New."', '"Still new."'], '')
        changed = adv.apply_patch_to_html(html, patch)
        self.assertIn('<figure><img src="x.png"/></figure>', changed)
        self.assertIn('"New."', changed)
        self.assertIn('"Still new." After.', changed)
        self.assertNotIn('"Old."', changed)
        self.assertEqual(changed, adv.apply_patch_to_html(changed, patch))

    def test_preserves_unrelated_inline_prose_markup(self):
        html = '<article class="prose"><p>Before <em>important</em> thought.</p><p>"Old."</p><p>"Still old."</p></article>'
        patch = adv.Patch(3, '3.V1', ['"Old."', '"Still old."'], ['"New."', '"Still new."'], '')
        changed = adv.apply_patch_to_html(html, patch)
        self.assertIn('<p>Before <em>important</em> thought.</p>', changed)
        self.assertIn('<p>"New."</p>', changed)
        self.assertIn('<p>"Still new."</p>', changed)

    def test_replace_after_anchor_preserves_current_through_anchor(self):
        html = '<article class="prose"><p>"Tell me."</p><p>"Impossible."</p><p>"Good."</p><p>"That one."</p></article>'
        patch = adv.Patch(
            13,
            '13.V1',
            ['"Tell me."', '"Impossible."', '"Good."', '"That one."'],
            ['"Good." Arlo seated the regulator.', '"Then watch the test."'],
            'Replace after Greg says `Impossible.` with:',
        )
        changed = adv.apply_patch_to_html(html, patch)
        self.assertIn('<p>"Tell me."</p>', changed)
        self.assertIn('<p>"Impossible."</p>', changed)
        self.assertIn('<p>"Good." Arlo seated the regulator.</p>', changed)
        self.assertIn('<p>"Then watch the test."</p>', changed)
        self.assertNotIn('<p>"That one."</p>', changed)

    def test_final_line_directive_replaces_only_last_current_line(self):
        html = '<article class="prose"><p>A.</p><p>B.</p><p>C.</p></article>'
        patch = adv.Patch(7, '7.V3', ['A.', 'B.', 'C.'], ['Replacement.'], 'Replace the final Antonius line with:')
        changed = adv.apply_patch_to_html(html, patch)
        self.assertIn('<p>A.</p>', changed)
        self.assertIn('<p>B.</p>', changed)
        self.assertIn('<p>Replacement.</p>', changed)
        self.assertNotIn('<p>C.</p>', changed)


if __name__ == '__main__':
    unittest.main()
