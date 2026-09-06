#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import html
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "state/editorial/performance-lab/NOVELIZATION_LIVE_REPORT.md"
ARTICLE_RE = re.compile(r'(<article\s+class="prose"[^>]*>)(.*?)(</article>)', re.S | re.I)
P_RE = re.compile(r'<p\b[^>]*>.*?</p>', re.S | re.I)
TAG_RE = re.compile(r'<[^>]+>')

TARGET_PATHS = (
    "chapters/007.html",
    "chapters/013.html",
    "chapters/018.html",
)
SOURCE_WINS = (2, 16)


@dataclass(frozen=True)
class Patch:
    patch_id: str
    path: str
    start: str
    end: str
    replacement: tuple[str, ...]
    rationale: str


def _plain(paragraph_html: str) -> str:
    text = html.unescape(TAG_RE.sub("", paragraph_html)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def _render_paragraph(text: str) -> str:
    if "—" in text:
        raise AssertionError("candidate paragraph contains an em dash")
    return f"<p>{html.escape(text, quote=False)}</p>"


def replace_paragraph_span(
    page: str,
    start: str,
    end: str,
    replacement: tuple[str, ...],
) -> str:
    article = ARTICLE_RE.search(page)
    if not article:
        raise AssertionError("missing article.prose")
    body = article.group(2)
    paragraphs = list(P_RE.finditer(body))
    plain = [_plain(match.group(0)) for match in paragraphs]

    start_norm = re.sub(r"\s+", " ", start).strip()
    end_norm = re.sub(r"\s+", " ", end).strip()
    starts = [idx for idx, value in enumerate(plain) if value == start_norm]
    if len(starts) != 1:
        raise AssertionError(f"start boundary matched {len(starts)} times: {start!r}")
    start_idx = starts[0]
    ends = [idx for idx, value in enumerate(plain) if idx >= start_idx and value == end_norm]
    if len(ends) != 1:
        raise AssertionError(f"end boundary matched {len(ends)} times after start: {end!r}")
    end_idx = ends[0]

    rendered = "".join(_render_paragraph(text) for text in replacement)
    body = body[: paragraphs[start_idx].start()] + rendered + body[paragraphs[end_idx].end() :]
    return page[: article.start(2)] + body + page[article.end(2) :]


PATCHES = (
    Patch(
        "007-value-shift",
        "chapters/007.html",
        '"Trash," he said.',
        "Antonius did not hand it over. Of course he didn't.",
        (
            '"Trash," he said.',
            '"No."',
            'He nudged the box with two fingers. "Bent precision scrap. Failed artificer. Nobody wanted it. Toss it."',
            "He kept moving toward the discard pile.",
            'I looked at the box. Then at Antonius. Then at the box again. For one beautiful second, the correct financial decision was obvious. Say nothing. Put it aside. Ask later whether I could have the trash. Free was an excellent price. I should have done that. Instead I said, "That is potentially extremely valuable."',
            "Antonius stopped. Fuck. He came back and picked up the gray frame himself.",
            "I turned one of the stepped plates toward the light. Three teeth. Where had I seen it? Think. Not enough information yet. But the workmanship was wrong for scrap. Tiny grooves. Matched steps. Reference surfaces rather than moving parts. Precision. Old precision.",
            '"Three silver," Antonius said.',
            '"Done," I said immediately.',
            "Antonius did not hand it over. Of course he didn't.",
        ),
        "Keep Antonius in cleanup mode until Greg's value claim earns a physical attention shift; preserve Greg's premature disclosure and the original three-silver opening price.",
    ),
    Patch(
        "007-valuation-exit",
        "chapters/007.html",
        "Antonius looked at the frame. Then at me.",
        '"End of week."',
        (
            "Antonius looked at the frame instead of at me.",
            '"And you are the right buyer?"',
            '"No."',
            '"Then tell me why it is worth anything."',
            'I pointed at the nested plates. "I think this is a master calibration gauge. Early mana-regulation work. You don\'t cast with it. You don\'t put it in a machine. It sets tolerances on the precision tools that make other fittings. To almost everyone in Carrow, it is a little gray box of useless metal. To the handful of artificers trying to reproduce this standard without rebuilding the reference from scratch? Forty gold is conservative."',
            '"Think?"',
            '"Arlo might be able to identify it. Maybe authenticate it. I recognize the standard, not the condition."',
            "That was the answer I should have led with. After buying it.",
            '"Who buys it?" Antonius asked.',
            "I hesitated. That mattered. I could remember the standard. I could remember the kind of people who cared. I could not yet name the buyer.",
            '"I can\'t name one yet."',
            "Antonius set the frame on the keep shelf, wrote my name on a scrap, and tucked it beneath the box.",
            '"Five silver. End of week."',
            '"You said three."',
            '"Before forty gold."',
            '"Four."',
            "Antonius picked up the broom.",
            '"Five."',
            "The negotiation was over because he had physically returned to cleaning. Offensive.",
            '"Fine. Five."',
        ),
        "Let buyer/use/price and physical ownership terminate the negotiation instead of another shared dry-comeback ladder; preserve five silver and end-of-week terms.",
    ),
    Patch(
        "013-process-ownership",
        "chapters/013.html",
        '"Fuck."',
        "He laughed despite himself.",
        (
            '"Fuck."',
            '"Yes."',
            '"Again."',
            '"Six runs answered this test."',
            '"Then change the order. Warm them first. Cold after. Change the input."',
            "Every answer had opened three more doors and apparently I intended to kick all of them at once.",
            "Arlo lifted the testing frame off the bench and put it on the shelf. I experienced actual pain.",
            '"Those are other tests. I spent two days answering this one."',
            "I stared at the six regulators.",
            '"What changed?"',
            "Arlo slid the notebook closer to himself.",
            "I looked from the notebook to the six regulators, trying to inventory clay, firing time, copper thickness, etch depth, cooling, assembly sequence, every reference piece he might have used. The whole workshop wanted to become one answer.",
            '"You can ask about the result. The process changes are mine until I decide otherwise," Arlo said.',
            "I closed my mouth. Fair. Annoying. Fair. I had brought him the Tere set. I did not own what he learned from it.",
            "Arlo took a cracked regulator from beneath the bench. The copper winding had darkened.",
            '"First I changed the clay. Then the winding. Then the firing. Then the etch."',
            "He set the ruined regulator between us.",
            '"Then I had six worse regulators and no idea what mattered."',
            '"So you stopped changing the object."',
            '"Eventually."',
            "Arlo pointed to the ugly wooden fixture on the shelf.",
            '"Same regulator. Twenty measurements."',
            "He opened the notebook to a page of readings and turned that page toward me without surrendering the rest of the notes.",
            "I read the numbers. Then reread them. The spread had dropped by more than half. Not because the regulator improved. Because the measurement did.",
            '"That dropped by more than half."',
            '"I stopped holding the input lead by hand."',
            '"You separated measurement error from object variation."',
            "Arlo tapped one finger against the wooden fixture.",
            '"I stopped holding the wire."',
            "His version was cheaper and, annoyingly, harder to turn into a lecture.",
            '"Then the regulators still spread?"',
            '"Yes. So I changed one thing. Winding tension."',
            "Arlo pointed at another object beside the mandrel. A stick. A spool. A hanging weight.",
            "The copper wire ran from the spool, over a small peg, beneath the weight, then toward the winding mandrel. Constant tension. Crude. Good. Very good.",
            '"You built a tensioner."',
            '"I hung a weight on a string."',
            '"That is what a tensioner is if you are poor."',
            "Arlo laughed once despite himself, then reached for the next regulator.",
        ),
        "Replace the refusal/counter ladder with fixture, notebook, failed regulator, readings, and tensioner behavior while preserving Arlo's authorship and Greg's systems-minded interiority.",
    ),
    Patch(
        "018-bean-instruction",
        "chapters/018.html",
        "Hessa took one bean and placed it on the table between us.",
        "I hated teachers.",
        (
            "Hessa took one bean and placed it on the table between us.",
            '"Move it."',
            "I looked at her.",
            '"With Barrier?"',
            "Hessa looked at me until I answered the unnecessary question myself.",
            "I hated teachers.",
        ),
        "Let Hessa establish the exercise through placement and waiting instead of a mini counter-exchange.",
    ),
    Patch(
        "018-fresh-bean",
        "chapters/018.html",
        "Hessa watched it fall.",
        '"Then we can afford your mistakes."',
        (
            "Hessa watched it fall, reached into the bowl, and put a fresh bean on the same spot before I could bend to retrieve the first.",
            '"Again."',
        ),
        "Realize bounded concern and test control by supplying a fresh trial rather than verbally explaining the lesson.",
    ),
    Patch(
        "018-placement",
        "chapters/018.html",
        "Hessa saw my face.",
        "She slid another bean onto the table.",
        (
            "Hessa's eyes moved to my face.",
            '"What changed?"',
            '"Placement. I intersected the target."',
            "The cup had been larger. That mattered more than I wanted it to.",
            "Hessa slid another bean onto the table.",
        ),
        "Keep pain observable to Hessa but let Greg own the inference; remove the shared size-joke ladder.",
    ),
    Patch(
        "018-anchor-wait",
        "chapters/018.html",
        "I stopped.",
        '"What about it?"',
        (
            "I stopped.",
            "Hessa stopped reaching for beans.",
            '"The anchor," I said.',
            "Hessa waited.",
        ),
        "When Greg notices the anchor problem, Hessa withholds the next attempt and lets his cognition do the work.",
    ),
    Patch(
        "018-no-dry-correction",
        "chapters/018.html",
        '"I think I\'m doing too much," I said.',
        "I ignored her.",
        (
            '"I think I\'m doing too much," I said.',
        ),
        "Preserve Greg's realization and remove two polished corrective buttons that the procedure has already earned.",
    ),
    Patch(
        "018-bean-redirect",
        "chapters/018.html",
        '"What does Barrier need to be Barrier?"',
        '"What does this exercise need?"',
        (
            '"What does Barrier need to be Barrier?"',
            "Hessa tapped the bean once with a fingertip.",
            '"What does this exercise need?"',
        ),
        "Use the bean itself to reduce Greg's oversized question instead of explanatory correction.",
    ),
    Patch(
        "018-one-finger",
        "chapters/018.html",
        '"It needs the bean to move."',
        '"One finger."',
        (
            '"It needs the bean to move."',
            'I looked at Hessa. "How far?"',
            '"One finger."',
        ),
        "Keep Greg responsible for asking the missing constraint once he understands the exercise.",
    ),
    Patch(
        "018-covered-bowl",
        "chapters/018.html",
        "Hessa reached across the table and covered the bowl with the cloth.",
        '"Not for you."',
        (
            "Hessa reached across the table and covered the bowl with the cloth.",
            '"I\'ve barely started."',
            '"Nineteen casts."',
            "I counted backward. I lost track at twelve. That was concerning.",
            '"I feel fine."',
            '"You feel interested."',
            "Hessa left the bowl covered.",
        ),
        "Make the covered bowl, attempt count, and continued refusal of access carry Hessa's concern without another perfect rebuttal chain.",
    ),
)


def _render_report(applied: list[str]) -> str:
    return """# PERFORMANCE Novelization Live Experiment Report

## Authority

- Source/current-main authority: `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`
- PERFORMANCE lab authority: `experiment/performance-lab` at `48bf312924c5d1d6836587e9cb3e21f3944a4d43`
- Scope: five tested scenes only.

## Scene decisions

| Scene | Novelization decision | Reason |
| --- | --- | --- |
| Canon 002 / displayed Ch 2, Antonius loan | SOURCE RETAINED | The source already realizes suspicion, transaction ownership, and Greg's younger persona shift. Novelization did not earn a clear overall improvement. |
| Canon 007 / displayed Ch 5, Antonius storeroom | CHANGE | The behavioral shift from cleanup to valuation survives prose while broom, shelf, name scrap, buyer/use questions, and Greg's premature disclosure replace a shared dry-comeback ladder. |
| Canon 013 / displayed Ch 9, Arlo workshop | CHANGE | Fixture, notebook, ruined regulator, readings, and tensioner carry Arlo's process ownership more distinctly than the source refusal ladder. |
| Canon 016 / displayed Ch 12, Jorren + Alden + Greg | SOURCE RETAINED | The source already has the strongest topology: teach, test, succeed, overapply, physical correction. The candidate mainly restaged an already healthy scene. |
| Canon 018 / displayed Ch 14, Hessa beans | CHANGE | Fresh beans, waiting, the bean tap, attempt counting, and the covered bowl carry Hessa's procedure/concern while Greg retains the technical and comic interiority. |

## Literary validation

- Dramatic truth: PASS. No scene outcome, debt term, magic result, object, timeline fact, relationship state, or knowledge ceiling is changed.
- Speaker ownership: PASS by construction. Dialogue remains in its speaker's paragraph or is paired only with that speaker's action.
- Action ownership: PASS by construction. Antonius owns broom/shelf/valuation behavior, Arlo owns workshop objects/process, Hessa owns exercise access/control, Greg owns Greg actions and interpretation.
- POV/interiority: PASS. Only Greg receives narrated internal cognition.
- Character performance: PASS. The novelization preserves the tested behavior rather than translating it back into explanatory banter.
- Greg narrator voice: PASS. Source interior beats are retained whenever they outperform script compression; new Greg lines remain analytical, self-aware, and comic without shifting him into neutral stage prose.
- Mundane/domain texture: PASS. Storeroom sorting/ownership, workshop apparatus/readings, and beans/procedure remain concrete.
- Explanatory smoothing: PASS. The three changed scenes use physical behavior as an answer where PERFORMANCE earned that change.
- Source-wins rule: PASS. Canon 002 and 016 remain byte-for-byte untouched by this experiment.

## Exact patch IDs applied

""" + "\n".join(f"- `{patch_id}`" for patch_id in applied) + """

## Publish boundary

This report authorizes only these validated candidate changes. It does not authorize a Chapters 1-20 pass, manuscript-wide PERFORMANCE, or further novelization rollout.
"""


def apply(write: bool = False) -> tuple[list[str], list[str]]:
    by_path: dict[str, list[Patch]] = {}
    for patch in PATCHES:
        by_path.setdefault(patch.path, []).append(patch)

    applied: list[str] = []
    changed_paths: list[str] = []
    for relative in TARGET_PATHS:
        path = ROOT / relative
        original = path.read_text(encoding="utf-8")
        updated = original
        for patch in by_path.get(relative, []):
            updated = replace_paragraph_span(updated, patch.start, patch.end, patch.replacement)
            applied.append(patch.patch_id)
        if updated == original:
            raise AssertionError(f"expected candidate prose change missing: {relative}")
        article = ARTICLE_RE.search(updated)
        if not article:
            raise AssertionError(f"missing article.prose after patch: {relative}")
        if "—" in _plain(article.group(2)):
            raise AssertionError(f"em dash present in authoritative prose after patch: {relative}")
        changed_paths.append(relative)
        if write:
            path.write_text(updated, encoding="utf-8")

    if write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(_render_report(applied), encoding="utf-8")
    return applied, changed_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply the bounded five-scene PERFORMANCE novelization experiment.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    applied, changed = apply(write=args.write)
    print(f"performance novelization: patches={len(applied)} changed={','.join(changed)} write={args.write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
