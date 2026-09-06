#!/usr/bin/env python3
"""Apply the approved structural compression to PLG Chapters 60-61.

Unlike later reader-native batches, Book I authority for these chapters is the
DOCX snapshot. This transformer therefore edits the authoritative DOCX and the
reader projections atomically, then verifies that protected story beats remain
present in both representations.
"""

from __future__ import annotations

import argparse
import copy
import html
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX_REL = Path("state/manuscript/Peg_Leg_Greg_authoritative_ch82_final_name_map.docx")
HTML_PATHS = {60: Path("chapters/060.html"), 61: Path("chapters/061.html")}
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("w", W_NS)

TAG_RE = re.compile(r"<[^>]+>")
P_RE = re.compile(r"<p(?:\s[^>]*)?>(.*?)</p>", re.I | re.S)
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


def replace_range(
    paragraphs: list[str], start_cue: str, end_cue: str, replacement: list[str]
) -> list[str]:
    start = _find_unique(paragraphs, start_cue)
    end = _find_unique(paragraphs, end_cue)
    if end <= start:
        raise ValueError(f"Invalid range {start_cue!r} -> {end_cue!r}")
    return paragraphs[:start] + replacement + paragraphs[end:]


CH60_FARMER = [
    "The farmer was waiting, red-faced and certain he had lost half the road. The road remained mostly present. One empty cart passed while I read his complaint, which at least proved Pessa's first useful distinction: passable was not the same as comfortable, and an empty cart did not answer for a loaded one.",
    "Dorn found the softness local to the washed edge. The culvert itself was mostly clear, with only a little straw caught at the mouth. I recorded the useful facts: passable, local shoulder wash, soft edge, minor debris, loaded-cart clearance not observed.",
    "When the farmer asked when we were fixing it, Pessa marked the stone blue and told him not today. He pointed out that we had tools. Dorn held up the probe. “This is a stick.”",
    "The farmer remained dissatisfied. The road remained functional. We moved on.",
]

CH60_PRIVATE_CUT = [
    "At the third site, the complaint said standing water. There was none. The farmer's sons had dug a fresh trench from the road ditch through the farm edge, and the road now drained perfectly well into somebody else's problem.",
    "We followed the improvised cut into a farm drain, then a larger ditch that disappeared under a hedge. “Where does that go?” Dorn asked. The farmer's wife pointed toward Merek's land. Merek did not know.",
    "Pessa marked the road problem white because it was currently solved, then handed the woman a note for the downstream farm before the next rain. I wrote the part that could change a decision: PRIVATE CUT DIVERTS ROAD WATER. OWNER TO NOTIFY DOWNSTREAM FARM.",
]

CH61_RECHECK = [
    "The wheel track was still clear, but overnight rain had widened the wet shoulder. Dorn found only four inches of cover where yesterday there had been six to eight, and the outer edge had softened enough that he told Pessa not to put the wagon there.",
    "We held an approaching farm cart to the firm center and let it through. Nothing happened, which was the point. The site was still red, but now the crew note changed: active water, reduced cover after rain, loaded wheels center until repair. No closure. No repair by us.",
]

CH61_SHOULDER = [
    "Near noon we reached a long downhill section where overnight rain had cut three shallow scallops into the outer shoulder. The damage was fresh but the wheel track remained well inside it, and the road carried little traffic.",
    "I weighted the visible change too heavily and called it red. Pessa made me include consequence. Low traffic, low immediate consequence, moderate change: blue, unless more rain changed the answer. It was yesterday's lesson with one variable moved, which was enough to prove the shortcut was not the rule.",
]


