#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

EXPECTED_SCENES = [
    'ch002-antonius-loan',
    'ch007-antonius-storeroom',
    'ch013-arlo-workshop',
    'ch016-jorren-alden-greg',
    'ch018-hessa-beans',
]
REQUIRED_REPORT_HEADINGS = [
    '## Dramatic Truth Gate',
    '## Behavioral Realization Gate',
    '## Exchange Rhythm Gate',
    '## Swap / Confusability Check',
    '## Source Comparison',
    '## Scene Verdict',
]
FORBIDDEN_OWNER_WORDS = {'I', 'HE', 'SHE', 'THEY', 'HIM', 'HER', 'THEM'}
BEAT_RE = re.compile(r'^\[(B\d{3,})\]\s+(.+?)\s+\[(ACTION|DIALOGUE|THOUGHT)\]\s*$')


def _owner_is_named(owner: str) -> bool:
    return owner.strip().upper() not in FORBIDDEN_OWNER_WORDS and bool(re.fullmatch(r'[A-Z][A-Z0-9_ -]*', owner.strip()))


def _check_performed(path: Path, fixture_text: str) -> list[str]:
    findings: list[str] = []
    text = path.read_text(encoding='utf-8')
    beats: set[str] = set()

    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.startswith('[B'):
            continue
        m = BEAT_RE.match(line)
        if not m:
            if '[DIALOGUE]' in line and '->' not in line:
                findings.append(f'{path}: line {line_no}: dialogue requires explicit addressee')
            else:
                findings.append(f'{path}: line {line_no}: malformed performed beat header')
            continue
        beat_id, owner_expr, kind = m.groups()
        beats.add(beat_id)
        if kind == 'DIALOGUE':
            if '->' not in owner_expr:
                findings.append(f'{path}: line {line_no}: dialogue requires explicit addressee')
                continue
            speaker, addressee = [x.strip() for x in owner_expr.split('->', 1)]
            for role, value in [('speaker', speaker), ('addressee', addressee)]:
                if not _owner_is_named(value):
                    findings.append(f'{path}: line {line_no}: pronoun owner not allowed for dialogue {role}: {value}')
        else:
            owner = owner_expr.strip()
            if '->' in owner or not _owner_is_named(owner):
                findings.append(f'{path}: line {line_no}: pronoun owner not allowed for {kind.lower()}: {owner}')
            if kind == 'THOUGHT' and owner != 'GREG' and f'POV AUTHORIZED: {owner}' not in fixture_text:
                findings.append(f'{path}: line {line_no}: non-Greg thought lacks POV authorization for {owner}')

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('BASELINE BEND:') and 'material' in line.lower() and 'none material' not in line.lower():
            realized = None
            for j in range(i + 1, min(i + 7, len(lines))):
                if lines[j].startswith('REALIZED BY:'):
                    realized = lines[j]
                    break
                if lines[j].startswith('### ') or lines[j].startswith('## '):
                    break
            if realized is None:
                findings.append(f'{path}: material BASELINE BEND requires REALIZED BY')
                continue
            refs = re.findall(r'B\d{3,}', realized)
            if not refs:
                findings.append(f'{path}: REALIZED BY must contain at least one beat reference')
            for ref in refs:
                if ref not in beats:
                    findings.append(f'{path}: REALIZED BY references missing beat {ref}')

    return findings


def check_lab(root: Path) -> list[str]:
    findings: list[str] = []
    if not root.exists():
        return [f'{root}: lab root does not exist']

    for required in ['README.md', 'authority.lock.json']:
        if not (root / required).exists():
            findings.append(f'{root}: missing {required}')

    for path in root.rglob('*'):
        if not path.is_file():
            continue
        name = path.name.lower()
        if name == 'canon.patch' or name.startswith('novel') or name.startswith('prose'):
            findings.append(f'{path}: forbidden artifact at pre-novelization stop boundary')
        if '—' in path.read_text(encoding='utf-8', errors='ignore') and path.name in {'performed.md'}:
            findings.append(f'{path}: em dash found in performed script artifact')

    scenes_root = root / 'scenes'
    if not scenes_root.exists():
        findings.append(f'{root}: missing scenes directory')
        return findings

    actual = sorted(p.name for p in scenes_root.iterdir() if p.is_dir())
    if actual != sorted(EXPECTED_SCENES):
        findings.append(f'{scenes_root}: expected exactly five scene directories')

    for scene in EXPECTED_SCENES:
        d = scenes_root / scene
        if not d.exists():
            findings.append(f'{d}: missing scene directory')
            continue
        required_paths = {name: d / name for name in ['fixture.md', 'performed.md', 'report.md']}
        for name, path in required_paths.items():
            if not path.exists():
                findings.append(f'{d}: missing {name}')
        fixture = required_paths['fixture.md']
        if fixture.exists():
            fixture_text = fixture.read_text(encoding='utf-8')
            for field in ['SOURCE REF:', 'SOURCE PATH:', 'SOURCE BLOB:', '## DRAMATIC SCRIPT']:
                if field not in fixture_text:
                    findings.append(f'{fixture}: missing {field}')
        else:
            fixture_text = ''
        performed = required_paths['performed.md']
        if performed.exists():
            findings.extend(_check_performed(performed, fixture_text))
        report = required_paths['report.md']
        if report.exists():
            report_text = report.read_text(encoding='utf-8')
            for heading in REQUIRED_REPORT_HEADINGS:
                if heading not in report_text:
                    findings.append(f'{report}: missing {heading}')

    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    args = ap.parse_args()
    findings = check_lab(args.root)
    if findings:
        for finding in findings:
            print(finding)
        return 1
    print('PERFORMANCE lab structural check passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
