import copy
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('.')
R2 = ROOT / 'r2'
SOURCE_REF = 'origin/experiment/r2-temporal-c-hybrid'
SOURCE_DIR = 'r2/experiments/temporal-writing/c-hybrid/round-08/reconciled'
START = 253
END = 278
OLD_END = 252


def show(path):
    return subprocess.check_output(['git', 'show', f'{SOURCE_REF}:{path}'], text=True)


def title_and_teaser(text):
    m = re.match(r'# Chapter \d+: ([^\n]+)\n\n(.*)', text, flags=re.S)
    assert m, text[:120]
    title = m.group(1).strip()
    body = m.group(2)
    teaser = next(line.strip() for line in body.splitlines() if line.strip())
    teaser = re.sub(r'^\*\*(.*?)\*\*$', r'\1', teaser)
    return title, teaser

selected = {}
for n in range(START, END + 1):
    text = show(f'{SOURCE_DIR}/ch{n:03d}.md')
    assert text.startswith(f'# Chapter {n}: ')
    assert 'Status: **EXPERIMENTAL' not in text
    selected[n] = text
    (R2 / f'assets/written/ch{n:03d}.md').write_text(text, encoding='utf-8')

old_path = R2 / f'data/chapters/ch{OLD_END:03d}.json'
old = json.loads(old_path.read_text(encoding='utf-8'))
old['navigation']['next'] = f'r2-ch{START:03d}'
old_path.write_text(json.dumps(old, separators=(',', ':')) + '\n', encoding='utf-8')

for n, text in selected.items():
    title, teaser = title_and_teaser(text)
    chapter = {
        'chapter_id': f'r2-ch{n:03d}',
        'display_number': n,
        'title': title,
        'status': 'published',
        'book': 1,
        'act': 1,
        'teaser': teaser,
        'audio': {'status': 'unavailable', 'path': None},
        'written': {'status': 'published', 'path': f'assets/written/ch{n:03d}.md'},
        'images': [],
        'navigation': {
            'previous': f'r2-ch{n-1:03d}',
            'next': None if n == END else f'r2-ch{n+1:03d}',
        },
    }
    (R2 / f'data/chapters/ch{n:03d}.json').write_text(json.dumps(chapter, separators=(',', ':')) + '\n', encoding='utf-8')

project_path = R2 / 'data/project.json'
project = json.loads(project_path.read_text(encoding='utf-8'))
project['chapters'] = [f'r2-ch{i:03d}' for i in range(1, END + 1)]
project['current_chapter'] = f'r2-ch{END:03d}'
project_path.write_text(json.dumps(project, indent=2) + '\n', encoding='utf-8')

registry_path = R2 / 'data/chapter-registry.json'
registry = json.loads(registry_path.read_text(encoding='utf-8'))
registry['current_chapter'] = f'r2-ch{END:03d}'
template = registry['chapters'][f'r2-ch{OLD_END:03d}']
for n, text in selected.items():
    title, _ = title_and_teaser(text)
    entry = copy.deepcopy(template)
    entry['display_number'] = n
    entry['title'] = title
    entry['status'] = 'in_progress'
    entry['pipeline']['written'] = 'published'
    entry['pipeline']['audio'] = 'not_started'
    entry['pipeline']['story_sync'] = 'in_progress'
    entry['pipeline']['image_plan'] = 'not_started'
    entry['pipeline']['image_generation'] = 'not_started'
    entry['pipeline']['image_review'] = 'not_started'
    entry['pipeline']['image_integration'] = 'not_started'
    entry['images'] = {'target_count': 2, 'planned': 0, 'generated': 0, 'approved': 0, 'integrated': 0}
    entry['last_completed_stage'] = 'written'
    entry['next_action'] = 'publish_audio_and_plan_images'
    registry['chapters'][f'r2-ch{n:03d}'] = entry
registry_path.write_text(json.dumps(registry, separators=(',', ':')) + '\n', encoding='utf-8')

test_path = ROOT / 'tests/test_r2_site.py'
test = test_path.read_text(encoding='utf-8')
test = test.replace('range(1, 253)', 'range(1, 279)')
test = test.replace("'r2-ch252'", "'r2-ch278'")
test = test.replace('chapter_two_hundred_fifty_two', 'chapter_two_hundred_seventy_eight')
test = test.replace('number == 252', 'number == 278')
test_path.write_text(test, encoding='utf-8')

project = json.loads(project_path.read_text(encoding='utf-8'))
assert project['current_chapter'] == 'r2-ch278'
assert project['chapters'][-1] == 'r2-ch278'
for n in range(START, END + 1):
    manifest = json.loads((R2 / f'data/chapters/ch{n:03d}.json').read_text(encoding='utf-8'))
    assert manifest['written']['status'] == 'published'
    assert manifest['navigation']['previous'] == f'r2-ch{n-1:03d}'
    assert manifest['navigation']['next'] == (None if n == END else f'r2-ch{n+1:03d}')

print('Round 08 public reader state 253-278 built from reconciled experiment authority: OK')
