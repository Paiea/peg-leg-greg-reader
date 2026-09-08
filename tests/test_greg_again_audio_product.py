import json
from pathlib import Path

from scripts.greg_again_audio import validate_manifest, validate_score

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "state/experiments/greg-again/audio"


def test_chapter_1_audio_state_is_complete_and_unrendered():
    score = json.loads((AUDIO / "chapters/001/score.json").read_text(encoding="utf-8"))
    manifest = json.loads((AUDIO / "chapters/001/manifest.json").read_text(encoding="utf-8"))
    validate_score(score)
    validate_manifest(manifest, score)
    assert score["title"] == "The Boy"
    assert len(score["blocks"]) >= 8
    assert manifest["renderer_status"] == "unrendered"
    assert manifest["approval_state"] == "experimental"
    assert manifest["selected_takes"] == {}


def test_narrator_brief_has_audio_first_rules():
    narrator = (AUDIO / "narrator.md").read_text(encoding="utf-8").lower()
    for phrase in ("one primary narrator", "dry humor", "speaker clarity", "do not overperform"):
        assert phrase in narrator


def test_pronunciations_are_not_silently_guessed():
    pronunciation = json.loads((AUDIO / "pronunciation.json").read_text(encoding="utf-8"))
    assert pronunciation["schema"] == "greg_again_pronunciation/v1"
    assert {entry["status"] for entry in pronunciation["entries"]} == {"confirm_before_render"}


def test_public_audio_page_is_small_and_audio_first():
    html = (ROOT / "greg-again/audio/index.html").read_text(encoding="utf-8")
    assert "GREG, AGAIN" in html
    assert "Audio-Native Proving Run" in html
    assert "The Boy" in html
    assert "<audio" in html
    assert "waveform" not in html.lower()
    assert "dashboard" not in html.lower()


def test_unrendered_public_manifest_has_no_fake_audio_asset():
    public = json.loads((ROOT / "greg-again/audio/manifest.json").read_text(encoding="utf-8"))
    assert public["status"] == "experimental"
    assert public["audio_src"] is None


def test_player_handles_unqualified_state_without_fake_source():
    js = (ROOT / "greg-again/audio/player.js").read_text(encoding="utf-8")
    assert "Audio render not yet qualified." in js
    assert "audio_src" in js
