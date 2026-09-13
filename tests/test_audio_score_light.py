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


def test_baseline_can_take_source_identity_from_manifest():
    mod = load_validator()
    source_path, source_sha = mod["resolve_source_identity"](
        raw="# Chapter 2: Two Things\n\nStatus: source\n\n---\n\nBody\n",
        chapter_id="002",
        sources={
            "002": {
                "source": "r2/assets/written/ch002.md",
                "source_blob_sha": "5304f99a6192d9ee73d5eb254990c5e63d0f284c",
            }
        },
    )
    assert source_path.as_posix() == "r2/assets/written/ch002.md"
    assert source_sha == "5304f99a6192d9ee73d5eb254990c5e63d0f284c"
