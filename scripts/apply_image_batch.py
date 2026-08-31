#!/usr/bin/env python3
"""Apply a manifest-backed illustration batch and build its contact sheet."""

import argparse
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def paragraph_bounds(document: str, anchor: str) -> tuple[int, int]:
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
        plain = html.unescape(document[start:end])
        if needle in plain.casefold():
            return start, end
        cursor = end
    raise ValueError(f"paragraph anchor not found: {anchor}")


def figure(item: dict, *, width: int, height: int) -> str:
    return (
        f'<figure class="chapter-art {item["role"]}">'
        f'<img src="../{item["target"]}" alt="{html.escape(item["alt"], quote=True)}" '
        f'width="{width}" height="{height}" loading="lazy" decoding="async"/>'
        "</figure>"
    )


def make_contact_sheet(root: Path, batch: dict) -> None:
    cols, rows = 5, 5
    cell_w, cell_h, label_h = 360, 440, 44
    sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "#eee7da")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=18)
    for index, item in enumerate(batch["items"][:25]):
        source = root / item["target"]
        with Image.open(source) as opened:
            image = opened.convert("RGB")
            image.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        x = (index % cols) * cell_w + (cell_w - image.width) // 2
        y0 = (index // cols) * (cell_h + label_h)
        y = y0 + (cell_h - image.height) // 2
        sheet.paste(image, (x, y))
        draw.text((x + 8, y0 + cell_h + 10), f'{index + 1:02d}  Ch{item["chapter"]}  {item["scene"]}', fill="#28231e", font=font)
    output = root / batch["contact_sheet"]
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=88, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    batch = json.loads(args.manifest.read_text(encoding="utf-8"))
    failures = []
    for item in batch["items"]:
        source = args.source_dir / item["source_generated"]
        target = root / item["target"]
        chapter = root / "chapters" / f'{item["chapter"]}.html'
        if not source.exists():
            failures.append(f"missing source: {source}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        document = chapter.read_text(encoding="utf-8")
        relative_ref = f'../{item["target"]}'
        if relative_ref not in document:
            try:
                start, _ = paragraph_bounds(document, item["anchor"])
            except ValueError as error:
                failures.append(f'Ch{item["chapter"]}: {error}')
                continue
            with Image.open(target) as opened:
                width, height = opened.size
            document = (
                document[:start]
                + figure(item, width=width, height=height)
                + document[start:]
            )
            chapter.write_text(document, encoding="utf-8")
    if failures:
        raise SystemExit("\n".join(failures))
    make_contact_sheet(root, batch)
    print(f'placed {len(batch["items"])} images; contact sheet: {batch["contact_sheet"]}')


if __name__ == "__main__":
    main()
