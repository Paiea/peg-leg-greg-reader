# Dragon Spotter Persistent Four-Act Runtime — CURRENT

Authority: **derived experimental state, not story canon**.

Active branch: `architecture/long-form-story-compiler`  
Draft PR: **#161**  
Settled runtime model: STORY STATE = memory; ACT I–IV = persistent temporal perspectives; REHEARSAL = experiment selection/orchestration; PERFORMANCE = high-fidelity embodied-behavior experiment; STORY SYNC = learning/convergence; PROSE = rendering.

Use Dragon Spotter only for this continuation surface. Keep Dragon-specific evidence project-local. Do not generate sustained prose from this trailhead. PR #161 remains draft and unmerged.

## Current authority: Cycle 3

Cycle 3 ran sequentially from the evolved Cycle 2 runtime through the actual public derived-only seam:

`plg_ai_tools.run_story_rehearsal_cycle`

Project-local inputs across the three cycles:

- `runtime-input.json`
- `first-bargain-evidence.json`
- `cycle-2-directional-evidence.json`
- `cycle-3-boundary-evidence.json`
- `creator-taste-context.json`
- first-bargain PERFORMANCE source: `../story-sync/first-bargain-rehearsal.json`
- Cycle 3 romantic-trust PERFORMANCE: `../story-sync/cycle-3-romantic-trust-performance.json`
- Cycle 3 structural rehearsals: `cycle-3-structural-boundary-rehearsals.json`

No sustained prose or canon write occurred.

## Verification authority

The generic boundary-learning fix and the real Dragon Cycle 3 run were verified on commit:

`bfa5e11d58831aca94b419a4bb19dcf73f0c23aa`

GitHub Actions STORY SYNC run:

`34137789593`

Observed verification:

- focused STORY SYNC/runtime suite: **72 tests, green**
- full repository suite: **529 tests, 6 skipped, green**
- CI remained read-only validation

The branch subsequently received two unrelated Gravity's Embrace continuation commits. They changed only Gravity project-local `CURRENT` files and did not alter Dragon or the generic runtime.

## High-heat romantic-trust PERFORMANCE result

The Act II → Act III `romantic_trust` target began as:

`guarded-respect` → `mutual-reliance`

PERFORMANCE did **not** support broad immediate mutual personal or romantic trust as the honest Act III entry state.

The strongest performed path was:

`third_path_operational_reliance_with_guarded_personal_trust`

Observed behavior:

- both leads retained meaningful professional competence
- neither could safely replace the other
- each had to accept a real reputational or physical cost to act on the other's judgment
- reciprocal operational reliance was reachable
- attraction intensified around competence but did not guarantee trust
- professional-only coordination remained viable but less adaptive
- asymmetric reliance remained plausible
- attraction plus persistent distrust remained plausible
- presumed/forced trust failed under pressure

The derived Act III `romantic_trust` state-in hypothesis therefore adapted from:

`mutual-reliance`

to:

`mutual-operational-reliance-with-guarded-personal-trust`

The old `mutual-reliance` value is preserved in boundary history with provenance. This is derived temporal learning, not story canon.

## Structural boundary rehearsals

### Act II → III `professional_role`

`political-liability` → `needed-envoy`

Development-level state-transition rehearsal supported the bridge through **reluctant deployment**:

Human institutions can continue treating the Spotter as politically embarrassing while still needing his dragon-facing effectiveness. Institutional rehabilitation is not required first.

### Act III → IV `public_identity`

`contested-human-interlocutor` → `dragon-recognized-interlocutor`

Development-level state-transition rehearsal supported the bridge through **recognition by repeated routing**:

Dragons can increasingly recognize the Spotter as the human who notices, answers, and carries obligations accurately while human institutions continue disputing his title or legitimacy. This does not choose Crown Spotter versus dragon envoy.

## Observed Cycle 3 convergence

Cycle 2 → Cycle 3:

- REHEARSAL targets: **17 → 12**
- boundary contradictions: **3 → 0**
- unresolved long-range messages: **1 → 0**
- constraint collisions: **0 → 0**
- open temporal pressure: **4 → 0**
- open branches: **11 → 11**
- branch delta: **0**
- forward consequences: **3 → 3**
- backward requirements: **2 → 2**

