from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
MOD = runpy.run_path(str(ROOT / "scripts" / "audio_score_capture_plan.py"))


def test_generation_paths_preserve_v2_default():
    source, output = MOD["generation_paths"]("v2", "013")
    assert source.as_posix() == "r2/assets/audio-score/ch013.md"
    assert output.as_posix() == "greg-again/audio/v2/takes/013/short-takes.json"


def test_generation_paths_route_light():
    source, output = MOD["generation_paths"]("light", "013")
    assert source.as_posix() == "r2/assets/audio-score-light/ch013.md"
    assert output.as_posix() == "greg-again/audio/light/takes/013/short-takes.json"


def test_long_written_paragraph_splits_at_natural_boundaries_without_text_loss():
    sentence = "Greg watched the wagon move and understood the load a little differently this time. "
    body = sentence * 9
    chunks = MOD["make_chunks"](body)
    assert "".join(chunks) == body
    assert len(chunks) >= 2
    assert all(len(MOD["provider_text"](chunk)) <= 500 for chunk in chunks)
