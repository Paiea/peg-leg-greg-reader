from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_REASONS = {
    'redundant_progression',
    'duplicate_information',
    'low_consequence_mundane',
    'bridge_not_needed',
    'superseded_by_stronger_chapter',
    'pacing',
    'other',
}
ALLOWED_ENTRY_FIELDS = {'showcase', 'reason'}
LEGACY_IDENTITY_KEY = '_legacy_identity'
DEFAULT_MANIFEST = {
    'version': 1,
    'mode': 'whole_chapter_only',
    'default': 'visible',
    'chapters': {},
}


@dataclass(frozen=True)
class ShowcaseMap:
    visible_canon: tuple[int, ...]
    _canon_to_showcase: dict[int, int]
    _index_by_canon: dict[int, int]
    _canonical_set: frozenset[int]

    def showcase_number(self, canon: int) -> int | None:
        return self._canon_to_showcase.get(canon)

    def previous_visible(self, canon: int) -> int | None:
        index = self._index_by_canon.get(canon)
        if index is None or index == 0:
            return None
        previous = self.visible_canon[index - 1]
        if any(number not in self._canonical_set for number in range(previous + 1, canon)):
            return None
        return previous

    def next_visible(self, canon: int) -> int | None:
        index = self._index_by_canon.get(canon)
        if index is None or index + 1 >= len(self.visible_canon):
            return None
        following = self.visible_canon[index + 1]
        if any(number not in self._canonical_set for number in range(canon + 1, following)):
            return None
        return following


def _validate_manifest_shape(data: dict) -> None:
    if data.get('version') != 1:
        raise ValueError('unsupported showcase manifest version')
    if data.get('mode') != 'whole_chapter_only':
        raise ValueError('showcase manifest mode must be whole_chapter_only')
    if data.get('default') not in {'visible', 'hidden'}:
        raise ValueError('showcase manifest default must be visible or hidden')
    if not isinstance(data.get('chapters'), dict):
        raise ValueError('showcase manifest chapters must be an object')


def load_showcase_manifest(path: Path) -> dict:
    if not path.exists():
        return {
            'version': DEFAULT_MANIFEST['version'],
            'mode': DEFAULT_MANIFEST['mode'],
            'default': DEFAULT_MANIFEST['default'],
            'chapters': {},
            LEGACY_IDENTITY_KEY: True,
        }
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('showcase manifest must be an object')
    _validate_manifest_shape(data)
    return data


def build_identity_showcase_map(canonical_numbers: list[int]) -> ShowcaseMap:
    canonical = tuple(sorted(set(canonical_numbers)))
    if any(number <= 0 for number in canonical):
        raise ValueError('canonical chapter numbers must be positive integers')
    index_by_canon = {canon: idx for idx, canon in enumerate(canonical)}
    return ShowcaseMap(
        canonical,
        {canon: canon for canon in canonical},
        index_by_canon,
        frozenset(canonical),
    )


def build_showcase_map(canonical_numbers: list[int], manifest: dict) -> ShowcaseMap:
    _validate_manifest_shape(manifest)
    canonical = tuple(sorted(set(canonical_numbers)))
    if any(number <= 0 for number in canonical):
        raise ValueError('canonical chapter numbers must be positive integers')
    if manifest.get(LEGACY_IDENTITY_KEY):
        return build_identity_showcase_map(list(canonical))

    canonical_set = set(canonical)
    overrides: dict[int, bool] = {}
    for raw_number, entry in manifest['chapters'].items():
        try:
            number = int(raw_number)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'invalid canonical chapter key {raw_number!r}') from exc
        if str(number) != str(raw_number):
            raise ValueError(f'invalid canonical chapter key {raw_number!r}')
        if number not in canonical_set:
            raise ValueError(f'unknown canonical chapter {number}')
        if not isinstance(entry, dict):
            raise ValueError(f'chapter {number} showcase entry must be an object')
        extra = set(entry) - ALLOWED_ENTRY_FIELDS
        if extra:
            raise ValueError(f'chapter {number} violates whole-chapter only showcase curation: {sorted(extra)}')
        visible = entry.get('showcase')
        if not isinstance(visible, bool):
            raise ValueError(f'chapter {number} showcase must be boolean')
        reason = entry.get('reason')
        if not visible:
            if reason not in SUPPORTED_REASONS:
                raise ValueError(f'chapter {number} has unsupported reason {reason!r}')
        elif reason is not None and reason not in SUPPORTED_REASONS:
            raise ValueError(f'chapter {number} has unsupported reason {reason!r}')
        overrides[number] = visible

    default_visible = manifest['default'] == 'visible'
    visible = tuple(number for number in canonical if overrides.get(number, default_visible))
    canon_to_showcase = {canon: idx for idx, canon in enumerate(visible, start=1)}
    index_by_canon = {canon: idx for idx, canon in enumerate(visible)}
    return ShowcaseMap(visible, canon_to_showcase, index_by_canon, frozenset(canonical_set))
