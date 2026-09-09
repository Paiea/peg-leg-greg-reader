import copy
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('.')
R2 = ROOT / 'r2'
SOURCE_REF = 'origin/experiment/r2-temporal-c-hybrid'
SOURCE_DIR = 'r2/experiments/temporal-writing/c-hybrid/round-04/reconciled'


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
for n in range(165, 191):
    path = f'{SOURCE_DIR}/ch{n:03d}.md'
    text = show(path)
    assert text.startswith(f'# Chapter {n}: ')
    assert 'Status: **EXPERIMENTAL' not in text
    selected[n] = text
    (R2 / f'assets/written/ch{n:03d}.md').write_text(text, encoding='utf-8')

# Preserve current chapter 164 metadata except for forward navigation.
ch164_path = R2 / 'data/chapters/ch164.json'
ch164 = json.loads(ch164_path.read_text(encoding='utf-8'))
ch164['navigation']['next'] = 'r2-ch165'
ch164_path.write_text(json.dumps(ch164, separators=(',', ':')) + '\n', encoding='utf-8')

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
            'next': None if n == 190 else f'r2-ch{n+1:03d}',
        },
    }
    path = R2 / f'data/chapters/ch{n:03d}.json'
    path.write_text(json.dumps(chapter, separators=(',', ':')) + '\n', encoding='utf-8')

project_path = R2 / 'data/project.json'
project = json.loads(project_path.read_text(encoding='utf-8'))
project['chapters'] = [f'r2-ch{i:03d}' for i in range(1, 191)]
project['current_chapter'] = 'r2-ch190'
project_path.write_text(json.dumps(project, indent=2) + '\n', encoding='utf-8')

registry_path = R2 / 'data/chapter-registry.json'
registry = json.loads(registry_path.read_text(encoding='utf-8'))
registry['current_chapter'] = 'r2-ch190'
template = registry['chapters']['r2-ch164']
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
test = test.replace("range(1, 165)", "range(1, 191)")
test = test.replace("'r2-ch164'", "'r2-ch190'")
test = test.replace('chapter_one_hundred_sixty_four', 'chapter_one_hundred_ninety')
test = test.replace('range(1, 165):', 'range(1, 191):')
test = test.replace('number == 164', 'number == 190')
test_path.write_text(test, encoding='utf-8')

# Final structural verification before repository tests.
project = json.loads(project_path.read_text(encoding='utf-8'))
assert project['current_chapter'] == 'r2-ch190'
assert project['chapters'][-1] == 'r2-ch190'
for n in range(165, 191):
    manifest = json.loads((R2 / f'data/chapters/ch{n:03d}.json').read_text(encoding='utf-8'))
    assert manifest['written']['status'] == 'published'
    assert manifest['navigation']['previous'] == f'r2-ch{n-1:03d}'
    assert manifest['navigation']['next'] == (None if n == 190 else f'r2-ch{n+1:03d}')

print('Round 04 public reader state 165-190 built from reconciled experiment authority: OK')
