# Greg, Again Audio Score v2 — Rolling Production Pool

Status: **ACTIVE**

Target frontier: **Chapter 030**
Maximum simultaneous synthesis lanes: **5**

Normative production rules remain in `r2/AUDIO_SCORE_PRODUCTION.md`.

## Current lanes

| Lane | Chapter | State | Durable owner |
|---|---:|---|---|
| A | 002 | short-take capture active | `audio/v2-greg-again-ch002-auto` |
| B | 003 | short-take capture active | `audio/v2-greg-again-ch003-auto` |
| C | 005 | short-take capture active | `audio/v2-greg-again-ch005-auto` |
| D | 011 | short-take capture active | `audio/v2-greg-again-ch011-auto` / PR #298 |
| E | 012 | short-take capture active | `audio/v2-greg-again-ch012-auto` / PR #299 |

Each active lane has crossed the durable provider boundary with playable preview artifacts. Continue the existing chapter; do not open overlapping claims.

## Already registered in v2 authority

001, 004, 006, 009, 010

## Assembled / integration work already in flight

- 007 — existing publication PR; do not resynthesize
- 008 — existing publication/integration PR; do not resynthesize

Integration/reconciliation does not consume a synthesis lane once the final MP3 and durable take artifacts already exist.

## Next queue

When a synthesis lane becomes complete and its durable final asset exists, immediately claim the earliest eligible chapter from:

013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 025, 026, 027, 028, 029, 030

Before claiming, re-read the v2 manifest, live claim branches, open v2 PRs, and this ledger because sibling workers may have advanced the frontier.

## Factory

Audio Score → natural preview-safe chunks (~500 chars max) → `deep` → identical `transcript` + `preview_transcript` → capture playable `preview_url` → persist provider identity and exact transcript → GitHub Actions download + byte gate + ffprobe → deterministic ffmpeg stitch → ~2-second settling tail → final ffprobe/hash/duration → reconcile v2 and public manifests.

Opaque provider-only submissions are historical evidence, not protected completed takes. A synthesized take becomes protected when the audio itself is durably recoverable. Never regenerate a take that already has a durable playable artifact.

## Pool rule

Keep five synthesis lanes full while eligible work remains through Chapter 030. A worker that finishes one chapter should refresh authority and claim the next earliest eligible queued chapter rather than stopping the production wave.
