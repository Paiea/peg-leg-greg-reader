#!/usr/bin/env python3
"""Repair two transition seams left by the first Chapters 60-61 compression pass."""

from __future__ import annotations

import argparse
import copy
import html
import re
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from scripts.apply_structural_compression_060_061 import (
    DOCX_REL,
    HTML_PATHS,
    W_NS,
    _set_paragraph_text,
    chapter_number_from_heading,
    p_text,
)

P_RE = re.compile(r"<p(?:\s[^>]*)?>(.*?)</p>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")

BAD_60 = "That was dangerous phrasing. Did I?"
GOOD_60 = "Second site was not on the complaint list."
BAD_61 = "Good. Bounded. We marked it. No repair. Moved."
GOOD_61 = "The paired culvert from yesterday had changed more."


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def plain(fragment: str) -> str:
    return norm(html.unescape(TAG_RE.sub("", re.sub(r"<br\s*/?>", " ", fragment, flags=re.I))))


def repair_paragraph(number: int, text: str) -> str:
    if number == 60 and BAD_60 in text and GOOD_60 in text:
        return text[text.index(GOOD_60):]
    if number == 61 and BAD_61 in text and GOOD_61 in text:
        return text[text.index(GOOD_61):]
    return text


def repair_html(path: Path, number: int) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        current = plain(match.group(1))
        fixed = repair_paragraph(number, current)
        if fixed == current:
            return match.group(0)
        changed = True
        return f"<p>{html.escape(fixed, quote=False)}</p>"

    updated = P_RE.sub(repl, text)
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def repair_docx(path: Path) -> bool:
    with zipfile.ZipFile(path, "r") as zin:
        original_xml = zin.read("word/document.xml")
        root = ET.fromstring(original_xml)
        body = next(node for node in root.iter() if node.tag == f"{{{W_NS}}}body")
        current_number: int | None = None
        changed = False
        for child in body:
            if child.tag != f"{{{W_NS}}}p":
                continue
            text = p_text(child)
            heading = chapter_number_from_heading(text)
            if heading in {60, 61, 62}:
                current_number = heading
                continue
            if current_number not in {60, 61} or not text:
                continue
            fixed = repair_paragraph(current_number, text)
            if fixed != text:
                _set_paragraph_text(child, fixed)
                changed = True

        if not changed:
            return False

        new_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        tmp.close()
        tmp_path = Path(tmp.name)
        with zipfile.ZipFile(tmp_path, "w") as zout:
            for info in zin.infolist():
                data = new_xml if info.filename == "word/document.xml" else zin.read(info.filename)
                zout.writestr(info, data)
    path.write_bytes(tmp_path.read_bytes())
    tmp_path.unlink(missing_ok=True)
    return True


def docx_chapter_text(path: Path, number: int) -> str:
    with zipfile.ZipFile(path, "r") as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
    body = next(node for node in root.iter() if node.tag == f"{{{W_NS}}}body")
    active = False
    parts: list[str] = []
    for child in body:
        if child.tag != f"{{{W_NS}}}p":
            continue
        text = p_text(child)
        heading = chapter_number_from_heading(text)
        if heading == number:
            active = True
            continue
        if active and heading is not None:
            break
        if active and text:
            parts.append(text)
    return "\n".join(parts)


def verify(root: Path) -> None:
    docx = root / DOCX_REL
    checks = {
        60: (BAD_60, GOOD_60),
        61: (BAD_61, GOOD_61),
    }
    for number, (bad, good) in checks.items():
        html_text = plain((root / HTML_PATHS[number]).read_text(encoding="utf-8"))
        source_text = docx_chapter_text(docx, number)
        for label, text in (("HTML", html_text), ("DOCX", source_text)):
            if bad in text:
                raise AssertionError(f"Chapter {number} {label}: dangling seam remains: {bad}")
            if good not in text:
                raise AssertionError(f"Chapter {number} {label}: next-scene boundary missing: {good}")
    print("Chapters 60-61 transition seams verified in DOCX and reader HTML")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()

    if args.verify:
        verify(root)
        return 0
    if not args.write:
        raise SystemExit("Use --write or --verify")

    changed = []
    for number, rel in HTML_PATHS.items():
        if repair_html(root / rel, number):
            changed.append(str(rel))
    if repair_docx(root / DOCX_REL):
        changed.append(str(DOCX_REL))
    verify(root)
    print("Repaired: " + (", ".join(changed) if changed else "nothing; already clean"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
