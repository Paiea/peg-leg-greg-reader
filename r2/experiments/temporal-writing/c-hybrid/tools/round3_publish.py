import json
import re
import subprocess
from pathlib import Path

ROOT = Path('.')
R2 = ROOT / 'r2'
SOURCE_REF = 'origin/experiment/r2-temporal-c-hybrid'
SOURCE_DIR = 'r2/experiments/temporal-writing/c-hybrid/round-03/reconciled'
START = 139
END = 164


def show(path):
    return subprocess.check_output(['git', 'show', f'{SOURCE_REF}:{path}'], text=True)


def parse_chapter(text, number):
    match = re.match(rf'^# Chapter {number}: ([^\n]+)\n\n', text)
    assert match, f'bad heading for {number}'
    title = match.group(1).strip()
    body = text[match.end():].strip()
    assert body, f'empty body for {number}'
    first_para = next(p.strip() for p in body.split('\n\n') if p.strip())
    teaser = re.split(r'(?<=[.!?])\s+', first_para, maxsplit=1)[0].strip()
    return title, teaser


selected = {}
metadata = {}
for number in range(START, END + 1):
    path = f'{SOURCE_DIR}/ch{number:03d}.md'
    text = show(path)
    assert 'Status: **EXPERIMENTAL' not in text
    assert text.startswith(f'# Chapter {number}: ')
    selected[number] = text if text.endswith('\n') else text + '\n'
    metadata[number] = parse_chapter(selected[number], number)

# Publish exact selected written prose.
written_dir = R2 / 'assets' / 'written'
written_dir.mkdir(parents=True, exist_ok=True)
for number, text in selected.items():
    (written_dir / f'ch{number:03d}.md').write_text(text, encoding='utf-8')

# Extend stable project manifest.
project_path = R2 / 'data' / 'project.json'
project = json.loads(project_path.read_text(encoding='utf-8'))
assert project['current_chapter'] == 'r2-ch138', project['current_chapter']
assert project['chapters'][-1] == 'r2-ch138'
for number in range(START, END + 1):
    chapter_id = f'r2-ch{number:03d}'
    assert chapter_id not in project['chapters']
    project['chapters'].append(chapter_id)
project['current_chapter'] = 'r2-ch164'
project_path.write_text(json.dumps(project, indent=2) + '\n', encoding='utf-8')

# Connect old frontier to new run.
ch138_path = R2 / 'data' / 'chapters' / 'ch138.json'
ch138 = json.loads(ch138_path.read_text(encoding='utf-8'))
assert ch138['navigation']['next'] is None
ch138['navigation']['next'] = 'r2-ch139'
ch138_path.write_text(json.dumps(ch138, separators=(',', ':')) + '\n', encoding='utf-8')

# Add one reader manifest per chapter. Sibling media remain unavailable.
chapters_dir = R2 / 'data' / 'chapters'
for number in range(START, END + 1):
    title, teaser = metadata[number]
    chapter_id = f'r2-ch{number:03d}'
    manifest = {
        'chapter_id': chapter_id,
        'display_number': number,
        'title': title,
        'status': 'published',
        'book': 1,
        'act': 1,
        'teaser': teaser,
        'audio': {'status': 'unavailable', 'path': None},
        'written': {'status': 'published', 'path': f'assets/written/ch{number:03d}.md'},
        'images': [],
        'navigation': {
            'previous': f'r2-ch{number - 1:03d}',
            'next': None if number == END else f'r2-ch{number + 1:03d}',
        },
    }
    out = chapters_dir / f'ch{number:03d}.json'
    assert not out.exists(), out
    out.write_text(json.dumps(manifest, separators=(',', ':')) + '\n', encoding='utf-8')

# Add written state without rewriting older concurrent authority.
registry_path = R2 / 'data' / 'chapter-registry.json'
registry = json.loads(registry_path.read_text(encoding='utf-8'))
assert registry['current_chapter'] == 'r2-ch138', registry['current_chapter']
for number in range(START, END + 1):
    chapter_id = f'r2-ch{number:03d}'
    title, _ = metadata[number]
    assert chapter_id not in registry['chapters']
    registry['chapters'][chapter_id] = {
        'display_number': number,
        'title': title,
        'status': 'in_progress',
        'pipeline': {
            'scene_packets': 'in_progress',
            'audio': 'not_started',
            'written': 'published',
            'story_sync': 'in_progress',
            'image_plan': 'not_started',
            'image_generation': 'not_started',
            'image_review': 'not_started',
            'image_integration': 'not_started',
        },
        'images': {
            'target_count': 2,
            'planned': 0,
            'generated': 0,
            'approved': 0,
            'integrated': 0,
        },
        'last_completed_stage': 'written',
        'next_action': 'publish_audio_and_plan_images',
    }
registry['current_chapter'] = 'r2-ch164'
registry_path.write_text(json.dumps(registry, separators=(',', ':')) + '\n', encoding='utf-8')

# Advance the explicit reader contract test.
test_path = ROOT / 'tests' / 'test_r2_site.py'
test = test_path.read_text(encoding='utf-8')
replacements = {
    "range(1, 139)": "range(1, 165)",
    "'r2-ch138'": "'r2-ch164'",
    "None if number == 138": "None if number == 164",
    "test_written_frontier_is_public_through_chapter_one_hundred_thirty_eight": "test_written_frontier_is_public_through_chapter_one_hundred_sixty_four",
}
for old, new in replacements.items():
    assert old in test, old
    test = test.replace(old, new)
test_path.write_text(test, encoding='utf-8')

# Verify the transaction shape before the repository test suite.
project_check = json.loads(project_path.read_text(encoding='utf-8'))
assert project_check['chapters'] == [f'r2-ch{i:03d}' for i in range(1, 165)]
assert project_check['current_chapter'] == 'r2-ch164'
for number in range(START, END + 1):
    chapter = json.loads((chapters_dir / f'ch{number:03d}.json').read_text(encoding='utf-8'))
    assert chapter['title'] == metadata[number][0]
    assert chapter['written']['status'] == 'published'
    assert (written_dir / f'ch{number:03d}.md').read_text(encoding='utf-8') == selected[number]
assert json.loads(ch138_path.read_text(encoding='utf-8'))['navigation']['next'] == 'r2-ch139'
print('Round 03 public transaction 139-164: PRETEST OK')
