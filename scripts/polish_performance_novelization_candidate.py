#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    ROOT / "chapters/007.html": (
        "<p>The negotiation was over because he had physically returned to cleaning. Offensive.</p>",
        "<p>The negotiation was over. He was sweeping again. Offensive.</p>",
    ),
    ROOT / "chapters/018.html": (
        '<p>Hessa stopped reaching for beans.</p><p>"The anchor," I said.</p><p>Hessa waited.</p><p>I looked at the table.</p>',
        '<p>Hessa stopped reaching for beans.</p><p>"The anchor," I said.</p><p>I looked at the table.</p>',
    ),
}


def main() -> int:
    for path, (old, new) in REPLACEMENTS.items():
        text = path.read_text(encoding="utf-8")
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"expected exactly one match in {path}: found {count}")
        text = text.replace(old, new, 1)
        if "—" in new:
            raise AssertionError("polish introduced em dash")
        path.write_text(text, encoding="utf-8")
        print(f"polished {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
