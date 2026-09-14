from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
MOD = runpy.run_path(str(ROOT / "scripts" / "audio_score_bind_captures.py"))


def test_light_capture_paths():
    plan, results = MOD["generation_paths"]("light", "007")
    assert plan.as_posix() == "greg-again/audio/light/takes/007/short-takes.json"
    assert results.as_posix() == "greg-again/audio/light/takes/007/capture-results.tsv"
