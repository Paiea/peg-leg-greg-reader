import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = runpy.run_path(str(ROOT / "scripts" / "audio_score_next.py"))


def make_score_dir(tmp_path: Path, chapters: list[int]) -> Path:
    score_dir = tmp_path / "scores"
    score_dir.mkdir()
    for chapter in chapters:
        (score_dir / f"ch{chapter:03d}.md").write_text(
            f"# Chapter {chapter}: T\n\n---\n\nbody\n",
            encoding="utf-8",
        )
    return score_dir


def make_manifest(tmp_path: Path, published: list[int]) -> Path:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps({"chapters": [{"number": n} for n in published]}),
        encoding="utf-8",
    )
    return manifest


def test_resolver_skips_published_and_claimed_and_returns_earliest_free(tmp_path):
    scores = make_score_dir(tmp_path, [1, 2, 3, 4, 5])
    manifest = make_manifest(tmp_path, [1, 3])
    claims = [
        "refs/heads/audio/v2-greg-again-ch002-auto",
        "refs/heads/audio/v2-greg-again-ch004-fill-gap",
    ]

    result = MOD["resolve_next_candidate"](scores, manifest, claims, minimum=1, maximum=5)

    assert result["generation"] == "v2"
    assert result["chapter"] == 5
    assert result["chapter_padded"] == "005"
    assert result["claim_branch"] == "audio/v2-greg-again-ch005-auto"
    assert result["source"].endswith("ch005.md")


def test_resolver_uses_actual_score_inventory_and_skips_missing_numbers(tmp_path):
    scores = make_score_dir(tmp_path, [1, 3, 7])
    manifest = make_manifest(tmp_path, [1])

    result = MOD["resolve_next_candidate"](scores, manifest, [], minimum=1, maximum=30)

    assert result["chapter"] == 3


def test_resolver_returns_none_when_no_free_score_exists(tmp_path):
    scores = make_score_dir(tmp_path, [1, 2])
    manifest = make_manifest(tmp_path, [1])

    result = MOD["resolve_next_candidate"](
        scores,
        manifest,
        ["refs/remotes/origin/audio/v2-greg-again-ch002-auto"],
        minimum=1,
        maximum=2,
    )

    assert result is None


def test_claim_parser_accepts_single_chapter_generation_branch_variants_only():
    parse = MOD["chapter_from_claim_ref"]
    assert parse("refs/heads/audio/v2-greg-again-ch014-auto") == 14
    assert parse("refs/heads/audio/v2-greg-again-ch014-fill-gap") == 14
    assert parse("refs/remotes/origin/audio/v2-greg-again-ch014-auto") == 14
    assert parse("refs/heads/audio/light-greg-again-ch014-auto") is None
    assert parse("refs/heads/audio/light-greg-again-ch014-auto", "light") == 14
    assert parse("refs/remotes/origin/audio/light-greg-again-ch014-repair", "light") == 14
    assert parse("refs/heads/audio/v2-greg-again-ch014-auto", "light") is None
    assert parse("refs/heads/audio/v2-greg-again-ch0140-auto") is None


def test_light_generation_uses_light_claim_namespace(tmp_path):
    scores = make_score_dir(tmp_path, [1, 2, 3])
    manifest = make_manifest(tmp_path, [1])
    claims = ["refs/heads/audio/light-greg-again-ch002-auto"]

    result = MOD["resolve_next_candidate"](
        scores,
        manifest,
        claims,
        generation="light",
        minimum=1,
        maximum=3,
    )

    assert result["generation"] == "light"
    assert result["chapter"] == 3
    assert result["claim_branch"] == "audio/light-greg-again-ch003-auto"


def test_generation_config_points_to_current_light_authority():
    config = MOD["generation_config"]("light")
    assert config["score_dir"] == "r2/assets/audio-score-light"
    assert config["manifest"] == "greg-again/audio/light/manifest.json"
    assert config["claim_prefix"] == "audio/light-greg-again-ch"
