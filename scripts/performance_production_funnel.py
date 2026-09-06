#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_RE = re.compile(r'(<article\s+class="prose"[^>]*>)(.*?)(</article>)', re.S | re.I)
P_RE = re.compile(r'<p\b[^>]*>.*?</p>', re.S | re.I)
SCENE_BREAK_RE = re.compile(r'<hr\b[^>]*>', re.I)
TAG_RE = re.compile(r'<[^>]+>')
DIALOGUE_RE = re.compile(r'(?:“([^”]+)”|"([^"]+)")', re.S)
MONEY_RE = re.compile(r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:copper|silver|gold)\b", re.I)
CAPITALIZED_RE = re.compile(r"\b[A-Z][A-Za-z'’-]*\b")
WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z'’-]*\b")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]+|[^.!?]+$")
SCENE_ID_RE = re.compile(r"^(?P<chapter>\d{3})\.s(?P<number>\d{3,})$")
ACTION_WORDS = {
    "lifted", "moved", "picked", "set", "turned", "walked", "reached", "tapped",
    "shook", "opened", "closed", "held", "placed", "wrote", "swept", "sweeping",
    "rotated", "pointed", "pushed", "pulled", "sat", "stood", "crossed", "carried",
}
COMPILER_VERSIONS = {
    "mechanical": "mechanical/v1",
    "semantic": "scene-semantic/v1",
    "performance": "performance/v1",
    "screenplay": "screenplay/v1",
    "comparison": "comparison/v1",
}
CLAIM_KINDS = {"observed", "inferred", "locked_derived"}
CLAIM_RANK = {"inferred": 1, "locked_derived": 2, "observed": 3}
VIEW_NAMES = {"performance", "dialogue", "continuity", "illustration", "comparison"}


