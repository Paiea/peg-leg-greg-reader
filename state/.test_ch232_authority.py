from pathlib import Path

m = Path('state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').read_text()
s = Path('state/MANUSCRIPT_STATE.md').read_text()
i = Path('state/MANUSCRIPT_CHAPTER_INDEX.md').read_text()

assert m.count('## Chapter 232 — THE COUNTERSIGN') == 1, 'canonical COUNTERSIGN chapter missing/duplicated'
assert '# CHAPTER 232\n\n## THE MATCHER' not in m, 'stale duplicate MATCHER chapter still present'
assert 'Current story endpoint: Chapter 232 — **THE COUNTERSIGN**.' in s, 'state endpoint not COUNTERSIGN'
assert '232. **THE COUNTERSIGN**' in i, 'index missing COUNTERSIGN'
assert '232. **THE MATCHER**' not in i, 'index incorrectly includes MATCHER'
print('chapter232_authority_ok')
