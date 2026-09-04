#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"


def repair_compound_ranges(text: str) -> str:
    # The initial migration shifted prefixed chapter refs but could not see the
    # unprefixed second endpoint in forms like Ch297–300.
    def short_range(m: re.Match[str]) -> str:
        prefix, first, sep, second = m.groups()
        n2 = int(second)
        if 221 <= n2 <= 301:
            n2 += 3
        return f"{prefix}{first}{sep}{n2}"

    text = re.sub(r"\b((?:Ch|Chapter)\s*)(\d{3})([–-])(\d{3})\b", short_range, text)

    # 'Chapters N–M' was not matched by the singular/prefixed migration at all.
    def plural_range(m: re.Match[str]) -> str:
        prefix, first, sep, second = m.groups()
        n1, n2 = int(first), int(second)
        if 221 <= n1 <= 301:
            n1 += 3
        if 221 <= n2 <= 301:
            n2 += 3
        return f"{prefix}{n1}{sep}{n2}"

    text = re.sub(r"\b(Chapters\s+)(\d{3})([–-])(\d{3})\b", plural_range, text)
    return text


def cleanup_state_ranges() -> None:
    for path in STATE.rglob("*.md"):
        if path.name in {"MANUSCRIPT_CHAPTER_INDEX.md", "BREN_220ABC_CANON.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        new = repair_compound_ranges(text)
        if new != text:
            path.write_text(new, encoding="utf-8")


def patch_manuscript_state() -> None:
    path = STATE / "MANUSCRIPT_STATE.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"- Current exact story endpoint: Chapter \d+ — \*\*[^*]+\*\*\.",
        "- Current exact story endpoint: Chapter 304 — **THE FALSE DOOR**.",
        text,
        count=1,
    )
    text = re.sub(
        r"- Permanent running manuscript is physically materialized through Chapter \d+\.\n- Exact Chapters [^\n]+",
        "- Permanent running manuscript is continuous through Chapter 234, with Chapter 251 also materialized.\n- Exact checkpoint files cover Chapters 235–250 and 252–304; exact prose outranks summaries/state. Synchronization debt remains. Never reconstruct exact prose from summaries.",
        text,
        count=1,
    )
    marker = "- Chapter 303 is explicitly not a structural milestone. Structural boundaries continue to follow actual story movement only."
    if marker in text and "Ch304 THE FALSE DOOR is exact manuscript authority" not in text:
        text = text.replace(
            marker,
            marker + "\n- Ch304 THE FALSE DOOR is exact manuscript authority and supersedes the older Chapter 304 trailhead. No Chapter 305 trailhead is currently materialized.",
            1,
        )
    text = text.replace("executable Chapter 304 trailhead", "no longer-current Chapter 304 trailhead")
    path.write_text(text, encoding="utf-8")


def patch_open_threads() -> None:
    path = STATE / "OPEN_THREADS.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"- Current exact story endpoint: Chapter \d+ — \*\*[^*]+\*\*\.",
        "- Current exact story endpoint: Chapter 304 — **THE FALSE DOOR**.",
        text,
        count=1,
    )
    text = re.sub(
        r"- Exact Chapters [^\n]+\n- Permanent running manuscript [^\n]+",
        "- Permanent running manuscript is continuous through Chapter 234, with Chapter 251 also materialized.\n- Exact checkpoint files cover Chapters 235–250 and 252–304; exact prose outranks summaries/state. Synchronization debt remains.",
        text,
        count=1,
    )
    text = re.sub(
        r"- Canonical inserted Chapters \*\*220A[^\n]+\n",
        "- Canonical repair sequence is Chapters **221 — THE SHORTAGE**, **222 — THE OLD MAN**, and **223 — THE ROUTE**, between Chapters 220 and 224.\n",
        text,
        count=1,
    )
    text = text.replace("See `MANUSCRIPT_STATE.md` for executable Chapter 304 trailhead.", "Chapter 304 is exact authority. No Chapter 305 trailhead is currently materialized.")
    text = text.replace("220A THE SHORTAGE", "221 THE SHORTAGE")
    text = text.replace("220B THE OLD MAN", "222 THE OLD MAN")
    text = text.replace("220C THE ROUTE", "223 THE ROUTE")
    text = text.replace("Ch220A", "Ch221").replace("Ch220B", "Ch222").replace("Ch220C", "Ch223")
    text = text.replace("220A–C", "221–223").replace("220A-C", "221-223")
    text = text.replace("`state/BREN_220ABC_CANON.md`", "`state/BREN_221_223_CANON.md`")
    path.write_text(text, encoding="utf-8")


