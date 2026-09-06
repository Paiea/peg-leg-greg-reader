#!/usr/bin/env python3
"""Apply the approved structural-compression batch for PLG Chapters 208-213.

Stable identity is preserved before display-number migration. Chapter 212 becomes
an inactive legacy alias whose necessary Vale setup is absorbed into Chapter 213.
Illustration state is advisory and does not veto structural cuts.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Dict

MARK = "STRUCTURAL-COMPRESSION-208-213"


def _paragraph_matches(text: str, cue: str):
    matches = []
    for m in re.finditer(r"<p\b[^>]*>.*?</p>", text, flags=re.I | re.S):
        plain = html.unescape(re.sub(r"<[^>]+>", "", m.group(0)))
        plain = re.sub(r"\s+", " ", plain).strip()
        if cue in plain:
            matches.append(m)
    return matches


def replace_paragraph_range(text: str, start_cue: str, end_cue: str, replacement: str) -> str:
    starts = _paragraph_matches(text, start_cue)
    ends = _paragraph_matches(text, end_cue)
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError(f"Expected unique paragraph cues: {start_cue!r} ({len(starts)}), {end_cue!r} ({len(ends)})")
    start, end = starts[0], ends[0]
    if end.end() < start.start():
        raise ValueError(f"End cue precedes start cue: {start_cue!r} -> {end_cue!r}")
    return text[: start.start()] + replacement + text[end.end() :]


def replace_nav(text: str, old: int, new: int) -> str:
    text = text.replace(f'href="{old}.html"', f'href="{new}.html"')
    text = text.replace(f'Chapter {old}', f'Chapter {new}')
    return text


def alias_page(source: str, target: int) -> str:
    if 'data-structural-status="merged"' in source:
        return source
    title_match = re.search(r"<title>(.*?)</title>", source, flags=re.S)
    title = title_match.group(1) if title_match else "Peg-Leg Greg"
    return (
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"/>'
        f'<title>{title}</title></head><body data-structural-status="merged" '
        f'data-merged-into="{target}"><main><p>This chapter identity was merged during structural editing.</p>'
        f'<p><a href="{target}.html">Continue to Chapter {target}</a></p></main></body></html>\n'
    )


def transform_208(text: str) -> str:
    if f"{MARK}:208" in text:
        return text
    text = replace_paragraph_range(
        text,
        "I woke because someone hit wood outside.",
        "At the hall, the front door was locked.",
        f'<!-- {MARK}:208-MORNING --><p>I woke to wood striking outside and was upright before I knew why. A cart rolled past. Nothing knocked on our door.</p>'
        '<p>By morning the fear had shrunk back to its proper size. Nothing sat under the cup. On the way out, Lyssa made me promise that if the men came back and leaving was possible, I would leave.</p>'
        '<p>"Better," she said.</p><p>Carrow remained offensively normal. At the hall, the front door was locked.</p>',
    )
    text = replace_paragraph_range(
        text,
        "Before house, Rinna made us check the things that could actually cost money.",
        "That was the entire council.",
        f'<!-- {MARK}:208-CHECKS --><p>Before house, Rinna made us check the things the men had actually named. Davin checked the lamps. Jori checked the rear latch and found one old screw working loose. The cart was fine.</p>'
        '<p>Pell wanted the roof and then a cellar we did not have. Rinna sent him to benches instead.</p>'
        '<p>Veya asked the useful questions: who sent them, how much, whether they named anyone. We had none of those answers. Nobody drew a map, assigned weapons, or discovered a criminal empire under the floor. That was the entire council.</p>',
    )
    return text


def transform_209(text: str) -> str:
    if f"{MARK}:209" in text:
        return text
    text = replace_paragraph_range(
        text,
        "There was still no note under the cup.",
        "At the hall, the front door was latched again.",
        f'<!-- {MARK}:209-MORNING --><p>There was still no note under the cup. Lyssa called that good. I called it the most accurate unknown available.</p>'
        '<p>On the walk I noticed one gray coat, then noticed the man wearing it had two legs. Progress.</p><p>At the hall, the front door was latched again.</p>',
    )
    text = replace_paragraph_range(
        text,
        "Rinna folded the scrap with Bren's possible name",
        "The board was already up.",
        f'<!-- {MARK}:209-BOUNDS --><p>Rinna folded the scrap beneath her ledger. The useful part was small: the man might be called Bren; another cart yard near Mason\'s Cut had heard the same "small share" language and the same wheel threat. Nobody who spoke to us had established that the same man lived there, worked there, or had personally touched our cart.</p>'
        '<p>That was enough information to remember and not enough to build anything larger from. The board was already up.</p>',
    )
    return text


def transform_210(text: str) -> str:
    if f"{MARK}:210" in text:
        return text
    text = replace_paragraph_range(
        text,
        "The cart came inside twenty minutes later.",
        "House opened.",
        f'<!-- {MARK}:210-LOGISTICS --><p>The cart came inside twenty minutes later with Davin\'s replacement pin fitted and the old wheel running straight. Rinna kept it farther inside than usual.</p>'
        '<p>That displaced the rear traffic just enough to make us move a painted wall and the Widow table twice. For several minutes the extortionists lost to ordinary theatre logistics.</p>'
        '<p>Davin checked the repair once more. The other pin was still good. House opened.</p>',
    )
    return text


def transform_211(text: str) -> str:
    if f"{MARK}:211" in text:
        return text
    text = replace_paragraph_range(
        text,
        "The door closed.",
        "The board said:",
        f'<!-- {MARK}:211-BOUNDS --><p>The door closed. Talla had independently given us more than rumor: probably Bren, probably the same heavy-coated man, probably the same left glove, the same small-share demand, one payment followed by more pressure.</p>'
        '<p>What we did not have stayed just as important. No surname. No address. No organization. No proof that later broken equipment belonged to him. No reason for me to go looking.</p>'
        '<p>Rinna watched me arrive at each missing piece and refused to let me turn it into a larger answer.</p><p>"Work," she said.</p><p>The board said:</p>',
    )
    return text


def transform_213(text: str) -> str:
    if f"{MARK}:213" in text:
        return text
    text = replace_nav(text, 212, 211)
    text = replace_paragraph_range(
        text,
        "Antonius sent a cart.",
        "The work was exactly what the note had promised.",
        f'<!-- {MARK}:213-INTRO --><p>Vale had sent for me before breakfast the day before: table work, delivery accounts, first bell, one hour, transport if required. I had written YES and briefly considered objecting to first bell in writing.</p>'
        '<p>Antonius sent a cart. Not a carriage. The distinction mattered because one had cushions and the other had a sack of nails under the bench.</p>'
        '<p>At his warehouse office he looked almost exactly as before. I had lost a leg, joined a theatre, accumulated several fragments of employment, and accidentally convinced an extortionist I might be dangerous. Antonius had changed coats.</p>'
        '<p>"I thought you\'d forgotten me," I said.</p><p>"I have a ledger."</p><p>There it was.</p>'
        '<p>The work was exactly what the note had promised.</p>',
    )
    text = replace_paragraph_range(
        text,
        "The work was exactly what the note had promised.",
        "Then I reached a receiving sheet marked for a yard near Mason's Cut.",
        f'<!-- {MARK}:213-ACCOUNTS --><p>The work was exactly what the note had promised: receiving sheets, cart tallies, invoices, repair charges. They should have agreed. They did not.</p>'
        '<p>One disagreement was a copied cart mark. Another was a wheel-repair charge attached to the wrong run; the repairman\'s margin note put the cart at a different destination. Most of the rest was ordinary mess: a cracked jar already explained, a driver spelling his own name two ways, one late delivery that was simply late.</p>'
        '<p>I found no conspiracy. This was comforting.</p><p>Then I reached a receiving sheet marked for a yard near Mason\'s Cut.</p>',
    )
    return text


def apply_transformations(docs: Dict[int, str]) -> Dict[int, str]:
    out = dict(docs)
    if 208 in out:
        out[208] = transform_208(out[208])
    if 209 in out:
        out[209] = transform_209(out[209])
    if 210 in out:
        out[210] = transform_210(out[210])
    if 211 in out:
        out[211] = transform_211(out[211])
        out[211] = replace_nav(out[211], 212, 213)
    if 212 in out:
        out[212] = alias_page(out[212], 213)
    if 213 in out:
        out[213] = transform_213(out[213])
    return out


def word_count(text: str) -> int:
    plain = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return len(re.findall(r"\b[\w'-]+\b", plain))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    roots = [Path("chapters"), Path("light")]
    changes = []
    stats = {}
    for root in roots:
        docs = {n: (root / f"{n}.html").read_text(encoding="utf-8") for n in range(208, 214)}
        transformed = apply_transformations(docs)
        for n in range(208, 214):
            before, after = docs[n], transformed[n]
            key = str(root / f"{n}.html")
            stats[key] = {"before_words": word_count(before), "after_words": word_count(after), "delta_words": word_count(after) - word_count(before)}
            if before != after:
                changes.append(key)
                if not args.check:
                    (root / f"{n}.html").write_text(after, encoding="utf-8")
    if args.check:
        if changes:
            raise SystemExit("Compression transform is not idempotent: " + ", ".join(changes))
        return 0
    manifest = {
        "schema_version": 1,
        "batch": "208-213",
        "status": "applied",
        "strength": "aggressive-on-repetition",
        "stable_id_actions": {
            "plg-ch-000208": {"status": "active", "action": "tightened_threat_aftermath"},
            "plg-ch-000209": {"status": "active", "action": "tightened_bren_rumor_and_bounds"},
            "plg-ch-000210": {"status": "active", "action": "preserved_pin_discovery_tightened_post_repair_logistics"},
            "plg-ch-000211": {"status": "active", "action": "preserved_talla_corroboration_tightened_unknowns"},
            "plg-ch-000212": {"status": "merged", "surviving_beats": ["plg-ch-000213"], "legacy_path": "212.html", "display_renumbering": "deferred"},
            "plg-ch-000213": {"status": "active", "action": "absorbed_vale_setup_tightened_accounting_procedure"},
        },
        "illustration_policy": "advisory_hold; story structure outranks art anchors",
        "stats": stats,
    }
    path = Path("state/compression-batches/208-213.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
