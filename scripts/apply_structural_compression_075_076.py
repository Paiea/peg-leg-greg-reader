#!/usr/bin/env python3
"""Apply the approved structural compression to PLG Chapters 75-76.

Book I authority for these chapters is the ch82 DOCX snapshot. The edit therefore
updates that source and the reader projections together. The two chapters remain
separate: 75 restores Greg's room; 76 restores access to the ground-floor world.
"""

from __future__ import annotations

import argparse
import copy
import html
import json
import re
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX_REL = Path("state/manuscript/Peg_Leg_Greg_authoritative_ch82_final_name_map.docx")
HTML_PATHS = {75: Path("chapters/075.html"), 76: Path("chapters/076.html")}
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("w", W_NS)

P_RE = re.compile(r"<p(?:\s[^>]*)?>(.*?)</p>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
ARTICLE_RE = re.compile(r"(<article class=\"prose\">)(.*?)(</article>)", re.I | re.S)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def plain_html(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    return norm(html.unescape(TAG_RE.sub("", fragment)))


def word_count(paragraphs: list[str]) -> int:
    return sum(len(re.findall(r"\b\w+[’'-]?\w*\b", p)) for p in paragraphs)


def _find_unique(paragraphs: list[str], cue: str) -> int:
    matches = [i for i, p in enumerate(paragraphs) if cue in p]
    if len(matches) != 1:
        raise ValueError(f"Expected unique cue {cue!r}; found {len(matches)}")
    return matches[0]


def replace_range(paragraphs: list[str], start_cue: str, end_cue: str, replacement: list[str]) -> list[str]:
    start = _find_unique(paragraphs, start_cue)
    end = _find_unique(paragraphs, end_cue)
    if end <= start:
        raise ValueError(f"Invalid range {start_cue!r} -> {end_cue!r}")
    return paragraphs[:start] + replacement + paragraphs[end:]


CH75_CLINIC = [
    "Another warehouse night-watch posting was already being taken when I passed the board. I kept moving. No job today. Sera's wound check was boring in the useful way: minimal drainage, no heat, no spreading redness, swelling down, questionable margin still viable.",
    "The sharp spot was still sharp. The numb patch was still numb. Phantom ankle had chosen outward today. Actual knee remained straight. Body maps were stupid.",
    "The rail was finished, so Sera moved the goal from seven steps to a home attempt. First she made me do seven up and down twice. The first ascent almost felt easy. The second did not. Fatigue arrived on schedule.",
    "On the second descent my thigh trembled, so she made me practice the useful failure case instead of pretending it would not happen: turn toward the rail, keep the residual limb clear, sit on a step, then stand again with rail, crutch, and right leg.",
    "At the bottom my arms shook. Sera looked once and said, “Home attempt this afternoon if swelling remains controlled.”",
    "“Fourteen?”",
    "“With rail. With a spotter. One ascent. You stay upstairs afterward.”",
    "There. My room. Descent could wait until tomorrow if the wound stayed quiet. The goal was not proving I could commute. It was getting back to the room without turning one good climb into three bad ones.",
    "*",
]

CH75_SPOTTER = [
    "Hessa showed Jorren the part that mattered: one step below and slightly behind, hand at my belt only if I actually lost balance, never grab the crutch, never improvise.",
    "Jorren listened. Actually listened. Good.",
]

CH76_CLINIC = [
    "Nerin arrived with a satchel and used the new rail. Everyone used the rail. Show-off. He unwrapped the limb and confirmed what I could mostly see: swelling back toward baseline, incision intact, no new drainage, no heat, no spreading redness, margin still viable.",
    "Sera's instruction through him was simple. One controlled descent if I still felt this good after the rewrap. No Guild trip required. No repeated stairs because I had discovered stairs existed.",
    "“Spotter?”",
    "“Jorren if available. Keeper if she can follow instructions and control your belt. Hessa is working.”",
    "“Alden?”",
    "“No.”",
    "“Everyone hates Alden.”",
    "“No one hates Alden. We understand Alden.”",
    "Fair.",
    "If I tired before the landing, I sat on a step. If I could not stand again, I waited and got help. I was not being chased. Apparently this was an important structural feature of stairs.",
    "“What if phantom foot goes first?”",
    "“Don't follow it.”",
    "“Excellent medical science.”",
    "Rail. Crutch. Right foot. Down. The order still felt wrong because my body remembered a left foot that was no longer available for the job.",
    "*",
]

CH76_SPOTTER = [
    "The keeper volunteered. “I've moved sacks heavier than you.”",
    "“I am not a sack.”",
    "“You complain more.”",
    "Nerin had left the same short instructions: below and slightly behind, belt only if needed, do not grab the crutch, do not pull unless I actually lost balance.",
    "“Simple,” she said.",
    "“That is what Jorren said.”",
    "“Did he drop you?”",
    "“No.”",
    "“Then.”",
]


def transform_chapter_paragraphs(number: int, paragraphs: list[str]) -> list[str]:
    out = list(paragraphs)
    if number == 75:
        if any("OLD WOUND INVENTORY AND SEVEN STEP DRILL" in p for p in out):
            out = replace_range(out, "No job today. Sera looked at the wound.", "At the Guild desk, the clerk had a note for me.", ["Sera compressed the wound check and seven-step drill into the decision that mattered: one controlled home ascent later, with a spotter, then stay upstairs."])
        elif not any("The goal was not proving I could commute." in p for p in out):
            out = replace_range(out, "Another for warehouse night watch.", "At the Guild desk, the clerk had a note for me.", CH75_CLINIC)

        if any("OLD SPOTTER INSTRUCTION LOOP" in p for p in out):
            out = replace_range(out, "Hessa showed him. Not by making me climb.", "Ready? Hessa asked. No.", ["Hessa gave Jorren the spotter rules once. He listened."])
        elif not any("Hessa showed Jorren the part that mattered" in p for p in out):
            out = replace_range(out, "Hessa showed him. Not by making me climb.", "Ready?", CH75_SPOTTER)

    elif number == 76:
        if any("OLD WOUND INVENTORY AND SPOTTER OPTIONS" in p for p in out):
            out = replace_range(out, "Nerin arrived with a satchel", "Jorren could not come.", ["Nerin confirmed the wound was stable enough for one controlled descent and repeated the only useful rule: if I tired, sit and get help. I was not being chased."])
        elif not any("No repeated stairs because I had discovered stairs existed." in p for p in out):
            out = replace_range(out, "Nerin arrived with a satchel and used the new rail.", "Jorren could not come.", CH76_CLINIC)

        if any("OLD KEEPER SPOTTER INSTRUCTION LOOP" in p for p in out):
            out = replace_range(out, "The keeper volunteered.", "Fine. I stood at the top.", ["The keeper took the spotter position and repeated the rules once. Fine."])
        elif not any("Nerin had left the same short instructions" in p for p in out):
            out = replace_range(out, "The keeper volunteered.", "Fine. I stood at the top.", CH76_SPOTTER)
    else:
        raise ValueError(f"Unsupported chapter {number}")
    return out


def html_paragraphs(text: str) -> list[str]:
    match = ARTICLE_RE.search(text)
    if not match:
        raise ValueError("Missing prose article")
    return [plain_html(m.group(1)) for m in P_RE.finditer(match.group(2))]


def html_replace_ranges(text: str, number: int) -> str:
    match = ARTICLE_RE.search(text)
    if not match:
        raise ValueError(f"Chapter {number}: missing prose article")
    body = match.group(2)
    items = list(P_RE.finditer(body))
    plain = [plain_html(m.group(1)) for m in items]
    transformed = transform_chapter_paragraphs(number, plain)
    if transformed == plain:
        return text

    # None of the approved cut ranges contains illustration figures. Rebuild the
    # prose stream while preserving every figure by reattaching it to its nearest
    # surviving semantic cue.
    figures = re.findall(r"<figure\b.*?</figure>", body, flags=re.I | re.S)
    new_body = "".join(f"<p>{html.escape(p, quote=False).replace(chr(10), '<br/>')}</p>" for p in transformed)
    for figure in figures:
        alt_match = re.search(r'alt="([^"]+)"', figure)
        alt = html.unescape(alt_match.group(1)) if alt_match else ""
        if number == 75 and "stairs" in alt.lower():
            cue = "Top. I was upstairs."
        elif number == 76 and "stairs" in alt.lower():
            cue = "Ground floor. Kitchen."
        else:
            # Unknown art remains advisory and held. Preserve it at the end rather
            # than allowing an image anchor to dictate story structure.
            cue = ""
        if cue and cue in new_body:
            pos = new_body.find(cue)
            p_end = new_body.find("</p>", pos)
            new_body = new_body[:p_end + 4] + figure + new_body[p_end + 4:]
        else:
            new_body += figure
    return text[:match.start(2)] + new_body + text[match.end(2):]


def p_text(p: ET.Element) -> str:
    return norm("".join(t.text or "" for t in p.iter() if t.tag == f"{{{W_NS}}}t"))


def chapter_number_from_heading(text: str) -> int | None:
    upper = norm(text).upper()
    if not upper.startswith("CHAPTER "):
        return None
    tail = upper[len("CHAPTER "):]
    for words, number in (
        ("SEVENTY-SEVEN", 77), ("SEVENTY SEVEN", 77),
        ("SEVENTY-SIX", 76), ("SEVENTY SIX", 76),
        ("SEVENTY-FIVE", 75), ("SEVENTY FIVE", 75),
    ):
        if tail.startswith(words):
            return number
    return None


def _set_paragraph_text(p: ET.Element, text: str) -> None:
    runs = [r for r in p if r.tag == f"{{{W_NS}}}r"]
    run = runs[0] if runs else ET.SubElement(p, f"{{{W_NS}}}r")
    texts = [t for t in run if t.tag == f"{{{W_NS}}}t"]
    first = texts[0] if texts else ET.SubElement(run, f"{{{W_NS}}}t")
    first.text = text
    first.set(f"{{{XML_NS}}}space", "preserve")
    for extra in texts[1:]:
        run.remove(extra)
    for extra_run in runs[1:]:
        p.remove(extra_run)


def transform_docx(path: Path) -> tuple[bytes, dict[int, tuple[int, int]]]:
    with zipfile.ZipFile(path, "r") as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
        body = next(node for node in root.iter() if node.tag == f"{{{W_NS}}}body")
        children = list(body)
        heading_positions: dict[int, int] = {}
        for i, child in enumerate(children):
            if child.tag != f"{{{W_NS}}}p":
                continue
            n = chapter_number_from_heading(p_text(child))
            if n in {75, 76, 77} and n not in heading_positions:
                heading_positions[n] = i
        if set(heading_positions) != {75, 76, 77}:
            raise ValueError(f"DOCX chapter boundaries missing: {heading_positions}")

        stats: dict[int, tuple[int, int]] = {}
        # Work backwards so earlier chapter positions remain stable.
        for number in (76, 75):
            current_children = list(body)
            starts: dict[int, int] = {}
            for i, child in enumerate(current_children):
                if child.tag == f"{{{W_NS}}}p":
                    n = chapter_number_from_heading(p_text(child))
                    if n in {75, 76, 77} and n not in starts:
                        starts[n] = i
            start, end = starts[number], starts[number + 1]
            body_ps = [c for c in current_children[start + 1:end] if c.tag == f"{{{W_NS}}}p" and p_text(c)]
            before = [p_text(p) for p in body_ps]
            after = transform_chapter_paragraphs(number, before)
            stats[number] = (word_count(before), word_count(after))
            if before == after:
                continue

            template = copy.deepcopy(body_ps[0]) if body_ps else ET.Element(f"{{{W_NS}}}p")
            for p in body_ps:
                body.remove(p)
            insert_at = start + 1
            for text in after:
                p = copy.deepcopy(template)
                for child in list(p):
                    if child.tag != f"{{{W_NS}}}pPr":
                        p.remove(child)
                _set_paragraph_text(p, text)
                body.insert(insert_at, p)
                insert_at += 1

        new_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        tmp.close()
        tmp_path = Path(tmp.name)
        with zipfile.ZipFile(tmp_path, "w") as zout:
            for info in zin.infolist():
                data = new_xml if info.filename == "word/document.xml" else zin.read(info.filename)
                zout.writestr(info, data)
        data = tmp_path.read_bytes()
        tmp_path.unlink(missing_ok=True)
        return data, stats


def extract_docx_chapter(path: Path, number: int) -> list[str]:
    with zipfile.ZipFile(path, "r") as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
    body = next(node for node in root.iter() if node.tag == f"{{{W_NS}}}body")
    children = list(body)
    starts: dict[int, int] = {}
    for i, child in enumerate(children):
        if child.tag == f"{{{W_NS}}}p":
            n = chapter_number_from_heading(p_text(child))
            if n in {75, 76, 77} and n not in starts:
                starts[n] = i
    start, end = starts[number], starts[number + 1]
    return [p_text(c) for c in children[start + 1:end] if c.tag == f"{{{W_NS}}}p" and p_text(c)]


def verify(root: Path) -> None:
    docx = root / DOCX_REL
    protected = {
        75: ["The rail was finished before I was.", "Top. I was upstairs.", "My room. Same bed. Same washbasin."],
        76: ["The chamber pot had become personal.", "The phantom left foot was already on the first lower step.", "I can use the privy.", "The storage room no longer felt like the only place I could exist."],
    }
    removed = {
        75: ["How do you know knife drills?", "Hessa showed him. Not by making me climb."],
        76: ["What if I can't stand again?", "She tied her apron tighter. Nerin had left instructions."],
    }
    for number in (75, 76):
        source = "\n".join(extract_docx_chapter(docx, number))
        reader = "\n".join(html_paragraphs((root / HTML_PATHS[number]).read_text(encoding="utf-8")))
        for cue in protected[number]:
            if cue not in source or cue not in reader:
                raise AssertionError(f"Chapter {number}: protected cue missing from DOCX or reader: {cue}")
        for cue in removed[number]:
            if cue in source or cue in reader:
                raise AssertionError(f"Chapter {number}: redundant cue survived in DOCX or reader: {cue}")
    print("Chapters 75-76 protected milestones and removed repetition verified in DOCX and reader HTML")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    if args.verify:
        verify(root)
        return 0
    if not args.write:
        raise SystemExit("Use --write or --verify")

    stats: dict[str, dict[str, int]] = {}
    for number, rel in HTML_PATHS.items():
        path = root / rel
        before_text = path.read_text(encoding="utf-8")
        before_paras = html_paragraphs(before_text)
        after_text = html_replace_ranges(before_text, number)
        after_paras = html_paragraphs(after_text)
        stats[str(rel)] = {
            "before_words": word_count(before_paras),
            "after_words": word_count(after_paras),
            "delta_words": word_count(after_paras) - word_count(before_paras),
        }
        if after_text != before_text:
            path.write_text(after_text, encoding="utf-8")

    docx_path = root / DOCX_REL
    docx_bytes, _ = transform_docx(docx_path)
    if docx_bytes != docx_path.read_bytes():
        docx_path.write_bytes(docx_bytes)

    verify(root)

    manifest = {
        "schema_version": 1,
        "batch": "075-076",
        "status": "applied",
        "strength": "aggressive-on-repetition-preserve-distinct-independence-milestones",
        "source_authority": str(DOCX_REL),
        "stable_id_actions": {
            "plg-ch-000075": {"status": "active", "action": "tightened_return_to_room"},
            "plg-ch-000076": {"status": "active", "action": "tightened_return_to_ground_floor_world"},
        },
        "illustration_policy": "advisory hold; art does not protect redundant prose or chapter boundaries",
        "stats": stats,
        "protected": {
            "75": ["finished rail", "home fourteen-step ascent", "landing pivot", "return to own room"],
            "76": ["first controlled descent", "phantom-foot hazard", "step rest", "privy independence", "ground-floor spontaneity and mobility asymmetry"],
        },
    }
    if args.manifest:
        manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
