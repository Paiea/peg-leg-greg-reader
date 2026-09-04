#!/usr/bin/env python3
"""Stable entrypoint for incremental dialogue live integration."""

from __future__ import annotations

import re
import sys

import run_dialogue_live_integration as impl


def _candidate_lt(self, other):
    if not isinstance(other, impl.Candidate):
        return NotImplemented
    return (
        self.paragraph_index,
        self.start,
        self.end,
        self.penalty,
    ) < (
        other.paragraph_index,
        other.start,
        other.end,
        other.penalty,
    )


def _arg_int(name: str, default: int) -> int:
    try:
        index = sys.argv.index(name)
    except ValueError:
        return default
    try:
        return int(sys.argv[index + 1])
    except (IndexError, ValueError) as exc:
        raise SystemExit(f"{name} requires an integer") from exc


def _modern_batch_to_legacy(content: str) -> str:
    """Normalize accepted newer patch-note syntax for the strict legacy parser.

    Consecutive Markdown blockquote lines belong to one prose paragraph unless a
    bare `>` separator appears between them. Folding them here preserves wrapped
    manuscript paragraphs instead of turning display wrapping into fake paragraph
    boundaries.
    """
    lines: list[str] = []
    quoted_parts: list[str] = []

    def flush_quote() -> None:
        if not quoted_parts:
            return
        value = " ".join(part.strip() for part in quoted_parts).replace("`", "\\`")
        lines.append(f"`{value}`")
        quoted_parts.clear()

    for raw in content.splitlines():
        if raw.startswith("> "):
            quoted_parts.append(raw[2:])
            continue
        if raw.strip() == ">":
            flush_quote()
            lines.append("")
            continue

        flush_quote()
        line = re.sub(r"^### Patch\b", "### Fix", raw, flags=re.IGNORECASE)
        if line.strip().lower() == "later:":
            line = "..."
        lines.append(line)
    flush_quote()
    return "\n".join(lines)


_original_parse_batch = impl.base._parse_batch


def _parse_batch_compat(content: str, source_file: str, min_chapter: int, max_chapter: int):
    return _original_parse_batch(
        _modern_batch_to_legacy(content), source_file, min_chapter, max_chapter
    )


impl.Candidate.__lt__ = _candidate_lt
impl.base._parse_batch = _parse_batch_compat

# Later continuity batches include tiny one-paragraph pronoun fixes that may sit
# inside a longer live paragraph. Keep the normal strict matcher first, then use
# a uniquely located substring only for one-paragraph patches. Also treat a
# repeated generic replacement as already applied only when the old text is gone.
_original_replace_exact_segment = impl._replace_exact_segment


def _replace_exact_segment_compat(article_body, patch):
    try:
        return _original_replace_exact_segment(article_body, patch)
    except RuntimeError as exc:
        message = str(exc)
        paragraphs = impl.base._paragraphs(article_body)
        if len(patch.current) == len(patch.replacement) == 1:
            current = impl._match_text(patch.current[0])
            replacement = patch.replacement[0]
            hits = []
            for index, node in enumerate(paragraphs):
                live = impl._match_text(node.text)
                start = live.find(current)
                if start >= 0:
                    hits.append((index, start, start + len(current)))
            if len(hits) == 1:
                index, start, end = hits[0]
                node = paragraphs[index]
                raw = article_body[node.start:node.end]
                open_end = raw.find(">") + 1
                close_start = raw.lower().rfind("</p>")
                text = node.text
                styled = impl._style_like(replacement, text)
                text = text[:start] + styled + text[end:]
                new_raw = raw[:open_end] + impl.base._html_for_text(text) + raw[close_start:]
                return article_body[:node.start] + new_raw + article_body[node.end:], "applied"
            if not hits and "replacement appears" in message:
                return article_body, "already"
        if "replacement appears" in message:
            current_hits = impl._find_sequence(paragraphs, patch.current)
            if not current_hits:
                current_hits = impl._find_sequence(paragraphs, patch.current, canonical=True)
            if not current_hits:
                return article_body, "already"
        raise


impl._replace_exact_segment = _replace_exact_segment_compat

# The override ledger contains reviewed drift exceptions from earlier publish
# increments. A later increment should require only overrides inside its own
# chapter range instead of failing because historical overrides are unused.
_original_load_overrides = impl._load_overrides


def _load_scoped_overrides():
    data = _original_load_overrides()
    min_chapter = _arg_int("--min-chapter", 6)
    max_chapter = _arg_int("--max-chapter", 80)
    scoped = {}
    for key, value in data.items():
        try:
            chapter = int(key.split("|", 1)[0])
        except (ValueError, IndexError) as exc:
            raise RuntimeError(f"invalid dialogue live override key: {key}") from exc
        if min_chapter <= chapter <= max_chapter:
            scoped[key] = value
    return scoped


impl._load_overrides = _load_scoped_overrides

# The legacy applicator uses --canonicalize-from as both the first chapter looped
# and the Book I name-map threshold. For Book II increments we need the full
# requested loop without applying the Book I Pell/Arlo map. A threshold above
# max-chapter is the explicit sentinel for that mode.
_requested_canonicalize_from = _arg_int("--canonicalize-from", 1)
_min_chapter = _arg_int("--min-chapter", 6)
_max_chapter = _arg_int("--max-chapter", 80)
_disable_canonicalize = _requested_canonicalize_from > _max_chapter
if _disable_canonicalize and "--canonicalize-from" in sys.argv:
    sys.argv[sys.argv.index("--canonicalize-from") + 1] = str(_min_chapter)

if _disable_canonicalize:
    impl.base._canonicalize_article_paragraphs = lambda body: (body, 0)


if __name__ == "__main__":
    raise SystemExit(impl.main())
