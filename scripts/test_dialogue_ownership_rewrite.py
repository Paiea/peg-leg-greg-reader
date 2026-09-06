#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.apply_dialogue_ownership_rewrite import action_events, cleanup_local_dialogue, transform_paragraph


def main() -> int:
    raw = '"How much?" Antonius asked. I named the offensive number. The man with the scar laughed. Antonius looked at my Bronze plate. "Collateral?"'
    events = action_events(raw)
    assert any(owner == 'OTHER' and pos == raw.index('The man with the scar laughed.') for pos, owner in events), events

    got, _ = transform_paragraph('"You," I said. She stared. I smiled.', 'GREG', 0)
    expected = '"You," I said. </p><p>She stared. </p><p>I smiled.'
    assert got == expected, (got, expected)

    got, _ = transform_paragraph('"At nineteen?" I shrugged. He drummed two fingers on the desk.', 'OTHER', 0)
    expected = '"At nineteen?" </p><p>I shrugged. </p><p>He drummed two fingers on the desk.'
    assert got == expected, (got, expected)

    cases = {
        '<p>"If I had an answer you\'d believe, I wouldn\'t need your money." He denied the large loan. Of course he did.</p>': '<p>"If I had an answer you\'d believe, I wouldn\'t need your money."</p><p>He denied the large loan. Of course he did.</p>',
        '<p>She stopped. "Do I know you?" I knew her future immediately.</p>': '<p>She stopped. "Do I know you?"</p><p>I knew her future immediately.</p>',
        '<p>"Then we\'ve discovered another stable property," I said. He should have thrown me out. Instead he looked back at the sample.</p>': '<p>"Then we\'ve discovered another stable property," I said.</p><p>He should have thrown me out. Instead he looked back at the sample.</p>',
        '<p>"How much do you think the idea is worth?" he asked. I nearly answered with the future.</p>': '<p>"How much do you think the idea is worth?" he asked.</p><p>I nearly answered with the future.</p>',
        '<p>"If Vale sent you, don\'t sign anything without reading it." I smiled.</p>': '<p>"If Vale sent you, don\'t sign anything without reading it."</p><p>I smiled.</p>',
        '<p>"I said if this becomes something, I\'m not your employee." I blinked.</p>': '<p>"I said if this becomes something, I\'m not your employee."</p><p>I blinked.</p>',
    }
    for before, expected in cases.items():
        got = cleanup_local_dialogue(before)
        assert got == expected, (got, expected)

    print('dialogue ownership rewrite regressions passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
