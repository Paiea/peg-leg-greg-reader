import json
from pathlib import Path

from scripts import plg_ai_tools


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


def test_audio_next_tool_is_read_only_and_uses_explicit_claim_refs(tmp_path):
    scores = make_score_dir(tmp_path, [1, 2, 3, 4])
    manifest = make_manifest(tmp_path, [1])

    result = plg_ai_tools.call_tool(
        "audio_next",
        {
            "score_dir": str(scores),
            "manifest": str(manifest),
            "minimum": 1,
            "maximum": 4,
            "claim_refs": ["refs/heads/audio/v2-greg-again-ch002-auto"],
        },
    )

    assert result["status"] == "available"
    assert result["generation"] == "v2"
    assert result["chapter"] == 3
    assert plg_ai_tools.TOOL_SPECS["audio_next"]["read_only"] is True
    assert plg_ai_tools.TOOL_SPECS["audio_next"]["write"] is False


def test_audio_next_tool_routes_light_generation(tmp_path):
    scores = make_score_dir(tmp_path, [1, 2, 3])
    manifest = make_manifest(tmp_path, [1])

    result = plg_ai_tools.call_tool(
        "audio_next",
        {
            "generation": "light",
            "score_dir": str(scores),
            "manifest": str(manifest),
            "claim_refs": ["refs/heads/audio/light-greg-again-ch002-auto"],
        },
    )

    assert result["status"] == "available"
    assert result["generation"] == "light"
    assert result["chapter"] == 3
    assert result["claim_branch"] == "audio/light-greg-again-ch003-auto"


def test_audio_next_tool_rejects_non_string_claim_refs(tmp_path):
    scores = make_score_dir(tmp_path, [1])
    manifest = make_manifest(tmp_path, [])

    try:
        plg_ai_tools.call_tool(
            "audio_next",
            {
                "score_dir": str(scores),
                "manifest": str(manifest),
                "claim_refs": [123],
            },
        )
    except ValueError as exc:
        assert "claim_refs" in str(exc)
    else:
        raise AssertionError("expected ValueError for invalid claim_refs")


def test_audio_claim_tool_is_explicit_write_and_delegates(monkeypatch, tmp_path):
    scores = make_score_dir(tmp_path, [1, 2])
    manifest = make_manifest(tmp_path, [1])
    seen = {}

    def fake_claim_next(score_dir, manifest_path, **kwargs):
        seen["score_dir"] = score_dir
        seen["manifest"] = manifest_path
        seen.update(kwargs)
        return {"status": "claimed", "chapter": 2, "claim_branch": "audio/light-greg-again-ch002-auto"}

    monkeypatch.setattr(plg_ai_tools.audio_score_claim, "claim_next", fake_claim_next)
    result = plg_ai_tools.call_tool(
        "audio_claim",
        {
            "generation": "light",
            "score_dir": str(scores),
            "manifest": str(manifest),
            "minimum": 1,
            "maximum": 2,
            "remote": "origin",
            "base_branch": "main",
        },
    )

    assert result["status"] == "claimed"
    assert seen["score_dir"] == scores
    assert seen["manifest"] == manifest
    assert seen["generation"] == "light"
    assert seen["minimum"] == 1
    assert seen["maximum"] == 2
    assert plg_ai_tools.TOOL_SPECS["audio_claim"]["write"] is True
    assert plg_ai_tools.TOOL_SPECS["audio_claim"]["read_only"] is False
