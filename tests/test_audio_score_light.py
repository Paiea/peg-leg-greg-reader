from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audio_score_light_validate.py"


def load_validator():
    try:
        return runpy.run_path(str(SCRIPT))
    except FileNotFoundError:
        pytest.fail("Audio Score Light validator does not exist yet")


def test_normalized_words_ignore_punctuation_and_lineation():
    mod = load_validator()
    a = "Wait, really?\n\nYes."
    b = "Wait really yes"
    assert mod["normalized_words"](a) == mod["normalized_words"](b)


def test_change_ratio_allows_small_word_edit():
    mod = load_validator()
    source = "one two three four five six seven eight nine ten"
    light = "one two three four five six seven eight nine okay"
    assert mod["word_change_ratio"](source, light) <= 0.15


def test_change_ratio_rejects_large_rewrite():
    mod = load_validator()
    source = "one two three four five six seven eight nine ten"
    light = "alpha beta gamma delta epsilon zeta eta theta iota kappa"
    assert mod["word_change_ratio"](source, light) > 0.15


def test_light_materializer_preserves_written_body_exactly():
    script = ROOT / "scripts" / "materialize_audio_score_light.py"
    try:
        mod = runpy.run_path(str(script))
    except FileNotFoundError:
        pytest.fail("Audio Score Light materializer does not exist yet")
    raw = "# Chapter 2: Two Things\n\nStatus: source\n\n---\n\nWait, really?\n\nYes.\n"
    rendered = mod["render_light"](
        raw=raw,
        source_path=Path("r2/assets/written/ch002.md"),
        source_sha="5304f99a6192d9ee73d5eb254990c5e63d0f284c",
    )
    assert rendered.split("\n---\n", 1)[1].strip() == "Wait, really?\n\nYes."
    assert "# Chapter 2: Two Things" in rendered
    assert "Word-level change: `0.00%`" in rendered