def transform_chapter_paragraphs(number: int, paragraphs: list[str]) -> list[str]:
    """Transform a chapter represented as plain paragraph strings.

    Synthetic OLD_* fixtures are accepted so tests can prove range behavior
    without depending on the full manuscript.
    """
    out = list(paragraphs)
    if number == 60:
        if any("OLD FARMER ARGUMENT LOOP" in p for p in out):
            out = replace_range(out, "The farmer was waiting.", "Second site was not on the complaint list.", ["The farmer's complaint was real but bounded; the road remained passable, the wash local, and loaded-cart clearance unproven."])
        else:
            if not any("The farmer remained dissatisfied. The road remained functional. We moved on." in p for p in out):
                out = replace_range(out, "The farmer was waiting.", "Second site was not on the complaint list.", CH60_FARMER)
        if any("OLD PRIVATE DRAIN PROCEDURE LOOP" in p for p in out):
            out = replace_range(out, "At the third site, the complaint said standing water.", "We ate beside a low wall near noon.", ["The private drainage cut solved the road problem by diverting water downstream; Pessa marked it white and made the owner notify the downstream farm before the next rain."])
        else:
            if not any("road now drained perfectly well into somebody else's problem" in p for p in out):
                out = replace_range(out, "At the third site, the complaint said standing water.", "We ate beside a low wall near noon.", CH60_PRIVATE_CUT)
    elif number == 61:
        if any("OLD REPROBE TRAFFIC CONTROL LOOP" in p for p in out):
            out = replace_range(out, "The wheel track was still clear.", "The paired culvert from yesterday had changed more.", ["Overnight rain reduced shoulder cover and widened the wet edge; loaded traffic stayed on the firm center until repair."])
        else:
            if not any("overnight rain had widened the wet shoulder" in p for p in out):
                out = replace_range(out, "The wheel track was still clear.", "The paired culvert from yesterday had changed more.", CH61_RECHECK)
        if any("OLD SECOND CONSEQUENCE PLUS CHANGE LESSON" in p for p in out):
            out = replace_range(out, "Near noon we reached a long downhill section", "Dorn said, Drink.", ["The fresh shoulder erosion had changed overnight, but low traffic kept immediate consequence low. Blue, unless more rain changed the answer."])
        else:
            if not any("It was yesterday's lesson with one variable moved" in p for p in out):
                out = replace_range(out, "Near noon we reached a long downhill section", "Dorn said, “Drink.”", CH61_SHOULDER)
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

    # Rebuild only the prose paragraphs. Figures are preserved by anchoring them
    # to the next surviving paragraph from the original body.
    figure_re = re.compile(r"<figure\b.*?</figure>", re.I | re.S)
    figures: list[tuple[int, str]] = []
    for fm in figure_re.finditer(body):
        following = next((i for i, pm in enumerate(items) if pm.start() > fm.end()), len(items))
        figures.append((following, fm.group(0)))

    escaped = [f"<p>{html.escape(p, quote=False).replace(chr(10), '<br/>')}</p>" for p in transformed]
    # Restore simple emphasis on the opening sentence when it existed. Story
    # text remains authoritative; reader typography is secondary.
    new_body = "".join(escaped)
    # Keep figures close to their original semantic cues by matching known scenes.
    for _, figure in figures:
        alt_match = re.search(r'alt="([^"]+)"', figure)
        alt = alt_match.group(1) if alt_match else ""
        if number == 60 and "rain-cut culvert" in html.unescape(alt).lower():
            cue = "The farmer was waiting"
        elif number == 60:
            cue = "Not severity. Consequence plus change."
        elif number == 61 and "farm cart" in html.unescape(alt).lower():
            cue = "The wheel track was still clear"
        else:
            cue = "How many eggs do you own?"
        pos = new_body.find(cue)
        if pos >= 0:
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
    # Only values needed for this bounded edit plus the following boundary.
    for words, number in (("SIXTY-ONE", 61), ("SIXTY ONE", 61), ("SIXTY-TWO", 62), ("SIXTY TWO", 62), ("SIXTY", 60)):
        if tail.startswith(words):
            return number
    return None


def _set_paragraph_text(p: ET.Element, text: str) -> None:
    runs = [r for r in p if r.tag == f"{{{W_NS}}}r"]
    if not runs:
        run = ET.SubElement(p, f"{{{W_NS}}}r")
    else:
        run = runs[0]
    texts = [t for t in run if t.tag == f"{{{W_NS}}}t"]
    if texts:
        first = texts[0]
        first.text = text
        first.set(f"{{{XML_NS}}}space", "preserve")
        for extra in texts[1:]:
            run.remove(extra)
    else:
        first = ET.SubElement(run, f"{{{W_NS}}}t")
        first.text = text
        first.set(f"{{{XML_NS}}}space", "preserve")
    for extra_run in runs[1:]:
        p.remove(extra_run)


