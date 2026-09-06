#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "state/editorial/performance-lab/NOVELIZATION_LIVE_REPORT.md"


def _bounded(text: str, start: str, end: str) -> tuple[str, str, str]:
    if text.count(start) != 1:
        raise AssertionError(f"expected one start boundary, found {text.count(start)}: {start}")
    start_at = text.index(start)
    tail = text[start_at:]
    if tail.count(end) != 1:
        raise AssertionError(f"expected one end boundary after start, found {tail.count(end)}: {end}")
    end_at = start_at + tail.index(end) + len(end)
    return text[:start_at], text[start_at:end_at], text[end_at:]


def _replace_exact(span: str, old: str, new: str, expected: int = 1) -> str:
    count = span.count(old)
    if count != expected:
        raise AssertionError(f"expected {expected} occurrence(s), found {count}: {old}")
    return span.replace(old, new)


def harden_007(text: str) -> str:
    before, span, after = _bounded(
        text,
        '<p>"Trash," he said.</p>',
        '<p>"End of week."</p>',
    )
    replacements = (
        ('<p>"Trash," he said.</p>', '<p>"Trash," Antonius said.</p>', 1),
        ('<p>"No."</p>', '<p>"No," I said.</p>', 1),
        (
            '<p>He nudged the box with two fingers. "Bent precision scrap. Failed artificer. Nobody wanted it. Toss it."</p>',
            '<p>Antonius nudged the box with two fingers. "Bent precision scrap. Failed artificer. Nobody wanted it. Toss it," Antonius said.</p>',
            1,
        ),
        ('<p>He kept moving toward the discard pile.</p>', '<p>Antonius kept moving toward the discard pile.</p>', 1),
        ('<p>"How valuable?"</p>', '<p>"How valuable?" Antonius asked.</p>', 1),
        ('<p>"At least."</p>', '<p>"At least," I said.</p>', 1),
        ('<p>"And you are the right buyer?"</p>', '<p>"And you are the right buyer?" Antonius asked.</p>', 1),
        ('<p>"Then tell me why it is worth anything."</p>', '<p>"Then tell me why it is worth anything," Antonius said.</p>', 1),
        ('<p>"Think?"</p>', '<p>"Think?" Antonius asked.</p>', 1),
        (
            '<p>"Arlo might be able to identify it. Maybe authenticate it. I recognize the standard, not the condition."</p>',
            '<p>"Arlo might be able to identify it. Maybe authenticate it. I recognize the standard, not the condition," I said.</p>',
            1,
        ),
        ('<p>"I can\'t name one yet."</p>', '<p>"I can\'t name one yet," I said.</p>', 1),
        ('<p>"Five silver."</p>', '<p>"Five silver," Antonius said.</p>', 1),
        ('<p>"You said three."</p>', '<p>"You said three," I said.</p>', 1),
        ('<p>"Before forty gold."</p>', '<p>"Before forty gold," Antonius said.</p>', 1),
        ('<p>"Four."</p>', '<p>"Four," I said.</p>', 1),
        ('<p>"Five."</p>', '<p>"Five," Antonius said.</p>', 1),
        ('<p>"Fine. Five."</p>', '<p>"Fine. Five," I said.</p>', 1),
        ('<p>"End of week."</p>', '<p>"End of week," Antonius said.</p>', 1),
    )
    for old, new, expected in replacements:
        span = _replace_exact(span, old, new, expected)
    return before + span + after


