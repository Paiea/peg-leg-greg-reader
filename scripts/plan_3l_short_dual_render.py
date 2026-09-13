#!/usr/bin/env python3
"""Plan preview-safe dual-render audio chunks for 3L cave-frame records."""

from __future__ import annotations

import argparse
import copy
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
    r"\b(?:Ithar|the dragon|dragon)\b.*(?:\b(?:continued|spoke|asked|said|answered|replied)\b|\btook the floor\b)",
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


def _resolve_quote_speaker(
    paragraph: str,
    last_speaker: str | None,
    next_hint: str | None,
) -> str:
    explicit = _attributed_speaker(paragraph)
    if explicit is not None:
        return explicit
    if next_hint in {"greg", "dragon"}:
        return next_hint
    if last_speaker is None:
        return "greg"
    return "dragon" if last_speaker == "greg" else "greg"


def _split_semantic_segments(paragraph: str, last_speaker: str | None, next_hint: str | None) -> tuple[list[dict], str | None]:
    """Split narration vs quoted speech while resolving cave dialogue turns."""
    matches = list(QUOTE_RE.finditer(paragraph))
    if not matches:
        return [{"role": "greg", "text": paragraph}], None

    quote_speaker = _resolve_quote_speaker(paragraph, last_speaker, next_hint)

    segments: list[dict] = []
    cursor = 0
    for match in matches:
        if match.start() > cursor:
            segments.append({"role": "greg", "text": paragraph[cursor:match.start()]})
        segments.append({"role": quote_speaker, "text": match.group(0)})
        cursor = match.end()
    if cursor < len(paragraph):
        segments.append({"role": "greg", "text": paragraph[cursor:]})

    return _collapse_segments(segments), quote_speaker


def _collapse_segments(segments: list[dict]) -> list[dict]:
    collapsed: list[dict] = []
    for segment in segments:
        if not segment["text"]:
            continue
        if collapsed and collapsed[-1]["role"] == segment["role"]:
            collapsed[-1]["text"] += segment["text"]
        else:
            collapsed.append(dict(segment))
    return collapsed


def _sustained_quote_segments(paragraph: str, role: str) -> tuple[list[dict], bool]:
    """Route one paragraph inside an already-open multi-paragraph quotation.

    Standard prose opens each continued paragraph with a new left smart quote and
    supplies a right smart quote only on the final paragraph. Everything through
    that final closing mark belongs to the same speaker. Any text after it returns
    to Greg narration.
    """
    close_at = paragraph.find("”")
    if close_at < 0:
        return [{"role": role, "text": paragraph}], True

    close_at += 1
    segments = [{"role": role, "text": paragraph[:close_at]}]
    if close_at < len(paragraph):
        segments.append({"role": "greg", "text": paragraph[close_at:]})
    return _collapse_segments(segments), False


def classify_paragraphs(text: str) -> list[dict]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]
    rows: list[dict] = []
    last_speaker: str | None = None
    next_hint: str | None = None
    open_quote_role: str | None = None

    for paragraph in paragraphs:
        explicit = _attributed_speaker(paragraph)

        if open_quote_role is not None and paragraph.startswith("“"):
            segments, remains_open = _sustained_quote_segments(paragraph, open_quote_role)
            spoken = open_quote_role
            role = spoken
            last_speaker = spoken
            next_hint = None
            if not remains_open:
                open_quote_role = None
            rows.append({"role": role, "text": paragraph, "segments": segments, "explicit": explicit})
            continue

        if paragraph.startswith("“") and "”" not in paragraph:
            spoken = _resolve_quote_speaker(paragraph, last_speaker, next_hint)
            open_quote_role = spoken
            last_speaker = spoken
            next_hint = None
            rows.append(
                {
                    "role": spoken,
                    "text": paragraph,
                    "segments": [{"role": spoken, "text": paragraph}],
                    "explicit": explicit,
                }
            )
            continue

        segments, spoken = _split_semantic_segments(paragraph, last_speaker, next_hint)
        if spoken is not None:
            last_speaker = spoken
            next_hint = None
        else:
            if DRAGON_NEXT_RE.search(paragraph):
                next_hint = "dragon"
            elif GREG_NEXT_RE.search(paragraph):
                next_hint = "greg"

        role = spoken or "greg"
        rows.append({"role": role, "text": paragraph, "segments": segments, "explicit": explicit})
    return rows


def extract_quote_inventory(text: str) -> list[dict]:
    """Return an occurrence-indexed quote ledger with heuristic speaker proposals."""
    rows = classify_paragraphs(text)
    inventory: list[dict] = []
    quote_id = 0
    for paragraph_index, row in enumerate(rows, start=1):
        for match in QUOTE_RE.finditer(row["text"]):
            quote_id += 1
            inventory.append(
                {
                    "id": quote_id,
                    "text": match.group(0),
                    "paragraph": paragraph_index,
                    "heuristic_role": row["role"],
                    "explicit": row.get("explicit"),
                    "context": row["text"],
                }
            )
    return inventory


