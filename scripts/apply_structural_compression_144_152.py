#!/usr/bin/env python3
"""Apply the approved first structural-compression wave for PLG Chapters 149-152.

This intentionally works on stable story identities before display-number migration.
Chapter 150 becomes an inactive legacy alias; its surviving story beats are folded
into Chapters 149 and 151. Illustration markup is advisory and may disappear when
its surrounding redundant prose is removed.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Dict


BRIDGE_MARKER = "<!-- STRUCTURAL-COMPRESSION-144-152:149-BRIDGE -->"
INTRO_MARKER = "<!-- STRUCTURAL-COMPRESSION-144-152:151-INTRO -->"
RESET_MARKER = "<!-- STRUCTURAL-COMPRESSION-144-152:152-RESET -->"
MERGED_ATTR = 'data-structural-status="merged"'


AUDIENCE_SETUP_START = "<p>We went opposite directions. That felt appropriate."
AUDIENCE_SETUP_END = (
    "<p>I went to the wing. The house had grown. Maybe forty now. People entered without ceremony. "
    "Some paid something at the front. Some apparently did not. A woman came in, saw someone she knew, "
    "crossed two rows to sit beside her, and immediately began talking. This was not an audience. "
    "It was a town temporarily facing the same direction. Teren stood in the center aisle.</p>"
)

SHOW_MONTAGE_START = "<p>The rest of the show happened around me. Not to me. That was different."
SHOW_MONTAGE_END = (
    "<p>A local worker dragged the broken pieces off during the next entrance. No one mentioned it again.</p>"
)

SECOND_SHOW_RESET_START = "<p>Pell was under a table. I found his boots first.</p>"
SECOND_SHOW_RESET_END = "<p>Then Teren called him and he got up. I stayed.</p>"


AUDIENCE_SETUP_REPLACEMENT = """<p>We went opposite directions. Backstage had become narrower since I left it: more people, more cloth, more things moving through spaces that had not been designed for them. Someone made me move for scenery. Pell was looking for something Marek had apparently been wearing. Teren found me before I could become useful.</p><p>\"Greg. Sword first.\"</p><p>\"What about Shopkeeper?\"</p><p>\"Later.\"</p><p>He was gone. Fine. I went to the wing. The house had grown to perhaps forty people, arriving without ceremony, talking to neighbors, leaving and returning. This was not an audience so much as a town temporarily facing the same direction.</p>"""


WORK_BRIDGE = f"""{BRIDGE_MARKER}<p>By the time Teren finally let the open rehearsal stop, I understood two things. The audience could change a scene, and chasing the version that had worked yesterday was another way of not listening to the one happening now.</p><p>River House had six rooms, one bathtub, three matching chairs, and a woman at the front desk who had already decided she hated actors.</p><p>\"We are not actors,\" Marek told her.</p><p>\"What are you?\"</p><p>\"Traveling cultural labor.\"</p><p>Serra said, \"He's an actor,\" took her key, and disappeared again. I did not ask where. Progress.</p><p>I got a room with Pell. Before dinner I checked the wrapping on my residual limb. Warm, irritated from the day, not damaged. I cleaned it, redid it once, then made myself leave the second attempt alone when it was secure. Tired judgment was still judgment.</p><p>Downstairs, the company had colonized half the common room with food, cards, thread, and unfinished clothing. I ate stew with Marek and Iven.</p><p>\"How much do we actually do this?\" I asked.</p><p>\"Eat?\" Marek said.</p><p>\"Shows.\"</p><p>They answered with theatre arithmetic. Sometimes one show in a town. Sometimes two a day. Sometimes a week to rehearse. Sometimes three days. Sometimes Teren apparently said, \"You're the priest now,\" and that was the rehearsal.</p><p>Iven said he had once learned a duke during intermission.</p><p>\"During the show?\"</p><p>\"Yes.\"</p><p>\"How many lines?\"</p><p>\"Thirty-something.\"</p><p>\"That is not possible.\"</p><p>\"I was bad.\"</p><p>Marek leaned forward. \"That's the work.\"</p><p>Iven tore bread. \"If you know the shape, you can fill.\"</p><p>Who wanted what. Who entered. Who left. Which line somebody actually needed. Suddenly Shopkeeper made more sense. Nobody had discovered I was secretly an actor. They had needed a Shopkeeper. I had been nearby. Less flattering. Better.</p><p>\"Do you get paid every show?\"</p><p>\"Yes,\" Iven said.</p><p>Marek lifted his beer. \"Money.\"</p><p>I lifted water. \"Money.\"</p><p>Teren arrived late enough to look personally offended by the day.</p><p>\"Two shows tomorrow,\" he said. \"Afternoon and night. Gate terms are done.\"</p><p>\"Good terms?\" Orin asked.</p><p>\"Done.\"</p><p>No Meren. I had Shopkeeper and Sword in both.</p><p>\"That is four roles.\"</p><p>Teren looked at me. \"Two roles twice.\"</p><p>Right. Work, not revelation. Tomorrow we did the show, got paid, ate something, repaired whatever broke, and did it again.</p>"""


