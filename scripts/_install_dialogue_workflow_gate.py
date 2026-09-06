#!/usr/bin/env python3
from pathlib import Path

path = Path('.github/workflows/light-edition.yml')
text = path.read_text(encoding='utf-8')
old = "      - name: Test reader tooling\n        run: python -m unittest discover -s tests -p 'test_*.py'\n      - name: Process illustration production state\n"
new = "      - name: Test reader tooling\n        run: python -m unittest discover -s tests -p 'test_*.py'\n      - name: Validate latest dialogue ownership\n        run: python scripts/dialogue_ownership_check.py --latest --strict\n      - name: Process illustration production state\n"
if text.count(old) != 1:
    raise SystemExit('expected one Light workflow test-to-production anchor')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
print('installed dialogue ownership Light workflow gate')
