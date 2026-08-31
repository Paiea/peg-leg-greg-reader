#!/usr/bin/env python3
"""Deterministic, non-destructive repository and visual-asset archaeology."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import zipfile
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
AUDIT_OUTPUTS = {
    "publishing/repository_inventory.json",
    "publishing/image_asset_manifest.json",
    "publishing/chapter_art_coverage.json",
}
TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".py", ".sh", ".txt", ".yaml", ".yml"
}
CHAPTER_HEADING = re.compile(r"(?im)^#{1,6}\s+CHAPTER\s+(\d+)\b")
DOCX_CHAPTER_HEADING = re.compile(
    r"(?im)^\s*(?:#{1,6}\s+)?CHAPTER\s+(\d+)\s*$"
)
ONES = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
TEENS = {
    10: "TEN", 11: "ELEVEN", 12: "TWELVE", 13: "THIRTEEN", 14: "FOURTEEN",
    15: "FIFTEEN", 16: "SIXTEEN", 17: "SEVENTEEN", 18: "EIGHTEEN", 19: "NINETEEN",
}
TENS = {
    20: "TWENTY", 30: "THIRTY", 40: "FORTY", 50: "FIFTY",
    60: "SIXTY", 70: "SEVENTY", 80: "EIGHTY", 90: "NINETY",
}
REFERENCE_PATTERN = re.compile(
    r"""(?:src|href|data-full-image)\s*=\s*["']([^"'#?]+)|url\(\s*["']?([^"')?#]+)""",
    re.IGNORECASE,
)


def repository_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(root).parts
        and ".worktrees" not in path.relative_to(root).parts
        and "__pycache__" not in path.relative_to(root).parts
        and path.relative_to(root).as_posix() not in AUDIT_OUTPUTS
    )


def number_words(number: int) -> str:
    if number < 10:
        return ONES[number]
    if number < 20:
        return TEENS[number]
    if number < 100:
        tens, remainder = divmod(number, 10)
        return TENS[tens * 10] + (f"-{ONES[remainder]}" if remainder else "")
    hundreds, remainder = divmod(number, 100)
    prefix = f"{ONES[hundreds]} HUNDRED"
    return prefix + (f" {number_words(remainder)}" if remainder else "")


NUMBER_WORD_PREFIXES = sorted(
    ((number_words(number), number) for number in range(1, 301)),
    key=lambda item: len(item[0]),
    reverse=True,
)


def docx_chapters(document: ElementTree.Element) -> list[int]:
    chapters = []
    for paragraph in (node for node in document.iter() if node.tag.endswith("}p")):
        text = "".join(
            node.text or "" for node in paragraph.iter() if node.tag.endswith("}t")
        ).strip().upper()
        if not text.startswith("CHAPTER "):
            continue
        tail = text[len("CHAPTER "):]
        numeric = re.match(r"(\d+)\b", tail)
        if numeric:
            chapters.append(int(numeric.group(1)))
            continue
        for words, number in NUMBER_WORD_PREFIXES:
            if tail.startswith(words):
                chapters.append(number)
                break
    return chapters


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_reference(source: Path, root: Path, reference: str) -> str | None:
    parsed = urlsplit(reference)
    if parsed.scheme or reference.startswith("//"):
        return None
    candidate = (source.parent / unquote(parsed.path)).resolve()
    try:
        return candidate.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def collect_references(root: Path, paths: Iterable[Path]) -> dict[str, list[str]]:
    references: dict[str, set[str]] = defaultdict(set)
    for source in paths:
        if source.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in REFERENCE_PATTERN.finditer(text):
            raw = match.group(1) or match.group(2)
            target = normalize_reference(source, root, raw)
            if target:
                references[target].add(source.relative_to(root).as_posix())
    return {path: sorted(sources) for path, sources in references.items()}


