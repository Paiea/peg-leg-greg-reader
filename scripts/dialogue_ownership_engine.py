#!/usr/bin/env python3
"""Identity-aware dialogue paragraph ownership helpers.

This module is deliberately conservative about prose rewriting. It identifies
clear dramatic-owner changes inside paragraphs that contain quoted dialogue and
returns paragraph-sized ownership beats without changing the words themselves.
"""
from __future__ import annotations

from dataclasses import dataclass
import re


SPEECH_VERBS = {
    "said", "asked", "answered", "replied", "told", "called", "shouted",
    "yelled", "whispered", "muttered", "murmured", "continued", "added",
    "offered", "warned", "insisted", "snapped", "growled", "sighed",
    "admitted", "agreed", "argued", "explained", "demanded", "ordered",
    "promised", "suggested", "announced", "observed", "remarked",
}

ACTION_VERBS = {
    "accepted", "adjusted", "answered", "asked", "blinked", "bowed",
    "breathed", "called", "checked", "closed", "continued", "counted",
    "crossed", "denied", "drummed", "exhaled", "flinched", "folded",
    "froze", "glanced", "glared", "grinned", "groaned", "laughed",
    "leaned", "left", "looked", "moved", "nodded", "opened", "paused",
    "picked", "pointed", "pulled", "pushed", "raised", "reached",
    "sat", "shook", "shrugged", "sighed", "smiled", "stared", "stood",
    "stopped", "swore", "tapped", "turned", "waited", "walked",
    "watched", "waved", "winced", "wrote", "took", "gave", "held",
    "set", "slid", "put", "ran", "stepped", "returned", "followed",
    "tilted", "rubbed", "scratched", "lifted", "dropped", "caught",
    "kicked", "flattened", "tightened", "changed", "softened",
}

ACTOR_PATTERN = (
    r"I|My|Greg|He|She|They|His|Her|Their"
    r"|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?"
    r"|[A-Z][a-z]+'s"
    r"|The\s+[a-z]+(?:\s+[a-z]+){0,3}"
    r"(?:\s+(?:with|in|at|by|from|near|behind|beside|under|over)"
    r"\s+(?:the\s+)?[a-z]+(?:\s+[a-z]+){0,3})?"
)


@dataclass(frozen=True)
class Beat:
    text: str
    owner: str | None
    explicit: bool


def quoted_spans(text: str) -> list[str]:
    """Return double-quoted spans in order, including quote marks."""
    spans: list[str] = []
    start: int | None = None
    escaped = False
    for index, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char != '"':
            continue
        if start is None:
            start = index
        else:
            spans.append(text[start:index + 1])
            start = None
    return spans


def _is_attribution_tail(text: str) -> bool:
    tail = text.lstrip()
    if not tail:
        return False
    actor = rf"(?:{ACTOR_PATTERN})"
    verbs = "|".join(sorted(SPEECH_VERBS, key=len, reverse=True))
    return re.match(rf"^{actor}\s+(?:{verbs})\b", tail) is not None


def _beat_ranges(text: str) -> list[tuple[int, int]]:
    """Split prose into sentence-like beats while keeping dialogue tags intact."""
    if not text.strip():
        return []
    boundaries: list[int] = []
    in_quote = False
    escaped = False
    for index, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            was_in_quote = in_quote
            in_quote = not in_quote
            if was_in_quote and index > 0 and text[index - 1] in ".!?":
                if not _is_attribution_tail(text[index + 1:]):
                    boundaries.append(index + 1)
            continue
        if not in_quote and char in ".!?":
            boundaries.append(index + 1)

    ranges: list[tuple[int, int]] = []
    start = 0
    for end in sorted(set(boundaries)):
        if end <= start:
            continue
        if text[start:end].strip():
            ranges.append((start, end))
        start = end
    if text[start:].strip():
        ranges.append((start, len(text)))
    return ranges


def _normalize_actor(actor: str) -> str:
    raw = actor.strip()
    if raw in {"I", "My", "Greg"}:
        return "GREG"
    if raw in {"He", "She", "They", "His", "Her", "Their"}:
        return f"PRONOUN:{raw.lower()}"
    if raw.endswith("'s") and raw[:-2] and raw[:-2][0].isupper():
        return f"NAME:{raw[:-2]}"
    if raw.startswith("The "):
        return "DESC:" + re.sub(r"\s+", " ", raw.lower())
    if raw and raw[0].isupper():
        # Prefer the first given/proper name as the stable identity. This keeps
        # `Antonius Vale` compatible with later `Antonius` beats.
        return f"NAME:{raw.split()[0]}"
    return "UNKNOWN"


