#!/usr/bin/env python3
"""Conservative dialogue-ownership candidate detection.

This module does not infer the true speaker and never rewrites prose. It only
surfaces paragraph shapes that deserve semantic review because an untagged
spoken turn is followed by a third-person/name action beat or because multiple
quoted turns are bridged by such an action inside one paragraph.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re


QUOTE_RE = re.compile(r'["“](.*?)["”]')
ACTION_SUBJECT_RE = re.compile(
    r"^\s*(?P<subject>"
    r"(?:The|the|A|a|An|an)\s+[a-z][A-Za-z'’\-]*(?:\s+[a-z][A-Za-z'’\-]*)?"
    r"|He|She|They|[A-Z][A-Za-z'’\-]+"
    r")\s+(?P<verb>[a-z][A-Za-z'’\-]*)\b"
)
SPEECH_VERBS = {
    "said",
    "asked",
    "replied",
    "answered",
    "continued",
    "added",
    "called",
    "shouted",
    "whispered",
    "muttered",
    "told",
    "remarked",
    "offered",
}
ACTION_VERBS = {
    "looked",
    "smiled",
    "laughed",
    "nodded",
    "frowned",
    "shrugged",
    "leaned",
    "stood",
    "sat",
    "turned",
    "stared",
    "watched",
    "pointed",
    "held",
    "took",
    "picked",
    "pushed",
    "pulled",
    "crossed",
    "sighed",
    "blinked",
    "froze",
    "stopped",
    "waited",
    "moved",
    "walked",
    "stepped",
    "glanced",
    "tapped",
    "reached",
    "opened",
    "closed",
    "followed",
    "started",
    "stayed",
    "kept",
    "put",
    "set",
    "folded",
    "unfolded",
    "lifted",
    "lowered",
    "handed",
    "touched",
    "checked",
    "counted",
    "tilted",
    "shook",
    "raised",
    "dropped",
    "waved",
    "grinned",
    "winced",
    "flinched",
    "paused",
    "breathed",
    "exhaled",
    "inhaled",
    "rubbed",
    "scratched",
    "shifted",
    "backed",
    "came",
    "went",
    "left",
    "returned",
    "approached",
    "grabbed",
    "caught",
    "released",
    "gestured",
    "did",
    "named",
    "swore",
    "considered",
}


@dataclass(frozen=True)
class OwnershipCandidate:
    paragraph_index: int
    rule: str
    confidence: str
    previous: str
    current: str
    following: str
    fingerprint: str


def _fingerprint(rule: str, previous: str, current: str, following: str) -> str:
    payload = "\0".join((rule, previous, current, following)).encode("utf-8")
    return sha256(payload).hexdigest()[:20]


def _third_person_action(text: str) -> re.Match[str] | None:
    match = ACTION_SUBJECT_RE.match(text)
    if not match:
        return None
    verb = match.group("verb").lower()
    if verb in SPEECH_VERBS or verb not in ACTION_VERBS:
        return None
    return match


def scan_paragraphs(paragraphs: list[str]) -> list[OwnershipCandidate]:
    """Return suspicious dialogue-ownership shapes with neighboring context.

    False positives are acceptable here. The output is a review queue, not an
    automatic prose verdict. In particular, a same-speaker `"No." He smiled.`
    beat can be structurally valid; semantic review decides whether the action
    actor is actually the speaker in that local exchange.
    """

    candidates: list[OwnershipCandidate] = []

    for index, current in enumerate(paragraphs):
        stripped = current.lstrip()
        if not stripped.startswith(('"', '“')):
            continue

        quotes = list(QUOTE_RE.finditer(current))
        if not quotes:
            continue

        previous = paragraphs[index - 1] if index else ""
        following = paragraphs[index + 1] if index + 1 < len(paragraphs) else ""
        first = quotes[0]

        if len(quotes) >= 2:
            between = current[first.end() : quotes[1].start()]
            if _third_person_action(between):
                rule = "possible_multi_speaker_paragraph"
                candidates.append(
                    OwnershipCandidate(
                        paragraph_index=index,
                        rule=rule,
                        confidence="review-high",
                        previous=previous,
                        current=current,
                        following=following,
                        fingerprint=_fingerprint(rule, previous, current, following),
                    )
                )
                continue

        trailing = current[first.end() :]
        if _third_person_action(trailing):
            rule = "untagged_dialogue_followed_by_action"
            candidates.append(
                OwnershipCandidate(
                    paragraph_index=index,
                    rule=rule,
                    confidence="review",
                    previous=previous,
                    current=current,
                    following=following,
                    fingerprint=_fingerprint(rule, previous, current, following),
                )
            )

    return candidates
