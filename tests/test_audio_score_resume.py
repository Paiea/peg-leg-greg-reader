import csv
import json
from pathlib import Path

from scripts import audio_score_resume


def write_take_map(tmp_path: Path, *, generation: str = "light", chapter: int = 11, take_count: int = 7, captured: tuple[int, ...] = ()) -> Path:
    chapter_s = f"{chapter:03d}"
    base = tmp_path / "greg-again" / "audio" / generation / "takes" / chapter_s
    base.mkdir(parents=True)
    takes = []
    for order in range(1, take_count + 1):
        take = {
            "order": order,
            "source_transcript": f"source {order}",
            "transcript": f"provider {order}",
            "preview_transcript": f"provider {order}",
        }
        if order in captured:
            take.update({
                "context_id": f"ctx-{order}",
                "preview_url": f"https://storage.googleapis.com/test/{order}.mp3",
            })
        takes.append(take)
    path = base / "short-takes.json"
    path.write_text(json.dumps({
        "chapter": chapter,
        "chapter_id": f"ga-{chapter_s}",
        "generation": generation,
        "title": "Test Chapter",
        "source": f"r2/assets/audio-score{'-light' if generation == 'light' else ''}/ch{chapter_s}.md",
        "source_blob_sha": "abc123",
        "voice": "deep",
        "status": "capture_partial" if captured else "capture_plan",
        "take_count": take_count,
        "takes": takes,
    }), encoding="utf-8")
    return path


def write_capture_results(take_map: Path, rows: list[tuple[int, str, str]]) -> Path:
    path = take_map.parent / "capture-results.tsv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["order", "context_id", "preview_url"])
        writer.writerows(rows)
    return path


def test_resume_returns_only_first_five_missing_takes_by_default(tmp_path):
    take_map = write_take_map(tmp_path, take_count=7, captured=(1, 3))

    packet = audio_score_resume.build_resume_packet(take_map)

    assert packet["schema"] == "audio_score_resume/v1"
    assert packet["generation"] == "light"
    assert packet["chapter"] == 11
    assert packet["captured_count"] == 2
    assert packet["missing_count"] == 5
    assert [take["order"] for take in packet["next_takes"]] == [2, 4, 5, 6, 7]
    assert all(set(take) == {"order", "transcript", "preview_transcript"} for take in packet["next_takes"])


def test_resume_honors_smaller_batch_size(tmp_path):
    take_map = write_take_map(tmp_path, take_count=7, captured=(1,))

    packet = audio_score_resume.build_resume_packet(take_map, batch_size=2)

    assert packet["batch_size"] == 2
    assert [take["order"] for take in packet["next_takes"]] == [2, 3]
    assert packet["missing_count"] == 6


def test_resume_counts_unbound_capture_results_as_captured(tmp_path):
    take_map = write_take_map(tmp_path, take_count=6, captured=(1, 2))
    write_capture_results(take_map, [
        (1, "ctx-1", "https://storage.googleapis.com/test/1.mp3"),
        (2, "ctx-2", "https://storage.googleapis.com/test/2.mp3"),
        (3, "ctx-3", "https://storage.googleapis.com/test/3.mp3"),
        (5, "ctx-5", "https://storage.googleapis.com/test/5.mp3"),
    ])

    packet = audio_score_resume.build_resume_packet(take_map)

    assert packet["captured_count"] == 4
    assert packet["missing_count"] == 2
    assert [take["order"] for take in packet["next_takes"]] == [4, 6]


def test_resume_is_complete_when_every_take_has_durable_capture(tmp_path):
    take_map = write_take_map(tmp_path, take_count=3, captured=(1, 2, 3))

    packet = audio_score_resume.build_resume_packet(take_map)

    assert packet["status"] == "capture_complete"
    assert packet["captured_count"] == 3
    assert packet["missing_count"] == 0
    assert packet["next_takes"] == []


def test_resume_rejects_duplicate_capture_result_order(tmp_path):
    take_map = write_take_map(tmp_path, take_count=3)
    write_capture_results(take_map, [
        (1, "ctx-a", "https://storage.googleapis.com/test/a.mp3"),
        (1, "ctx-b", "https://storage.googleapis.com/test/b.mp3"),
    ])

    try:
        audio_score_resume.build_resume_packet(take_map)
    except ValueError as exc:
        assert "duplicate capture result" in str(exc)
    else:
        raise AssertionError("expected duplicate capture result to be rejected")


def test_resume_rejects_capture_without_durable_preview_url(tmp_path):
    take_map = write_take_map(tmp_path, take_count=3)
    write_capture_results(take_map, [(1, "ctx-1", "https://example.com/not-durable.mp3")])

    try:
        audio_score_resume.build_resume_packet(take_map)
    except ValueError as exc:
        assert "invalid preview_url" in str(exc)
    else:
        raise AssertionError("expected invalid preview URL to be rejected")


def test_generation_paths_route_light_and_v2(tmp_path):
    light = audio_score_resume.take_map_path(tmp_path, "light", 11)
    v2 = audio_score_resume.take_map_path(tmp_path, "v2", 11)

    assert light.as_posix().endswith("greg-again/audio/light/takes/011/short-takes.json")
    assert v2.as_posix().endswith("greg-again/audio/v2/takes/011/short-takes.json")
