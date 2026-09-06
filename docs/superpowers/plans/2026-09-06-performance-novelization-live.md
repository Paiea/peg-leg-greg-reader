# PERFORMANCE Novelization + Live Reader Experiment Plan

> **Scope:** exactly five tested scenes. Novelize only surviving PERFORMANCE gains, validate, ship live, then stop.

## Pinned authority

- Current manuscript / reader authority: `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`
- Preserved PERFORMANCE lab: `experiment/performance-lab` at `48bf312924c5d1d6836587e9cb3e21f3944a4d43`
- Integration branch: `experiment/performance-novelization-live`
- For chapters <=155, current repo integration code treats `chapters/NNN.html` as durable prose authority. These five edits therefore land in the authoritative early-chapter surface, not a website-only copy.

## Five-scene decision gate

1. Canon 002 / displayed Chapter 2, Antonius loan: source currently wins unless novelization produces a clear gain.
2. Canon 007 / displayed Chapter 5, Antonius storeroom: novelize the validated behavior shift from cleanup to valuation, preserving broom/shelf/ownership behavior.
3. Canon 013 / displayed Chapter 9, Arlo workshop: novelize the validated object/process behavior, reducing refusal ladders while preserving fixture/notebook/regulator/tensioner texture.
4. Canon 016 / displayed Chapter 12, Jorren + Alden + Greg: source currently wins unless novelization produces a clear gain.
5. Canon 018 / displayed Chapter 14, Hessa beans: novelize validated procedure/action behavior while preserving Greg interiority and the narrow magic result.

Source wins every tie. No quota requires all five to change.

## Implementation

Use exact-match paragraph-span patches against the pinned current prose. A patch must fail closed if either boundary is missing or ambiguous. No unrelated prose may be rewritten.

Temporary implementation harness:
- `scripts/apply_performance_novelization_experiment.py`
- `tests/test_performance_novelization_experiment.py`
- `.github/workflows/performance-novelization-live.yml`

Durable review artifact:
- `state/editorial/performance-lab/NOVELIZATION_LIVE_REPORT.md`

The temporary harness is removed before merge; only validated chapter prose, the review artifact, and this plan may remain.

## Validation

For every changed scene validate:
- locked / required Dramatic Script facts remain;
- speaker and action ownership remain explicit;
- no non-Greg internal state enters narration;
- continuity, money, magic, objects, body state, and outcome do not drift;
- Greg narrator cognition remains recognizably PLG;
- mundane/domain texture survives;
- PERFORMANCE behavior is not smoothed back into explanatory dialogue;
- no em dash is added;
- repository tests, `git diff --check`, and reader-frontier validation pass;
- final diff changes no prose outside canon 007, 013, and 018 unless the source-wins decision is explicitly overturned by a clear comparison win.

## Publish

1. Run the one-off integration on the feature branch.
2. Review exact diff and validation report.
3. Remove temporary harness.
4. Open a PR to `main` and merge after checks are green.
5. Follow the normal Pages deployment from merged main.
6. Verify live pages for every changed chapter and record the merged authority, generated/main reader commit, Pages deployment, and live locations.
7. Stop. Do not broaden PERFORMANCE or novelization beyond these five scenes.
