# Successful PERFORMANCE Roundtrip Archive

## Authority boundary

This directory is **derived editorial reference material**.

**Canonical chapter prose remains the only story authority.** Nothing in this archive may override current prose, establish a new canon fact, or silently become permanent character state.

Each archived scene is an example of a PERFORMANCE solution that survived translation back into prose under one specific set of dramatic, relational, physical, and scene-pressure conditions.

Read it as:

> This performance worked here.

Never as:

> This character always behaves this way.

## Persistence rule

Create a heavy archive only after a PERFORMANCE round trip earns a surviving prose change.

Each successful chapter directory contains:

- `source.lock.json` for historical source/result provenance and freshness anchors
- `dramatic.md` for locked dramatic truth and state boundaries
- `performance.md` for the temporary frames actually used
- `screenplay.md` for the successful explicit performed script
- `comparison.md` for the reason it beat the source and the final prose result

Ordinary `SOURCE WIN` scenes stay in the compact batch/round-trip record. Do not create a five-file archive for them merely because an intermediate screenplay was generated.

## Stable read path

Consumers should use:

`python scripts/performance_roundtrip_references.py --check`

or import the read-only helpers from `scripts.performance_roundtrip_references`.

Freshness is scene-local. Every `result_scene_anchor` must still appear exactly once in current canonical prose. Illustration tags or unrelated prose changes do not by themselves stale a reference. If the performed scene changes materially and its anchors disappear or become ambiguous, the reference becomes stale.

Stale references remain historical evidence for humans. Automated consumers must ignore their visual/performance guidance.

## Novelization boundary

PERFORMANCE owns dramatic behavior and exchange structure. It does **not** own final prose punctuation, sentence count, or paragraph count.

A performed beat boundary is not automatically a prose sentence boundary. When adjacent beats form one continuous observation, causal chain, physical process, or thought, the prose renderer may integrate them into one shaped sentence or paragraph. Preserve separation when the stop itself carries contrast, comedy, urgency, realization, physical impact, uncertainty, deliberate withholding, speaker ownership, or another clear dramatic function.

When translating PERFORMANCE back into prose:

1. preserve dramatic truth, behavior, action ownership, speaker ownership, information, and useful concrete detail;
2. reduce semantic repetition and unnecessary sentence boundaries before reducing meaningful detail;
3. prefer one shaped sentence over several clipped sentences when they express one continuous semantic movement;
4. preserve short units when their boundary is doing real dramatic or character work;
5. never make prose longer or smoother merely to demonstrate the rule.

The source-wins rule still applies. If recomposition does not clearly improve the reading experience, retain the source rhythm.

## Durable character learning

Successful PERFORMANCE archives are episodic evidence, not automatic additions to character memory.

A future worker may promote a behavioral or relational tendency into `state/CHARACTER_BIBLE.md` only when repeated current canon evidence supports it. Do not promote one successful exchange into an `always` rule, fixed cadence, catchphrase, or permanent personality setting.

## Illustration use

A fresh archive may expose a compact `visual_reference` derived from the successful screenplay. It may help with scene selection, blocking, props, action ownership, silent reactions, and character-specific physical behavior.

It is optional. The illustration pipeline must still validate against canonical prose before generation. If this archive is absent or stale, illustration generation proceeds without it.

## Initial backfill

The initial recoverable examples are:

- `007/` Antonius storeroom
- `013/` Arlo workshop
- `018/` Hessa beans

They are copied from committed PERFORMANCE-lab evidence at `48bf312924c5d1d6836587e9cb3e21f3944a4d43`, which locked source authority `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`. Their surviving prose changes were published through PR #141 at merge commit `fb703c47db1e682ea32f45da5e5bb89b319c4c93`.
