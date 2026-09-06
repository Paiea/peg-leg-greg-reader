#!/usr/bin/env python3
from scripts.apply_dialogue_ownership_semantic import action_events, transform_paragraph


def main() -> int:
    # Regression: a generic noun-phrase actor must count as a different owner.
    raw = '"How much?" Antonius asked. I named the offensive number. The man with the scar laughed. Antonius looked at my Bronze plate. "Collateral?"'
    events = action_events(raw)
    assert any(owner == 'OTHER' and pos == raw.index('The man with the scar laughed.') for pos, owner in events), events

    # Regression: a dialogue paragraph may leave and then return to the speaker,
    # but each ownership change must create a paragraph boundary.
    got, _ = transform_paragraph('"You," I said. She stared. I smiled.', 'GREG', 0)
    expected = '"You," I said. </p><p>She stared. </p><p>I smiled.'
    assert got == expected, (got, expected)

    # Regression: when the spoken line belongs to the other speaker, Greg's
    # reaction must not ride in the same visual paragraph.
    got, _ = transform_paragraph('"At nineteen?" I shrugged. He drummed two fingers on the desk.', 'OTHER', 0)
    expected = '"At nineteen?" </p><p>I shrugged. </p><p>He drummed two fingers on the desk.'
    assert got == expected, (got, expected)

    print('dialogue ownership rewrite regressions passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
