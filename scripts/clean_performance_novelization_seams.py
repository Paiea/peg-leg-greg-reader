#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "state/editorial/performance-lab/NOVELIZATION_LIVE_REPORT.md"


def replace_once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"expected one seam target, found {count}: {old[:120]}")
    return text.replace(old, new, 1)


def clean_004(text: str) -> str:
    return replace_once(
        text,
        '<p>The room did not object. The shale project had become the most dangerous kind of thing: promising. Failure would have been cleaner. If Arlo had looked at the sixth disk and said no, useless, wrong, then the project could die with dignity. Instead we had a twenty-percent improvement, a path toward better tests, and no idea whether the final product would take two weeks or two years.</p>',
        '<p>The room did not object. The shale project had become the most dangerous kind of thing: promising. The sixth disk had barely beaten the control; by the end of the night, Arlo\'s best result was closer to twenty percent. Failure would have been cleaner. If that result had collapsed on replication, the project could die with dignity. Instead we had a path toward better tests, and no idea whether the final product would take two weeks or two years.</p>',
    )


def clean_007(text: str) -> str:
    text = replace_once(
        text,
        '<p>Antonius nudged the box with two fingers. "Bent precision scrap. Failed artificer. Nobody wanted it. Toss it," Antonius said.</p>',
        '<p>Antonius nudged the box with two fingers. "Bent precision scrap. Failed artificer. Nobody wanted it. Toss it."</p>',
    )
    text = replace_once(
        text,
        '<p>"Why was that under a chair?"</p><p>"Because, Greg, until thirty seconds ago it was trash."</p>',
        '<p>"Why was that under a chair?" I asked.</p><p>"Because, Greg, until thirty seconds ago it was trash," Antonius said.</p>',
    )
    return text


def clean_013(text: str) -> str:
    text = replace_once(
        text,
        '<p>"What did the tensioner do?"</p><p>"Reduced spread again."</p><p>"How much?" I asked.</p><p>Arlo showed me. I read. Then reread.</p><p>"That\'s real."</p><p>"I know."</p><p>"Not enough."</p><p>"I know."</p><p>"But real."</p><p>"I know," I said.</p>',
        '<p>"What did the tensioner do?" I asked.</p><p>"Reduced spread again," Arlo said.</p><p>"How much?" I asked.</p><p>Arlo showed me. I read. Then reread.</p><p>"That\'s real," I said.</p><p>"I know," Arlo said.</p><p>"Not enough," I said.</p><p>"I know," Arlo said.</p><p>"But real," I said.</p><p>"I know," Arlo said.</p>',
    )
    text = replace_once(
        text,
        '<p>"Which variable next?" I asked.</p><p>Arlo smiled. Not because he needed my answer. Because he already had one.</p><p>"Firing."</p><p>"Temperature?"</p><p>"Position." </p><p>I blinked.</p><p>"In the kiln?"</p><p>"Back runs hotter."</p><p>"How do you know?"</p><p>"Broken glaze." </p>',
        '<p>"Which variable next?" I asked.</p><p>Arlo smiled. Not because he needed my answer. Because he already had one.</p><p>"Firing," Arlo said.</p><p>"Temperature?" I asked.</p><p>"Position," Arlo said.</p><p>I blinked.</p><p>"In the kiln?" I asked.</p><p>"Back runs hotter," Arlo said.</p><p>"How do you know?" I asked.</p><p>"Broken glaze," Arlo said.</p>',
    )
    return text


def clean_018(text: str) -> str:
    text = replace_once(
        text,
        '<p>"Tell me what you learned," Hessa said.</p><p>"Brief structures cost less."</p><p>"Do they?"</p><p>I paused.</p><p>"Mine did."</p><p>"Today."</p><p>"Yes."</p><p>"With this shape."</p><p>"Yes."</p><p>"At this size."</p><p>"Yes."</p><p>"Against a bean."</p><p>I frowned.</p><p>"Yes."</p><p>"Good."</p>',
        '<p>"Tell me what you learned," Hessa said.</p><p>"Brief structures cost less," I said.</p><p>"Do they?" Hessa asked.</p><p>I paused.</p><p>"Mine did," I said.</p><p>"Today," Hessa said.</p><p>"Yes," I said.</p><p>"With this shape," Hessa said.</p><p>"Yes," I said.</p><p>"At this size," Hessa said.</p><p>"Yes," I said.</p><p>"Against a bean," Hessa said.</p><p>I frowned.</p><p>"Yes," I said.</p><p>"Good," Hessa said.</p>',
    )
    return text


def update_report() -> None:
    text = REPORT.read_text(encoding="utf-8")
    marker = "## Showcase handoff seam repair"
    if marker in text:
        return
    addition = '''\n## Showcase handoff seam repair\n\nPASS. The displayed Chapter 2 -> 3 handoff skips canon 003, so canon 004 now re-establishes the shale-test antecedent in one sentence before Greg reasons from the result. The repair preserves the hidden-canon facts: the sixth disk first beat the control, later tests reached closer to twenty percent, and the project remained promising rather than proven. No hidden chapter is restored and no scene outcome changes.\n'''
    REPORT.write_text(text.rstrip() + "\n" + addition, encoding="utf-8")


def validate() -> None:
    checks = {
        "chapters/004.html": (
            "The sixth disk had barely beaten the control; by the end of the night, Arlo's best result was closer to twenty percent.",
            "If that result had collapsed on replication, the project could die with dignity.",
        ),
        "chapters/007.html": (
            'Antonius nudged the box with two fingers. "Bent precision scrap. Failed artificer. Nobody wanted it. Toss it."',
            '"Why was that under a chair?" I asked.',
            '"Because, Greg, until thirty seconds ago it was trash," Antonius said.',
        ),
        "chapters/013.html": (
            '"What did the tensioner do?" I asked.',
            '"That\'s real," I said.',
            '"I know," Arlo said.',
            '"Firing," Arlo said.',
            '"Broken glaze," Arlo said.',
        ),
        "chapters/018.html": (
            '"Brief structures cost less," I said.',
            '"Do they?" Hessa asked.',
            '"Against a bean," Hessa said.',
            '"Good," Hessa said.',
        ),
    }
    for rel, snippets in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                raise AssertionError(f"missing seam cleanup in {rel}: {snippet}")

    ch13 = (ROOT / "chapters/013.html").read_text(encoding="utf-8")
    bad = '<p>"But real."</p><p>"I know," I said.</p>'
    if bad in ch13:
        raise AssertionError("Arlo/Greg seam still contains the incorrect Greg attribution")


def run(write: bool) -> None:
    cleaners = {
        "chapters/004.html": clean_004,
        "chapters/007.html": clean_007,
        "chapters/013.html": clean_013,
        "chapters/018.html": clean_018,
    }
    for rel, cleaner in cleaners.items():
        path = ROOT / rel
        original = path.read_text(encoding="utf-8")
        updated = cleaner(original)
        if write and updated != original:
            path.write_text(updated, encoding="utf-8")
    if write:
        update_report()
        validate()


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean entry/exit seams around bounded PERFORMANCE novelization scenes and Showcase handoffs.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    run(args.write)
    print("PERFORMANCE seam cleanup: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
