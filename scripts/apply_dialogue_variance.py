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
BATCH_NAME_RE = re.compile(r'BATCH_(\d+)_(\d+)\.md')


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

        patch_header = lines[i].startswith('### Patch')
        patch_match = re.match(r'^### Patch\s+([^\s—–-]+)', lines[i])
        if patch_header and not patch_match:
            raise AssertionError(f'malformed Patch header: {lines[i].strip()}')
        if patch_match and chapter is None:
            raise AssertionError(f'{patch_match.group(1)}: Patch appears before a Chapter heading')
        if not patch_match:
            i += 1
            continue

        patch_id = patch_match.group(1)
        section_end = i + 1
        while section_end < len(lines) and not lines[section_end].startswith('### ') and not lines[section_end].startswith('## Chapter '):
            section_end += 1
        section = lines[i + 1:section_end]
        current_indices = [
            j for j, line in enumerate(section)
            if line.strip().lower().startswith('current')
        ]
        replace_indices = [
            j for j, line in enumerate(section)
            if line.strip().lower().startswith('replace')
        ]
        if len(current_indices) > 1:
            raise AssertionError(f'{patch_id}: duplicate Current section')
        if len(replace_indices) > 1:
            raise AssertionError(f'{patch_id}: duplicate Replace section')
        current_idx = current_indices[0] if current_indices else None
        replace_idx = replace_indices[0] if replace_indices else None
        if current_idx is None:
            raise AssertionError(f'{patch_id}: missing Current section')
        if replace_idx is None:
            raise AssertionError(f'{patch_id}: missing Replace section')
        if replace_idx <= current_idx:
            raise AssertionError(f'{patch_id}: Replace section must follow Current section')
        reason_idx = next((j for j in range(replace_idx + 1, len(section)) if section[j].strip().lower().startswith('reason:')), len(section))
        current = _code_lines(section[current_idx + 1:replace_idx])
        replacement = _code_lines(section[replace_idx + 1:reason_idx])
        if not current:
            raise AssertionError(f'{patch_id}: has no Current prose')
        if not replacement:
            raise AssertionError(f'{patch_id}: has no replacement prose')
        if any('—' in line for line in replacement):
            raise AssertionError(f'{patch_id}: replacement prose contains an em dash')
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


def _literal_pattern(text: str) -> str:
    parts: list[str] = []
    for char in text:
        if char == '"':
            parts.append('["“”]')
        elif char == "'":
            parts.append("['‘’]")
        else:
            parts.append(re.escape(char))
    return ''.join(parts)


def _sequence_pattern(lines: list[str]) -> re.Pattern[str]:
    if not lines:
        raise AssertionError('cannot match empty dialogue sequence')
    literals = [line for line in lines if line != '...']
    if not literals:
        raise AssertionError('dialogue sequence cannot contain only an ellipsis')

    parts = [_literal_pattern(literals[0])]
    separator = rf'(?:\s|{FIGURE_TOKEN_RE})*'
    gap_index = 0
    pending_ellipsis = False
    first_literal_seen = False
    for line in lines:
        if line == '...':
            if not first_literal_seen:
                raise AssertionError('dialogue ellipsis must follow a literal line')
            pending_ellipsis = True
            continue
        if not first_literal_seen:
            first_literal_seen = True
            continue
        gap_pattern = r'.*?' if pending_ellipsis else separator
        parts.append(rf'(?P<gap{gap_index}>{gap_pattern})')
        parts.append(_literal_pattern(line))
        gap_index += 1
        pending_ellipsis = False
    if pending_ellipsis:
        raise AssertionError('dialogue ellipsis must precede a literal line')
    return re.compile(''.join(parts), re.S)


def _reader_typography(text: str, matched: str) -> str:
    if '“' in matched or '”' in matched:
        text = re.sub(r'"([^"\n]*)"', lambda m: f'“{m.group(1)}”', text)
    if '’' in matched:
        text = re.sub(r"(?<=\w)'(?=\w)", '’', text)
    return text


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


