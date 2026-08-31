#!/usr/bin/env python3
"""Publish the supplied forward-running Markdown chapters without prose edits."""

import argparse
import html
import re
from pathlib import Path


CHAPTER_RE = re.compile(
    r"^# CHAPTER (?P<number>\d+)\s+^## (?P<title>[^\n]+)\s+(?P<body>.*?)(?=^# CHAPTER \d+|\Z)",
    re.MULTILINE | re.DOTALL,
)


def paragraphs(body: str) -> list[str]:
    output = []
    for block in re.split(r"\n\s*\n", body):
        text = " ".join(line.strip() for line in block.splitlines()).strip()
        if text and set(text) != {"-"}:
            output.append(text)
    return output


def chapter_html(number: int, title: str, body: list[str], endpoint: int) -> str:
    prose = "".join(f"<p>{html.escape(p, quote=False)}</p>" for p in body)
    previous = f'<a href="{number - 1:03}.html">← Previous</a>'
    toc = '<a class="toclink" href="../index.html">Table of Contents</a>'
    following = f'<a href="{number + 1:03}.html">Next Chapter →</a>' if number < endpoint else ""
    return (
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"/>'
        '<meta content="width=device-width,initial-scale=1" name="viewport"/>'
        f'<title>Chapter {number}: {title.title()} — Peg-Leg Greg</title>'
        '<link href="../assets/reader.css" rel="stylesheet"/></head><body>'
        '<header class="site-head"><a href="../index.html">PEG-LEG GREG</a>'
        '<nav aria-label="Reader navigation" class="site-nav"><a href="../art.html">ART</a></nav></header>'
        '<main class="chapter-shell"><header class="chapter-title">'
        f'<div class="number">CHAPTER {number}</div><h1>{html.escape(title)}</h1></header>'
        f'<article class="prose">{prose}</article>'
        f'<nav aria-label="Chapter navigation" class="chapter-nav">{previous}{toc}{following}</nav>'
        '</main></body></html>\n'
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    source = args.source.read_text(encoding="utf-8")
    chapters = [
        (int(match["number"]), match["title"].strip(), paragraphs(match["body"]))
        for match in CHAPTER_RE.finditer(source)
    ]
    if not chapters or chapters[0][0] != 138:
        raise SystemExit("forward manuscript must begin at Chapter 138")
    numbers = [number for number, _, _ in chapters]
    if numbers != list(range(numbers[0], numbers[-1] + 1)):
        raise SystemExit(f"non-contiguous forward range: {numbers}")
    endpoint = numbers[-1]
    for number, title, body in chapters:
        (root / "chapters" / f"{number:03}.html").write_text(
            chapter_html(number, title, body, endpoint), encoding="utf-8"
        )

    prior = root / "chapters" / "137.html"
    document = prior.read_text(encoding="utf-8")
    if 'href="138.html"' not in document:
        marker = '</nav></main></body></html>'
        document = document.replace(
            marker,
            '<a href="138.html">Next Chapter →</a>' + marker,
            1,
        )
        prior.write_text(document, encoding="utf-8")

    index_path = root / "index.html"
    index = index_path.read_text(encoding="utf-8")
    additions = "".join(
        f'<a href="chapters/{number:03}.html"><span class="num">{number}</span>'
        f'<span class="title">{html.escape(title.title())}</span></a>'
        for number, title, _ in chapters
    )
    index = re.sub(
        r'<a href="chapters/(?:13[8-9]|14\d|15\d)\.html">.*?</a>',
        '',
        index,
    )
    marker = '</section>\n</section>\n</main>'
    index = index.replace(marker, additions + marker, 1)
    index_path.write_text(index, encoding="utf-8")
    print(f"published Chapters 138–{endpoint} from {args.source}")


if __name__ == "__main__":
    main()
