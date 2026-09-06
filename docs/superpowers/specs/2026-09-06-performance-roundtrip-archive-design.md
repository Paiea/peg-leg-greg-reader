# PERFORMANCE Roundtrip Archive Design

## Status

APPROVED ARCHITECTURE

This design records the authority and interoperability contract for preserving successful PERFORMANCE round-trip evidence.

## Goal

Preserve the exact derived dramatic, PERFORMANCE, and screenplay evidence for scenes where a PERFORMANCE round trip earns a surviving prose change, without creating a second manuscript or weakening canonical prose authority.

## Authority

**CANON PROSE is the only story authority.**

Everything under `state/editorial/performance-roundtrip/` is derived editorial reference material. It may explain why a scene was changed, demonstrate how a character successfully performed under one specific set of conditions, and supply optional visual evidence to adjacent systems. It may never override current canonical prose, establish a new canon fact, or promote scene-local PERFORMANCE state into permanent character state.

A saved PERFORMANCE example means:

> This performance worked under these scene conditions.

It does **not** mean:

> This character must always behave this way.

If current canonical prose conflicts with an archived reference, canonical prose wins and the archived reference is stale until deliberately refreshed by a later validated round trip.

## Persistence rule

### Surviving PERFORMANCE edit

When a PERFORMANCE round trip produces a prose change that survives validation and publication, preserve the successful evidence permanently at:

`state/editorial/performance-roundtrip/<canon-chapter>/`

Each successful scene directory contains:

- `source.lock.json`
  - source chapter/path
  - historical source blob SHA
  - source authority commit
  - displayed Showcase chapter when applicable
  - exact historical PERFORMANCE-lab provenance
  - resulting canon commit
  - scene-local final-prose anchors used for freshness validation
  - compact optional visual evidence derived from the successful screenplay
- `dramatic.md`
  - locked dramatic truth
  - required result
  - state in/state out
  - ownership and non-drift boundaries
  - environment/active task
- `performance.md`
  - the temporary PERFORMANCE frames actually used
  - state
  - performed stance
  - attention
  - baseline bend
  - material shift trigger when present
- `screenplay.md`
  - the explicit performed screenplay that earned the change
  - speaker, action, and thought ownership
  - addressee where useful
  - blocking and object interaction
- `comparison.md`
  - why the performed version beat the source
  - source material deliberately retained
  - candidate/source material deliberately rejected
  - behavioral distinction that earned the change
  - final prose outcome and resulting canon commit

### Source win

A source-win scene does not receive the heavy five-file archive by default. The normal compact round-trip record remains sufficient:

- dramatic diagnosis
- script verdict
- source retained
- reason

Temporary generated intermediates for source wins may be discarded after validation unless a later editorial decision explicitly identifies reusable diagnostic value.

## Backfill policy

Backfill only from traceable committed evidence. Never reconstruct a historical PERFORMANCE frame from memory or from the final prose alone.

The first archive backfill covers the three successful early-book cases whose original fixtures, performed scripts, and reports still exist at historical PERFORMANCE-lab commit `48bf312924c5d1d6836587e9cb3e21f3944a4d43`:

- canon 007, Antonius storeroom
- canon 013, Arlo workshop
- canon 018, Hessa beans

Their historical source authority is `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`. Their published first-20 round-trip result is merge commit `fb703c47db1e682ea32f45da5e5bb89b319c4c93`.

## Stable read path

`scripts/performance_roundtrip_references.py` is the read-only interface for consumers.

It:

1. resolves `state/editorial/performance-roundtrip/<chapter>/source.lock.json`;
2. extracts and normalizes only the current chapter's `article.prose` text;
3. verifies every archived final-scene anchor still occurs exactly once;
4. reports the reference as `fresh` or `stale` with reasons;
5. returns optional visual evidence only for fresh references.

Consumers must not parse historical git objects or old lab folders themselves when current archived references exist.

## Staleness model

Freshness is deliberately **scene-local**, not raw-file or whole-chapter equality.

A reference is fresh only when all `result_scene_anchors` in `source.lock.json` appear exactly once in the current canonical prose for the locked chapter. This detects material changes to the performed scene while ignoring irrelevant HTML churn such as illustration tags and unrelated chapter edits.

A reference is stale when:

- its canonical chapter is missing;
- its source lock is malformed;
- any final-scene anchor is missing;
- any final-scene anchor becomes ambiguous;
- the archive claims canonical authority or violates the derived-reference contract.

Stale references remain useful historical evidence for humans, but automated consumers must not use their screenplay/visual evidence.

## Illustration integration

The illustration pipeline may consume a **fresh** successful screenplay reference as optional derived visual evidence. It remains subordinate to canonical prose.

The archive can expose screenplay-backed evidence such as:

- characters physically present
- active task
- location
- meaningful props
- action ownership
- blocking and spatial movement
- silent reactions
- physical scene endings
- character-specific physical behavior

The generation queue may carry this evidence in a supplemental `performance_reference` field. That field never changes candidate status, paragraph-anchor validity, required characters, canon facts, or generation readiness.

If a reference is missing or stale, the field is omitted and the illustration pipeline behaves exactly as it did before this feature.

The illustration worker must still read/validate canonical prose before generation. The successful screenplay is one especially clear physical performance of canonical truth, not a replacement for that truth.

## Future PERFORMANCE batch rule

Every future batch follows the same persistence policy:

**SURVIVING PERFORMANCE EDIT -> preserve successful derived screenplay evidence.**

**SOURCE WIN -> keep compact verdict only unless there is an explicit reason to retain more.**

Archive creation belongs after a candidate has survived prose translation and validation. The archive must lock the exact source evidence actually used and the final canonical result, not a later reconstructed approximation.

## Non-goals

This change does not:

- edit manuscript prose;
- rerun the first 20 chapters;
- authorize the next PERFORMANCE prose batch;
- make PERFORMANCE material canonical;
- make the art pipeline dependent on PERFORMANCE;
- create permanent character-state rules from scene-local frames;
- persist heavy screenplay artifacts for ordinary source wins;
- auto-refresh stale archives from current prose.

A stale archive requires deliberate editorial review, not silent regeneration.
