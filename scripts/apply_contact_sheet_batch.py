#!/usr/bin/env python3
"""Crop a 5x5 discovery sheet and place manifest-backed chapter art."""

import argparse
import html
import json
from pathlib import Path

from PIL import Image


def paragraph_start(document: str, anchor: str) -> int:
    needle = anchor.casefold()
    cursor = 0
    while True:
        start = document.find("<p", cursor)
        if start < 0:
            break
        end = document.find("</p>", start)
        if end < 0:
            break
        end += 4
        if needle in html.unescape(document[start:end]).casefold():
            return start
        cursor = end
    raise ValueError(f"paragraph anchor not found: {anchor}")


def figure(item: dict) -> str:
    return (
        f'<figure class="chapter-art {item["role"]}">'
        f'<img src="../{item["target"]}" alt="{html.escape(item["alt"], quote=True)}" loading="lazy"/>'
        "</figure>"
    )


def crop_panel(sheet: Image.Image, row: int, column: int) -> Image.Image:
    left = round((column - 1) * sheet.width / 5)
    top = round((row - 1) * sheet.height / 5)
    right = round(column * sheet.width / 5)
    bottom = round(row * sheet.height / 5)
    panel = sheet.crop((left + 2, top + 2, right - 2, bottom - 2)).convert("RGB")
    return panel.resize((1000, 1000), Image.Resampling.LANCZOS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    batch = json.loads(args.manifest.read_text(encoding="utf-8"))
    sheets = {}
    failures = []
    for item in batch["items"]:
        source = root / item["source_sheet"]
        if source not in sheets:
            sheets[source] = Image.open(source).convert("RGB")
        target = root / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        crop_panel(sheets[source], item["row"], item["column"]).save(
            target, quality=91, optimize=True
        )
        chapter = root / "chapters" / f'{int(item["chapter"]):03}.html'
        document = chapter.read_text(encoding="utf-8")
        relative_ref = f'../{item["target"]}'
        if relative_ref not in document:
            try:
                start = paragraph_start(document, item["anchor"])
            except ValueError as error:
                failures.append(f'Ch{item["chapter"]}: {error}')
                continue
            document = document[:start] + figure(item) + document[start:]
            chapter.write_text(document, encoding="utf-8")
    for sheet in sheets.values():
        sheet.close()
    if failures:
        raise SystemExit("\n".join(failures))
    print(f'cropped and placed {len(batch["items"])} contact-sheet panels')


if __name__ == "__main__":
    main()
