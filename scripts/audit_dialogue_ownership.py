#!/usr/bin/env python3
"""Audit showcased PLG prose for dialogue-ownership review candidates."""

from __future__ import annotations

import argparse
from collections import Counter
import html
import json
import re
from pathlib import Path

from dialogue_ownership import scan_paragraphs
from showcase import build_showcase_map, load_showcase_manifest


ARTICLE_RE = re.compile(
    r'<article\s+class=["\'][^"\']*\bprose\b[^"\']*["\'][^>]*>(.*?)</article>',
    re.IGNORECASE | re.DOTALL,
)
P_RE = re.compile(r'<p(?:\s[^>]*)?>(.*?)</p>', re.IGNORECASE | re.DOTALL)
BR_RE = re.compile(r'<br\s*/?>', re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')
SCANNER_VERSION = 1


def _plain_text(inner_html: str) -> str:
    value = BR_RE.sub("\n", inner_html)
    value = TAG_RE.sub("", value)
    return html.unescape(value).strip()


def extract_prose_paragraphs(document: str) -> list[str]:
    match = ARTICLE_RE.search(document)
    if not match:
        raise ValueError('chapter document has no article.prose')
    return [
        text
        for paragraph in P_RE.finditer(match.group(1))
        if (text := _plain_text(paragraph.group(1)))
    ]


def build_full_review_markdown(root: Path, start: int, end: int) -> str:
    """Return every prose paragraph in a chapter range, one review line each."""
    if start < 1 or end < start:
        raise ValueError(f'invalid review range: {start}-{end}')
    root = root.resolve()
    chapters_dir = root / 'chapters'
    lines = [
        '# PLG Full Dialogue Ownership Review Packet',
        '',
        f'- Canonical range: Chapters {start:03d}-{end:03d}',
        '- Derived review surface only. Canonical chapter HTML remains authority.',
        '- Every prose paragraph is present, including paragraphs the scanner did not flag.',
        '',
    ]
    for chapter in range(start, end + 1):
        path = chapters_dir / f'{chapter:03d}.html'
        if not path.exists():
            raise ValueError(f'missing canonical chapter: {path}')
        paragraphs = extract_prose_paragraphs(path.read_text(encoding='utf-8'))
        lines.extend([
            f'## Canon Chapter {chapter:03d}',
            '',
        ])
        for index, paragraph in enumerate(paragraphs, start=1):
            review_text = paragraph.replace('\\', '\\\\').replace('\n', '\\n')
            lines.append(f'P{index:04d} | {review_text}')
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def _canonical_numbers(chapters_dir: Path) -> list[int]:
    numbers: list[int] = []
    for path in chapters_dir.glob('*.html'):
        if path.stem.isdigit():
            numbers.append(int(path.stem))
    numbers = sorted(set(numbers))
    if not numbers:
        raise ValueError(f'no canonical chapter HTML found in {chapters_dir}')
    return numbers


def audit_chapters(root: Path, manifest_path: Path) -> dict:
    root = root.resolve()
    chapters_dir = root / 'chapters'
    canonical = _canonical_numbers(chapters_dir)
    manifest = load_showcase_manifest(manifest_path)
    showcase = build_showcase_map(canonical, manifest)

    candidates: list[dict[str, object]] = []
    for canon in showcase.visible_canon:
        path = chapters_dir / f'{canon:03d}.html'
        paragraphs = extract_prose_paragraphs(path.read_text(encoding='utf-8'))
        showcase_number = showcase.showcase_number(canon)
        if showcase_number is None:
            raise RuntimeError(f'visible canonical chapter {canon} lacks showcase number')
        for item in scan_paragraphs(paragraphs):
            candidates.append({
                'canonical_chapter': canon,
                'showcase_chapter': showcase_number,
                'paragraph_index': item.paragraph_index,
                'rule': item.rule,
                'confidence': item.confidence,
                'previous': item.previous,
                'current': item.current,
                'following': item.following,
                'fingerprint': item.fingerprint,
            })

    by_rule = Counter(str(item['rule']) for item in candidates)
    by_confidence = Counter(str(item['confidence']) for item in candidates)
    visible_count = len(showcase.visible_canon)
    return {
        'version': 1,
        'scanner_version': SCANNER_VERSION,
        'endpoint': max(canonical),
        'canonical_chapters': len(canonical),
        'visible_chapters': visible_count,
        'hidden_chapters': len(canonical) - visible_count,
        'candidate_count': len(candidates),
        'candidate_counts_by_rule': dict(sorted(by_rule.items())),
        'candidate_counts_by_confidence': dict(sorted(by_confidence.items())),
        'candidates': candidates,
    }


def _markdown(report: dict) -> str:
    lines = [
        '# PLG Dialogue Ownership Candidate Report',
        '',
        f'- Canon endpoint: Chapter {report["endpoint"]}',
        f'- Canonical chapters: {report["canonical_chapters"]}',
        f'- Visible showcase chapters: {report["visible_chapters"]}',
        f'- Hidden canon chapters skipped: {report["hidden_chapters"]}',
        f'- Review candidates: {report["candidate_count"]}',
        '',
        'This is a candidate queue, not a prose verdict. Exact local context decides whether a flagged action belongs to the speaker or creates false attribution.',
        '',
    ]
    for item in report['candidates']:
        lines.extend([
            f'## Canon {item["canonical_chapter"]} / Showcase {item["showcase_chapter"]} / Paragraph {item["paragraph_index"]}',
            '',
            f'- Rule: `{item["rule"]}`',
            f'- Confidence: `{item["confidence"]}`',
            f'- Fingerprint: `{item["fingerprint"]}`',
            '',
            'Previous:',
            '',
            f'> {item["previous"]}' if item['previous'] else '> [chapter boundary]',
            '',
            'Candidate:',
            '',
            f'> {item["current"]}',
            '',
            'Following:',
            '',
            f'> {item["following"]}' if item['following'] else '> [chapter boundary]',
            '',
        ])
    return '\n'.join(lines).rstrip() + '\n'


def write_reports(report: dict, json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    md_path.write_text(_markdown(report), encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument(
        '--manifest',
        type=Path,
        default=Path('publishing/showcase_chapters.json'),
    )
    parser.add_argument(
        '--json',
        type=Path,
        default=Path('state/editorial/dialogue-ownership-pass/CANDIDATES.json'),
    )
    parser.add_argument(
        '--markdown',
        type=Path,
        default=Path('state/editorial/dialogue-ownership-pass/CANDIDATES.md'),
    )
    parser.add_argument('--review-start', type=int)
    parser.add_argument('--review-end', type=int)
    parser.add_argument('--review-markdown', type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    manifest = args.manifest if args.manifest.is_absolute() else root / args.manifest
    json_path = args.json if args.json.is_absolute() else root / args.json
    md_path = args.markdown if args.markdown.is_absolute() else root / args.markdown

    report = audit_chapters(root, manifest)
    write_reports(report, json_path, md_path)

    if any(value is not None for value in (args.review_start, args.review_end, args.review_markdown)):
        if None in (args.review_start, args.review_end, args.review_markdown):
            parser.error('--review-start, --review-end, and --review-markdown must be supplied together')
        review_path = args.review_markdown
        if not review_path.is_absolute():
            review_path = root / review_path
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text(
            build_full_review_markdown(root, args.review_start, args.review_end),
            encoding='utf-8',
        )
        print(f'full review packet: chapters {args.review_start:03d}-{args.review_end:03d} -> {review_path}')

    print(
        f'dialogue ownership audit: {report["candidate_count"]} candidates across '
        f'{report["visible_chapters"]} visible chapters; '
        f'{report["hidden_chapters"]} hidden chapters skipped'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
