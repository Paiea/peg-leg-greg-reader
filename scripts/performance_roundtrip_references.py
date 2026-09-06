from __future__ import annotations

import argparse
from html import unescape
import json
from pathlib import Path
import re
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = ROOT / "state" / "editorial" / "performance-roundtrip"
CHAPTER_ROOT = ROOT / "chapters"
REQUIRED_FILES = {
    "source.lock.json",
    "dramatic.md",
    "performance.md",
    "screenplay.md",
    "comparison.md",
}
ARTICLE_RE = re.compile(
    r"<article\b[^>]*class=[\"'][^\"']*\bprose\b[^\"']*[\"'][^>]*>(.*?)</article>",
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)
SPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    return SPACE_RE.sub(" ", unescape(TAG_RE.sub(" ", text))).strip()


def extract_prose(html: str) -> str:
    match = ARTICLE_RE.search(html)
    if not match:
        return ""
    return normalize_text(match.group(1))


def _reference_dir(chapter: int, archive_root: Path) -> Path:
    return archive_root / f"{chapter:03d}"


def _display_archive_path(reference_dir: Path) -> str:
    try:
        return reference_dir.relative_to(ROOT).as_posix()
    except ValueError:
        return reference_dir.as_posix()


def _load_lock(reference_dir: Path) -> tuple[dict | None, list[str]]:
    lock_path = reference_dir / "source.lock.json"
    if not lock_path.exists():
        return None, ["missing source.lock.json"]
    try:
        value = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"invalid source.lock.json: {exc}"]
    if not isinstance(value, dict):
        return None, ["source.lock.json must contain a JSON object"]
    return value, []


def validate_reference(
    chapter: int,
    *,
    archive_root: Path | None = None,
    chapter_root: Path | None = None,
) -> dict:
    archive_root = archive_root or ARCHIVE_ROOT
    chapter_root = chapter_root or CHAPTER_ROOT
    reference_dir = _reference_dir(chapter, archive_root)
    if not reference_dir.exists():
        return {
            "chapter": chapter,
            "archive_path": _display_archive_path(reference_dir),
            "status": "missing",
            "reasons": ["reference archive does not exist"],
        }

    lock, reasons = _load_lock(reference_dir)
    if lock is None:
        return {
            "chapter": chapter,
            "archive_path": _display_archive_path(reference_dir),
            "status": "stale",
            "reasons": reasons,
        }

    missing_files = sorted(name for name in REQUIRED_FILES if not (reference_dir / name).exists())
    if missing_files:
        reasons.append(f"missing required archive files: {', '.join(missing_files)}")

    if lock.get("authority") != "derived_editorial_reference":
        reasons.append("authority must be derived_editorial_reference")
    if lock.get("canon_authority") is not False:
        reasons.append("canon_authority must be false")
    if lock.get("canon_chapter") != chapter:
        reasons.append(f"canon_chapter must equal {chapter}")

    anchors = lock.get("result_scene_anchors")
    if not isinstance(anchors, list) or not anchors or not all(isinstance(anchor, str) and anchor.strip() for anchor in anchors):
        reasons.append("result_scene_anchors must be a non-empty list of strings")
        anchors = []

    source_path = lock.get("source_path")
    if isinstance(source_path, str) and source_path.strip():
        chapter_path = chapter_root / Path(source_path).name
    else:
        chapter_path = chapter_root / f"{chapter:03d}.html"
        reasons.append("source_path must identify the canonical chapter file")

    if not chapter_path.exists():
        reasons.append(f"canonical chapter missing: {chapter_path.name}")
    else:
        try:
            prose = extract_prose(chapter_path.read_text(encoding="utf-8"))
        except OSError as exc:
            prose = ""
            reasons.append(f"could not read canonical chapter: {exc}")
        if not prose:
            reasons.append("canonical chapter has no readable article.prose")
        else:
            for anchor in anchors:
                normalized_anchor = normalize_text(anchor)
                count = prose.count(normalized_anchor)
                if count != 1:
                    reasons.append(
                        f"scene anchor match count is {count}, expected 1: {normalized_anchor[:120]}"
                    )

    return {
        "chapter": chapter,
        "archive_path": _display_archive_path(reference_dir),
        "status": "stale" if reasons else "fresh",
        "reasons": reasons,
    }


def load_reference(
    chapter: int,
    *,
    archive_root: Path | None = None,
    chapter_root: Path | None = None,
) -> dict | None:
    archive_root = archive_root or ARCHIVE_ROOT
    validation = validate_reference(chapter, archive_root=archive_root, chapter_root=chapter_root)
    if validation["status"] != "fresh":
        return None
    reference_dir = _reference_dir(chapter, archive_root)
    lock, reasons = _load_lock(reference_dir)
    if lock is None or reasons:
        return None
    result = dict(lock)
    result["archive_path"] = validation["archive_path"]
    result["status"] = "fresh"
    return result


def load_visual_reference(
    chapter: int,
    *,
    archive_root: Path | None = None,
    chapter_root: Path | None = None,
) -> dict | None:
    reference = load_reference(
        chapter,
        archive_root=archive_root,
        chapter_root=chapter_root,
    )
    if reference is None:
        return None
    visual_reference = reference.get("visual_reference")
    anchors = reference.get("result_scene_anchors")
    if not isinstance(visual_reference, dict) or not visual_reference:
        return None
    if not isinstance(anchors, list) or not anchors:
        return None
    return {
        "archive_path": reference["archive_path"],
        "chapter": chapter,
        "displayed_showcase_chapter": reference.get("displayed_showcase_chapter"),
        "scene_anchors": list(anchors),
        "visual_reference": visual_reference,
    }


def load_visual_references(
    chapters: Iterable[int],
    *,
    archive_root: Path | None = None,
    chapter_root: Path | None = None,
) -> dict[int, dict]:
    result: dict[int, dict] = {}
    for chapter in sorted(set(chapters)):
        reference = load_visual_reference(
            chapter,
            archive_root=archive_root,
            chapter_root=chapter_root,
        )
        if reference is not None:
            result[chapter] = reference
    return result


def _archived_chapters(archive_root: Path) -> list[int]:
    if not archive_root.exists():
        return []
    chapters: list[int] = []
    for path in archive_root.iterdir():
        if path.is_dir() and path.name.isdigit() and (path / "source.lock.json").exists():
            chapters.append(int(path.name))
    return sorted(chapters)


def check_all(*, archive_root: Path = ARCHIVE_ROOT, chapter_root: Path = CHAPTER_ROOT) -> list[dict]:
    return [
        validate_reference(chapter, archive_root=archive_root, chapter_root=chapter_root)
        for chapter in _archived_chapters(archive_root)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate derived successful PERFORMANCE roundtrip references.")
    parser.add_argument("--check", action="store_true", help="validate every committed successful reference")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")

    results = check_all()
    stale = [result for result in results if result["status"] != "fresh"]
    print(json.dumps({"references": results, "stale_count": len(stale)}, indent=2))
    if stale:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
