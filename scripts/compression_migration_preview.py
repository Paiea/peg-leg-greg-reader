#!/usr/bin/env python3
"""Preview structural chapter migrations without mutating manuscript or reader files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_preview(registry: dict, mapping: dict) -> dict:
    records = {row['chapter_id']: row for row in registry.get('chapters', [])}
    unknown = sorted(set(mapping) - set(records))
    if unknown:
        raise ValueError(f'unknown chapter ids in mapping: {unknown}')

    active = []
    aliases = {}
    art_migrations = []
    actions = []
    used_numbers = set()

    for chapter_id, source in records.items():
        directive = mapping.get(chapter_id, {
            'status': 'active',
            'display_number': source['current_display_number'],
        })
        status = directive.get('status', 'active')
        if status == 'active':
            number = int(directive.get('display_number', source['current_display_number']))
            if number in used_numbers:
                raise ValueError(f'duplicate active display number: {number}')
            used_numbers.add(number)
            slug = f'chapters/{number:03d}.html'
            active.append((number, chapter_id, slug))
            if source.get('public_slug') and source['public_slug'] != slug:
                aliases[source['public_slug']] = slug
            actions.append({'chapter_id': chapter_id, 'action': 'active', 'new_display_number': number})
            continue

        if status in {'merged', 'redirect'}:
            destination = directive.get('merged_into') or directive.get('redirect_to')
            if destination not in records:
                raise ValueError(f'{chapter_id} points to unknown destination {destination}')
            dest_directive = mapping.get(destination, {})
            dest_number = int(dest_directive.get('display_number', records[destination]['current_display_number']))
            dest_slug = f'chapters/{dest_number:03d}.html'
            if source.get('public_slug'):
                aliases[source['public_slug']] = dest_slug
            for asset in source.get('illustration_refs', []):
                art_migrations.append({
                    'asset_path': asset,
                    'source_chapter_id': chapter_id,
                    'destination_chapter_id': destination,
                    'proposed_disposition': 'REASSIGN_TO_SURVIVING_BEAT',
                })
            actions.append({'chapter_id': chapter_id, 'action': status, 'destination_chapter_id': destination})
            continue

        if status in {'cut', 'retired', 'archived'}:
            for asset in source.get('illustration_refs', []):
                art_migrations.append({
                    'asset_path': asset,
                    'source_chapter_id': chapter_id,
                    'destination_chapter_id': None,
                    'proposed_disposition': 'REVIEW_REQUIRED',
                })
            actions.append({'chapter_id': chapter_id, 'action': status})
            continue

        raise ValueError(f'unsupported migration status for {chapter_id}: {status}')

    active.sort()
    active_sequence = [chapter_id for _, chapter_id, _ in active]
    expected = list(range(1, len(active) + 1))
    actual = [number for number, _, _ in active]
    warnings = []
    if actual != expected:
        warnings.append({'kind': 'non_sequential_active_numbers', 'actual': actual, 'expected': expected})

    return {
        'schema_version': 1,
        'active_sequence': active_sequence,
        'active_numbers': actual,
        'aliases': dict(sorted(aliases.items())),
        'art_migrations': art_migrations,
        'actions': actions,
        'warnings': warnings,
        'safe_to_apply': not warnings and all(row['proposed_disposition'] != 'REVIEW_REQUIRED' for row in art_migrations),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--registry', type=Path, default=Path('publishing/chapter_identity_registry.json'))
    parser.add_argument('--map', dest='mapping', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('publishing/compression_migration_preview.json'))
    parser.add_argument('--stdout', action='store_true')
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding='utf-8'))
    mapping = json.loads(args.mapping.read_text(encoding='utf-8'))
    payload = build_preview(registry, mapping.get('chapters', mapping))
    if args.stdout:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(f'wrote migration preview to {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