def _replacement_with_preserved_gaps(match: re.Match[str], replacement: list[str], target: list[str]) -> str:
    styled = [_reader_typography(line, match.group(0)) for line in replacement]
    literal_count = sum(line != '...' for line in target)
    gaps = [match.group(f'gap{i}') for i in range(max(0, literal_count - 1))]
    has_ellipsis = '...' in target

    if not has_ellipsis and len(styled) == literal_count:
        pieces = [styled[0]]
        for idx, line in enumerate(styled[1:]):
            pieces.append(gaps[idx])
            pieces.append(line)
        return ''.join(pieces)

    figures = re.findall(FIGURE_TOKEN_RE, match.group(0))
    text = '\n\n'.join(styled)
    if figures:
        missing_figures = [figure for figure in figures if figure not in text]
        if missing_figures:
            if len(styled) > 1:
                first, rest = text.split('\n\n', 1)
                text = first + '\n\n' + '\n\n'.join(missing_figures) + '\n\n' + rest
            else:
                text += '\n\n' + '\n\n'.join(missing_figures)
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
        lambda match: _replacement_with_preserved_gaps(match, patch.replacement, target),
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
        match = BATCH_NAME_RE.fullmatch(path.name)
        if match and int(match.group(1)) < edge:
            selected.append(path)
    return selected


def validate_batch_contract(edge: int, batches: list[Path]) -> list[Patch]:
    if not batches:
        raise AssertionError('no completed sequential dialogue variance batches found')

    ranged: list[tuple[int, int, Path]] = []
    for path in batches:
        match = BATCH_NAME_RE.fullmatch(path.name)
        if not match:
            raise AssertionError(f'unrecognized dialogue variance batch name: {path.name}')
        start, end = map(int, match.groups())
        if start > end:
            raise AssertionError(f'{path.name}: batch range is reversed')
        ranged.append((start, end, path))
    ranged.sort(key=lambda item: (item[0], item[1], item[2].name))

    expected_start = 1
    for start, end, path in ranged:
        if start < expected_start:
            raise AssertionError(
                f'{path.name}: batch range overlap; expected Chapter {expected_start}, found {start}'
            )
        if start > expected_start:
            if expected_start == 1:
                raise AssertionError(f'sequential dialogue variance batches must start at Chapter 1, found {start}')
            raise AssertionError(
                f'dialogue variance batch gap before {path.name}: expected Chapter {expected_start}, found {start}'
            )
        if end >= edge:
            raise AssertionError(
                f'{path.name}: batch extends beyond reviewed edge {edge}; last reviewed chapter is {edge - 1}'
            )
        expected_start = end + 1

    if expected_start != edge:
        raise AssertionError(
            f'dialogue variance batch gap before reviewed edge {edge}: expected Chapter {expected_start}'
        )

    patches: list[Patch] = []
    seen_patch_ids: dict[str, str] = {}
    for start, end, path in ranged:
        batch_text = path.read_text(encoding='utf-8')
        if not batch_text.strip():
            raise AssertionError(f'{path.name}: contains no patches or review content')
        batch_patches = parse_batch(batch_text)
        for patch in batch_patches:
            if not start <= patch.chapter <= end:
                raise AssertionError(
                    f'{patch.patch_id}: Chapter {patch.chapter} is outside batch range {start}-{end} in {path.name}'
                )
            if patch.patch_id in seen_patch_ids:
                raise AssertionError(
                    f'duplicate patch id {patch.patch_id}: {seen_patch_ids[patch.patch_id]} and {path.name}'
                )
            seen_patch_ids[patch.patch_id] = path.name
        patches.extend(batch_patches)
    return patches


def integrate(*, write: bool = True) -> tuple[int, int]:
    edge = reviewed_edge()
    batches = selected_batches(edge)
    patches = validate_batch_contract(edge, batches)

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
