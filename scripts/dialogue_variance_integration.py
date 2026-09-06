#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import apply_dialogue_attribution_patches as attribution
import apply_dialogue_variance as variance
import generate_light

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
RECOVERED = ROOT / "state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md"
RUNNING = ROOT / "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
CHECKPOINT_GLOB = "Peg_Leg_Greg_Chapter_*_EXACT_WIP.md"
REPORT = ROOT / "state/editorial/global-reports/DIALOGUE_VARIANCE_INTEGRATION_REPORT.md"
BATCH_RE = re.compile(r"BATCH_(\d+)_(\d+)\.md$")
BOUNDARY_RE = re.compile(
    r"^(?:# CHAPTER (?P<standard_num>\d+)[ \t]*|## Chapter (?P<combined_num>\d+)[ \t]*[—–-][ \t]*(?P<combined_title>[^\n]+?)[ \t]*)$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class IntegrationPatch:
    chapter: int
    label: str
    current: tuple[str, ...]
    replacement: tuple[str, ...]
    source_file: str
    directive: str = ""
    kind: str = "variance"


@dataclass
class Stats:
    applied: int = 0
    already: int = 0
    stale: int = 0
    ambiguous: int = 0

    def record(self, status: str) -> None:
        setattr(self, status, getattr(self, status) + 1)


def git_text(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout


def _inject_missing_patch_reasons(text: str) -> str:
    """Add metadata-only reasons where an approved legacy patch omitted them."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith("### Patch "):
            out.append(lines[i])
            i += 1
            continue
        end = i + 1
        while (
            end < len(lines)
            and not lines[end].startswith("### Patch ")
            and not lines[end].startswith("## Chapter ")
            and not lines[end].startswith("### Editorial ")
        ):
            end += 1
        section = lines[i:end]
        has_current = any(line.strip().lower().startswith("current") for line in section)
        has_replace = any(line.strip().lower().startswith("replace") for line in section)
        has_reason = any(line.strip().lower().startswith("reason:") for line in section)
        if has_current and has_replace and not has_reason:
            section.extend(["", "Reason: approved variance patch from reviewed editorial manifest"])
        out.extend(section)
        i = end
    return "\n".join(out)


def _normalize_variance_batch(text: str) -> str:
    """Normalize legacy ledger syntax into the hardened canonical parser format."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    chapter: int | None = None
    repair_mode = False
    repair_count = 0
    prose_section: str | None = None
    quote_buffer: list[str] = []

    def flush_quote_buffer() -> None:
        nonlocal quote_buffer
        if quote_buffer:
            paragraph = " ".join(part.strip() for part in quote_buffer if part.strip())
            if paragraph:
                out.append(f"`{paragraph}`")
            quote_buffer = []

    for raw in lines:
        stripped = raw.strip()
        lowered = stripped.lower()

        if prose_section and raw.lstrip().startswith(">"):
            quoted = raw.lstrip()[1:].lstrip()
            if quoted:
                quote_buffer.append(quoted)
            else:
                flush_quote_buffer()
            continue

        if prose_section and not stripped:
            flush_quote_buffer()
            out.append(raw)
            continue

        flush_quote_buffer()

        canonical_chapter = re.match(r"^## Chapter\s+(\d+)\b", raw)
        bare_chapter = re.match(r"^##\s+(\d+)\s+(.+?)\s*$", raw)
        if canonical_chapter:
            chapter = int(canonical_chapter.group(1))
            repair_mode = False
            repair_count = 0
            prose_section = None
            out.append(raw)
            continue
        if bare_chapter:
            chapter = int(bare_chapter.group(1))
            repair_mode = False
            repair_count = 0
            prose_section = None
            out.append(f"## Chapter {chapter} — {bare_chapter.group(2)}")
            continue
        if raw.startswith("## "):
            repair_mode = False
            prose_section = None
            out.append(f"### Editorial {raw[3:]}")
            continue

        bare_patch = re.match(r"^(\d+\.V\d+)(?:\s*[—–-]\s*(.*))?$", stripped)
        if bare_patch:
            suffix = f" — {bare_patch.group(2)}" if bare_patch.group(2) else ""
            out.append(f"### Patch {bare_patch.group(1)}{suffix}")
            repair_mode = False
            prose_section = None
            continue

        inline_sequence = re.match(r"^(Current|Replace(?: with)?):\s*`(.+)`\s*$", stripped, re.I)
        if inline_sequence:
            label, payload = inline_sequence.groups()
            is_current = label.lower().startswith("current")
            prose_section = "current" if is_current else "replacement"
            out.append("Current:" if is_current else "Replace with:")
            for part in payload.split(" / "):
                out.append(f"`{part.strip()}`")
            continue

        if lowered.startswith("current"):
            prose_section = "current"
            out.append(raw)
            continue
        if lowered.startswith("replace"):
            prose_section = "replacement"
            out.append(raw)
            continue
        if lowered.startswith("reason:") or lowered == "reason":
            prose_section = None
            out.append(raw)
            continue

        if lowered.endswith("repairs:"):
            prose_section = None
            repair_mode = True
            out.append(raw)
            continue

        repair = re.match(r"^\s*-\s*`([^`]+)`\s*(?:->|→)\s*`([^`]+)`\s*$", raw)
        if repair_mode and repair and chapter is not None:
            repair_count += 1
            old, new = repair.groups()
            out.extend(
                [
                    f"### Patch {chapter}.R{repair_count}",
                    "Current:",
                    f"`{old}`",
                    "Replace with:",
                    f"`{new}`",
                    "Reason: approved referent/POV repair",
                ]
            )
            continue

        if stripped and not stripped.startswith("-"):
            if stripped.endswith(":") and not lowered.startswith("reason:"):
                repair_mode = False
        out.append(raw)

    flush_quote_buffer()
    return _inject_missing_patch_reasons("\n".join(out))


def _parse_variance_batch(
    content: str,
    source_file: str,
    min_chapter: int,
    max_chapter: int,
) -> list[IntegrationPatch]:
    normalized = _normalize_variance_batch(content)
    parsed = variance.parse_batch(normalized)
    return [
        IntegrationPatch(
            chapter=p.chapter,
            label=p.patch_id,
            current=tuple(p.current),
            replacement=tuple(p.replacement),
            source_file=source_file,
            directive=p.directive,
            kind="variance",
        )
        for p in parsed
        if min_chapter <= p.chapter <= max_chapter
    ]


def _parse_attribution_batch(
    content: str,
    source_file: str,
    min_chapter: int,
    max_chapter: int,
) -> list[IntegrationPatch]:
    parsed = attribution._parse_batch(content, source_file, min_chapter, max_chapter)
    return [
        IntegrationPatch(
            chapter=p.chapter,
            label=p.label,
            current=p.current,
            replacement=p.replacement,
            source_file=p.source_file,
            kind="attribution",
        )
        for p in parsed
    ]


def merge_patch_sets(attribution_patches: list, variance_patches: list) -> list:
    """Authority order matters: attribution first, then the variance pass."""
    return [*attribution_patches, *variance_patches]


def _batch_paths(ref: str, directory: str, min_chapter: int, max_chapter: int) -> list[str]:
    listing = git_text("ls-tree", "-r", "--name-only", ref, directory)
    found: list[tuple[int, int, str]] = []
    for raw in listing.splitlines():
        match = BATCH_RE.search(raw)
        if not match:
            continue
        start, end = map(int, match.groups())
        if end < min_chapter or start > max_chapter:
            continue
        found.append((start, end, raw))
    return [path for _, _, path in sorted(found)]


def load_approved_patches(
    ref: str,
    min_chapter: int,
    max_chapter: int,
) -> tuple[list[IntegrationPatch], list[IntegrationPatch]]:
    attr: list[IntegrationPatch] = []
    for path in _batch_paths(ref, "state/editorial/dialogue-pass", min_chapter, max_chapter):
        attr.extend(
            _parse_attribution_batch(
                git_text("show", f"{ref}:{path}"), path, min_chapter, max_chapter
            )
        )

    var: list[IntegrationPatch] = []
    for path in _batch_paths(ref, "state/editorial/dialogue-variance-pass", min_chapter, max_chapter):
        var.extend(
            _parse_variance_batch(
                git_text("show", f"{ref}:{path}"), path, min_chapter, max_chapter
            )
        )
    return attr, var


def _to_attr_patch(patch: IntegrationPatch) -> attribution.Patch:
    return attribution.Patch(
        chapter=patch.chapter,
        label=patch.label,
        current=patch.current,
        replacement=patch.replacement,
        source_file=patch.source_file,
    )


def _to_variance_patch(patch: IntegrationPatch) -> variance.Patch:
    return variance.Patch(
        patch.chapter,
        patch.label,
        list(patch.current),
        list(patch.replacement),
        patch.directive,
    )


def _failure_status(exc: Exception) -> str:
    message = str(exc).lower()
    if "matched " in message and " times" in message:
        return "ambiguous"
    if "appears " in message and " times" in message:
        return "ambiguous"
    return "stale"


def apply_patches_to_html(
    page: str,
    patches: list[IntegrationPatch],
    stats: dict[str, Stats],
    conflicts: list[str],
) -> str:
    current = page
    for patch in patches:
        bucket = stats[patch.kind]
        try:
            if patch.kind == "attribution":
                match = attribution.ARTICLE_RE.search(current)
                if not match:
                    raise RuntimeError(f"chapter {patch.chapter} has no article.prose")
                body, status = attribution._replace_patch(match.group(2), _to_attr_patch(patch))
                updated = current[: match.start(2)] + body + current[match.end(2) :]
            else:
                updated = variance.apply_patch_to_html(current, _to_variance_patch(patch))
                status = "already" if updated == current else "applied"
            bucket.record(status)
            current = updated
        except (AssertionError, RuntimeError) as exc:
            status = _failure_status(exc)
            bucket.record(status)
            conflicts.append(
                f"- Chapter {patch.chapter} `{patch.label}` ({patch.kind}, `{patch.source_file}`): "
                f"**{status.upper()}** — {exc}"
            )
    return current


def _canonical_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")).strip()


def _markdown_literal_pattern(text: str, group_name: str) -> str:
    pieces: list[str] = []
    cursor = 0
    for whitespace in re.finditer(r"\s+", text):
        literal = text[cursor:whitespace.start()]
        pieces.append(_markdown_escape_literal(literal))
        pieces.append(r"\s+")
        cursor = whitespace.end()
    pieces.append(_markdown_escape_literal(text[cursor:]))
    return rf"(?P<{group_name}>{''.join(pieces)})"


def _markdown_escape_literal(text: str) -> str:
    parts: list[str] = []
    for char in text:
        if char == '"':
            parts.append('["“”]')
        elif char == "'":
            parts.append("['‘’]")
        else:
            parts.append(re.escape(char))
    return "".join(parts)


def _markdown_sequence_pattern(lines: list[str] | tuple[str, ...]) -> tuple[re.Pattern[str], list[int]]:
    if not lines:
        raise AssertionError("cannot match empty markdown sequence")
    literal_indices = [idx for idx, line in enumerate(lines) if line != "..."]
    if not literal_indices:
        raise AssertionError("markdown sequence cannot contain only ellipsis")

    parts: list[str] = []
    previous_literal: int | None = None
    gap_number = 0
    pending_ellipsis = False
    for literal_number, line_index in enumerate(literal_indices):
        if previous_literal is not None:
            between = lines[previous_literal + 1 : line_index]
            pending_ellipsis = pending_ellipsis or "..." in between
            gap = r".*?" if pending_ellipsis else r"\s*"
            parts.append(rf"(?P<gap{gap_number}>{gap})")
            gap_number += 1
            pending_ellipsis = False
        parts.append(_markdown_literal_pattern(lines[line_index], f"lit{literal_number}"))
        previous_literal = line_index
    return re.compile("".join(parts), re.S), literal_indices


def _markdown_target_and_replacement(patch: IntegrationPatch) -> tuple[list[str], list[str]]:
    if patch.kind == "variance":
        vp = _to_variance_patch(patch)
        return list(variance._target_lines(vp)), list(patch.replacement)
    return list(patch.current), list(patch.replacement)


def _markdown_replacement(
    match: re.Match[str],
    target: list[str],
    replacement: list[str],
) -> str:
    literal_target = [line for line in target if line != "..."]
    styled = [variance._reader_typography(line, match.group(0)) for line in replacement]

    if "..." not in target and len(styled) == len(literal_target):
        pieces: list[str] = []
        for idx, new_line in enumerate(styled):
            old_line = literal_target[idx]
            if _canonical_text(new_line) == _canonical_text(old_line):
                pieces.append(match.group(f"lit{idx}"))
            else:
                pieces.append(new_line)
            if idx < len(styled) - 1:
                pieces.append(match.group(f"gap{idx}"))
        return "".join(pieces)

    return "\n\n".join(styled)


def _apply_patch_to_markdown_body(body: str, patch: IntegrationPatch) -> tuple[str, str]:
    target, replacement = _markdown_target_and_replacement(patch)
    target_pattern, _ = _markdown_sequence_pattern(target)
    matches = list(target_pattern.finditer(body))
    if not matches:
        replacement_pattern, _ = _markdown_sequence_pattern(replacement)
        if replacement_pattern.search(body):
            return body, "already"
        raise AssertionError(
            f"{patch.label}: approved current prose not found in chapter {patch.chapter}"
        )
    if len(matches) != 1:
        raise AssertionError(
            f"{patch.label}: approved current prose matched {len(matches)} times in chapter {patch.chapter}"
        )
    match = matches[0]
    replaced = body[: match.start()] + _markdown_replacement(match, target, replacement) + body[match.end() :]
    return replaced, "applied"


def _chapter_body_span(text: str, number: int) -> tuple[int, int]:
    matches = list(BOUNDARY_RE.finditer(text))
    for idx, match in enumerate(matches):
        raw = match.group("standard_num") or match.group("combined_num")
        if int(raw) != number:
            continue
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        if match.group("standard_num"):
            chunk = text[match.end():end]
            title = re.search(r"^##\s+.+?\s*$", chunk, re.MULTILINE)
            if not title:
                raise RuntimeError(f"Chapter {number} source has no title heading")
            return match.end() + title.end(), end
        return match.end(), end
    raise RuntimeError(f"Chapter {number} not found in source")


def apply_patches_to_markdown_chapter(
    source_text: str,
    chapter: int,
    patches: list[IntegrationPatch],
    stats: dict[str, Stats],
    conflicts: list[str],
) -> tuple[str, bool]:
    start, end = _chapter_body_span(source_text, chapter)
    original_body = source_text[start:end]
    body = original_body

    for patch in patches:
        bucket = stats[patch.kind]
        try:
            body, status = _apply_patch_to_markdown_body(body, patch)
            bucket.record(status)
        except (AssertionError, RuntimeError) as exc:
            status = _failure_status(exc)
            bucket.record(status)
            conflicts.append(
                f"- Chapter {patch.chapter} `{patch.label}` ({patch.kind}, `{patch.source_file}`): "
                f"**{status.upper()}** — {exc}"
            )

    if body == original_body:
        return source_text, False
    return source_text[:start] + body + source_text[end:], True


def authority_index() -> dict[int, Path]:
    index: dict[int, Path] = {}
    recovered = generate_light.parse_markdown_chapters(RECOVERED, "recovered")
    for n in recovered:
        index[n] = RECOVERED

    running = generate_light.parse_markdown_chapters(RUNNING, "manuscript")
    for n in running:
        index[n] = RUNNING
    running_edge = max(running, default=0)

    for path in sorted(RUNNING.parent.glob(CHECKPOINT_GLOB)):
        checkpoint = generate_light.parse_markdown_chapters(path, "checkpoint")
        for n in checkpoint:
            if n > running_edge:
                index[n] = path
    return index


def _render_report(
    patch_ref: str,
    min_chapter: int,
    max_chapter: int,
    attr_count: int,
    var_count: int,
    stats: dict[str, Stats],
    changed_files: list[str],
    conflicts: list[str],
) -> str:
    lines = [
        "# Dialogue Variance Integration Report",
        "",
        f"- Patch authority: `{patch_ref}`",
        f"- Replay scope: Chapters {min_chapter}-{max_chapter}",
        f"- Attribution manifests parsed: {attr_count} patches",
        f"- Variance manifests parsed: {var_count} patches",
        f"- Durable files changed: {len(changed_files)}",
        "",
        "## Results",
        "",
        "| Pass | Applied | Already live | Stale | Ambiguous |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for key in ("attribution", "variance"):
        s = stats[key]
        lines.append(
            f"| {key.title()} | {s.applied} | {s.already} | {s.stale} | {s.ambiguous} |"
        )
    lines.extend(["", "## Durable files changed", ""])
    lines.extend(f"- `{path}`" for path in changed_files)
    lines.extend(["", "## Skipped stale/ambiguous edits", ""])
    if conflicts:
        lines.extend(conflicts)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "Stale or ambiguous edits were deliberately not applied. Exact current manuscript authority wins.",
            "",
        ]
    )
    return "\n".join(lines)


def integrate(
    *,
    patch_ref: str,
    min_chapter: int = 1,
    max_chapter: int = 430,
    write: bool = False,
    report_path: Path = REPORT,
) -> tuple[dict[str, Stats], list[str], list[str]]:
    attr, var = load_approved_patches(patch_ref, min_chapter, max_chapter)
    by_chapter: dict[int, list[IntegrationPatch]] = {}
    for patch in merge_patch_sets(attr, var):
        by_chapter.setdefault(patch.chapter, []).append(patch)

    stats = {"attribution": Stats(), "variance": Stats()}
    conflicts: list[str] = []
    changed_files: list[str] = []
    authorities = authority_index()
    source_cache: dict[Path, str] = {}

    for chapter in sorted(by_chapter):
        patches = by_chapter[chapter]
        if chapter <= 155:
            path = CHAPTERS / f"{chapter:03d}.html"
            if not path.exists():
                conflicts.append(f"- Chapter {chapter}: **MISSING AUTHORITY** — `{path}`")
                continue
            original = path.read_text(encoding="utf-8")
            updated = apply_patches_to_html(original, patches, stats, conflicts)
            if updated != original:
                article = attribution.ARTICLE_RE.search(updated)
                if article and "—" in attribution._plain_text(article.group(2)):
                    raise RuntimeError(f"em dash found after integration in {path}")
                if write:
                    path.write_text(updated, encoding="utf-8")
                changed_files.append(str(path.relative_to(ROOT)))
            continue

        path = authorities.get(chapter)
        if path is None:
            conflicts.append(
                f"- Chapter {chapter}: **MISSING AUTHORITY** — no recovered/running/checkpoint source resolved"
            )
            continue
        text = source_cache.get(path)
        if text is None:
            text = path.read_text(encoding="utf-8")
        updated, changed = apply_patches_to_markdown_chapter(
            text, chapter, patches, stats, conflicts
        )
        source_cache[path] = updated
        relative = str(path.relative_to(ROOT))
        if changed and relative not in changed_files:
            changed_files.append(relative)

    if write:
        for path, text in source_cache.items():
            original = path.read_text(encoding="utf-8")
            if text != original:
                path.write_text(text, encoding="utf-8")

    report = _render_report(
        patch_ref,
        min_chapter,
        max_chapter,
        len(attr),
        len(var),
        stats,
        sorted(changed_files),
        conflicts,
    )
    if write:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")

    return stats, conflicts, sorted(changed_files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replay approved dialogue manifests onto current manuscript authority without overwriting drift."
    )
    parser.add_argument("--patch-ref", default="origin/editor/voice-compression-pass")
    parser.add_argument("--min-chapter", type=int, default=1)
    parser.add_argument("--max-chapter", type=int, default=430)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()

    stats, conflicts, changed = integrate(
        patch_ref=args.patch_ref,
        min_chapter=args.min_chapter,
        max_chapter=args.max_chapter,
        write=args.write,
        report_path=args.report,
    )
    print(
        "dialogue variance integration: "
        f"changed_files={len(changed)} conflicts={len(conflicts)} "
        f"attr(applied={stats['attribution'].applied},already={stats['attribution'].already},"
        f"stale={stats['attribution'].stale},ambiguous={stats['attribution'].ambiguous}) "
        f"variance(applied={stats['variance'].applied},already={stats['variance'].already},"
        f"stale={stats['variance'].stale},ambiguous={stats['variance'].ambiguous})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