def apply_quote_role_overrides(rows: list[dict], overrides: dict[int, str]) -> list[dict]:
    """Apply authoritative occurrence-indexed speaker roles while keeping narration Greg."""
    adjusted = copy.deepcopy(rows)
    quote_id = 0
    for row in adjusted:
        paragraph = row["text"]
        matches = list(QUOTE_RE.finditer(paragraph))
        if not matches:
            # Multi-paragraph quote rows are already semantically classified and
            # must not be reset to Greg merely because they have no local closing mark.
            if paragraph.startswith("“") and row.get("role") in {"greg", "dragon"}:
                continue
            row["role"] = "greg"
            row["segments"] = [{"role": "greg", "text": paragraph}]
            continue

        segments: list[dict] = []
        cursor = 0
        first_quote_role: str | None = None
        for match in matches:
            quote_id += 1
            if match.start() > cursor:
                segments.append({"role": "greg", "text": paragraph[cursor:match.start()]})
            role = overrides.get(quote_id, row["role"])
            if role not in {"greg", "dragon"}:
                raise ValueError(f"invalid role for quote {quote_id}: {role}")
            if first_quote_role is None:
                first_quote_role = role
            segments.append({"role": role, "text": match.group(0)})
            cursor = match.end()
        if cursor < len(paragraph):
            segments.append({"role": "greg", "text": paragraph[cursor:]})
        row["segments"] = _collapse_segments(segments)
        row["role"] = first_quote_role or "greg"
    unknown = sorted(set(overrides) - set(range(1, quote_id + 1)))
    if unknown:
        raise ValueError(f"quote override ids out of range: {unknown}")
    return adjusted


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
    required = sorted({"deep" if span["role"] == "greg" else "normal" for span in spans})
    return {
        "index": index,
        "transcript": transcript,
        "char_count": len(transcript),
        "roles": roles,
        "semantic_spans": spans,
        "required_voices": required,
        "dual_render": len(required) == 2,
        "captures": {voice: None for voice in required},
    }


def _split_oversize(item: dict, max_chars: int) -> list[dict]:
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
        # Oversize pieces inherit the already-resolved semantic owner. Re-running
        # quote alternation here can corrupt sustained Dragon territories.
        role = item["role"] if item["role"] in {"greg", "dragon"} else "greg"
        pieces.append({"role": role, "text": piece, "segments": [{"role": role, "text": piece}], "explicit": item.get("explicit")})
    if remaining:
        role = item["role"] if item["role"] in {"greg", "dragon"} else "greg"
        pieces.append({"role": role, "text": remaining, "segments": [{"role": role, "text": remaining}], "explicit": item.get("explicit")})
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


def _load_role_overrides(path: Path | None) -> dict[int, str]:
    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    mapping = raw.get("roles", raw)
    return {int(key): value for key, value in mapping.items()}


def _write_inventory(path: Path, inventory: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["id\theuristic_role\texplicit\tquote\tcontext"]
    for item in inventory:
        clean_context = re.sub(r"\s+", " ", item["context"]).replace("\t", " ").strip()
        clean_quote = item["text"].replace("\t", " ").replace("\n", " ")
        lines.append(
            f"{item['id']:03d}\t{item['heuristic_role']}\t{item['explicit'] or ''}\t{clean_quote}\t{clean_context}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_plan(markdown: str, source: str, max_chars: int = 500, quote_roles: dict[int, str] | None = None) -> dict:
    record, title, body = strip_headings(markdown)
    paragraphs = classify_paragraphs(body)
    if quote_roles:
        paragraphs = apply_quote_role_overrides(paragraphs, quote_roles)
    chunks = make_chunks(paragraphs, max_chars=max_chars)
    rebuilt = "\n\n".join(chunk["transcript"] for chunk in chunks)
    if rebuilt != body:
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
        "quote_roles_locked": bool(quote_roles),
        "quote_count": len(extract_quote_inventory(body)),
        "chunk_count": len(chunks),
        "chunks": chunks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--max-chars", type=int, default=500)
    parser.add_argument("--quote-roles", type=Path)
    parser.add_argument("--inventory-output", type=Path)
    args = parser.parse_args()
    source = Path(args.input)
    output = Path(args.output)
    markdown = source.read_text(encoding="utf-8")
    _, _, body = strip_headings(markdown)
    inventory = extract_quote_inventory(body)
    if args.inventory_output:
        _write_inventory(args.inventory_output, inventory)
    plan = build_plan(
        markdown,
        str(source),
        args.max_chars,
        quote_roles=_load_role_overrides(args.quote_roles),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Record {plan['record']} {plan['title']}: {plan['chunk_count']} chunks, {plan['quote_count']} quotes")


if __name__ == "__main__":
    main()