def next_visible_chapters(manifest: dict, *, after_chapter: int, count: int, max_chapter: int) -> list[int]:
    default_visible = manifest.get("default", "visible") == "visible"
    overrides = manifest.get("chapters", {})
    selected: list[int] = []
    for chapter in range(after_chapter + 1, max_chapter + 1):
        if not overrides.get(str(chapter), {}).get("showcase", default_visible):
            continue
        selected.append(chapter)
        if len(selected) == count:
            break
    return selected


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _plain(fragment_html: str) -> str:
    text = html.unescape(TAG_RE.sub("", fragment_html)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def extract_paragraphs(page: str) -> list[str]:
    article = ARTICLE_RE.search(page)
    if not article:
        return []
    return [_plain(match.group(0)) for match in P_RE.finditer(article.group(2)) if _plain(match.group(0))]


def dependency_fingerprint(*parts: object) -> str:
    payload = json.dumps(parts, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def source_fingerprint(paragraphs: list[str]) -> str:
    normalized = "\n".join(re.sub(r"\s+", " ", paragraph).strip() for paragraph in paragraphs)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _dialogue_spans(text: str) -> list[str]:
    spans: list[str] = []
    for match in DIALOGUE_RE.finditer(text):
        spans.append(next(group for group in match.groups() if group is not None))
    return spans


def build_mechanical_ir(scene: dict) -> dict:
    source = scene.get("source") if isinstance(scene, dict) else None
    paragraphs = source.get("paragraphs") if isinstance(source, dict) else None
    if not isinstance(paragraphs, list) or not all(isinstance(value, str) for value in paragraphs):
        raise ValueError("scene source paragraphs must be a list of strings")

    text = "\n".join(paragraphs)
    words = WORD_RE.findall(text)
    dialogue = _dialogue_spans(text)
    dialogue_words = sum(len(WORD_RE.findall(span)) for span in dialogue)
    sentence_count = sum(len(SENTENCE_RE.findall(paragraph)) for paragraph in paragraphs)
    action_word_hits = sum(1 for word in words if word.lower() in ACTION_WORDS)
    capitalized = sorted(set(CAPITALIZED_RE.findall(text)))
    money_mentions = [re.sub(r"\s+", " ", match.group(0)).lower() for match in MONEY_RE.finditer(text)]

    return {
        "paragraph_count": len(paragraphs),
        "sentence_count": sentence_count,
        "word_count": len(words),
        "dialogue_turns": len(dialogue),
        "dialogue_word_count": dialogue_words,
        "dialogue_ratio": round(dialogue_words / len(words), 4) if words else 0.0,
        "question_count": text.count("?"),
        "money_mentions": money_mentions,
        "capitalized_tokens": capitalized,
        "action_word_hits": action_word_hits,
    }


def _scene_number(scene_id: str) -> int:
    match = SCENE_ID_RE.match(scene_id)
    if not match:
        raise ValueError(f"invalid scene id: {scene_id}")
    return int(match.group("number"))


def _format_scene_id(chapter: int, number: int) -> str:
    return f"{chapter:03d}.s{number:03d}"


def _allocate_between(chapter: int, left: int | None, right: int | None, used: set[int]) -> str:
    if left is None and right is None:
        candidate = 10
    elif left is None:
        candidate = max(1, right // 2)
    elif right is None:
        candidate = left + 10
    elif right - left > 1:
        candidate = left + (right - left) // 2
    else:
        candidate = (max(used) if used else left) + 10
    while candidate in used:
        candidate += 1
    used.add(candidate)
    return _format_scene_id(chapter, candidate)


def _previous_scene_entries(previous_manifest: dict | None) -> dict[str, dict]:
    if not isinstance(previous_manifest, dict):
        return {}
    entries = previous_manifest.get("scenes")
    return entries if isinstance(entries, dict) else {}


def segment_chapter(page: str, chapter: int, previous_manifest: dict | None = None) -> list[dict]:
    if not isinstance(chapter, int) or chapter < 1:
        raise ValueError("chapter must be a positive integer")
    article = ARTICLE_RE.search(page)
    if not article:
        raise ValueError("missing article.prose")

    raw_segments = SCENE_BREAK_RE.split(article.group(2))
    sources: list[dict] = []
    paragraph_cursor = 1
    for raw_segment in raw_segments:
        paragraphs = [_plain(match.group(0)) for match in P_RE.finditer(raw_segment)]
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        if not paragraphs:
            continue
        start = paragraph_cursor
        end = paragraph_cursor + len(paragraphs) - 1
        sources.append({
            "chapter": chapter,
            "paragraphs": paragraphs,
            "paragraph_span": [start, end],
            "start_anchor": paragraphs[0],
            "end_anchor": paragraphs[-1],
            "hash": source_fingerprint(paragraphs),
        })
        paragraph_cursor = end + 1
    if not sources:
        raise ValueError("article.prose contains no readable paragraphs")

    previous_entries = _previous_scene_entries(previous_manifest)
    previous_order = previous_manifest.get("scene_order", []) if isinstance(previous_manifest, dict) else []
    if not isinstance(previous_order, list):
        previous_order = []
    previous_order = [scene_id for scene_id in previous_order if scene_id in previous_entries]
    hash_to_ids: dict[str, list[str]] = {}
    for scene_id in previous_order:
        source_hash = previous_entries[scene_id].get("source_hash")
        if isinstance(source_hash, str):
            hash_to_ids.setdefault(source_hash, []).append(scene_id)

    assigned: list[str | None] = [None] * len(sources)
    used_ids: set[str] = set()
    for index, source in enumerate(sources):
        candidates = [scene_id for scene_id in hash_to_ids.get(source["hash"], []) if scene_id not in used_ids]
        if len(candidates) == 1:
            assigned[index] = candidates[0]
            used_ids.add(candidates[0])

    if not previous_entries:
        assigned = [_format_scene_id(chapter, (index + 1) * 10) for index in range(len(sources))]
    else:
        used_numbers = {_scene_number(scene_id) for scene_id in previous_entries}
        used_numbers.update(_scene_number(scene_id) for scene_id in used_ids)
        for index, scene_id in enumerate(assigned):
            if scene_id is not None:
                continue
            left_number = None
            for left_index in range(index - 1, -1, -1):
                if assigned[left_index] is not None:
                    left_number = _scene_number(assigned[left_index])
                    break
            right_number = None
            for right_index in range(index + 1, len(assigned)):
                if assigned[right_index] is not None:
                    right_number = _scene_number(assigned[right_index])
                    break
            assigned[index] = _allocate_between(chapter, left_number, right_number, used_numbers)

    scenes: list[dict] = []
    for scene_id, source in zip(assigned, sources):
        assert scene_id is not None
        scene = {"scene_id": scene_id, "source": source}
        scene["mechanical"] = build_mechanical_ir(scene)
        scene["dependencies"] = {
            "mechanical": {
                "source_hash": source["hash"],
                "compiler": COMPILER_VERSIONS["mechanical"],
            }
        }
        scenes.append(scene)
    return scenes


def build_chapter_manifest(
    chapter: int,
    source_path: str,
    scenes: list[dict],
    compiler_versions: dict,
    previous_manifest: dict | None = None,
) -> dict:
    del previous_manifest
    scene_entries: dict[str, dict] = {}
    for scene in scenes:
        source = scene["source"]
        scene_entries[scene["scene_id"]] = {
            "source_hash": source["hash"],
            "start_anchor": source["start_anchor"],
            "end_anchor": source["end_anchor"],
            "paragraph_span": source["paragraph_span"],
            "status": "current",
        }
    return {
        "schema": "performance_chapter_manifest/v1",
        "chapter": chapter,
        "source_path": source_path,
        "source_hash": dependency_fingerprint([scene["source"]["hash"] for scene in scenes]),
        "compiler_versions": dict(compiler_versions),
        "scene_order": [scene["scene_id"] for scene in scenes],
        "scenes": scene_entries,
    }


def cache_status(
    scene_record: dict,
    *,
    source_hash: str,
    semantic_version: str,
    performance_version: str,
) -> dict:
    record_source = scene_record.get("source", {})
    dependencies = scene_record.get("dependencies", {})
    semantic_dep = dependencies.get("semantic", {}) if isinstance(dependencies, dict) else {}
    performance_dep = dependencies.get("performance", {}) if isinstance(dependencies, dict) else {}
    mechanical_valid = isinstance(record_source, dict) and record_source.get("hash") == source_hash
    semantic_valid = (
        mechanical_valid
        and isinstance(semantic_dep, dict)
        and semantic_dep.get("source_hash") == source_hash
        and semantic_dep.get("compiler") == semantic_version
    )
    performance_valid = (
        semantic_valid
        and isinstance(performance_dep, dict)
        and performance_dep.get("source_hash") == source_hash
        and performance_dep.get("compiler") == performance_version
    )
    return {
        "mechanical_valid": mechanical_valid,
        "semantic_valid": semantic_valid,
        "performance_valid": performance_valid,
    }


def validate_claim(claim: dict) -> None:
    if not isinstance(claim, dict) or "value" not in claim:
        raise ValueError("claim value is required")
    kind = claim.get("kind")
    if kind not in CLAIM_KINDS:
        raise ValueError(f"claim kind must be one of {sorted(CLAIM_KINDS)}")
    confidence = claim.get("confidence")
    if confidence is not None and (
        isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1
    ):
        raise ValueError("claim confidence must be between 0 and 1")
    if kind == "inferred":
        if confidence is None:
            raise ValueError("inferred claim confidence is required")
        if not _nonempty_text(claim.get("compiler")):
            raise ValueError("inferred claim compiler is required")
    if kind == "locked_derived" and not _nonempty_text(claim.get("compiler")):
        raise ValueError("locked_derived claim compiler is required")


def merge_derived_layer(
    scene_record: dict,
    layer: str,
    payload: dict,
    *,
    compiler: str,
    dependency_hash: str,
) -> dict:
    if layer not in {"semantic", "performance"}:
        raise ValueError("derived layer must be semantic or performance")
    if not isinstance(payload, dict):
        raise ValueError("derived layer payload must be an object")
    if not _nonempty_text(compiler) or not _nonempty_text(dependency_hash):
        raise ValueError("compiler and dependency_hash are required")
    updated = copy.deepcopy(scene_record)
    current = updated.get(layer)
    if not isinstance(current, dict):
        current = {}
        updated[layer] = current
    conflicts = updated.get("semantic_conflicts")
    if not isinstance(conflicts, list):
        conflicts = []
        updated["semantic_conflicts"] = conflicts

    for field, candidate in payload.items():
        validate_claim(candidate)
        existing = current.get(field)
        if existing is None:
            current[field] = copy.deepcopy(candidate)
            continue
        validate_claim(existing)
        if existing.get("value") == candidate.get("value"):
            if CLAIM_RANK[candidate["kind"]] > CLAIM_RANK[existing["kind"]]:
                current[field] = copy.deepcopy(candidate)
            continue
        if CLAIM_RANK[candidate["kind"]] > CLAIM_RANK[existing["kind"]]:
            current[field] = copy.deepcopy(candidate)
            continue
        conflicts.append({
            "field": f"{layer}.{field}",
            "previous": copy.deepcopy(existing),
            "candidate": copy.deepcopy(candidate),
            "status": "semantic_conflict",
        })

    dependencies = updated.get("dependencies")
    if not isinstance(dependencies, dict):
        dependencies = {}
        updated["dependencies"] = dependencies
    dependencies[layer] = {"dependency_hash": dependency_hash, "compiler": compiler}
    return updated


def _source_pointer(scene_record: dict) -> dict:
    source = scene_record.get("source")
    if not isinstance(source, dict):
        return {}
    return {
        key: copy.deepcopy(source[key])
        for key in ("hash", "chapter", "paragraph_span", "start_anchor", "end_anchor")
        if key in source
    }


def _pick(mapping: object, fields: tuple[str, ...]) -> dict:
    if not isinstance(mapping, dict):
        return {}
    return {field: copy.deepcopy(mapping[field]) for field in fields if field in mapping}


def render_scene_view(scene_record: dict, view: str) -> dict:
    if view not in VIEW_NAMES:
        raise ValueError(f"unknown scene view: {view}")
    source = _source_pointer(scene_record)
    mechanical = scene_record.get("mechanical", {})
    semantic = scene_record.get("semantic", {})
    result: dict = {"scene_id": scene_record.get("scene_id"), "source": source}

    if view == "performance":
        result["mechanical"] = _pick(mechanical, ("dialogue_turns", "dialogue_ratio", "question_count", "action_word_hits", "capitalized_tokens"))
        result["semantic"] = _pick(semantic, ("active_task", "characters", "state_in", "state_out", "relationship_pressure", "required_outcome", "must_not_drift", "location", "physical_state"))
        if isinstance(scene_record.get("performance"), dict):
            result["performance"] = copy.deepcopy(scene_record["performance"])
    elif view == "dialogue":
        result["mechanical"] = _pick(mechanical, ("dialogue_turns", "dialogue_word_count", "dialogue_ratio", "question_count", "capitalized_tokens", "action_word_hits"))
        result["semantic"] = _pick(semantic, ("characters", "relationship_pressure", "dialogue_mode", "voice_separation", "social_register", "emotional_state"))
        if isinstance(scene_record.get("performance"), dict):
            result["performance"] = copy.deepcopy(scene_record["performance"])
    elif view == "continuity":
        result["mechanical"] = _pick(mechanical, ("money_mentions", "capitalized_tokens"))
        result["semantic"] = _pick(semantic, ("continuity", "state_in", "state_out", "relationship_pressure", "required_outcome", "must_not_drift", "location", "objects"))
    elif view == "illustration":
        result["mechanical"] = _pick(mechanical, ("capitalized_tokens", "action_word_hits"))
        result["semantic"] = _pick(semantic, ("characters", "location", "objects", "active_task", "physical_state", "scene_turn", "required_outcome"))
        if isinstance(scene_record.get("performance"), dict):
            result["performance"] = copy.deepcopy(scene_record["performance"])
    else:  # comparison
        result["mechanical"] = _pick(mechanical, ("dialogue_turns", "dialogue_ratio", "question_count", "action_word_hits"))
        result["semantic"] = _pick(semantic, ("source_strengths", "compression_pressure", "performance_opportunity", "relationship_pressure", "required_outcome", "must_not_drift"))
        if isinstance(scene_record.get("performance"), dict):
            result["performance"] = copy.deepcopy(scene_record["performance"])
        if "screenplay" in scene_record:
            result["screenplay"] = copy.deepcopy(scene_record["screenplay"])
        if "comparison" in scene_record:
            result["comparison"] = copy.deepcopy(scene_record["comparison"])
    return result


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def write_compiled_chapter(
    chapter: int,
    page: str,
    output_root: Path,
    previous_manifest: dict | None = None,
) -> list[Path]:
    chapter_root = output_root / f"{chapter:03d}"
    manifest_path = chapter_root / "manifest.json"
    if previous_manifest is None and manifest_path.exists():
        try:
            loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
            previous_manifest = loaded if isinstance(loaded, dict) else None
        except (OSError, json.JSONDecodeError):
            previous_manifest = None
    scenes = segment_chapter(page, chapter, previous_manifest=previous_manifest)
    manifest = build_chapter_manifest(
        chapter,
        f"chapters/{chapter:03d}.html",
        scenes,
        COMPILER_VERSIONS,
        previous_manifest=previous_manifest,
    )
    written: list[Path] = []
    _write_json(manifest_path, manifest)
    written.append(manifest_path)
    for scene in scenes:
        suffix = scene["scene_id"].split(".", 1)[1]
        scene_path = chapter_root / f"{suffix}.json"
        _write_json(scene_path, scene)
        written.append(scene_path)
    return written


def validate_record(record: dict) -> None:
    chapter = record.get("chapter")
    if not isinstance(chapter, int) or chapter < 1:
        raise ValueError("chapter must be a positive integer")
    verdict = record.get("verdict")
    if verdict not in {"source_win", "change_survives"}:
        raise ValueError("verdict must be source_win or change_survives")
    screen = record.get("screen")
    if not isinstance(screen, dict):
        raise ValueError("screen is required")
    if screen.get("decision") not in {"source_win", "deep_review"}:
        raise ValueError("screen decision must be source_win or deep_review")
    if not isinstance(screen.get("signals"), list):
        raise ValueError("screen signals must be a list")
    if not _nonempty_text(screen.get("reason")):
        raise ValueError("screen reason is required")
    if verdict == "source_win":
        if screen.get("decision") == "deep_review" and not _nonempty_text(record.get("comparison")):
            raise ValueError("comparison is required for a deep-review source win")
        return
    if screen.get("decision") != "deep_review":
        raise ValueError("change_survives verdict requires deep_review screen decision")
    for field in ("dramatic", "performance", "screenplay", "comparison"):
        if not _nonempty_text(record.get(field)):
            raise ValueError(f"{field} is required for a surviving change")
    patches = record.get("patches")
    if not isinstance(patches, list) or not patches:
        raise ValueError("patches are required for a surviving change")
    for index, patch in enumerate(patches):
        if not isinstance(patch, dict):
            raise ValueError(f"patch {index} must be an object")
        for field in ("start", "end", "rationale"):
            if not _nonempty_text(patch.get(field)):
                raise ValueError(f"patch {index} {field} is required")
        replacement = patch.get("replacement")
        if not isinstance(replacement, list) or not replacement or not all(_nonempty_text(line) for line in replacement):
            raise ValueError(f"patch {index} replacement must contain prose paragraphs")
        if any("—" in line for line in replacement):
            raise ValueError(f"patch {index} replacement contains an em dash")


def validate_batch(batch: dict) -> None:
    if batch.get("schema") != "performance_production_batch/v1":
        raise ValueError("schema must be performance_production_batch/v1")
    if not _nonempty_text(batch.get("source_authority")):
        raise ValueError("source_authority is required")
    scope = batch.get("scope")
    if not isinstance(scope, list) or not scope or not all(isinstance(chapter, int) and chapter > 0 for chapter in scope):
        raise ValueError("scope must contain positive chapter integers")
    if len(scope) != len(set(scope)):
        raise ValueError("scope must not contain duplicate chapters")
    records = batch.get("records")
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    record_chapters = [record.get("chapter") for record in records if isinstance(record, dict)]
    if len(records) != len(scope) or sorted(record_chapters) != sorted(scope):
        raise ValueError("batch coverage must include every scope chapter exactly once")
    for record in records:
        validate_record(record)


def _render_paragraph(text: str) -> str:
    if "—" in text:
        raise ValueError("replacement contains an em dash")
    return f"<p>{html.escape(text, quote=True)}</p>"


def _replace_paragraph_span(page: str, patch: dict) -> str:
    article = ARTICLE_RE.search(page)
    if not article:
        raise ValueError("missing article.prose")
    body = article.group(2)
    paragraphs = list(P_RE.finditer(body))
    plain = [_plain(match.group(0)) for match in paragraphs]
    start = re.sub(r"\s+", " ", patch["start"]).strip()
    end = re.sub(r"\s+", " ", patch["end"]).strip()
    starts = [index for index, value in enumerate(plain) if value == start]
    if len(starts) != 1:
        raise ValueError(f"start boundary matched {len(starts)} times: {patch['start']!r}")
    start_index = starts[0]
    ends = [index for index, value in enumerate(plain) if index >= start_index and value == end]
    if len(ends) != 1:
        raise ValueError(f"end boundary matched {len(ends)} times after start: {patch['end']!r}")
    end_index = ends[0]
    rendered = "".join(_render_paragraph(text) for text in patch["replacement"])
    body = body[:paragraphs[start_index].start()] + rendered + body[paragraphs[end_index].end():]
    return page[:article.start(2)] + body + page[article.end(2):]


def apply_record(page: str, record: dict) -> str:
    validate_record(record)
    if record["verdict"] == "source_win":
        return page
    updated = page
    for patch in record["patches"]:
        updated = _replace_paragraph_span(updated, patch)
    return updated


def apply_batch_to_root(batch: dict, chapter_root: Path) -> list[Path]:
    validate_batch(batch)
    changed: list[Path] = []
    for record in batch["records"]:
        if record["verdict"] != "change_survives":
            continue
        path = chapter_root / f"{record['chapter']:03d}.html"
        if not path.exists():
            raise ValueError(f"canonical chapter missing: {path.name}")
        original = path.read_text(encoding="utf-8")
        updated = apply_record(original, record)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or apply a PERFORMANCE production batch.")
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--chapter-root", type=Path, default=ROOT / "chapters")
    args = parser.parse_args()
    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    validate_batch(batch)
    if args.apply:
        changed = apply_batch_to_root(batch, args.chapter_root)
        print(json.dumps({"changed": [path.as_posix() for path in changed]}, indent=2))
    else:
        print(json.dumps({"scope_count": len(batch["scope"]), "survivors": [r["chapter"] for r in batch["records"] if r["verdict"] == "change_survives"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