Temporal trajectory status is now:

`candidate_passable`

That does **not** mean the story is fully converged. It means the current four temporal act states no longer contain an untested adjacent-boundary contradiction or unresolved long-range temporal obligation.

Cycle 3 produced no branch pruning and no new forward/backward obligations. Convergence came from evidence-backed bridge learning and one later-state revision.

## STORY SYNC after Cycle 3

The new high-heat PERFORMANCE supplied genuinely independent adversarial evidence.

`mutual-indispensability`:

- Cycle 2 maturity: **strong_thread**
- Cycle 3 maturity: **story_truth**

This promotion was produced by STORY SYNC after the thread survived another independent high-heat challenge. It was not inserted as a desired Cycle 3 result.

`heat-through-competence`:

- Cycle 2 maturity: **repeated_signal**
- Cycle 3 maturity: **strong_thread**

New discovery:

- `operational-reliance-before-personal-trust`: **speculation**

Current repeated signals: **none**.

Current strong threads:

- `gift-reciprocity`
- `heat-through-competence`
- `improvisation-is-competence-path`

Current story truths:

- `mutual-indispensability`

## Branch authority

No branch changed in Cycle 3.

Act I first-bargain branches remain:

- `first-bargain.land-restoration`: **active / viable**
- `first-bargain.relic-restitution`: **active / viable**
- `first-bargain.protocol-only`: **superseded / redundant**
- `first-bargain.reckless-improvisation`: **superseded / redundant**

Land-restoration and relic-restitution remain legitimately unresolved. Do not choose one simply because the temporal trajectory is now candidate-passable.

Shared STORY SYNC contradictions still alive:

- `first-gift-form`
- `ending-office-role`

These are now more important than boundary repair because temporal pressure has reached zero without resolving them.

## Generic runtime defect exposed by Cycle 3

The real rehearsal exposed one generic learning defect.

Before Cycle 3, REHEARSAL evidence could add message constraint responses, but it could not:

1. revise an existing derived `state_in` / `state_out` temporal hypothesis when PERFORMANCE contradicted it, or
2. record that a non-identical adjacent boundary had an evidence-backed transition and retire that exact bridge experiment.

The generic fix landed in `scripts/persistent_act_runtime.py`:

- `state_boundary_update` delta revises an existing derived boundary hypothesis
- prior value/confidence/provenance are preserved in `history`
- `boundary_response` records evidence-backed bridge resolution in the target act
- a latest `supported` boundary response retires that exact mismatch from `boundary_contradictions` and REHEARSAL target selection
- endpoint values are not forced equal
- no story canon authority is gained
- no Dragon-specific strings or assumptions were added to generic runtime code

The generic RED/GREEN contract is in `tests.test_story_sync_constraint_response_evidence`.

## Exact next edge

Do **not** return to boundary repair and do **not** start sustained prose yet.

The four-act temporal trajectory is now candidate-passable, but STORY SYNC still has meaningful unresolved search state.

Next bounded research should test convergence rather than invent more architecture:

1. **Pressure-test the new relationship third path across temporal distance.** Test whether `mutual-operational-reliance-with-guarded-personal-trust` remains coherent deeper into Act III and Act IV. Do not assume it must become romance or broad trust. If Act IV requires something stronger, let Act IV produce that requirement explicitly.
2. **Resolve or sharpen `first-gift-form`.** Keep land-restoration and relic-restitution live until a bounded comparison produces discriminating evidence.
3. **Resolve or sharpen `ending-office-role`.** Preserve Crown Spotter versus dragon envoy until downstream consequences or backward requirements distinguish them.
4. **Challenge existing mature threads instead of manufacturing novelty.** Especially test `mutual-indispensability` now that STORY SYNC classifies it as story truth, and verify that its concrete expression does not secretly require one gift or office branch.
5. Watch whether major novelty continues slowing while constraints close and existing threads deepen. Branch expansion is still allowed if a genuinely new third path earns it.

Current research question:

**Can the now candidate-passable four-act Dragon Spotter trajectory continue converging at the STORY SYNC level without prematurely collapsing its remaining gift, office, and relationship uncertainty?**
