#!/usr/bin/env python3
"""Plan preview-safe dual-render audio chunks for 3L cave-frame records."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

QUOTE_RE = re.compile(r"“[^”]*”")
GREG_ATTR_RE = re.compile(
    r"\bI\s+(?:said|asked|answered|replied|told|added|continued|repeated|muttered|whispered|shouted|called|said again)\b",
    re.IGNORECASE,
)
DRAGON_ATTR_RE = re.compile(
    r"\b(?:Ithar|the dragon|dragon|he)\s+(?:said|asked|answered|replied|added|continued|spoke|said again)\b",
    re.IGNORECASE,
)
DRAGON_NEXT_RE = re.compile(
    r"\b(?:Ithar|the dragon|dragon)\b.*\b(?:continued|spoke|asked|said|answered|replied)\b",
    re.IGNORECASE,
)
GREG_NEXT_RE = re.compile(
    r"\bI\b.*\b(?:said|asked|answered|replied|continued|repeated)\b",
    re.IGNORECASE,
)


def strip_headings(markdown: str) -> tuple[str | None, str | None, str]:
    lines = markdown.splitlines()
    record = None
    title = None
    body_start = 0
    headings_seen = 0
    for index, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        headings_seen += 1
        value = line[3:].strip()
        if headings_seen == 1:
            record = value.replace("RECORD ", "").strip()
        elif headings_seen == 2:
            title = value
            body_start = index + 1
            break
    body = "\n".join(lines[body_start:]).strip()
    return record, title, body


def _attributed_speaker(paragraph: str) -> str | None:
    if GREG_ATTR_RE.search(paragraph):
        return "greg"
    if DRAGON_ATTR_RE.search(paragraph):
        return "dragon"
    return None


def _split_semantic_segments(paragraph: str, last_speaker: str | None, next_hint: str | None) -> tuple[list[dict], str | None]:
    """Split narration vs quoted speech while resolving cave dialogue turns."""
    matches = list(QUOTE_RE.finditer(paragraph))
    if not matches:
        return [{"role": "greg", "text": paragraph}], last_speaker

    explicit = _attributed_speaker(paragraph)
    quote_speaker = explicit
    if quote_speaker is None:
        if next_hint in {"greg", "dragon"}:
            quote_speaker = next_hint
        elif last_speaker is None:
            # Record openings normally resume Greg's account unless attribution says otherwise.
            quote_speaker = "greg"
        else:
            quote_speaker = "dragon" if last_speaker == "greg" else "greg"

    segments: list[dict] = []
    cursor = 0
    for match in matches:
        if match.start() > cursor:
            segments.append({"role": "greg", "text": paragraph[cursor:match.start()]})
        segments.append({"role": quote_speaker, "text": match.group(0)})
        cursor = match.end()
    if cursor < len(paragraph):
        segments.append({"role": "greg", "text": paragraph[cursor:]})

    # Collapse adjacent same-role pieces without changing characters.
    collapsed: list[dict] = []
    for segment in segments:
        if not segment["text"]:
            continue
        if collapsed and collapsed[-1]["role"] == segment["role"]:
            collapsed[-1]["text"] += segment["text"]
        else:
            collapsed.append(dict(segment))
    return collapsed, quote_speaker


def classify_paragraphs(text: str) -> list[dict]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]
    rows: list[dict] = []
    last_speaker: str | None = None
    next_hint: str | None = None

    for paragraph in paragraphs:
        segments, spoken = _split_semantic_segments(paragraph, last_speaker, next_hint)
        explicit = _attributed_speaker(paragraph)
        if spoken is not None:
            last_speaker = spoken
            next_hint = None
        else:
            if DRAGON_NEXT_RE.search(paragraph):
                next_hint = "dragon"
            elif GREG_NEXT_RE.search(paragraph):
                next_hint = "greg"

        # Coarse paragraph role exists for audits/tests. Mixed narration + quote retains
        # the spoken turn's role; detailed segments remain authoritative for assembly.
        role = spoken or "greg"
        rows.append({"role": role, "text": paragraph, "segments": segments, "explicit": explicit})
    return rows


def _chunk_from_items(items: list[dict], index: int) -> dict:
    transcript_parts: list[str] = []
    spans: list[dict] = []
    roles: list[str] = []
    offset = 0
    for item_index, item in enumerate(items):
        if item_index:
            transcript_parts.append("\n\n")
            offset += 2
        roles.append(item["role"])
        paragraph_start = offset
        transcript_parts.append(item["text"])
        for segment in item.get("segments", [{"role": item["role"], "text": item["text"]}]):
            seg_start = offset
            seg_end = seg_start + len(segment["text"])
            if spans and spans[-1]["role"] == segment["role"] and spans[-1]["end"] == seg_start:
                spans[-1]["end"] = seg_end
                spans[-1]["text"] += segment["text"]
            else:
                spans.append({"start": seg_start, "end": seg_end, "role": segment["role"], "text": segment["text"]})
            offset = seg_end
        if offset != paragraph_start + len(item["text"]):
            raise ValueError("semantic segments do not reconstruct paragraph exactly")
    transcript = "".join(transcript_parts)
    return {
        "index": index,
        "transcript": transcript,
        "char_count": len(transcript),
        "roles": roles,
        "semantic_spans": spans,
        "dual_render": True,
        "captures": {"deep": None, "normal": None},
    }


def _split_oversize(item: dict, max_chars: int) -> list[dict]:
    """Split an exceptional oversize paragraph at sentence/space boundaries."""
    text = item["text"]
    if len(text) <= max_chars:
        return [item]
    pieces: list[dict] = []
    remaining = text
    while len(remaining) > max_chars:
        window = remaining[: max_chars + 1]
        candidates = [m.end() for m in re.finditer(r"[.!?][”']?(?:\s+|$)", window)]
        cut = max(candidates) if candidates else window.rfind(" ") + 1
        if cut <= 0 or cut > max_chars:
            cut = max_chars
        piece = remaining[:cut]
        remaining = remaining[cut:]
        # Preserve every character. The split piece is re-segmented independently.
        segs, _ = _split_semantic_segments(piece, None, item["role"] if item["role"] in {"greg", "dragon"} else None)
        pieces.append({"role": item["role"], "text": piece, "segments": segs, "explicit": item.get("explicit")})
    if remaining:
        segs, _ = _split_semantic_segments(remaining, None, item["role"] if item["role"] in {"greg", "dragon"} else None)
        pieces.append({"role": item["role"], "text": remaining, "segments": segs, "explicit": item.get("explicit")})
    return pieces


def make_chunks(paragraphs: list[dict], max_chars: int = 500) -> list[dict]:
    expanded: list[dict] = []
    for item in paragraphs:
        expanded.extend(_split_oversize(item, max_chars))

    chunks: list[dict] = []
    current: list[dict] = []
    current_len = 0
    for item in expanded:
        addition = len(item["text"]) + (2 if current else 0)
        if current and current_len + addition > max_chars:
            chunks.append(_chunk_from_items(current, len(chunks) + 1))
            current = []
            current_len = 0
            addition = len(item["text"])
        current.append(item)
        current_len += addition
    if current:
        chunks.append(_chunk_from_items(current, len(chunks) + 1))
    return chunks


def build_plan(markdown: str, source: str, max_chars: int = 500) -> dict:
    record, title, body = strip_headings(markdown)
    paragraphs = classify_paragraphs(body)
    chunks = make_chunks(paragraphs, max_chars=max_chars)
    rebuilt = "\n\n".join(chunk["transcript"] for chunk in chunks)
    if rebuilt != body:
        # Oversize paragraph splitting preserves characters but not necessarily paragraph separators.
        # Compare normalized whitespace as a final guard without changing output.
        normalize = lambda value: re.sub(r"\s+", " ", value).strip()
        if normalize(rebuilt) != normalize(body):
            raise ValueError("chunk plan does not preserve canon text")
    return {
        "record": record,
        "title": title,
        "source": source,
        "method": "preview-safe-short-dual-render",
        "authority": "3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md",
        "max_chars": max_chars,
        "voices": {"greg": "deep", "dragon": "normal"},
        "chunk_count": len(chunks),
        "chunks": chunks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--max-chars", type=int, default=500)
    args = parser.parse_args()
    source = Path(args.input)
    output = Path(args.output)
    plan = build_plan(source.read_text(encoding="utf-8"), str(source), args.max_chars)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Record {plan['record']} {plan['title']}: {plan['chunk_count']} chunks")


if __name__ == "__main__":
    main()