SHOW_INTRO = f"""{INTRO_MARKER}<p>By afternoon, the hall had stopped feeling like rehearsal space. People had paid to be there. Teren said places. I went to the wall opening, set my crutches where I could reach them, and did the one useful thing I had learned yesterday.</p><p>I listened.</p>"""


SHOW_MONTAGE_REPLACEMENT = """<p>The rest of the show happened around me more than to me. That was different. Backstage, repairs happened without becoming emergencies. Nessa fixed Serra while Serra was still wearing the dress. Pell changed a hem on an actress standing on a box. Davin vanished beneath the stage with a hammer and the loose board stopped making noise. The replacement for the broken blue poison jar was brown. The audience accepted that brown was poison.</p><p>Orin came offstage furious because people had laughed at his death. Marek forgot a name and called the man \"my loyal friend\" until the correct name returned. None of it stopped the play. Nobody congratulated the recovery because the recovery was the job.</p><p>By the final act, everyone was tired enough to stop giving slow scenes room to remain slow. Then Marek sat on a chair and the chair folded under him. The audience screamed, then laughed.</p><p>\"I have been betrayed,\" Marek said from the floor.</p><p>Serra looked down at him. \"By furniture.\"</p><p>He stood. The scene continued. The broken chair disappeared before anyone had time to turn it into a crisis.</p>"""


SECOND_SHOW_RESET_REPLACEMENT = f"""{RESET_MARKER}<p>Three hours sounded like time until I watched theatre people use it. The broken chair disappeared. Costumes were repaired. People ate wherever there was space, slept wherever there was less noise, argued over objects, and kept moving.</p><p>My first show money was still in my pocket. I checked once. Then, annoyingly, once more.</p><p>Marek found me eating beans with pork and stole a piece.</p><p>\"Rich man.\"</p><p>\"No.\"</p><p>\"Paid actor.\"</p><p>\"Technically.\"</p><p>\"After tonight, we go out.\"</p><p>\"I am tired.\"</p><p>\"So is everyone.\"</p><p>He looked tired too. The cut on his jaw had opened slightly. When I pointed it out, he touched it as though he had forgotten it existed. Then he fell asleep against the wall in less than a minute.</p><p>Serra returned later with fried food, gave pieces to Nessa and Rinna, kept one, and walked past me. I did not ask where she had been. Progress.</p><p>I found a quiet corner and sat. Iven joined me without speaking.</p><p>After a while he said, \"Don't do the dead uncle.\"</p><p>\"Why?\"</p><p>\"Because you want to.\"</p><p>\"It worked.\"</p><p>\"Exactly.\"</p><p>I disliked him.</p><p>\"What are you going to say?\"</p><p>\"No idea.\"</p><p>\"That is irresponsible.\"</p><p>He smiled without opening his eyes. \"Paid actor.\"</p><p>Then Teren called him and the room started becoming a theatre again.</p>"""


LEGACY_150_BODY = (
    '<article class="prose" data-structural-status="merged">'
    '<p>This legacy chapter address is retained during structural editing. '
    'Its surviving story material has been merged into Chapters 149 and 151 under stable manuscript identity.</p>'
    '</article>'
)


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    start_count = text.count(start)
    end_count = text.count(end)
    if start_count != 1 or end_count != 1:
        raise ValueError(
            f"expected one start/end marker, got start={start_count} end={end_count}: {start!r} / {end!r}"
        )
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[:i] + replacement + text[j:]


def replace_article(text: str, replacement: str) -> str:
    match = re.search(r'<article class="prose(?: light-prose)?"[^>]*>.*?</article>', text, flags=re.S)
    if not match:
        raise ValueError("article block not found")
    return text[: match.start()] + replacement + text[match.end() :]


def insert_before_article_end(text: str, insertion: str) -> str:
    if insertion in text:
        return text
    marker = "</article>"
    if text.count(marker) != 1:
        raise ValueError("expected exactly one article end")
    return text.replace(marker, insertion + marker, 1)


