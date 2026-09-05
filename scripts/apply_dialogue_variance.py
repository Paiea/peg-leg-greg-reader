#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'state' / 'editorial' / 'DIALOGUE_VARIANCE_PASS_STATE.md'
BATCH_DIR = ROOT / 'state' / 'editorial' / 'dialogue-variance-pass'
CHAPTERS = ROOT / 'chapters'
FIGURE_TOKEN_RE = r'\[\[\[PLG_FIGURE_\d+\]\]\]'
INLINE_TOKEN_RE = r'\[\[\[PLG_INLINE_\d+\]\]\]'


@dataclass(frozen=True)
class Patch:
    chapter: int
    patch_id: str
    current: list[str]
    replacement: list[str]
    directive: str


def _code_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if len(stripped) >= 2 and stripped.startswith('`') and stripped.endswith('`'):
            out.append(stripped[1:-1])
    return out


def parse_batch(text: str) -> list[Patch]:
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    patches: list[Patch] = []
    chapter: int | None = None
    i = 0
    while i < len(lines):
        chapter_match = re.match(r'^## Chapter\s+(\d+)\b', lines[i])
        if chapter_match:
            chapter = int(chapter_match.group(1))
            i += 1
            continue
        patch_match = re.match(r'^### Patch\s+([^\s—–-]+)', lines[i])
        if not patch_match or chapter is None:
            i += 1
            continue
        patch_id = patch_match.group(1)
        section_end = i + 1
        while section_end < len(lines) and not lines[section_end].startswith('### ') and not lines[section_end].startswith('## Chapter '):
            section_end += 1
        section = lines[i + 1:section_end]
        current_idx = next((j for j, line in enumerate(section) if line.strip().lower().startswith('current')), None)
        replace_idx = next((j for j, line in enumerate(section) if line.strip().lower().startswith('replace')), None)
        if current_idx is not None and replace_idx is not None and replace_idx > current_idx:
            reason_idx = next((j for j in range(replace_idx + 1, len(section)) if section[j].strip().lower().startswith('reason:')), len(section))
            current = _code_lines(section[current_idx + 1:replace_idx])
            replacement = _code_lines(section[replace_idx + 1:reason_idx])
            if current and replacement:
                patches.append(Patch(chapter, patch_id, current, replacement, section[replace_idx].strip()))
        i = section_end
    return patches


def _protect_inline(inner: str, sentinels: dict[str, str], counter: list[int]) -> str:
    def protect(match: re.Match[str]) -> str:
        token = f'[[[PLG_INLINE_{counter[0]}]]]'
        counter[0] += 1
        sentinels[token] = match.group(0)
        return token

    protected = re.sub(r'<[^>]+>', protect, inner)
    return html.unescape(protected)


def _sequence_pattern(lines: list[str]) -> re.Pattern[str]:
    if not lines:
        raise AssertionError('cannot match empty dialogue sequence')
    parts = [re.escape(lines[0])]
    separator = rf'(?:\s|{FIGURE_TOKEN_RE})*'
    for idx, line in enumerate(lines[1:]):
        parts.append(rf'(?P<gap{idx}>{separator})')
        parts.append(re.escape(line))
    return re.compile(''.join(parts), re.S)


def _target_lines(patch: Patch) -> list[str]:
    directive = patch.directive
    lowered = directive.lower()

    if 'replace after' in lowered:
        anchors = re.findall(r'`([^`]+)`', directive)
        for anchor in reversed(anchors):
            matching = [idx for idx, line in enumerate(patch.current) if anchor in line]
            if len(matching) > 1:
                raise AssertionError(f'{patch.patch_id}: directive anchor {anchor!r} is ambiguous')
            if len(matching) == 1:
                idx = matching[0]
                if idx + 1 < len(patch.current):
                    return patch.current[idx + 1:]

    if patch.replacement and patch.replacement[0] in patch.current:
        idx = patch.current.index(patch.replacement[0])
        if idx > 0:
            return patch.current[idx:]
    if 'final' in lowered and patch.replacement[0] not in patch.current:
        return patch.current[-1:]
    if 'first' in lowered and patch.replacement[0] not in patch.current:
        return patch.current[:1]
    return patch.current


def _replacement_with_preserved_gaps(match: re.Match[str], replacement: list[str], target_count: int) -> str:
    gaps = [match.group(f'gap{i}') for i in range(max(0, target_count - 1))]
    if len(replacement) == target_count:
        pieces = [replacement[0]]
        for idx, line in enumerate(replacement[1:]):
            pieces.append(gaps[idx])
            pieces.append(line)
        return ''.join(pieces)

    figures: list[str] = []
    for gap in gaps:
        figures.extend(re.findall(FIGURE_TOKEN_RE, gap))
    text = '\n\n'.join(replacement)
    if figures:
        if len(replacement) > 1:
            first, rest = text.split('\n\n', 1)
            text = first + '\n\n' + '\n\n'.join(figures) + '\n\n' + rest
        else:
            text += '\n\n' + '\n\n'.join(figures)
    return text


