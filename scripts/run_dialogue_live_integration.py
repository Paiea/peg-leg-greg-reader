#!/usr/bin/env python3
"""Run Book 1 dialogue integration with explicit current-main drift overrides.

The durable editorial batches remain the default authority. This wrapper applies
small, reviewed overrides only where current `main` contains preserved prose
beats that an editorial batch abbreviated. Overrides never enable fuzzy
matching: they replace one patch's exact current/replacement tuples and then the
strict base integrator still requires an exact unique match.

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
