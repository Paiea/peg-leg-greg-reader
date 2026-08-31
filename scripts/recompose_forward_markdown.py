#!/usr/bin/env python3
"""Conservatively recompose fragment-heavy forward Markdown prose."""

import argparse
import re
from pathlib import Path


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’']+\b", text))


def is_boundary(paragraph: str) -> bool:
    stripped = paragraph.lstrip()
    if stripped and set(stripped) == {"-"}:
        return True
    if stripped.startswith(('"', '“', '”')):
        return True
    letters = [character for character in stripped if character.isalpha()]
    if letters and all(character.isupper() for character in letters):
        return True
    if stripped.endswith(":") and word_count(stripped) <= 5:
        return True
    return False


def recompose_body(body: str) -> str:
    paragraphs = [" ".join(block.split()) for block in re.split(r"\n\s*\n", body) if block.strip()]
    output = []
    buffer = ""
    for paragraph in paragraphs:
        if is_boundary(paragraph):
            if buffer:
                output.append(buffer)
                buffer = ""
            output.append(paragraph)
            continue
        if not buffer:
            buffer = paragraph
            continue
        combined = word_count(buffer) + word_count(paragraph)
        if combined <= 90 and (word_count(buffer) < 42 or word_count(paragraph) <= 12):
            buffer += " " + paragraph
        else:
            output.append(buffer)
            buffer = paragraph
    if buffer:
        output.append(buffer)
    return "\n\n".join(output)


def recompose_document(document: str) -> str:
    matches = list(re.finditer(r"^# CHAPTER \d+\s+^## [^\n]+\s+", document, re.MULTILINE))
    if not matches:
        raise ValueError("no chapter headings found")
    prefix = document[: matches[0].end()]
    pieces = [prefix.rstrip()]
    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(document)
        pieces.append(recompose_body(document[body_start:body_end]))
        if index + 1 < len(matches):
            heading = document[matches[index + 1].start() : matches[index + 1].end()].strip()
            pieces.append(heading)
    return "\n\n".join(pieces).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    source = args.path.read_text(encoding="utf-8")
    args.path.write_text(recompose_document(source), encoding="utf-8")
    print(f"recomposed forward prose rhythm in {args.path}")


if __name__ == "__main__":
    main()
