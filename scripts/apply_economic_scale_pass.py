#!/usr/bin/env python3
"""Repair the bounded Chapter 471-489 economic continuity seam.

The pass is intentionally assertion-heavy. Every edit is scoped to one authoritative
checkpoint and must match exactly once. Reader prose is refreshed only when the
existing <article class="prose"> exactly matches the unedited checkpoint.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "state" / "manuscript"
CHAPTER_DIR = ROOT / "chapters"


def source_path(number: int) -> Path:
    return SOURCE_DIR / f"Peg_Leg_Greg_Chapter_{number}_EXACT_WIP.md"


def paragraphs(body: str) -> list[str]:
    output: list[str] = []
    for block in re.split(r"\n\s*\n", body):
        text = " ".join(line.strip() for line in block.splitlines()).strip()
        if text and set(text) != {"-"}:
            output.append(text)
    return output


def article_from_source(document: str, number: int) -> str:
    match = re.match(
        rf"^# CHAPTER {number}\s+^## [^\n]+\s+(?P<body>.*)\Z",
        document,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not parse authoritative checkpoint for Chapter {number}")
    prose = "".join(
        f"<p>{html.escape(p, quote=False)}</p>" for p in paragraphs(match.group("body"))
    )
    return prose


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one literal match, found {count}: {old!r}")
    return text.replace(old, new, 1)


PATCHES: dict[int, list[tuple[str, str]]] = {
    471: [
        ("\"Why five?\"", "\"Why two silver?\""),
        ("Being wrong cost somebody more than five copper.", "Being wrong cost somebody more than two silver."),
        ("Five copper and a second rung.", "Two silver and a second rung."),
    ],
    473: [
        ("Instead I arrived with sixteen.", "Instead I arrived with fifteen."),
        ("Illegal choice improved my purse by six copper.", "Illegal choice improved my purse by five copper."),
    ],
    474: [
        ("No. I currently have sixteen copper.", "No. I currently have fourteen copper."),
        ("Sixteen to fifteen. Still five above floor.", "Fourteen to thirteen. Still three above floor."),
        ("1S OR 2S INTRODUCTION CONDITION", "3C OR 5C INTRODUCTION CONDITION"),
        ("Fifteen to fourteen. Four above floor.", "Thirteen to twelve. Two above floor."),
        ("Two-silver commission pending.", "Five-copper commission pending."),
        ("Cash fourteen. Potential seventeen.", "Cash twelve. Potential seventeen."),
    ],
    475: [
        ("possible two silver commission", "possible five copper commission"),
        ("Eighteen copper. Twenty-three Vale. Five commission still pending. Ten-copper floor.", "Twelve copper and thirteen silver. Twenty-three Vale. Five copper commission still pending. Ten-copper floor."),
        ("14c -> 18c", "8s + 12c -> 13s + 12c"),
        ("Eighteen copper in purse. Five more maybe beyond the road.", "Twelve copper and thirteen silver in purse. Five copper more maybe beyond the road."),
    ],
    476: [
        ("possible two silver road commission", "possible five copper road commission"),
        ("Eighteen copper sounded better than it was if ten had a job. Eight was my actual flexible copper.", "Thirteen silver sounded better than it was if five had a job. Eight was my actual flexible silver."),
        ("maybe that five coming from the road", "maybe that five copper coming from the road"),
        ("Eighteen copper. Twenty-three Vale. Five pending. Same as morning.", "Twelve copper and thirteen silver. Twenty-three Vale. Five copper pending. Same as morning."),
    ],
    477: [
        ("Eighteen copper.", "Twelve copper and thirteen silver."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Eight flexible copper.", "Eight flexible silver."),
        ("I had thirteen copper.", "I had seven copper and thirteen silver."),
        ("Thirteen became eighteen again.", "Seven became twelve again. The thirteen silver stayed untouched."),
        ("18c start", "12c + 13s start"),
        ("18c end", "12c + 13s end"),
        ("10c floor", "5s floor"),
    ],
    478: [
        ("Eighteen copper.", "Twelve copper and thirteen silver."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Eight flexible copper.", "Eight flexible silver."),
        ("Eighteen stayed in purse", "Twelve copper and thirteen silver stayed in purse"),
    ],
    479: [
        ("Eighteen copper.", "Twelve copper and thirteen silver."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Eight flexible copper.", "Eight flexible silver."),
        ("Eighteen became twelve.", "Twelve became six. The thirteen silver stayed untouched."),
        ("Cash twelve after fare. Vale twenty-three. Bits unspecified. Ten floor. Two flexible.", "Cash six copper and thirteen silver after fare. Vale twenty-three. Bits unspecified. Five-silver floor. Eight silver flexible."),
    ],
    480: [
        ("Twelve copper after fare.", "Six copper and thirteen silver after fare."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Two flexible copper.", "Eight flexible silver."),
    ],
    481: [
        ("Twelve copper.", "Six copper and thirteen silver."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Two flexible copper.", "Eight flexible silver."),
        ("Twelve became fifteen.", "Six became nine. The thirteen silver stayed untouched."),
        ("Fifteen copper.", "Nine copper and thirteen silver."),
    ],
    482: [
        ("Fifteen copper.", "Nine copper and thirteen silver."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Five flexible copper.", "Eight flexible silver."),
    ],
    483: [
        ("Fifteen copper.", "Nine copper and thirteen silver."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Five flexible copper.", "Eight flexible silver."),
    ],
    484: [
        ("Eighteen copper.", "Nine copper and fifteen silver."),
        ("Ten-copper floor.", "Five-silver operating floor."),
        ("Eight deployable copper.", "Ten deployable silver."),
        ("Seller got three copper.", "Seller got six silver."),
        ("\"Three copper.\"", "\"Two silver.\""),
        ("One-silver-two-copper transaction.", "Eight-silver transaction."),
        ("Three copper earned.", "Two silver earned."),
    ],
    486: [
        ("Ten copper. If paid.", "Twelve silver. If paid."),
        ("Twenty-two plus ten. Thirty-two.", "Twenty-one plus twelve. Thirty-three."),
        ("I put the copper away.", "I put the silver away."),
        ("reference mattered almost as much as copper", "reference mattered almost as much as silver"),
    ],
    488: [
        ("Twenty copper lasted through breakfast.", "Fifteen silver and nine copper lasted through breakfast."),
        ("Less impressive than thirty-two.", "Less than before Vale."),
        ("More useful than nine.", "More useful than nine copper."),
        ("Vale eleven.", "Vale still open."),
        ("Cash twenty-one.", "Cash fifteen silver and ten copper."),
        ("paid Vale twelve yesterday", "paid Vale eighteen silver yesterday"),
        ("Twenty-one copper", "Fifteen silver and ten copper"),
    ],
    489: [
        ("Twenty-one copper.", "Fifteen silver and ten copper."),
        ("Vale eleven.", "Vale still open."),
    ],
}


def main() -> None:
    changed: list[str] = []
    for number, patches in PATCHES.items():
        src = source_path(number)
        original = src.read_text(encoding="utf-8")
        old_article = article_from_source(original, number)

        page_path = CHAPTER_DIR / f"{number:03d}.html"
        page = page_path.read_text(encoding="utf-8")
        article_match = re.search(r'<article\s+class="prose"[^>]*>(.*?)</article>', page, re.DOTALL | re.IGNORECASE)
        if not article_match:
            raise SystemExit(f"Chapter {number}: reader page missing prose article")
        if article_match.group(1) != old_article:
            raise SystemExit(f"Chapter {number}: reader prose has diverged from authoritative checkpoint; refusing overwrite")

        updated = original
        for old, new in patches:
            updated = replace_once(updated, old, new, label=f"Chapter {number}")
        src.write_text(updated, encoding="utf-8")
        changed.append(str(src.relative_to(ROOT)))

        new_article = article_from_source(updated, number)
        page = page[: article_match.start(1)] + new_article + page[article_match.end(1) :]
        page_path.write_text(page, encoding="utf-8")
        changed.append(str(page_path.relative_to(ROOT)))

    print("Economic continuity repair applied:")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
