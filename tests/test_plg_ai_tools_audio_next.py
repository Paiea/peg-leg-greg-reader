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
    assert result["chapter"] == 3
    assert plg_ai_tools.TOOL_SPECS["audio_next"]["read_only"] is True
    assert plg_ai_tools.TOOL_SPECS["audio_next"]["write"] is False


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
