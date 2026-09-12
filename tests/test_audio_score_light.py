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