def apply_patch_to_html(page: str, patch: Patch) -> str:
    article_match = re.search(r'(<article\b[^>]*class=["\'][^"\']*\bprose\b[^"\']*["\'][^>]*>)(.*?)(</article>)', page, re.I | re.S)
    if not article_match:
        raise AssertionError(f'{patch.patch_id}: chapter {patch.chapter} has no prose article')
    inner = article_match.group(2)
    block_re = re.compile(r'<figure\b.*?</figure>|<p\b[^>]*>.*?</p>', re.I | re.S)
    blocks = block_re.findall(inner)
    if not blocks:
        raise AssertionError(f'{patch.patch_id}: chapter {patch.chapter} has no prose blocks')

    sentinels: dict[str, str] = {}
    inline_counter = [0]
    plain_blocks: list[str] = []
    for idx, block in enumerate(blocks):
        if block.lower().startswith('<figure'):
            token = f'[[[PLG_FIGURE_{idx}]]]'
            sentinels[token] = block
            plain_blocks.append(token)
            continue
        p = re.match(r'<p\b[^>]*>(.*?)</p>', block, re.I | re.S)
        if not p:
            raise AssertionError(f'{patch.patch_id}: malformed paragraph')
        plain_blocks.append(_protect_inline(p.group(1), sentinels, inline_counter))

    stream = '\n\n'.join(plain_blocks)
    target = _target_lines(patch)
    target_pattern = _sequence_pattern(target)
    matches = list(target_pattern.finditer(stream))
    replacement_pattern = _sequence_pattern(patch.replacement)
    if not matches:
        if replacement_pattern.search(stream):
            return page
        raise AssertionError(f'{patch.patch_id}: approved current prose not found in chapter {patch.chapter}')
    if len(matches) != 1:
        raise AssertionError(f'{patch.patch_id}: approved current prose matched {len(matches)} times in chapter {patch.chapter}')

    stream = target_pattern.sub(
        lambda match: _replacement_with_preserved_gaps(match, patch.replacement, len(target)),
        stream,
        count=1,
    )
    rebuilt: list[str] = []
    for block in stream.split('\n\n'):
        if block in sentinels and block.startswith('[[[PLG_FIGURE_'):
            rebuilt.append(sentinels[block])
            continue
        escaped = html.escape(block, quote=False)
        for token, original in sentinels.items():
            if token.startswith('[[[PLG_INLINE_'):
                escaped = escaped.replace(token, original)
        rebuilt.append(f'<p>{escaped}</p>')
    new_inner = ''.join(rebuilt)
    return page[:article_match.start(2)] + new_inner + page[article_match.end(2):]


def reviewed_edge() -> int:
    text = STATE.read_text(encoding='utf-8')
    match = re.search(r'Current sequential variance edge:\s*\*\*Chapter\s+(\d+)\*\*', text)
    if not match:
        raise AssertionError('could not resolve sequential dialogue variance edge')
    return int(match.group(1))


def selected_batches(edge: int) -> list[Path]:
    selected: list[Path] = []
    for path in sorted(BATCH_DIR.glob('BATCH_*.md')):
        match = re.fullmatch(r'BATCH_(\d+)_(\d+)\.md', path.name)
        if match and int(match.group(2)) < edge:
            selected.append(path)
    return selected


def integrate(*, write: bool = True) -> tuple[int, int]:
    edge = reviewed_edge()
    batches = selected_batches(edge)
    if not batches:
        raise AssertionError('no completed sequential dialogue variance batches found')
    patches: list[Patch] = []
    for path in batches:
        patches.extend(parse_batch(path.read_text(encoding='utf-8')))

    changed_chapters = 0
    applied = 0
    by_chapter: dict[int, list[Patch]] = {}
    for patch in patches:
        by_chapter.setdefault(patch.chapter, []).append(patch)
    for chapter, chapter_patches in sorted(by_chapter.items()):
        path = CHAPTERS / f'{chapter:03d}.html'
        if not path.is_file():
            raise AssertionError(f'missing published Chapter {chapter}')
        original = path.read_text(encoding='utf-8')
        page = original
        for patch in chapter_patches:
            updated = apply_patch_to_html(page, patch)
            if updated != page:
                applied += 1
            page = updated
        if page != original:
            changed_chapters += 1
            if write:
                path.write_text(page, encoding='utf-8')
    print(f'dialogue variance edge {edge}: {len(patches)} approved patches, {applied} newly applied across {changed_chapters} chapters')
    return applied, changed_chapters


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='validate without writing')
    args = parser.parse_args()
    integrate(write=not args.check)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