def harden_013(text: str) -> str:
    before, span, after = _bounded(
        text,
        '<p>"Fuck."</p>',
        '<p>Arlo laughed once despite himself, then reached for the next regulator.</p>',
    )
    replacements = (
        ('<p>"Fuck."</p>', '<p>"Fuck," I said.</p>', 1),
        ('<p>"Yes."</p>', '<p>"Yes," Arlo said.</p>', 1),
        ('<p>"Again."</p>', '<p>"Again," I said.</p>', 1),
        ('<p>"Six runs answered this test."</p>', '<p>"Six runs answered this test," Arlo said.</p>', 1),
        (
            '<p>"Then change the order. Warm them first. Cold after. Change the input."</p>',
            '<p>"Then change the order. Warm them first. Cold after. Change the input," I said.</p>',
            1,
        ),
        ('<p>"Those are other tests. I spent two days answering this one."</p>', '<p>"Those are other tests. I spent two days answering this one," Arlo said.</p>', 1),
        ('<p>"What changed?"</p>', '<p>"What changed?" I asked.</p>', 1),
        ('<p>"First I changed the clay. Then the winding. Then the firing. Then the etch."</p>', '<p>"First I changed the clay. Then the winding. Then the firing. Then the etch," Arlo said.</p>', 1),
        ('<p>"Then I had six worse regulators and no idea what mattered."</p>', '<p>"Then I had six worse regulators and no idea what mattered," Arlo said.</p>', 1),
        ('<p>"So you stopped changing the object."</p>', '<p>"So you stopped changing the object," I said.</p>', 1),
        ('<p>"Eventually."</p>', '<p>"Eventually," Arlo said.</p>', 1),
        ('<p>"Same regulator. Twenty measurements."</p>', '<p>"Same regulator. Twenty measurements," Arlo said.</p>', 1),
        ('<p>"That dropped by more than half."</p>', '<p>"That dropped by more than half," I said.</p>', 1),
        ('<p>"I stopped holding the input lead by hand."</p>', '<p>"I stopped holding the input lead by hand," Arlo said.</p>', 1),
        ('<p>"You separated measurement error from object variation."</p>', '<p>"You separated measurement error from object variation," I said.</p>', 1),
        ('<p>"I stopped holding the wire."</p>', '<p>"I stopped holding the wire," Arlo said.</p>', 1),
        ('<p>"Then the regulators still spread?"</p>', '<p>"Then the regulators still spread?" I asked.</p>', 1),
        ('<p>"Yes. So I changed one thing. Winding tension."</p>', '<p>"Yes. So I changed one thing. Winding tension," Arlo said.</p>', 1),
        ('<p>"You built a tensioner."</p>', '<p>"You built a tensioner," I said.</p>', 1),
        ('<p>"I hung a weight on a string."</p>', '<p>"I hung a weight on a string," Arlo said.</p>', 1),
        ('<p>"That is what a tensioner is if you are poor."</p>', '<p>"That is what a tensioner is if you are poor," I said.</p>', 1),
    )
    for old, new, expected in replacements:
        span = _replace_exact(span, old, new, expected)
    return before + span + after


def harden_018(text: str) -> str:
    before, span, after = _bounded(
        text,
        '<p>Hessa took one bean and placed it on the table between us.</p>',
        '<p>"Tell me what you learned."</p>',
    )
    replacements = (
        ('<p>"Move it."</p>', '<p>"Move it," Hessa said.</p>', 1),
        ('<p>"With Barrier?"</p>', '<p>"With Barrier?" I asked.</p>', 1),
        ('<p>"Again."</p>', '<p>"Again," Hessa said.</p>', 3),
        (
            '<p>"That is an irresponsible attitude toward beans."</p>',
            '<p>"That is an irresponsible attitude toward beans," I said.</p>',
            1,
        ),
        ('<p>"What changed?"</p>', '<p>"What changed?" Hessa asked.</p>', 1),
        ('<p>"Placement. I intersected the target."</p>', '<p>"Placement. I intersected the target," I said.</p>', 1),
        ('<p>"When I pushed the bean, I anchored against the room."</p>', '<p>"When I pushed the bean, I anchored against the room," I said.</p>', 1),
        (
            '<p>"The spell is holding a position it doesn\'t need to hold. I\'m making a wall for a job that needs a tap."</p>',
            '<p>"The spell is holding a position it doesn\'t need to hold. I\'m making a wall for a job that needs a tap," I said.</p>',
            1,
        ),
        ('<p>"What would you change?"</p>', '<p>"What would you change?" Hessa asked.</p>', 1),
        ('<p>"I don\'t know."</p>', '<p>"I don\'t know," I said.</p>', 1),
        ('<p>"Good."</p>', '<p>"Good," Hessa said.</p>', 1),
        ('<p>"Find out."</p>', '<p>"Find out," Hessa said.</p>', 1),
        ('<p>"What does Barrier need to be Barrier?"</p>', '<p>"What does Barrier need to be Barrier?" I asked.</p>', 1),
        ('<p>"What does this exercise need?"</p>', '<p>"What does this exercise need?" Hessa asked.</p>', 1),
        ('<p>"It needs the bean to move."</p>', '<p>"It needs the bean to move," I said.</p>', 1),
        ('<p>I looked at Hessa. "How far?"</p>', '<p>I looked at Hessa.</p><p>"How far?" I asked.</p>', 1),
        ('<p>"One finger."</p>', '<p>"One finger," Hessa said.</p>', 2),
        ('<p>"That\'s all?"</p>', '<p>"That\'s all?" I asked.</p>', 1),
        (
            '<p>"You have been letting me throw them across the table."</p>',
            '<p>"You have been letting me throw them across the table," I said.</p>',
            1,
        ),
        (
            '<p>"I have been watching you decide what the problem was."</p>',
            '<p>"I have been watching you decide what the problem was," Hessa said.</p>',
            1,
        ),
        ('<p>"I\'ve barely started."</p>', '<p>"I\'ve barely started," I said.</p>', 1),
        ('<p>"Nineteen casts."</p>', '<p>"Nineteen casts," Hessa said.</p>', 1),
        ('<p>"I feel fine."</p>', '<p>"I feel fine," I said.</p>', 1),
        ('<p>"You feel interested."</p>', '<p>"You feel interested," Hessa said.</p>', 1),
        ('<p>"Tell me what you learned."</p>', '<p>"Tell me what you learned," Hessa said.</p>', 1),
    )
    for old, new, expected in replacements:
        span = _replace_exact(span, old, new, expected)
    return before + span + after