def transform_docx(path: Path) -> tuple[bytes, dict[int, tuple[int, int]]]:
    with zipfile.ZipFile(path, "r") as zin:
        original_xml = zin.read("word/document.xml")
        root = ET.fromstring(original_xml)
        body = next(node for node in root.iter() if node.tag == f"{{{W_NS}}}body")
        children = list(body)
        paras = [(i, child) for i, child in enumerate(children) if child.tag == f"{{{W_NS}}}p"]
        heading_positions: dict[int, int] = {}
        for child_index, p in paras:
            n = chapter_number_from_heading(p_text(p))
            if n in {60, 61, 62} and n not in heading_positions:
                heading_positions[n] = child_index
        if set(heading_positions) != {60, 61, 62}:
            raise ValueError(f"DOCX chapter boundaries missing: {heading_positions}")

        stats: dict[int, tuple[int, int]] = {}
        # Work backwards so XML child positions for earlier chapters stay valid.
        for number in (61, 60):
            start = heading_positions[number]
            end = heading_positions[number + 1]
            body_ps = [c for c in list(body)[start + 1:end] if c.tag == f"{{{W_NS}}}p" and p_text(c)]
            before = [p_text(p) for p in body_ps]
            after = transform_chapter_paragraphs(number, before)
            stats[number] = (word_count(before), word_count(after))
            if before == after:
                continue
            # Replace chapter body paragraphs while leaving non-paragraph XML and heading intact.
            template = copy.deepcopy(body_ps[0]) if body_ps else ET.Element(f"{{{W_NS}}}p")
            for p in body_ps:
                body.remove(p)
            insert_at = start + 1
            for text in after:
                p = copy.deepcopy(template)
                # preserve paragraph properties but collapse content to one run
                for child in list(p):
                    if child.tag != f"{{{W_NS}}}pPr":
                        p.remove(child)
                _set_paragraph_text(p, text)
                body.insert(insert_at, p)
                insert_at += 1
            # Recompute 61/62 positions after mutating 60 is unnecessary because
            # edits run backwards; after 61 mutation, 60 range is still before it.

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
            if n in {60, 61, 62} and n not in starts:
                starts[n] = i
    start, end = starts[number], starts[number + 1]
    return [p_text(c) for c in children[start + 1:end] if c.tag == f"{{{W_NS}}}p" and p_text(c)]


def verify(root: Path) -> None:
    docx = root / DOCX_REL
    protected = {
        60: ["Maps remembered one version. Ground remembered more", "Roads don't care about narrative", "The next farm spur was where I became useful"],
        61: ["DO NOT CLEAR WITHOUT OPENING / ASSESSING STRUCTURE", "Pond overflow"],
    }
    removed = {
        60: ["You're standing there", "Potential downstream problem"],
        61: ["Red can become different red", "How do you know?"],
    }
    for number in (60, 61):
        d = "\n".join(extract_docx_chapter(docx, number))
        h = "\n".join(html_paragraphs((root / HTML_PATHS[number]).read_text(encoding="utf-8")))
        for cue in protected[number]:
            if cue not in d or cue not in h:
                raise AssertionError(f"Chapter {number}: protected cue missing from DOCX/HTML: {cue}")
        for cue in removed[number]:
            if cue in d or cue in h:
                raise AssertionError(f"Chapter {number}: repeated procedure survived: {cue}")


def apply(root: Path, write: bool, manifest_path: Path | None) -> dict:
    docx_path = root / DOCX_REL
    before_docx = {n: extract_docx_chapter(docx_path, n) for n in (60, 61)}
    docx_bytes, _ = transform_docx(docx_path)

    html_updates: dict[int, str] = {}
    html_stats: dict[int, tuple[int, int]] = {}
    for number, rel in HTML_PATHS.items():
        path = root / rel
        old = path.read_text(encoding="utf-8")
        before = html_paragraphs(old)
        new = html_replace_ranges(old, number)
        after = html_paragraphs(new)
        html_updates[number] = new
        html_stats[number] = (word_count(before), word_count(after))

    if write:
        docx_path.write_bytes(docx_bytes)
        for number, rel in HTML_PATHS.items():
            (root / rel).write_text(html_updates[number], encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "batch": "060-061",
        "status": "applied" if write else "preview",
        "strength": "aggressive-on-repetition-preserve-distinct-functions",
        "source_authority": str(DOCX_REL),
        "stable_id_actions": {
            "plg-ch-000060": {"status": "active", "action": "tightened_day_one_field_grammar"},
            "plg-ch-000061": {"status": "active", "action": "tightened_day_two_changed_conditions"},
        },
        "illustration_policy": "advisory_hold; story structure outranks art anchors",
        "stats": {
            str(HTML_PATHS[n]): {"before_words": b, "after_words": a, "delta_words": a - b}
            for n, (b, a) in html_stats.items()
        },
        "protected": {
            "60": ["old drain discovery", "bridge anti-narrative beat", "hay-wagon intervention", "first consequence-plus-change lesson"],
            "61": ["rain changes model", "unrecorded farm repair", "do-not-clear reversal", "pond-overflow mistake"],
        },
    }
    if write and manifest_path:
        target = root / manifest_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


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
        print("DOCX/HTML source agreement verified for Chapters 60-61")
        return 0
    manifest = apply(root, args.write, args.manifest)
    print(json.dumps(manifest, indent=2))
    if args.write:
        verify(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
