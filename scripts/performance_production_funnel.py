#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_RE = re.compile(r'(<article\s+class="prose"[^>]*>)(.*?)(</article>)', re.S | re.I)
P_RE = re.compile(r'<p\b[^>]*>.*?</p>', re.S | re.I)
TAG_RE = re.compile(r'<[^>]+>')


def next_visible_chapters(manifest: dict, *, after_chapter: int, count: int, max_chapter: int) -> list[int]:
    default_visible = manifest.get("default", "visible") == "visible"
    overrides = manifest.get("chapters", {})
    selected: list[int] = []
    for chapter in range(after_chapter + 1, max_chapter + 1):
        if not overrides.get(str(chapter), {}).get("showcase", default_visible):
            continue
        selected.append(chapter)
        if len(selected) == count:
            break
    return selected


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_record(record: dict) -> None:
    chapter = record.get("chapter")
    if not isinstance(chapter, int) or chapter < 1:
        raise ValueError("chapter must be a positive integer")
    verdict = record.get("verdict")
    if verdict not in {"source_win", "change_survives"}:
        raise ValueError("verdict must be source_win or change_survives")
    screen = record.get("screen")
    if not isinstance(screen, dict):
        raise ValueError("screen is required")
    if screen.get("decision") not in {"source_win", "deep_review"}:
        raise ValueError("screen decision must be source_win or deep_review")
    if not isinstance(screen.get("signals"), list):
        raise ValueError("screen signals must be a list")
    if not _nonempty_text(screen.get("reason")):
        raise ValueError("screen reason is required")
    if verdict == "source_win":
        if screen.get("decision") == "deep_review" and not _nonempty_text(record.get("comparison")):
            raise ValueError("comparison is required for a deep-review source win")
        return
    if screen.get("decision") != "deep_review":
        raise ValueError("change_survives verdict requires deep_review screen decision")
    for field in ("dramatic", "performance", "screenplay", "comparison"):
        if not _nonempty_text(record.get(field)):
            raise ValueError(f"{field} is required for a surviving change")
    patches = record.get("patches")
    if not isinstance(patches, list) or not patches:
        raise ValueError("patches are required for a surviving change")
    for index, patch in enumerate(patches):
        if not isinstance(patch, dict):
            raise ValueError(f"patch {index} must be an object")
        for field in ("start", "end", "rationale"):
            if not _nonempty_text(patch.get(field)):
                raise ValueError(f"patch {index} {field} is required")
        replacement = patch.get("replacement")
        if not isinstance(replacement, list) or not replacement or not all(_nonempty_text(line) for line in replacement):
            raise ValueError(f"patch {index} replacement must contain prose paragraphs")
        if any("—" in line for line in replacement):
            raise ValueError(f"patch {index} replacement contains an em dash")


def validate_batch(batch: dict) -> None:
    if batch.get("schema") != "performance_production_batch/v1":
        raise ValueError("schema must be performance_production_batch/v1")
    if not _nonempty_text(batch.get("source_authority")):
        raise ValueError("source_authority is required")
    scope = batch.get("scope")
    if not isinstance(scope, list) or not scope or not all(isinstance(chapter, int) and chapter > 0 for chapter in scope):
        raise ValueError("scope must contain positive chapter integers")
    if len(scope) != len(set(scope)):
        raise ValueError("scope must not contain duplicate chapters")
    records = batch.get("records")
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    record_chapters = [record.get("chapter") for record in records if isinstance(record, dict)]
    if len(records) != len(scope) or sorted(record_chapters) != sorted(scope):
        raise ValueError("batch coverage must include every scope chapter exactly once")
    for record in records:
        validate_record(record)


def _plain(paragraph_html: str) -> str:
    text = html.unescape(TAG_RE.sub("", paragraph_html)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def _render_paragraph(text: str) -> str:
    if "—" in text:
        raise ValueError("replacement contains an em dash")
    return f"<p>{html.escape(text, quote=True)}</p>"


def _replace_paragraph_span(page: str, patch: dict) -> str:
    article = ARTICLE_RE.search(page)
    if not article:
        raise ValueError("missing article.prose")
    body = article.group(2)
    paragraphs = list(P_RE.finditer(body))
    plain = [_plain(match.group(0)) for match in paragraphs]
    start = re.sub(r"\s+", " ", patch["start"]).strip()
    end = re.sub(r"\s+", " ", patch["end"]).strip()
    starts = [index for index, value in enumerate(plain) if value == start]
    if len(starts) != 1:
        raise ValueError(f"start boundary matched {len(starts)} times: {patch['start']!r}")
    start_index = starts[0]
    ends = [index for index, value in enumerate(plain) if index >= start_index and value == end]
    if len(ends) != 1:
        raise ValueError(f"end boundary matched {len(ends)} times after start: {patch['end']!r}")
    end_index = ends[0]
    rendered = "".join(_render_paragraph(text) for text in patch["replacement"])
    body = body[:paragraphs[start_index].start()] + rendered + body[paragraphs[end_index].end():]
    return page[:article.start(2)] + body + page[article.end(2):]


def apply_record(page: str, record: dict) -> str:
    validate_record(record)
    if record["verdict"] == "source_win":
        return page
    updated = page
    for patch in record["patches"]:
        updated = _replace_paragraph_span(updated, patch)
    return updated


def apply_batch_to_root(batch: dict, chapter_root: Path) -> list[Path]:
    validate_batch(batch)
    changed: list[Path] = []
    for record in batch["records"]:
        if record["verdict"] != "change_survives":
            continue
        path = chapter_root / f"{record['chapter']:03d}.html"
        if not path.exists():
            raise ValueError(f"canonical chapter missing: {path.name}")
        original = path.read_text(encoding="utf-8")
        updated = apply_record(original, record)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or apply a PERFORMANCE production batch.")
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--chapter-root", type=Path, default=ROOT / "chapters")
    args = parser.parse_args()
    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    validate_batch(batch)
    if args.apply:
        changed = apply_batch_to_root(batch, args.chapter_root)
        print(json.dumps({"changed": [path.as_posix() for path in changed]}, indent=2))
    else:
        print(json.dumps({"scope_count": len(batch["scope"]), "survivors": [r["chapter"] for r in batch["records"] if r["verdict"] == "change_survives"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
