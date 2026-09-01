from pathlib import Path
import re

p = Path('state/manuscript/Peg_Leg_Greg_Running_Manuscript.md')
text = p.read_text(encoding='utf-8')
old = "I remembered the man at the wrong Vale because he had worked hard for the wrong room."
new = "I remembered the man at the wrong office because he had worked hard for the wrong room."
assert text.count(old) == 1
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')

chapter = text.split('# CHAPTER 245', 1)[1]
words = len(re.findall(r"\b\w[\w'’-]*\b", chapter))
emdashes = chapter.count('—')
assert words == 2662, words
assert emdashes == 0, emdashes
assert old not in chapter
assert new in chapter
assert chapter.rstrip().endswith('That was where they belonged.')
print(f'VERIFIED_CH245_WORDS={words}')
print(f'VERIFIED_CH245_EMDASHES={emdashes}')
print('VERIFIED_WRONG_OFFICE_FIX=1')
