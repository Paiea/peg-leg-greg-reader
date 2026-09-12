import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "greg-again" / "audio" / "manifest.json"
V2 = ROOT / "greg-again" / "audio" / "v2" / "manifest.json"

public = json.loads(PUBLIC.read_text(encoding="utf-8"))
by_id = {chapter["chapter_id"]: chapter for chapter in public["chapters"]}

by_id["ga-007"].update({
    "audio_finish": "audio-score-v2",
    "take_count": 31,
    "duration_seconds": 623.448,
    "audio_src": "assets/v2/chapter-007.mp3",
    "note": "Audio Score v2 Chapter 7 from the exact audio-native score. Thirty-one preview-safe deep-voice takes preserve moving-action causality, Meral's redirection from stopping to turning the wagon, and Greg's tiny brace under load. Exact score coverage, ordered capture, MP3 playability, and the chapter settling tail were mechanically verified; subjective human listen-back remains separate."
})
by_id["ga-008"].update({
    "audio_finish": "audio-score-v2",
    "take_count": 20,
    "duration_seconds": 535.8,
    "audio_src": "assets/v2/chapter-008.mp3",
    "note": "Audio Score v2 Chapter 8: twenty preview-safe deep-voice chunks captured from the Audio Score, objectively verified for exact ordered source coverage, durable Google Storage artifact capture, ffprobe playability, ordered assembly, and a two-second settling tail. Subjective human listen-back remains separate QA."
})
PUBLIC.write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

v2 = json.loads(V2.read_text(encoding="utf-8"))
v2_by_id = {chapter["chapter_id"]: chapter for chapter in v2["chapters"]}
v2_by_id["ga-007"] = {
    "chapter_id": "ga-007",
    "number": 7,
    "title": "The Extra Guard",
    "status": "verified_unlistened",
    "source": "r2/assets/audio-score/ch007.md",
    "source_blob_sha": "d179b9621a0903c286171b707264b6256600b99f",
    "voice": "deep",
    "take_count": 31,
    "capture_mode": "preview-safe-short-takes",
    "duration_seconds": 623.448,
    "audio_src": "assets/v2/chapter-007.mp3",
    "verification": "greg-again/audio/v2/verification/007/"
}
v2_by_id["ga-008"] = {
    "chapter_id": "ga-008",
    "number": 8,
    "title": "Road Work",
    "status": "verified",
    "source": "r2/assets/audio-score/ch008.md",
    "source_blob_sha": "70fb72370291aa2a47b76d383cae9434254305e8",
    "voice": "deep",
    "capture_factory": "preview-safe-identical-transcript",
    "take_count": 20,
    "duration_seconds": 535.8,
    "audio_src": "assets/v2/chapter-008.mp3",
    "listener_qa": "not_performed",
    "verification": "greg-again/audio/v2/verification/008/"
}
v2["chapters"] = sorted(v2_by_id.values(), key=lambda chapter: chapter["number"])
V2.write_text(json.dumps(v2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