def _transform_149(text: str) -> str:
    if BRIDGE_MARKER not in text:
        text = replace_between(text, AUDIENCE_SETUP_START, AUDIENCE_SETUP_END, AUDIENCE_SETUP_REPLACEMENT)
        text = insert_before_article_end(text, WORK_BRIDGE)
    text = text.replace('rel="next" href="150.html"', 'rel="next" href="151.html"')
    return text


def _transform_150(text: str) -> str:
    if MERGED_ATTR not in text:
        text = replace_article(text, LEGACY_150_BODY)
    return text


def _transform_151(text: str) -> str:
    if INTRO_MARKER not in text:
        old_first = '<p>Then listened. Serra\'s line came. Not the line I expected.'
        new_first = SHOW_INTRO + '<p>Serra\'s line came. Not the line I expected.'
        if text.count(old_first) != 1:
            raise ValueError("Chapter 151 opening marker not found exactly once")
        text = text.replace(old_first, new_first, 1)
        text = replace_between(text, SHOW_MONTAGE_START, SHOW_MONTAGE_END, SHOW_MONTAGE_REPLACEMENT)
    text = text.replace('rel="prev" href="150.html"', 'rel="prev" href="149.html"')
    return text


def _transform_152(text: str) -> str:
    if RESET_MARKER not in text:
        text = replace_between(
            text,
            SECOND_SHOW_RESET_START,
            SECOND_SHOW_RESET_END,
            SECOND_SHOW_RESET_REPLACEMENT,
        )
    return text


def apply_transformations(docs: Dict[int, str]) -> Dict[int, str]:
    required = {149, 150, 151, 152}
    missing = required.difference(docs)
    if missing:
        raise ValueError(f"missing chapter docs: {sorted(missing)}")
    return {
        149: _transform_149(docs[149]),
        150: _transform_150(docs[150]),
        151: _transform_151(docs[151]),
        152: _transform_152(docs[152]),
    }


def prose_word_count(text: str) -> int:
    match = re.search(r'<article class="prose(?: light-prose)?"[^>]*>(.*?)</article>', text, flags=re.S)
    if not match:
        return 0
    body = re.sub(r'<[^>]+>', ' ', match.group(1))
    body = html.unescape(body)
    return len(re.findall(r"\b[\w’'-]+\b", body))


def apply_root(root: Path, check: bool = False) -> int:
    surfaces = [root / "chapters", root / "light"]
    changed = []
    stats = {}
    for surface in surfaces:
        docs = {n: (surface / f"{n}.html").read_text(encoding="utf-8") for n in range(149, 153)}
        edited = apply_transformations(docs)
        for n in range(149, 153):
            path = surface / f"{n}.html"
            before = docs[n]
            after = edited[n]
            stats[str(path.relative_to(root))] = {
                "before_words": prose_word_count(before),
                "after_words": prose_word_count(after),
                "delta_words": prose_word_count(after) - prose_word_count(before),
            }
            if before != after:
                changed.append(path)
                if not check:
                    path.write_text(after, encoding="utf-8")

    if check:
        if changed:
            print("structural compression pending:")
            for path in changed:
                print(path.relative_to(root))
            return 1
        print("structural compression 149-152 is current")
        return 0

    manifest = {
        "schema_version": 1,
        "batch": "144-152-wave1",
        "status": "applied",
        "strength": "moderate/aggressive-on-repetition",
        "stable_id_actions": {
            "plg-ch-000149": {"status": "active", "action": "tightened_and_absorbed_work_bridge"},
            "plg-ch-000150": {
                "status": "merged",
                "surviving_beats": ["plg-ch-000149", "plg-ch-000151"],
                "legacy_path": "150.html",
                "display_renumbering": "deferred",
            },
            "plg-ch-000151": {"status": "active", "action": "tightened_first_show"},
            "plg-ch-000152": {"status": "active", "action": "tightened_second_show_reset"},
        },
        "illustration_policy": "advisory_hold; removed prose may orphan old chapter-art anchors pending later art migration",
        "stats": stats,
    }
    try:
        manifest["source_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
    except Exception:
        manifest["source_commit"] = None

    manifest_path = root / "state" / "compression-batches" / "144-152-wave1.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    for path in changed:
        print(f"updated {path.relative_to(root)}")
    print(f"wrote {manifest_path.relative_to(root)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return apply_root(Path(args.root).resolve(), check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
