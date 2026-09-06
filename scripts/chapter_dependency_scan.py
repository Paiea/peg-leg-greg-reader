#!/usr/bin/env python3
"""Find chapter-number-coupled references that structural compression could break."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

TEXT_SUFFIXES = {'.html', '.md', '.json', '.py', '.txt', '.yaml', '.yml', '.js', '.css'}
PATTERNS = (
    ('reader_slug', re.compile(r'chapters/(\d{1,3})\.html')),
    ('chapter_art_path', re.compile(r'(?:visual/)?chapter_art/(\d{1,3})/')),
    ('chapter_text', re.compile(r'\bChapter\s+(\d{1,3})\b', re.I)),
    ('asset_name', re.compile(r'\bCh(\d{3})\b', re.I)),
)
SKIP_PREFIXES = ('.git/', '.worktrees/')


def scan_dependencies(root: Path) -> dict:
    root = root.resolve()
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    scanned = 0
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        if relative.startswith(SKIP_PREFIXES) or '__pycache__' in path.parts:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        scanned += 1
        for kind, pattern in PATTERNS:
            for match in pattern.finditer(text):
                number = str(int(match.group(1)))
                line = text.count('\n', 0, match.start()) + 1
                item = {'kind': kind, 'path': relative, 'line': line, 'match': match.group(0)}
                if item not in by_chapter[number]:
                    by_chapter[number].append(item)
    for refs in by_chapter.values():
        refs.sort(key=lambda row: (row['path'], row['line'], row['kind']))
    return {
        'schema_version': 1,
        'scanned_files': scanned,
        'chapters_with_dependencies': len(by_chapter),
        'reference_count': sum(len(rows) for rows in by_chapter.values()),
        'by_chapter': dict(sorted(by_chapter.items(), key=lambda item: int(item[0]))),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=Path('publishing/chapter_dependency_report.json'))
    parser.add_argument('--stdout', action='store_true')
    args = parser.parse_args()
    payload = scan_dependencies(args.root)
    if args.stdout:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        output = args.output if args.output.is_absolute() else args.root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(f'wrote {payload["reference_count"]} chapter-coupled references to {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
