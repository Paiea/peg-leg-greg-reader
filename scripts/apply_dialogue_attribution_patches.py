#!/usr/bin/env python3
"""Apply approved dialogue/attribution patch batches to illustrated Book 1 pages.

The patch batches live on the durable editorial branch. This tool reads them
through git, applies only exact paragraph-level replacements, canonicalizes the
approved Book 1 name map in prose paragraphs, and preserves all non-paragraph
reader markup (including illustrations and navigation).

It is intentionally strict: unresolved or multiply-matching patches fail.
Editorial `...` lines are treated as explicit preserved gaps between exact
replacement segments, never as permission for fuzzy matching.
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


BATCH_RE = re.compile(r"BATCH_(\d{3})_(\d{3})\.md$")
CHAPTER_RE = re.compile(r"^## Chapter\s+(\d+)\b", re.IGNORECASE)
FIX_RE = re.compile(r"^### Fix\b", re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"^`(.*)`$")
P_RE = re.compile(r"<p(?:\s[^>]*)?>(.*?)</p>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
ARTICLE_RE = re.compile(r"(<article\s+class=\"prose\"[^>]*>)(.*?)(</article>)", re.DOTALL | re.IGNORECASE)
GAP = "\0PLG_PATCH_GAP\0"


@dataclass(frozen=True)
class Patch:
    chapter: int
    label: str
    current: tuple[str, ...]
    replacement: tuple[str, ...]
    source_file: str


@dataclass
class Paragraph:
    start: int
    end: int
    inner: str
    text: str


def git_text(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout


def _decode_patch_line(value: str) -> str:
    # Early patch files escaped straight quotes for Markdown readability.
    return value.replace(r'\"', '"')


def _plain_text(inner_html: str) -> str:
    value = BR_RE.sub("\n", inner_html)
    value = TAG_RE.sub("", value)
    return html.unescape(value)


def _html_for_text(text: str) -> str:
    return html.escape(text, quote=False).replace("\n", "<br/>")


def _canonicalize_names(text: str) -> str:
    # Approved Book 1 name map only. Do not add new renames here.
    text = text.replace("Pel Marris", "Silas Marris")
    text = text.replace("Ressa Vale", "Iona Vale")
    text = re.sub(r"\bPellian\b", "Arlo", text)
    text = re.sub(r"\bPell\b", "Arlo", text)
    text = re.sub(r"\bPera\b", "Iris", text)
    text = re.sub(r"\bLysa\b", "Lyssa", text)
    return text


def _batch_paths(ref: str, min_chapter: int, max_chapter: int) -> list[str]:
    listing = git_text("ls-tree", "-r", "--name-only", ref, "state/editorial/dialogue-pass")
    paths: list[tuple[int, int, str]] = []
    for raw in listing.splitlines():
        match = BATCH_RE.search(raw)
        if not match:
            continue
        start, end = int(match.group(1)), int(match.group(2))
        if end < min_chapter or start > max_chapter:
            continue
        paths.append((start, end, raw))
    paths.sort()
    if not paths:
        raise RuntimeError(f"no dialogue patch batches found on {ref}")
    return [path for _, _, path in paths]


def _parse_batch(content: str, source_file: str, min_chapter: int, max_chapter: int) -> list[Patch]:
    patches: list[Patch] = []
    chapter: int | None = None
    label: str | None = None
    current: list[str] = []
    replacement: list[str] = []
    mode: str | None = None

    def finalize() -> None:
        nonlocal label, current, replacement, mode
        if label and chapter is not None and min_chapter <= chapter <= max_chapter:
            if current and replacement:
                patches.append(
                    Patch(
                        chapter=chapter,
                        label=label,
                        current=tuple(current),
                        replacement=tuple(replacement),
                        source_file=source_file,
                    )
                )
        label = None
        current = []
        replacement = []
        mode = None

    for raw_line in content.splitlines():
        chapter_match = CHAPTER_RE.match(raw_line)
        if chapter_match:
            finalize()
            chapter = int(chapter_match.group(1))
            continue

        if FIX_RE.match(raw_line):
            finalize()
            label = raw_line.lstrip("# ").strip()
            continue

        lowered = raw_line.strip().lower()
        if label:
            if lowered.startswith("replace"):
                mode = "replacement"
                continue
            if lowered.startswith("current") or lowered.startswith("stale reader rendering"):
                mode = "current"
                continue
            if lowered.startswith("reason:"):
                finalize()
                continue

            if raw_line.strip() == "..." and mode in {"current", "replacement"}:
                target = current if mode == "current" else replacement
                if target and target[-1] != GAP:
                    target.append(GAP)
                continue

            code_match = INLINE_CODE_RE.match(raw_line.strip())
            if code_match and mode in {"current", "replacement"}:
                value = _decode_patch_line(code_match.group(1))
                if mode == "current":
                    current.append(value)
                else:
                    replacement.append(value)

    finalize()
    return patches


def load_patches(ref: str, min_chapter: int, max_chapter: int) -> list[Patch]:
    patches: list[Patch] = []
    for path in _batch_paths(ref, min_chapter, max_chapter):
        content = git_text("show", f"{ref}:{path}")
        patches.extend(_parse_batch(content, path, min_chapter, max_chapter))
    return patches


def _paragraphs(article_body: str) -> list[Paragraph]:
    result: list[Paragraph] = []
    for match in P_RE.finditer(article_body):
        inner = match.group(1)
        result.append(
            Paragraph(
                start=match.start(),
                end=match.end(),
                inner=inner,
                text=_plain_text(inner),
            )
        )
    return result


def _find_sequence(paragraphs: list[Paragraph], wanted: tuple[str, ...]) -> list[int]:
    if not wanted:
        return []
    texts = [p.text for p in paragraphs]
    width = len(wanted)
    return [
        idx
        for idx in range(0, len(texts) - width + 1)
        if tuple(texts[idx : idx + width]) == wanted
    ]


def _find_sequence_canonical(paragraphs: list[Paragraph], wanted: tuple[str, ...]) -> list[int]:
    canonical_wanted = tuple(_canonicalize_names(text) for text in wanted)
    texts = [_canonicalize_names(p.text) for p in paragraphs]
    width = len(canonical_wanted)
    return [
        idx
        for idx in range(0, len(texts) - width + 1)
        if tuple(texts[idx : idx + width]) == canonical_wanted
    ]


def _split_gaps(values: tuple[str, ...]) -> list[tuple[str, ...]]:
    segments: list[list[str]] = [[]]
    for value in values:
        if value == GAP:
            if segments[-1]:
                segments.append([])
            continue
        segments[-1].append(value)
    return [tuple(segment) for segment in segments if segment]


def _replace_exact_segment(article_body: str, patch: Patch) -> tuple[str, str]:
    paragraphs = _paragraphs(article_body)

    replacement_hits = _find_sequence(paragraphs, patch.replacement)
    if not replacement_hits:
        replacement_hits = _find_sequence_canonical(paragraphs, patch.replacement)
    if len(replacement_hits) == 1:
        return article_body, "already"
    if len(replacement_hits) > 1:
        raise RuntimeError(
            f"{patch.source_file} {patch.label}: replacement appears {len(replacement_hits)} times in chapter {patch.chapter}"
        )

    hits = _find_sequence(paragraphs, patch.current)
    if not hits:
        hits = _find_sequence_canonical(paragraphs, patch.current)
    if len(hits) != 1:
        raise RuntimeError(
            f"{patch.source_file} {patch.label}: expected current text exactly once in chapter {patch.chapter}, found {len(hits)}"
        )

    idx = hits[0]
    old_nodes = paragraphs[idx : idx + len(patch.current)]

    if len(old_nodes) == len(patch.replacement):
        edits: list[tuple[int, int, str]] = []
        for node, new_text in zip(old_nodes, patch.replacement):
            raw = article_body[node.start : node.end]
            open_end = raw.find(">") + 1
            close_start = raw.lower().rfind("</p>")
            new_raw = raw[:open_end] + _html_for_text(new_text) + raw[close_start:]
            edits.append((node.start, node.end, new_raw))
        for start, end, new_raw in reversed(edits):
            article_body = article_body[:start] + new_raw + article_body[end:]
        return article_body, "applied"

    first, last = old_nodes[0], old_nodes[-1]
    between = article_body[first.start : last.end]
    stripped = P_RE.sub("", between)
    if stripped.strip():
        raise RuntimeError(
            f"{patch.source_file} {patch.label}: paragraph-count-changing patch crosses non-paragraph markup"
        )
    new_block = "".join(f"<p>{_html_for_text(text)}</p>" for text in patch.replacement)
    article_body = article_body[: first.start] + new_block + article_body[last.end :]
    return article_body, "applied"


def _replace_patch(article_body: str, patch: Patch) -> tuple[str, str]:
    if GAP not in patch.current and GAP not in patch.replacement:
        return _replace_exact_segment(article_body, patch)

    current_segments = _split_gaps(patch.current)
    replacement_segments = _split_gaps(patch.replacement)
    if len(current_segments) != len(replacement_segments):
        raise RuntimeError(
            f"{patch.source_file} {patch.label}: gapped patch has {len(current_segments)} current segments and {len(replacement_segments)} replacement segments"
        )

    statuses: list[str] = []
    for index, (current, replacement) in enumerate(zip(current_segments, replacement_segments), start=1):
        segment_patch = Patch(
            chapter=patch.chapter,
            label=f"{patch.label} [segment {index}]",
            current=current,
            replacement=replacement,
            source_file=patch.source_file,
        )
        article_body, status = _replace_exact_segment(article_body, segment_patch)
        statuses.append(status)
    return article_body, "already" if all(status == "already" for status in statuses) else "applied"


def _canonicalize_article_paragraphs(article_body: str) -> tuple[str, int]:
    edits: list[tuple[int, int, str]] = []
    changed = 0
    for match in P_RE.finditer(article_body):
        inner = match.group(1)
        new_inner = _canonicalize_names(inner)
        if new_inner != inner:
            changed += 1
            edits.append((match.start(1), match.end(1), new_inner))
    for start, end, new_inner in reversed(edits):
        article_body = article_body[:start] + new_inner + article_body[end:]
    return article_body, changed


def apply_to_chapter(path: Path, patches: list[Patch], canonicalize: bool) -> tuple[bool, dict[str, int]]:
    original = path.read_text(encoding="utf-8")
    match = ARTICLE_RE.search(original)
    if not match:
        raise RuntimeError(f"no article.prose found in {path}")

    body = match.group(2)
    stats = {"applied": 0, "already": 0, "name_paragraphs": 0}
    for patch in patches:
        body, status = _replace_patch(body, patch)
        stats[status] += 1

    if canonicalize:
        body, name_changes = _canonicalize_article_paragraphs(body)
        stats["name_paragraphs"] += name_changes

    updated = original[: match.start(2)] + body + original[match.end(2) :]
    if "—" in _plain_text(body):
        raise RuntimeError(f"em dash found in prose after integration: {path}")
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True, stats
    return False, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-ref", default="origin/editor/voice-compression-pass")
    parser.add_argument("--min-chapter", type=int, default=6)
    parser.add_argument("--max-chapter", type=int, default=80)
    parser.add_argument("--chapters-dir", type=Path, default=Path("chapters"))
    parser.add_argument(
        "--canonicalize-from",
        type=int,
        default=1,
        help="first chapter whose prose receives the approved Book 1 name map",
    )
    args = parser.parse_args()

    patches = load_patches(args.patch_ref, args.min_chapter, args.max_chapter)
    by_chapter: dict[int, list[Patch]] = {}
    for patch in patches:
        by_chapter.setdefault(patch.chapter, []).append(patch)

    total = {"applied": 0, "already": 0, "name_paragraphs": 0, "files_changed": 0}
    for chapter in range(args.canonicalize_from, args.max_chapter + 1):
        path = args.chapters_dir / f"{chapter:03d}.html"
        if not path.exists():
            raise RuntimeError(f"missing chapter page: {path}")
        changed, stats = apply_to_chapter(path, by_chapter.get(chapter, []), canonicalize=True)
        total["files_changed"] += int(changed)
        for key in ("applied", "already", "name_paragraphs"):
            total[key] += stats[key]

    expected_patch_chapters = sorted(by_chapter)
    print(
        "dialogue integration complete: "
        f"patches={len(patches)} applied={total['applied']} already={total['already']} "
        f"name_paragraphs={total['name_paragraphs']} files_changed={total['files_changed']} "
        f"patch_chapters={expected_patch_chapters[0] if expected_patch_chapters else 'none'}-"
        f"{expected_patch_chapters[-1] if expected_patch_chapters else 'none'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
