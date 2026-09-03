#!/usr/bin/env python3
"""Run Book 1 dialogue integration with explicit current-main drift overrides.

The durable editorial batches remain the default authority. This wrapper applies
small, reviewed overrides only where current `main` contains preserved prose
beats that an editorial batch abbreviated. Overrides never enable fuzzy
matching: they replace one patch's exact current/replacement tuples and then the
strict base integrator still requires an exact unique match.

Reader typography is normalized only for matching. Book I contains both straight
and curly quotation/apostrophe styles, while the editorial patch notes use
straight quotes. Replacement prose inherits the typography of the paragraph it
replaces.

During validation, unresolved patches are collected across all chapters and
reported together. Successful patches may modify the temporary CI checkout,
but the run still fails before source promotion until every mismatch has an
explicit reviewed resolution.
"""

from __future__ import annotations

import json
from pathlib import Path

import apply_dialogue_attribution_patches as base


OVERRIDES_PATH = Path("state/editorial/dialogue-live-overrides.json")


def _load_overrides() -> dict[str, dict[str, object]]:
    if not OVERRIDES_PATH.exists():
        return {}
    data = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"{OVERRIDES_PATH} must contain a JSON object")
    return data


def _values(raw: object, key: str) -> tuple[str, ...]:
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise RuntimeError(f"override {key} must be a list of strings")
    return tuple(base.GAP if item == "..." else item for item in raw)


def _match_text(text: str, *, canonical: bool = False) -> str:
    value = (
        text.replace("“", '"')
        .replace("”", '"')
        .replace("„", '"')
        .replace("’", "'")
        .replace("‘", "'")
        .replace("\u00a0", " ")
    )
    return base._canonicalize_names(value) if canonical else value


def _find_sequence(paragraphs: list[base.Paragraph], wanted: tuple[str, ...], *, canonical: bool = False) -> list[int]:
    if not wanted:
        return []
    wanted_norm = tuple(_match_text(value, canonical=canonical) for value in wanted)
    texts = [_match_text(paragraph.text, canonical=canonical) for paragraph in paragraphs]
    width = len(wanted_norm)
    return [
        index
        for index in range(0, len(texts) - width + 1)
        if tuple(texts[index : index + width]) == wanted_norm
    ]


def _smart_double_quotes(text: str) -> str:
    out: list[str] = []
    opening = True
    for char in text:
        if char == '"':
            out.append("“" if opening else "”")
            opening = not opening
        else:
            out.append(char)
    return "".join(out)


def _style_like(text: str, sample: str) -> str:
    value = text
    if ("“" in sample or "”" in sample) and '"' in value:
        value = _smart_double_quotes(value)
    if "’" in sample and "'" in value:
        value = value.replace("'", "’")
    return value


def _replace_exact_segment(article_body: str, patch: base.Patch) -> tuple[str, str]:
    paragraphs = base._paragraphs(article_body)

    replacement_hits = _find_sequence(paragraphs, patch.replacement)
    if not replacement_hits:
        replacement_hits = _find_sequence(paragraphs, patch.replacement, canonical=True)
    if len(replacement_hits) == 1:
        return article_body, "already"
    if len(replacement_hits) > 1:
        raise RuntimeError(
            f"{patch.source_file} {patch.label}: replacement appears {len(replacement_hits)} times in chapter {patch.chapter}"
        )

    hits = _find_sequence(paragraphs, patch.current)
    if not hits:
        hits = _find_sequence(paragraphs, patch.current, canonical=True)
    if len(hits) != 1:
        raise RuntimeError(
            f"{patch.source_file} {patch.label}: expected current text exactly once in chapter {patch.chapter}, found {len(hits)}"
        )

    index = hits[0]
    old_nodes = paragraphs[index : index + len(patch.current)]

    if len(old_nodes) == len(patch.replacement):
        edits: list[tuple[int, int, str]] = []
        for node, new_text in zip(old_nodes, patch.replacement):
            raw = article_body[node.start : node.end]
            open_end = raw.find(">") + 1
            close_start = raw.lower().rfind("</p>")
            styled = _style_like(new_text, node.text)
            new_raw = raw[:open_end] + base._html_for_text(styled) + raw[close_start:]
            edits.append((node.start, node.end, new_raw))
        for start, end, new_raw in reversed(edits):
            article_body = article_body[:start] + new_raw + article_body[end:]
        return article_body, "applied"

    first, last = old_nodes[0], old_nodes[-1]
    between = article_body[first.start : last.end]
    stripped = base.P_RE.sub("", between)
    if stripped.strip():
        raise RuntimeError(
            f"{patch.source_file} {patch.label}: paragraph-count-changing patch crosses non-paragraph markup"
        )
    sample = " ".join(node.text for node in old_nodes)
    new_block = "".join(
        f"<p>{base._html_for_text(_style_like(text, sample))}</p>"
        for text in patch.replacement
    )
    article_body = article_body[: first.start] + new_block + article_body[last.end :]
    return article_body, "applied"


def main() -> int:
    overrides = _load_overrides()
    original_load_patches = base.load_patches
    errors: list[str] = []

    def load_patches_with_overrides(ref: str, min_chapter: int, max_chapter: int):
        patches = original_load_patches(ref, min_chapter, max_chapter)
        seen: set[str] = set()
        result: list[base.Patch] = []
        for patch in patches:
            key = f"{patch.chapter}|{patch.label}"
            override = overrides.get(key)
            if override is None:
                result.append(patch)
                continue
            if not isinstance(override, dict):
                raise RuntimeError(f"override {key} must be an object")
            current = _values(override.get("current"), f"{key}.current")
            replacement = _values(override.get("replacement"), f"{key}.replacement")
            result.append(
                base.Patch(
                    chapter=patch.chapter,
                    label=patch.label,
                    current=current,
                    replacement=replacement,
                    source_file=f"{OVERRIDES_PATH} overriding {patch.source_file}",
                )
            )
            seen.add(key)

        unused = sorted(set(overrides) - seen)
        if unused:
            raise RuntimeError(f"unused dialogue live overrides: {unused}")
        return result

    def apply_collecting(path: Path, patches: list[base.Patch], canonicalize: bool):
        original = path.read_text(encoding="utf-8")
        match = base.ARTICLE_RE.search(original)
        if not match:
            errors.append(f"no article.prose found in {path}")
            return False, {"applied": 0, "already": 0, "name_paragraphs": 0}

        body = match.group(2)
        stats = {"applied": 0, "already": 0, "name_paragraphs": 0}
        for patch in patches:
            try:
                body, status = base._replace_patch(body, patch)
            except RuntimeError as exc:
                errors.append(str(exc))
                continue
            stats[status] += 1

        if canonicalize:
            body, name_changes = base._canonicalize_article_paragraphs(body)
            stats["name_paragraphs"] += name_changes

        updated = original[: match.start(2)] + body + original[match.end(2) :]
        if "—" in base._plain_text(body):
            errors.append(f"em dash found in prose after integration: {path}")
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            return True, stats
        return False, stats

    base.load_patches = load_patches_with_overrides
    base._replace_exact_segment = _replace_exact_segment
    base.apply_to_chapter = apply_collecting
    result = base.main()

    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise RuntimeError(
            f"dialogue integration has {len(errors)} unresolved exact-match issue(s):\n{joined}"
        )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