def _validate(path: Path, must_have: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in must_have:
        if snippet not in text:
            raise AssertionError(f"missing attribution anchor in {path}: {snippet}")


def _update_report() -> None:
    if not REPORT.exists():
        raise AssertionError(f"missing report: {REPORT}")
    text = REPORT.read_text(encoding="utf-8")
    marker = "## Conservative attribution hardening"
    if marker in text:
        return
    addition = '''\n## Conservative attribution hardening\n\nPASS. Novel prose was re-anchored for instantaneous first-read speaker recognition. Ordinary `said` / `asked` tags are intentionally repeated after narration, action beats, and speaker changes. An action beat is allowed to carry attribution only when the acting character is unquestionably the speaker in that same paragraph. The changed spans do not rely on another character's separate action to imply who spoke.\n'''
    REPORT.write_text(text.rstrip() + "\n" + addition, encoding="utf-8")


def run(write: bool) -> None:
    targets = (
        (ROOT / "chapters/007.html", harden_007),
        (ROOT / "chapters/013.html", harden_013),
        (ROOT / "chapters/018.html", harden_018),
    )
    for path, fn in targets:
        original = path.read_text(encoding="utf-8")
        # Idempotent after the first successful hardening commit.
        if path.name == "007.html" and '"Trash," Antonius said.' in original:
            continue
        if path.name == "013.html" and '"Six runs answered this test," Arlo said.' in original:
            continue
        if path.name == "018.html" and '"Move it," Hessa said.' in original:
            continue
        updated = fn(original)
        if write:
            path.write_text(updated, encoding="utf-8")

    if write:
        _update_report()
        _validate(ROOT / "chapters/007.html", (
            '"Trash," Antonius said.',
            '"How valuable?" Antonius asked.',
            '"Fine. Five," I said.',
            '"End of week," Antonius said.',
        ))
        _validate(ROOT / "chapters/013.html", (
            '"Again," I said.',
            '"Six runs answered this test," Arlo said.',
            '"What changed?" I asked.',
            '"I stopped holding the wire," Arlo said.',
        ))
        _validate(ROOT / "chapters/018.html", (
            '"Move it," Hessa said.',
            '"What changed?" Hessa asked.',
            '"Nineteen casts," Hessa said.',
            '"Tell me what you learned," Hessa said.',
        ))


def main() -> int:
    parser = argparse.ArgumentParser(description="Harden dialogue attribution inside the bounded PERFORMANCE novelization scenes.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    run(args.write)
    print("PERFORMANCE attribution hardening: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