def classify_path(path: str) -> str:
    if path == "AGENTS.md" or path.startswith("state/") and "/history/" not in path:
        if path.startswith("state/manuscript/") and (
            "_Ch" in Path(path).name or "history/" in path
        ):
            return "HISTORICAL_KEEP"
        return "ACTIVE_AUTHORITY"
    if path.startswith("state/manuscript/history/"):
        return "HISTORICAL_KEEP"
    if re.fullmatch(r"chapters/\d{3}\.html", path):
        return "GENERATED"
    if path.startswith(("assets/", "scripts/")) or path in {
        "index.html", "light.html", "latest.html", "art.html", "README.md"
    }:
        return "ACTIVE_SUPPORT"
    if path.startswith("visual/chapter_art/") or path.startswith("visual/reference/"):
        return "ACTIVE_SUPPORT"
    if path.startswith(("visual/development/", "visual/production/", "harvested_photos/")):
        return "HISTORICAL_KEEP"
    if path.startswith("publishing/") or path.startswith("docs/"):
        return "ACTIVE_SUPPORT"
    if path.startswith("test_"):
        return "ACTIVE_SUPPORT"
    return "UNKNOWN_REVIEW_REQUIRED"


def inventory_repository(root: Path) -> dict:
    paths = repository_files(root)
    references = collect_references(root, paths)
    rows = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        rows.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
                "category": classify_path(relative),
                "referenced_by": references.get(relative, []),
            }
        )
    totals: dict[str, int] = defaultdict(int)
    for row in rows:
        totals[row["category"]] += row["size_bytes"]
    return {
        "schema_version": 1,
        "files": rows,
        "totals_by_category_bytes": dict(sorted(totals.items())),
        "total_bytes": sum(row["size_bytes"] for row in rows),
    }


def detect_manuscript_ranges(root: Path) -> list[dict]:
    manuscript_root = root / "state" / "manuscript"
    rows = []
    if not manuscript_root.exists():
        return rows
    for path in sorted(manuscript_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".docx"}:
            continue
        if path.suffix.lower() == ".docx":
            try:
                with zipfile.ZipFile(path) as archive:
                    document = ElementTree.fromstring(
                        archive.read("word/document.xml")
                    )
                chapters = docx_chapters(document)
            except (KeyError, zipfile.BadZipFile, ElementTree.ParseError):
                continue
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
            chapters = [int(value) for value in CHAPTER_HEADING.findall(text)]
        if not chapters:
            continue
        unique = sorted(set(chapters))
        low, high = unique[0], unique[-1]
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "chapters": unique,
                "duplicate_headings": sorted(
                    number for number in set(chapters) if chapters.count(number) > 1
                ),
                "range": f"{low}-{high}",
                "missing_within_range": sorted(set(range(low, high + 1)) - set(unique)),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return rows


def image_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as handle:
        header = handle.read(32)
        if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
            return struct.unpack(">II", header[16:24])
        if header[:2] != b"\xff\xd8":
            return None, None
        handle.seek(2)
        while True:
            marker_start = handle.read(1)
            if not marker_start:
                break
            if marker_start != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {bytes([value]) for value in range(0xC0, 0xC4)} | {
                bytes([value]) for value in range(0xC5, 0xC8)
            } | {bytes([value]) for value in range(0xC9, 0xCC)} | {
                bytes([value]) for value in range(0xCD, 0xD0)
            }:
                length = struct.unpack(">H", handle.read(2))[0]
                data = handle.read(length - 2)
                if len(data) >= 5:
                    height, width = struct.unpack(">HH", data[1:5])
                    return width, height
                break
            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                break
            length = struct.unpack(">H", length_bytes)[0]
            handle.seek(max(0, length - 2), 1)
    return None, None


def chapter_from_path(path: str) -> int | None:
    match = re.search(r"(?:chapter_art/|chapters/)(\d{1,3})(?:/|\.html)", path)
    return int(match.group(1)) if match else None


def quality_flags(width: int | None, height: int | None, size: int) -> list[str]:
    flags = []
    if width is None or height is None:
        flags.append("DIMENSIONS_UNREADABLE")
        return flags
    if min(width, height) < 512 or width * height < 500_000:
        flags.append("LOW_RESOLUTION")
    if size >= 3_000_000:
        flags.append("OVERSIZED_FILE")
    ratio = width / height if height else 0
    if ratio > 2.4 or ratio < 0.42:
        flags.append("EXTREME_ASPECT_RATIO")
    return flags