def rewrite_bren_state() -> None:
    old = STATE / "BREN_220ABC_CANON.md"
    new = STATE / "BREN_221_223_CANON.md"
    content = """# BREN 221–223 CANON STATE

## Status

Chapters **221 — THE SHORTAGE**, **222 — THE OLD MAN**, and **223 — THE ROUTE** are canonical chapters between Chapter 220 and Chapter 224.

Their exact prose is integrated into `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`.

## Local Bren / theatre pressure outcome

Chapter 220 establishes that Olin has been questioned about theatre oil deliveries and that Rinna begins sharing the questions across her network.

Chapter 221 escalates the pressure into a material cost. Olin stops sending his delivery boy after two men watch and question the route. The theatre still gets oil, but Nessa and Jori must collect it themselves, costing work time. No attacker identity beyond the existing evidence ceiling is established.

Chapter 222 fulfills Bren's prior `Next time won't be one` threat. Bren returns with two men and demands five copper. Rinna remains the theatre's authority. Greg uses deliberate performance, stage geometry, the already-established coat-shadow logic, prepared blue-glass theatrical magic, silence, and genuine old-life threat-reading to make the situation difficult to price. Greg does **not** cast a new personal illusion spell and gains no new independent magic capability. Bren recognizes that some effects are theatre, but cannot determine which other pieces of Greg's apparent knowledge or capability are staged. Bren's group withdraws. This is a bluff success through uncertainty, not domination.

The confrontation also establishes a clearer on-page memory pattern: Greg can retrieve a deeply practiced procedural lesson from his first life while failing to retrieve the name attached to the autobiographical memory. This supports the durable rule that repeated-use, embodied, and operational knowledge tends to survive more reliably than incidental identifiers or directly searchable personal detail. Personal and emotional memory are not erased.

Chapter 223 makes the local resolution legible. Rinna's informal network shares questions rather than isolated answers, businesses become harder to pressure privately, and Olin's ordinary delivery route eventually resumes. Greg's bluff wins space once; network friction makes the theatre a worse extortion target over time.

## What is resolved

The **local Bren extortion pressure against the theatre and its immediate supplier network** is resolved/dormant after Chapter 223 unless independently reactivated by later story causality.

Do not automatically bring Bren back simply because he remains alive or because the broader criminal ecology is unresolved.

## What remains unresolved

Do not invent or infer without later evidence:

- Bren's surname;
- Bren's employer or boss;
- a gang or organization name;
- the full scale of the extortion network;
- whether every prior watcher/questioner worked for Bren;
- whether Bren permanently leaves Carrow;
- any Vale/Bren connection.

The local theatre problem can be resolved without explaining the entire criminal ecology of Carrow.

## Continuity into Chapter 224

The repair chapters do not add supervised mana draws, shaping attempts, or external-effect attempts.

They do not alter Hessa's restrictions.

Prepared theatrical magical effects remain distinct from Greg's personal spellcasting.

Therefore Chapter 224's Hessa note, supervised far-distance work, and existing magic counts remain valid after Chapter 223.

Chapter 224 may begin after the ordinary delivery has resumed without implying that Bren's wider identity or organization has been solved.

## Future editorial rule

When later structural or dialogue passes reach this region, preserve the functional progression:

**220 inquiry/network awareness → 221 material cost → 222 deliberate bluff/withdrawal → 223 systemic friction and ordinary route restoration → 224 return to other life/work/magic.**

Do not compress the progression back into an unresolved fadeout. Do not inflate it into a combat climax.
"""
    new.write_text(content, encoding="utf-8")
    if old.exists():
        old.unlink()
    for path in STATE.rglob("*.md"):
        if path == new:
            continue
        text = path.read_text(encoding="utf-8")
        newer = text.replace("BREN_220ABC_CANON.md", "BREN_221_223_CANON.md")
        if newer != text:
            path.write_text(newer, encoding="utf-8")


def verify() -> None:
    ms = (STATE / "MANUSCRIPT_STATE.md").read_text(encoding="utf-8")
    ot = (STATE / "OPEN_THREADS.md").read_text(encoding="utf-8")
    assert "Chapter 304 — **THE FALSE DOOR**" in ms
    assert "Chapter 304 — **THE FALSE DOOR**" in ot
    assert "No Chapter 305 trailhead is currently materialized" in ms
    assert "No Chapter 305 trailhead is currently materialized" in ot
    assert not (STATE / "BREN_220ABC_CANON.md").exists()
    assert (STATE / "BREN_221_223_CANON.md").exists()
    assert "220A" not in ot and "220B" not in ot and "220C" not in ot
    # Detect the characteristic malformed post-shift ranges, where the second
    # endpoint is lower only because it was left in the old namespace.
    for path in STATE.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"\bCh(\d{3})[–-](\d{3})\b", text):
            if int(m.group(1)) > int(m.group(2)):
                raise AssertionError(f"descending chapter range in {path}: {m.group(0)}")


def main() -> None:
    cleanup_state_ranges()
    patch_manuscript_state()
    patch_open_threads()
    rewrite_bren_state()
    verify()
    print("post-renumber state cleanup verified")


if __name__ == "__main__":
    main()
