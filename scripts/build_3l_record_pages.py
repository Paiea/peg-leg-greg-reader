#!/usr/bin/env python3
"""Generate 3L record pages, record index, and listening archive from canon."""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "3l" / "manuscript"
RECORD_DIR = ROOT / "3l" / "records"
AUDIO_DIR = ROOT / "3l" / "audio"
ASSET_DIR = ROOT / "3l" / "assets" / "audio"


LEDE = {
    "001": "Greg reaches the dragon's cave with a request large enough to sound impossible.",
    "002": "Greg claims a second lifetime of memory. Ithar makes him define exactly what that means.",
    "003": "Greg tries to limit the story. Ithar decides what an honest account will require.",
    "004": "Greg begins where the second life began: nineteen again, carrying memories that did not belong in that body.",
    "005": "Greg remembers the first small choice that stopped feeling like a detour and started becoming another life.",
    "006": "Greg accounts for the ordinary years at East Four, where repetition became part of the life rather than empty space between events.",
    "007": "A man who was supposed to die survives, and Greg's remembered future stops behaving like a map.",
    "008": "Greg tries to save Nessa with foreknowledge and learns that knowing the outcome is not the same as knowing the cause.",
    "009": "Greg explains why he stayed, and why ordinary life eventually outweighed a road he had already climbed once.",
    "010": "Greg meets a man he loved in the first life and accepts that the second life no longer owes him the people he remembers.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_metadata(path: Path) -> tuple[str, str]:
    headings = [line[3:].strip() for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("## ")]
    if len(headings) < 2 or not headings[0].startswith("RECORD "):
        raise ValueError(f"{path}: expected RECORD and title headings")
    return headings[0].replace("RECORD ", "", 1).strip(), headings[1]


def current_audio(record: str) -> tuple[bool, str | None]:
    if record == "001":
        asset = ASSET_DIR / "record-001-headspace-v6.mp3"
        return asset.exists(), "record-001-headspace-v6.mp3" if asset.exists() else None

    plan = AUDIO_DIR / f"record-{record}-short-dual-plan.json"
    audit = AUDIO_DIR / "verification" / f"record-{record}-short-dual-audio.json"
    asset = ASSET_DIR / f"record-{record}.mp3"
    if not (plan.exists() and audit.exists() and asset.exists()):
        return False, None
    try:
        receipt = json.loads(audit.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return False, None
    if receipt.get("status") != "verified":
        return False, None
    if receipt.get("plan_sha256") != sha256(plan):
        return False, None
    if receipt.get("sha256") != sha256(asset):
        return False, None
    return True, f"record-{record}.mp3"


def record_page(record: str, title: str, has_audio: bool, audio_filename: str | None, first: str, last: str) -> str:
    safe_title = html.escape(title)
    safe_lede = html.escape(LEDE.get(record, "Greg continues the account under Ithar's examination."))
    audio = ""
    if has_audio and audio_filename:
        audio = f'''<section class="record-audio" aria-labelledby="listen-title"><p class="eyebrow">LISTEN</p><h2 id="listen-title">Record {record}</h2><p class="audio-note">Greg narrates. Ithar examines.</p><audio class="audio-player" controls preload="metadata" src="../assets/audio/{audio_filename}">Your browser does not support the audio element.</audio><div class="page-actions"><a class="button button-primary" href="../audio/">Listening Archive</a></div></section>'''
    else:
        audio = f'''<section class="record-audio" aria-labelledby="listen-title"><p class="eyebrow">AUDIO</p><h2 id="listen-title">Record {record}</h2><p class="audio-note">Audio rebuild in production. The written record below is current.</p></section>'''

    number = int(record)
    prev_link = f'<a class="button" href="{number - 1:03d}.html">← Record {number - 1:03d}</a>' if record != first else ""
    next_link = f'<a class="button" href="{number + 1:03d}.html">Record {number + 1:03d} →</a>' if record != last else ""

    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#080908"><meta name="description" content="Record {record} of The Third Leg: {safe_title.title()}."><title>Record {record} · {safe_title.title()} · The Third Leg</title><link rel="stylesheet" href="../assets/css/site.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header" aria-label="Site header"><a class="site-mark" href="../" aria-label="The Third Leg home">3L</a><nav class="primary-nav" aria-label="Primary"><a href="../#story">Story</a><a href="./">Records</a><a href="../#timeline">World</a><a href="../about/">About</a><a href="../../index.html">PLG</a><a href="../../r2/">R2</a></nav><nav class="medium-nav" aria-label="Formats"><a href="../audio/">Listen</a><a aria-current="page" href="{record}.html">Read</a></nav></header><main id="main" class="page-main record-page"><header class="page-hero"><p class="eyebrow">RECORD {record}</p><h1>{safe_title}</h1><p class="record-meta">THE ACCOUNT · REMEMBERED FROM THE DRAGON'S CAVE</p><p class="page-lede">{safe_lede}</p></header>{audio}<section class="record-reading" aria-labelledby="read-title"><div class="section-head"><div><p class="eyebrow">READ</p><h2 id="read-title">The written record</h2></div></div><article id="record-prose" class="reading-copy" aria-live="polite"><p>Loading the record…</p></article><noscript><p class="reading-fallback">JavaScript is disabled. <a href="../manuscript/record-{record}.md">Open the canonical prose.</a></p></noscript></section><div class="page-actions" aria-label="Record navigation">{prev_link}<a class="button" href="./">All Records</a>{next_link}</div></main><footer class="site-footer"><div class="footer-mark"><strong>3L</strong><span>Record {record} · {safe_title.title()}</span></div><nav aria-label="Lineage"><a href="../../index.html">PLG</a><span aria-hidden="true">→</span><a href="../../r2/">R2</a><span aria-hidden="true">→</span><a href="../">3L</a></nav></footer><script>const prose=document.getElementById('record-prose');fetch('../manuscript/record-{record}.md').then(r=>{{if(!r.ok)throw new Error('Record unavailable');return r.text()}}).then(markdown=>{{const lines=markdown.split(/\r?\n/);let headings=0;const body=[];for(const line of lines){{if(headings<2&&line.startsWith('## ')){{headings++;continue}}if(headings>=2)body.push(line)}}prose.replaceChildren();body.join('\n').trim().split(/\n\s*\n/).filter(Boolean).forEach(paragraph=>{{const p=document.createElement('p');p.textContent=paragraph.trim();prose.appendChild(p)}})}}).catch(()=>{{prose.replaceChildren();const p=document.createElement('p');p.append('The written record could not be loaded. ');const link=document.createElement('a');link.href='../manuscript/record-{record}.md';link.textContent='Open the canonical prose.';p.appendChild(link);prose.appendChild(p)}});</script></body></html>
'''


def records_index(records: list[tuple[str, str, bool]]) -> str:
    cards = []
    for record, title, has_audio in records:
        status = "Published · Listen and read" if has_audio else "Published · Read · Audio in production"
        cards.append(f'''<article class="record-list-item"><p class="eyebrow">RECORD {record}</p><h2><a href="{record}.html">{html.escape(title)}</a></h2><p>The account</p><p>{status}</p><a class="text-link" href="{record}.html">Open Record {record} →</a></article>''')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#080908"><meta name="description" content="The Third Leg records. Greg's account begins in the dragon's cave."><title>Records · The Third Leg</title><link rel="stylesheet" href="../assets/css/site.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header" aria-label="Site header"><a class="site-mark" href="../" aria-label="The Third Leg home">3L</a><nav class="primary-nav" aria-label="Primary"><a href="../#story">Story</a><a aria-current="page" href="./">Records</a><a href="../#timeline">World</a><a href="../about/">About</a><a href="../../index.html">PLG</a><a href="../../r2/">R2</a></nav><nav class="medium-nav" aria-label="Formats"><a href="../audio/">Listen</a><a href="001.html">Read</a></nav></header><main id="main" class="page-main"><header class="page-hero"><p class="eyebrow">THE ACCOUNT</p><h1>Records</h1><p class="page-lede">The written frontier is published through Record {records[-1][0]}. Audio appears only when it is verified against the current record plan.</p></header><section class="record-list" aria-label="Published records">{''.join(cards)}</section></main><footer class="site-footer"><div class="footer-mark"><strong>3L</strong><span>People change. Some things remember.</span></div><nav aria-label="Lineage"><a href="../../index.html">PLG</a><span aria-hidden="true">→</span><a href="../../r2/">R2</a><span aria-hidden="true">→</span><a href="../">3L</a></nav></footer></body></html>
'''


def audio_index(records: list[tuple[str, str, bool, str | None]]) -> str:
    blocks = []
    for record, title, has_audio, filename in records:
        if not has_audio or not filename:
            continue
        blocks.append(f'''<article class="record-list-item"><p class="eyebrow">RECORD {record}</p><h2>{html.escape(title)}</h2><audio class="audio-player" controls preload="metadata" src="../assets/audio/{filename}">Your browser does not support the audio element.</audio><div class="page-actions"><a class="button" href="../records/{record}.html">Read Record {record}</a></div></article>''')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#080908"><meta name="description" content="Listen to verified records of The Third Leg."><title>Listening Archive · The Third Leg</title><link rel="stylesheet" href="../assets/css/site.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header" aria-label="Site header"><a class="site-mark" href="../">3L</a><nav class="primary-nav" aria-label="Primary"><a href="../#story">Story</a><a href="../records/">Records</a><a href="../about/">About</a><a href="../../index.html">PLG</a><a href="../../r2/">R2</a></nav><nav class="medium-nav" aria-label="Formats"><a aria-current="page" href="./">Listen</a><a href="../records/001.html">Read</a></nav></header><main id="main" class="page-main"><header class="page-hero"><p class="eyebrow">AUDIO FIRST</p><h1>Listening Archive</h1><p class="page-lede">Only audio verified against the current record plan appears here.</p></header><section class="record-list" aria-label="Verified audio records">{''.join(blocks)}</section></main><footer class="site-footer"><div class="footer-mark"><strong>3L</strong><span>Verified listening frontier</span></div></footer></body></html>
'''


def build() -> list[tuple[str, str, bool, str | None]]:
    manuscripts = sorted(MANUSCRIPT_DIR.glob("record-[0-9][0-9][0-9].md"))
    if not manuscripts:
        raise SystemExit("no 3L manuscripts found")
    metadata = [record_metadata(path) for path in manuscripts]
    expected = [f"{number:03d}" for number in range(1, int(metadata[-1][0]) + 1)]
    actual = [record for record, _ in metadata]
    if actual != expected:
        raise ValueError(f"non-contiguous manuscript frontier: {actual}")

    RECORD_DIR.mkdir(parents=True, exist_ok=True)
    records: list[tuple[str, str, bool, str | None]] = []
    for record, title in metadata:
        has_audio, filename = current_audio(record)
        records.append((record, title, has_audio, filename))
    first, last = records[0][0], records[-1][0]
    for record, title, has_audio, filename in records:
        (RECORD_DIR / f"{record}.html").write_text(
            record_page(record, title, has_audio, filename, first, last), encoding="utf-8"
        )
    (RECORD_DIR / "index.html").write_text(
        records_index([(record, title, has_audio) for record, title, has_audio, _ in records]), encoding="utf-8"
    )
    (AUDIO_DIR / "index.html").write_text(audio_index(records), encoding="utf-8")
    print("reader frontier:", last, "current audio:", [record for record, _, available, _ in records if available])
    return records


if __name__ == "__main__":
    build()
