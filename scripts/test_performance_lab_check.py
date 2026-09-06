import json
import tempfile
import unittest
from pathlib import Path

from scripts.performance_lab_check import check_lab

SCENES = [
    'ch002-antonius-loan',
    'ch007-antonius-storeroom',
    'ch013-arlo-workshop',
    'ch016-jorren-alden-greg',
    'ch018-hessa-beans',
]


def make_base(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / 'README.md').write_text('lab\n', encoding='utf-8')
    (root / 'authority.lock.json').write_text(json.dumps({'manuscript': {}, 'performance_authority': {}}), encoding='utf-8')
    scenes = root / 'scenes'
    for name in SCENES:
        d = scenes / name
        d.mkdir(parents=True, exist_ok=True)
        (d / 'fixture.md').write_text(
            'SOURCE REF: abc\nSOURCE PATH: chapters/001.html\nSOURCE BLOB: def\n\n## DRAMATIC SCRIPT\n',
            encoding='utf-8',
        )
        (d / 'performed.md').write_text(
            '## PERFORMANCE FRAMES\n\n### GREG\nSTATE: interested\nPERFORMED STANCE: casual\nATTENTION: task\nBASELINE BEND: none\n\n## PERFORMED SCRIPT\n\n[B001] GREG -> OTHER [DIALOGUE]\n"Hello."\n\n[B002] OTHER [ACTION]\nNods.\n',
            encoding='utf-8',
        )
        (d / 'report.md').write_text(
            '## Dramatic Truth Gate\nPASS\n\n## Behavioral Realization Gate\nPASS\n\n## Exchange Rhythm Gate\nOK\n\n## Swap / Confusability Check\nOK\n\n## Source Comparison\nOK\n\n## Scene Verdict\nNO MATERIAL GAIN\n',
            encoding='utf-8',
        )
    return root


class PerformanceLabCheckTests(unittest.TestCase):
    def test_missing_authority_lock_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            (root / 'authority.lock.json').unlink()
            self.assertTrue(any('authority.lock.json' in x for x in check_lab(root)))

    def test_dialogue_requires_explicit_addressee(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            p = root / 'scenes' / SCENES[0] / 'performed.md'
            p.write_text(p.read_text().replace('GREG -> OTHER [DIALOGUE]', 'GREG [DIALOGUE]'), encoding='utf-8')
            self.assertTrue(any('addressee' in x.lower() for x in check_lab(root)))

    def test_action_requires_named_owner(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            p = root / 'scenes' / SCENES[0] / 'performed.md'
            p.write_text(p.read_text().replace('OTHER [ACTION]', 'HE [ACTION]'), encoding='utf-8')
            self.assertTrue(any('pronoun owner' in x.lower() for x in check_lab(root)))

    def test_pronoun_owner_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            p = root / 'scenes' / SCENES[0] / 'performed.md'
            p.write_text(p.read_text().replace('GREG -> OTHER [DIALOGUE]', 'HE -> OTHER [DIALOGUE]'), encoding='utf-8')
            self.assertTrue(any('pronoun owner' in x.lower() for x in check_lab(root)))

    def test_non_pov_thought_fails_without_authorization(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            p = root / 'scenes' / SCENES[0] / 'performed.md'
            p.write_text(p.read_text() + '\n[B003] ANTONIUS [THOUGHT]\nPrivate thought.\n', encoding='utf-8')
            self.assertTrue(any('pov authorization' in x.lower() for x in check_lab(root)))

    def test_material_bend_requires_evidence_beat_reference(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            p = root / 'scenes' / SCENES[0] / 'performed.md'
            p.write_text(p.read_text().replace('BASELINE BEND: none', 'BASELINE BEND: material lower patience'), encoding='utf-8')
            self.assertTrue(any('realized by' in x.lower() for x in check_lab(root)))

    def test_realized_by_missing_beat_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            p = root / 'scenes' / SCENES[0] / 'performed.md'
            p.write_text(p.read_text().replace('BASELINE BEND: none', 'BASELINE BEND: material lower patience\nREALIZED BY: B999'), encoding='utf-8')
            self.assertTrue(any('b999' in x.lower() for x in check_lab(root)))

    def test_stop_boundary_rejects_novel_prose_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            (root / 'novel-prose.md').write_text('forbidden', encoding='utf-8')
            self.assertTrue(any('forbidden artifact' in x.lower() for x in check_lab(root)))

    def test_minimal_valid_scene_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_base(Path(td) / 'lab')
            self.assertEqual([], check_lab(root))


if __name__ == '__main__':
    unittest.main()
