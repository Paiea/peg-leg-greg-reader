#!/usr/bin/env python3
"""Parse the chapter-number prefix used across PLG canonical DOCX sources."""

from __future__ import annotations

import re

ONES = {
    "ZERO": 0,
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
    "SIX": 6,
    "SEVEN": 7,
    "EIGHT": 8,
    "NINE": 9,
    "TEN": 10,
    "ELEVEN": 11,
    "TWELVE": 12,
    "THIRTEEN": 13,
    "FOURTEEN": 14,
    "FIFTEEN": 15,
    "SIXTEEN": 16,
    "SEVENTEEN": 17,
    "EIGHTEEN": 18,
    "NINETEEN": 19,
}
TENS = {
    "TWENTY": 20,
    "THIRTY": 30,
    "FORTY": 40,
    "FIFTY": 50,
    "SIXTY": 60,
    "SEVENTY": 70,
    "EIGHTY": 80,
    "NINETY": 90,
}
HEADING_RE = re.compile(r"^CHAPTER\s+([^\n]+)(?:\n.*)?$", re.IGNORECASE)


def words_to_number(value: str) -> int | None:
    tokens = [token for token in value.upper().replace("-", " ").split() if token != "AND"]
    if not tokens:
        return None
    if len(tokens) == 1:
        if tokens[0] in ONES:
            return ONES[tokens[0]]
        if tokens[0] in TENS:
            return TENS[tokens[0]]
        return None

    total = 0
    if "HUNDRED" in tokens:
        idx = tokens.index("HUNDRED")
        if idx != 1 or tokens[0] not in ONES or ONES[tokens[0]] == 0:
            return None
        total = ONES[tokens[0]] * 100
        tokens = tokens[idx + 1 :]
        if not tokens:
            return total

    if len(tokens) == 1:
        if tokens[0] in ONES:
            return total + ONES[tokens[0]]
        if tokens[0] in TENS:
            return total + TENS[tokens[0]]
        return None
    if len(tokens) == 2 and tokens[0] in TENS and tokens[1] in ONES:
        return total + TENS[tokens[0]] + ONES[tokens[1]]
    return None


def number_from_heading(text: str) -> int | None:
    match = HEADING_RE.match(text.strip())
    if not match:
        return None
    token = match.group(1).strip()
    if token.isdigit():
        return int(token)
    return words_to_number(token)