def _speech_owner(text: str) -> str | None:
    if '"' not in text:
        return None
    verbs = "|".join(sorted(SPEECH_VERBS, key=len, reverse=True))
    actor = rf"(?P<actor>{ACTOR_PATTERN})"

    # Dialogue followed by attribution: "No," Sella said.
    after = re.search(rf'"\s*{actor}\s+(?:{verbs})\b', text)
    if after:
        return _normalize_actor(after.group("actor"))

    # Attribution followed by dialogue: Sella said, "No."
    before = re.search(rf'\b{actor}\s+(?:{verbs})\b[^"\n]*"', text)
    if before:
        return _normalize_actor(before.group("actor"))
    return None


def _subject_owner(text: str) -> str | None:
    outside = re.sub(r'"(?:[^"\\]|\\.)*"', '', text).strip()
    if not outside:
        return None
    verbs = "|".join(sorted(ACTION_VERBS | SPEECH_VERBS, key=len, reverse=True))
    actor = rf"(?P<actor>{ACTOR_PATTERN})"
    match = re.match(rf"^{actor}\s+(?:{verbs})\b", outside)
    if match:
        return _normalize_actor(match.group("actor"))
    return None


def _beat_owner(text: str) -> tuple[str | None, bool]:
    speech = _speech_owner(text)
    if speech:
        return speech, True
    subject = _subject_owner(text)
    if subject:
        return subject, not subject.startswith("PRONOUN:")
    return None, False


def _compatible(current: str | None, incoming: str | None, *, incoming_explicit: bool) -> bool:
    if incoming is None:
        return True
    if current is None:
        return False
    if current == incoming:
        return True

    if incoming.startswith("PRONOUN:"):
        if current == "GREG":
            return False
        # Third-person pronouns may continue an explicitly established
        # non-Greg owner. Splitting every `He` after `Antonius said` would make
        # the book artificially choppy.
        return current.startswith(("NAME:", "DESC:", "PRONOUN:"))

    if current.startswith("PRONOUN:") and incoming_explicit:
        # An explicit identity after an unresolved pronoun is a safer place to
        # begin a new paragraph than to guess they are the same person.
        return False

    return False


def split_paragraph(text: str) -> list[str]:
    """Return one-owner paragraph beats for a paragraph containing dialogue.

    Ordinary narration without dialogue is deliberately untouched.
    """
    original = text.strip()
    if not original or '"' not in original:
        return [original] if original else []

    raw_beats = [original[start:end].strip() for start, end in _beat_ranges(original)]
    if len(raw_beats) <= 1:
        return [original]

    beats: list[Beat] = []
    for raw in raw_beats:
        owner, explicit = _beat_owner(raw)
        beats.append(Beat(raw, owner, explicit))

    groups: list[list[str]] = []
    current_parts: list[str] = []
    current_owner: str | None = None

    for beat in beats:
        owner = beat.owner

        # Pure quoted dialogue after an established action/speaker belongs to
        # that owner. At paragraph start it remains unknown until evidence
        # arrives, and we split rather than attach it to a later actor blindly.
        if owner is None and beat.text.startswith('"') and current_owner is not None:
            owner = current_owner

        if not current_parts:
            current_parts = [beat.text]
            current_owner = owner
            continue

        should_split = False
        if current_owner is None and owner is not None:
            # Unknown opening dialogue followed by a clear reactor is exactly
            # the risky pattern that created false attribution in the reader.
            should_split = True
        elif not _compatible(current_owner, owner, incoming_explicit=beat.explicit):
            should_split = True

        if should_split:
            groups.append(current_parts)
            current_parts = [beat.text]
            current_owner = owner
        else:
            current_parts.append(beat.text)
            if current_owner is None and owner is not None:
                current_owner = owner

    if current_parts:
        groups.append(current_parts)

    result = [" ".join(parts).strip() for parts in groups if any(part.strip() for part in parts)]

    # Automated ownership work must never alter quoted dialogue wording.
    if quoted_spans(" ".join(result)) != quoted_spans(original):
        raise ValueError("dialogue changed while splitting paragraph")
    return result


def explicit_owners(text: str) -> list[str]:
    """Return distinct explicit owners found in dialogue-bearing sentence beats."""
    owners: list[str] = []
    for start, end in _beat_ranges(text.strip()):
        owner, explicit = _beat_owner(text.strip()[start:end].strip())
        if owner and explicit and owner not in owners:
            owners.append(owner)
    return owners


def mixed_owner_candidate(text: str) -> bool:
    """Flag obvious residual multi-owner dialogue paragraphs for audit."""
    if '"' not in text:
        return False
    return len(explicit_owners(text)) > 1
