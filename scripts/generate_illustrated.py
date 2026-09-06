#!/usr/bin/env python3
"""Generate Illustrated Reader chapter shells from exact manuscript authority."""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_light import Chapter, load_all_sources, selected_numbers
from showcase import ShowcaseMap, build_showcase_map, load_showcase_manifest
from scripts.illustration_state import load_registry

CHAPTERS_DIR = Path("chapters")
ART_ROOT = Path("visual/chapter_art")
REGISTRY_PATH = Path("state/visual/ILLUSTRATION_REGISTRY.json")
SHOWCASE_MANIFEST = Path("publishing/showcase_chapters.json")
ART_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".svg"}


def chapter_art(number: int) -> list[Path]:
    directory = ART_ROOT / f"{number:03d}"
    if not directory.exists():
        return []
    return sorted(path for path in directory.iterdir() if path.is_file() and path.suffix.lower() in ART_EXTENSIONS)


def _art_figure(path: Path, number: int, record: dict | None = None) -> str:
    src = "../" + path.as_posix()
    alt_text = f"A story scene from Chapter {number}."
    caption = ""
    if record:
        registry_alt = record.get("alt_text")
        registry_caption = record.get("caption")
        if isinstance(registry_alt, str) and registry_alt.strip():
            alt_text = registry_alt.strip()
        if isinstance(registry_caption, str) and registry_caption.strip():
            caption = registry_caption.strip()
    parts = [
        '<figure class="chapter-art scene-illustration">',
        f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt_text, quote=True)}" loading="lazy"/>',
    ]
    if caption:
        parts.append(f"<figcaption>{html.escape(caption)}</figcaption>")
    parts.append("</figure>")
    return "".join(parts)


def _asset_key(path: Path) -> str:
    return path.as_posix().lstrip("./")


def prose_with_art(
    prose_html: str,
    art: list[Path],
    number: int,
    registry_by_asset: dict[str, dict] | None = None,
) -> str:
    if not art:
        return prose_html

    registry_by_asset = registry_by_asset or {}
    anchored: list[tuple[Path, dict]] = []
    floating: list[Path] = []
    for path in art:
        record = registry_by_asset.get(_asset_key(path))
        anchor = record.get("paragraph_anchor") if record else None
        if isinstance(anchor, str) and anchor.strip():
            anchored.append((path, record))
        else:
            floating.append(path)

    paragraphs = re.findall(r"<p>.*?</p>", prose_html, flags=re.S)
    if not paragraphs:
        rendered = prose_html
        if floating:
            rendered += "\n" + "\n".join(
                _art_figure(path, number, registry_by_asset.get(_asset_key(path))) for path in floating
            )
    else:
        slots: dict[int, list[Path]] = {}
        total = len(paragraphs)
        for idx, path in enumerate(floating, start=1):
            slot = max(1, min(total, round(idx * total / (len(floating) + 1))))
            slots.setdefault(slot, []).append(path)
        rendered_parts: list[str] = []
        for idx, paragraph in enumerate(paragraphs, start=1):
            rendered_parts.append(paragraph)
            for path in slots.get(idx, []):
                rendered_parts.append(_art_figure(path, number, registry_by_asset.get(_asset_key(path))))
        rendered = "\n".join(rendered_parts)

    for path, record in anchored:
        anchor = record["paragraph_anchor"].strip()
        target = f"<p>{html.escape(anchor, quote=False)}</p>"
        count = rendered.count(target)
        if count != 1:
            raise ValueError(
                f"illustration {record.get('id', _asset_key(path))} paragraph anchor must occur exactly once; "
                f"found {count}: {anchor!r}"
            )
        rendered = rendered.replace(target, target + "\n" + _art_figure(path, number, record), 1)

    return rendered


def live_registry_for_chapter(registry: list[dict], number: int) -> dict[str, dict]:
    return {
        record["live_asset"]: record
        for record in registry
        if record.get("status") == "live"
        and record.get("kind") == "chapter_illustration"
        and record.get("chapter") == number
        and isinstance(record.get("live_asset"), str)
        and record.get("live_asset")
    }


def render_chapter(
    chapter: Chapter,
    art: list[Path],
    showcase: ShowcaseMap,
    registry_by_asset: dict[str, dict] | None = None,
) -> str:
    display_number = showcase.showcase_number(chapter.number)
    if display_number is None:
        raise ValueError(f"canonical chapter {chapter.number} is hidden from showcase")

    previous = showcase.previous_visible(chapter.number)
    following = showcase.next_visible(chapter.number)
    if previous is None:
        prev_link = '<span class="is-disabled">← Previous</span>'
    else:
        previous_display = showcase.showcase_number(previous)
        prev_link = f'<a rel="prev" href="{previous:03d}.html">← Chapter {previous_display}</a>'
    if following is None:
        next_link = '<span class="is-disabled">Next →</span>'
    else:
        following_display = showcase.showcase_number(following)
        next_link = f'<a rel="next" href="{following:03d}.html">Chapter {following_display} →</a>'

    prose = prose_with_art(chapter.prose_html, art, chapter.number, registry_by_asset)
    title = html.escape(chapter.title)
    title_case = html.escape(chapter.title.title())
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><meta name="description" content="Peg-Leg Greg Chapter {display_number}: {title_case}."/><title>Chapter {display_number}: {title_case} — Peg-Leg Greg</title><link href="../assets/reader.css" rel="stylesheet"/></head>
<body><header class="site-head"><a href="../index.html">PEG-LEG GREG</a><nav aria-label="Reader navigation" class="site-nav"><a href="../index.html#chapters">CHAPTERS</a><a href="../light/{chapter.number:03d}.html">TEXT</a><a href="../art.html">ART</a></nav></header>
<main class="chapter-shell"><nav class="chapter-nav chapter-nav-top" aria-label="Chapter navigation">{prev_link}<a href="../index.html#chapters">Chapters</a>{next_link}</nav><header class="chapter-title"><div class="number">CHAPTER {display_number}</div><h1>{title}</h1></header><article class="prose">{prose}</article><nav class="chapter-nav" aria-label="Chapter navigation">{prev_link}<a href="../index.html#chapters">Chapters</a>{next_link}</nav></main>
<script>try{{localStorage.setItem('plg:lastIllustratedChapter','{chapter.number}')}}catch(e){{}}</script></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate static Illustrated Reader chapters from exact prose authority.")
    parser.add_argument("range", help="N-N, for example 156-219")
    args = parser.parse_args()
    all_chapters = load_all_sources()
    showcase = build_showcase_map(sorted(all_chapters), load_showcase_manifest(SHOWCASE_MANIFEST))
    requested = selected_numbers(args.range, all_chapters)
    wanted = [number for number in requested if showcase.showcase_number(number) is not None]
    if not wanted:
        print(f"no visible Illustrated Reader chapters for {args.range}")
        return 0
    registry = load_registry(REGISTRY_PATH, root=Path(".")) if REGISTRY_PATH.exists() else []
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    for number in wanted:
        chapter = all_chapters[number]
        placement = live_registry_for_chapter(registry, number)
        (CHAPTERS_DIR / f"{number:03d}.html").write_text(
            render_chapter(chapter, chapter_art(number), showcase, placement),
            encoding="utf-8",
        )
    print(f"generated {len(wanted)} visible Illustrated Reader chapters: {wanted[0]}-{wanted[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
