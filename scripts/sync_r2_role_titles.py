#!/usr/bin/env python3
"""Keep R2 chapter title metadata synchronized by stable chapter number.

The approved editorial map lives in ``r2/TITLE_ROLE_AUDIT.md``. Selected
written headings carry the semantic title in their first-line title segment,
while their existing editorial prefix (``Chapter 12``, ``Year Chapter 03``,
``D730``, etc.) remains untouched.

This tool never invents a title. ``--promote-audit`` applies only the explicit
approved map, then synchronizes title metadata to public manifests, any
existing production-registry entries, and existing Greg, Again audio entries.
Stable identities, routes, media paths, and prose below the first heading are
not rewritten by title promotion.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

R2_ID_RE = re.compile(r"^r2-ch(?P<number>\d{3})$")
AUDIT_LINE_RE = re.compile(r"^(?P<number>\d{3})\s+(?P<title>.+)$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def chapter_number_from_r2_id(chapter_id: str) -> int:
    match = R2_ID_RE.fullmatch(chapter_id)
    if match is None:
        raise ValueError(f"invalid R2 chapter id: {chapter_id!r}")
    return int(match.group("number"))


def split_heading(first_line: str, path: Path) -> tuple[str, str]:
    if not first_line.startswith("# ") or ": " not in first_line:
        raise ValueError(f"invalid selected chapter heading in {path}: {first_line!r}")
    prefix, title = first_line.split(": ", 1)
    if not prefix.strip() or not title.strip():
        raise ValueError(f"invalid selected chapter heading in {path}: {first_line!r}")
    return prefix, title.strip()


def public_numbers(root: Path) -> list[int]:
    project = read_json(root / "r2" / "data" / "project.json")
    return [chapter_number_from_r2_id(chapter_id) for chapter_id in project["chapters"]]


def selected_title(root: Path, number: int) -> str:
    path = root / "r2" / "assets" / "written" / f"ch{number:03d}.md"
    if not path.exists():
        raise ValueError(f"missing selected written chapter: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError(f"empty selected written chapter: {path}")
    _prefix, title = split_heading(lines[0], path)
    return title


def selected_titles(root: Path) -> dict[int, str]:
    return {number: selected_title(root, number) for number in public_numbers(root)}


def approved_audit_titles(root: Path) -> dict[int, str]:
    path = root / "r2" / "TITLE_ROLE_AUDIT.md"
    if not path.exists():
        raise ValueError(f"missing approved role-title audit: {path}")
    text = path.read_text(encoding="utf-8")
    marker = "## Approved title map"
    if marker not in text:
        raise ValueError(f"{path}: missing {marker!r}")

    section = text.split(marker, 1)[1]
    in_block = False
    titles: dict[int, str] = {}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            if in_block:
                break
            in_block = True
            continue
        if not in_block or not line:
            continue
        match = AUDIT_LINE_RE.fullmatch(line)
        if match is None:
            raise ValueError(f"{path}: invalid approved title-map line: {raw_line!r}")
        number = int(match.group("number"))
        if number in titles:
            raise ValueError(f"{path}: duplicate approved title for Chapter {number}")
        titles[number] = match.group("title").strip()

    if not titles:
        raise ValueError(f"{path}: approved title map is empty")
    return titles


def validate_audit_coverage(root: Path, audit: dict[int, str]) -> list[int]:
    numbers = public_numbers(root)
    expected = set(numbers)
    actual = set(audit)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        details = []
        if missing:
            details.append(f"missing {missing}")
        if extra:
            details.append(f"extra {extra}")
        raise ValueError("approved audit does not match public frontier: " + "; ".join(details))
    return numbers


def promote_audit_headings(root: Path) -> list[Path]:
    audit = approved_audit_titles(root)
    numbers = validate_audit_coverage(root, audit)
    changed: list[Path] = []

    for number in numbers:
        path = root / "r2" / "assets" / "written" / f"ch{number:03d}.md"
        if not path.exists():
            raise ValueError(f"approved audit chapter has no selected written file: {path}")

        original = path.read_text(encoding="utf-8")
        first_line, separator, remainder = original.partition("\n")
        prefix, _old_title = split_heading(first_line, path)
        replacement = f"{prefix}: {audit[number]}"
        if first_line == replacement:
            continue

        updated = replacement + (separator + remainder if separator else "")
        path.write_text(updated, encoding="utf-8")
        changed.append(path)

    return changed


def validate_public_identity(chapter: dict, number: int, path: Path) -> None:
    expected_id = f"r2-ch{number:03d}"
    if chapter.get("chapter_id") != expected_id:
        raise ValueError(f"{path}: chapter_id {chapter.get('chapter_id')!r} != {expected_id!r}")
    if chapter.get("display_number") != number:
        raise ValueError(f"{path}: display_number {chapter.get('display_number')!r} != {number}")


def validate_registry_identity(chapter: dict, number: int, path: Path) -> None:
    if chapter.get("display_number") != number:
        raise ValueError(f"{path}: registry display_number {chapter.get('display_number')!r} != {number}")


def audio_by_number(manifest: dict, path: Path) -> dict[int, dict]:
    by_number: dict[int, dict] = {}
    for chapter in manifest.get("chapters", []):
        number = chapter.get("number")
        if not isinstance(number, int):
            raise ValueError(f"{path}: audio chapter missing numeric number: {chapter!r}")
        expected_id = f"ga-{number:03d}"
        if chapter.get("chapter_id") != expected_id:
            raise ValueError(
                f"{path}: audio chapter_id {chapter.get('chapter_id')!r} != {expected_id!r}"
            )
        if number in by_number:
            raise ValueError(f"{path}: duplicate audio chapter number {number}")
        by_number[number] = chapter
    return by_number


def collect_drift(root: Path) -> list[str]:
    titles = selected_titles(root)
    drift: list[str] = []

    registry_path = root / "r2" / "data" / "chapter-registry.json"
    registry = read_json(registry_path) if registry_path.exists() else {"chapters": {}}
    registry_chapters = registry.get("chapters", {})

    for number, title in titles.items():
        public_path = root / "r2" / "data" / "chapters" / f"ch{number:03d}.json"
        public = read_json(public_path)
        validate_public_identity(public, number, public_path)
        if public.get("title") != title:
            drift.append(
                f"chapter {number}: public title {public.get('title')!r} != selected {title!r}"
            )

        chapter_id = f"r2-ch{number:03d}"
        if chapter_id in registry_chapters:
            registry_chapter = registry_chapters[chapter_id]
            validate_registry_identity(registry_chapter, number, registry_path)
            if registry_chapter.get("title") != title:
                drift.append(
                    f"chapter {number}: registry title {registry_chapter.get('title')!r} != selected {title!r}"
                )

    audio_path = root / "greg-again" / "audio" / "manifest.json"
    if audio_path.exists():
        audio = read_json(audio_path)
        for number, chapter in audio_by_number(audio, audio_path).items():
            if number not in titles:
                continue
            title = titles[number]
            if chapter.get("title") != title:
                drift.append(
                    f"chapter {number}: audio title {chapter.get('title')!r} != selected {title!r}"
                )

    return drift


def apply_titles(root: Path) -> list[Path]:
    titles = selected_titles(root)
    changed: list[Path] = []

    for number, title in titles.items():
        public_path = root / "r2" / "data" / "chapters" / f"ch{number:03d}.json"
        public = read_json(public_path)
        validate_public_identity(public, number, public_path)
        if public.get("title") != title:
            public["title"] = title
            write_json(public_path, public)
            changed.append(public_path)

    registry_path = root / "r2" / "data" / "chapter-registry.json"
    if registry_path.exists():
        registry = read_json(registry_path)
        registry_changed = False
        registry_chapters = registry.get("chapters", {})
        for number, title in titles.items():
            chapter_id = f"r2-ch{number:03d}"
            if chapter_id not in registry_chapters:
                continue
            chapter = registry_chapters[chapter_id]
            validate_registry_identity(chapter, number, registry_path)
            if chapter.get("title") != title:
                chapter["title"] = title
                registry_changed = True
        if registry_changed:
            write_json(registry_path, registry)
            changed.append(registry_path)

    audio_path = root / "greg-again" / "audio" / "manifest.json"
    if audio_path.exists():
        audio = read_json(audio_path)
        audio_changed = False
        for number, chapter in audio_by_number(audio, audio_path).items():
            if number not in titles:
                continue
            title = titles[number]
            if chapter.get("title") != title:
                chapter["title"] = title
                audio_changed = True
        if audio_changed:
            write_json(audio_path, audio)
            changed.append(audio_path)

    return changed


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root(), help="repository root")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report title drift without modifying files")
    mode.add_argument("--apply", action="store_true", help="sync metadata from selected written headings")
    mode.add_argument(
        "--promote-audit",
        action="store_true",
        help="apply approved audit titles to heading title segments, then sync metadata",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        changed: list[Path] = []
        if args.promote_audit:
            changed.extend(promote_audit_headings(root))
            changed.extend(apply_titles(root))
        elif args.apply:
            changed.extend(apply_titles(root))
        else:
            drift = collect_drift(root)
            if drift:
                for item in drift:
                    print(item)
                return 1
            print("R2 role titles are synchronized.")
            return 0

        remaining = collect_drift(root)
        if remaining:
            for item in remaining:
                print(item)
            return 1

        changed = unique_paths(changed)
        if changed:
            for path in changed:
                print(path.relative_to(root))
        else:
            print("R2 role titles already synchronized.")
        return 0
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())