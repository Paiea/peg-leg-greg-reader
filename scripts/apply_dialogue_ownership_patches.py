#!/usr/bin/env python3
"""Apply reviewed, exact paragraph-level dialogue ownership patches.

The manifest is authority for every prose change this tool may make. Current
paragraph sequences must match exactly once, or the already-approved replacement
must already match exactly once. No fuzzy matching and no speaker inference are
performed here.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import html
import json
import re
from pathlib import Path

ARTICLE_RE = re.compile(r'(<article\s+class=["\'][^"\']*\bprose\b[^"\']*["\'][^>]*>)(.*?)(</article>)', re.I | re.S)
P_RE = re.compile(r'<p(?:\s[^>]*)?>(.*?)</p>', re.I | re.S)
BR_RE = re.compile(r'<br\s*/?>', re.I)
TAG_RE = re.compile(r'<[^>]+>')


@dataclass(frozen=True)
class Patch:
    chapter: int
    label: str
    current: tuple[str, ...]
    replacement: tuple[str, ...]


@dataclass(frozen=True)
class Paragraph:
    start: int
    end: int
    text: str


def _plain(inner: str) -> str:
    value = BR_RE.sub('\n', inner)
    value = TAG_RE.sub('', value)
    return html.unescape(value)


def _html_text(text: str) -> str:
    return html.escape(text, quote=False).replace('\n', '<br/>')


def _paragraphs(body: str) -> list[Paragraph]:
    return [
        Paragraph(match.start(), match.end(), _plain(match.group(1)))
        for match in P_RE.finditer(body)
    ]


def _hits(paragraphs: list[Paragraph], wanted: tuple[str, ...]) -> list[int]:
    texts = [p.text for p in paragraphs]
    width = len(wanted)
    if not width:
        return []
    return [
        index
        for index in range(len(texts) - width + 1)
        if tuple(texts[index:index + width]) == wanted
    ]


def _load_manifest(path: Path) -> list[Patch]:
    payload = json.loads(path.read_text(encoding='utf-8'))
    if payload.get('version') != 1:
        raise RuntimeError(f'unsupported dialogue ownership manifest version: {payload.get("version")}')
    patches: list[Patch] = []
    for raw in payload.get('patches', []):
        patch = Patch(
            chapter=int(raw['chapter']),
            label=str(raw['label']),
            current=tuple(str(x) for x in raw['current']),
            replacement=tuple(str(x) for x in raw['replacement']),
        )
        if not patch.current or not patch.replacement:
            raise RuntimeError(f'empty current/replacement in patch {patch.label}')
        patches.append(patch)
    return patches


def _apply_patch(body: str, patch: Patch) -> tuple[str, str]:
    paragraphs = _paragraphs(body)
    replacement_hits = _hits(paragraphs, patch.replacement)
    if len(replacement_hits) == 1:
        return body, 'already'
    if len(replacement_hits) > 1:
        raise RuntimeError(
            f'chapter {patch.chapter} {patch.label}: replacement appears {len(replacement_hits)} times'
        )

    current_hits = _hits(paragraphs, patch.current)
    if len(current_hits) != 1:
        raise RuntimeError(
            f'chapter {patch.chapter} {patch.label}: current appears {len(current_hits)} times, expected exactly 1'
        )

    index = current_hits[0]
    old_nodes = paragraphs[index:index + len(patch.current)]
    first, last = old_nodes[0], old_nodes[-1]
    between = body[first.start:last.end]
    if P_RE.sub('', between).strip():
        raise RuntimeError(
            f'chapter {patch.chapter} {patch.label}: replacement would cross non-paragraph markup'
        )
    new_block = ''.join(f'<p>{_html_text(text)}</p>' for text in patch.replacement)
    return body[:first.start] + new_block + body[last.end:], 'applied'


def apply_manifest(manifest_path: Path, chapters_dir: Path) -> dict[str, int]:
    patches = _load_manifest(manifest_path)
    by_chapter: dict[int, list[Patch]] = {}
    for patch in patches:
        by_chapter.setdefault(patch.chapter, []).append(patch)

    stats = {'patches': len(patches), 'applied': 0, 'already': 0, 'files_changed': 0}
    for chapter, chapter_patches in sorted(by_chapter.items()):
        path = chapters_dir / f'{chapter:03d}.html'
        if not path.exists():
            raise RuntimeError(f'missing chapter page: {path}')
        original = path.read_text(encoding='utf-8')
        article = ARTICLE_RE.search(original)
        if not article:
            raise RuntimeError(f'no article.prose in {path}')
        body = article.group(2)
        for patch in chapter_patches:
            body, status = _apply_patch(body, patch)
            stats[status] += 1
        updated = original[:article.start(2)] + body + original[article.end(2):]
        if updated != original:
            path.write_text(updated, encoding='utf-8')
            stats['files_changed'] += 1
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--chapters-dir', type=Path, default=Path('chapters'))
    args = parser.parse_args()
    stats = apply_manifest(args.manifest, args.chapters_dir)
    print(
        'dialogue ownership patches: '
        f"patches={stats['patches']} applied={stats['applied']} "
        f"already={stats['already']} files_changed={stats['files_changed']}"
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