def inventory_images(root: Path) -> list[dict]:
    paths = repository_files(root)
    references = collect_references(root, paths)
    image_paths = [path for path in paths if path.suffix.lower() in IMAGE_SUFFIXES]
    hashes = {path: sha256(path) for path in image_paths}
    groups: dict[str, list[Path]] = defaultdict(list)
    for path, digest in hashes.items():
        groups[digest].append(path)
    duplicate_ids = {
        digest: f"sha256:{digest[:12]}" for digest, members in groups.items() if len(members) > 1
    }
    rows = []
    for path in image_paths:
        relative = path.relative_to(root).as_posix()
        width, height = image_dimensions(path)
        sources = references.get(relative, [])
        chapter_sources = sorted(
            {
                chapter
                for source in sources
                if (chapter := chapter_from_path(source)) is not None
            }
        )
        chapter = chapter_from_path(relative)
        if chapter is None and len(chapter_sources) == 1:
            chapter = chapter_sources[0]
        flags = quality_flags(width, height, path.stat().st_size)
        status = "REFERENCED" if sources else "UNUSED_REVIEW"
        action = "KEEP"
        if not sources:
            action = "UNUSED_REVIEW"
        elif "LOW_RESOLUTION" in flags:
            action = "REPLACE_LATER"
        elif "OVERSIZED_FILE" in flags:
            action = "OPTIMIZE"
        rows.append(
            {
                "chapter": chapter,
                "asset_path": relative,
                "width": width,
                "height": height,
                "aspect_ratio": round(width / height, 4) if width and height else None,
                "file_size": path.stat().st_size,
                "format": path.suffix.lower().lstrip("."),
                "referenced_by": sources,
                "status": status,
                "quality_flags": flags,
                "recommended_action": action,
                "sha256": hashes[path],
                "duplicate_group": duplicate_ids.get(hashes[path]),
            }
        )
    return rows


class ImageReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sources: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != "img":
            return
        source = dict(attrs).get("src")
        if source:
            self.sources.append(source)


def chapter_art_coverage(root: Path, images: list[dict]) -> dict:
    existing = {row["asset_path"] for row in images}
    chapters = {}
    broken = []
    for page in sorted((root / "chapters").glob("[0-9][0-9][0-9].html")):
        number = int(page.stem)
        parser = ImageReferenceParser()
        parser.feed(page.read_text(encoding="utf-8"))
        valid = []
        for source in parser.sources:
            normalized = normalize_reference(page, root, source)
            if normalized in existing:
                valid.append(normalized)
            elif normalized:
                broken.append({"chapter": number, "asset_path": normalized})
        chapters[f"{number:03d}"] = {
            "chapter": number,
            "image_count": len(valid),
            "assets": valid,
            "referenced_images": len(parser.sources),
        }
    counts = {number: row["image_count"] for number, row in chapters.items()}
    return {
        "schema_version": 1,
        "chapters": chapters,
        "summary": {
            "no_art": [int(number) for number, count in counts.items() if count == 0],
            "one_image": [int(number) for number, count in counts.items() if count == 1],
            "multiple_images": [int(number) for number, count in counts.items() if count >= 2],
            "maximum_images": max(counts.values(), default=0),
        },
        "broken_references": broken,
    }


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    inventory = inventory_repository(root)
    inventory["manuscript_ranges"] = detect_manuscript_ranges(root)
    images = inventory_images(root)
    coverage = chapter_art_coverage(root, images)
    if args.write:
        write_json(root / "publishing/repository_inventory.json", inventory)
        write_json(root / "publishing/image_asset_manifest.json", images)
        write_json(root / "publishing/chapter_art_coverage.json", coverage)
    print(
        json.dumps(
            {
                "files": len(inventory["files"]),
                "images": len(images),
                "chapters": len(coverage["chapters"]),
                "broken_image_references": len(coverage["broken_references"]),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
