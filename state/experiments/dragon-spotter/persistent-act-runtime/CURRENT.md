# Dragon Spotter Persistent Four-Act Runtime — CURRENT

Authority: **derived experimental state, not story canon**.

Active branch: `architecture/long-form-story-compiler`  
Draft PR: **#161**  
Settled runtime model: STORY STATE = memory; ACT I–IV = persistent temporal perspectives; REHEARSAL = experiment selection/orchestration; PERFORMANCE = high-fidelity embodied-behavior experiment; STORY SYNC = learning/convergence; PROSE = rendering.

Do not substitute another story proving ground for Dragon Spotter in a Dragon continuation chat. Do not turn project-local discoveries into generic compiler assumptions. Do not generate sustained prose from this trailhead.

## Current authority: Cycle 2

Cycle 2 ran sequentially from Cycle 1's evolved runtime through the public derived-only seam:

`plg_ai_tools.run_story_rehearsal_cycle`

Cycle 1 inputs remained:

- `runtime-input.json`
- `first-bargain-evidence.json`
- `creator-taste-context.json`
- source PERFORMANCE evidence: `../story-sync/first-bargain-rehearsal.json`

Cycle 2 added only bounded directional evidence from:

- `rehearsal-evidence-cycle-002.json`

Cycle 2 did **not** add branch updates, shared discoveries, story truths, or prose. Its four evidence items only supplied message-local `constraint_response` deltas where existing Dragon state already supported the answer.

## Generic experiment-retirement fix

Cycle 2 first exposed a generic scheduling defect: a directional message could receive a latest `supported` constraint response while remaining status `open`, and `compile_rehearsal_targets` would still enqueue the identical `forward_consequence_test` or `backward_prerequisite_test` forever.

The generic fix is now landed in `scripts/persistent_act_runtime.py`:

- open directional messages still remain open as story-state messages
- no Dragon state is fake-closed
- `compile_rehearsal_targets` inspects the target act's latest response
- when the latest response is `supported`, the identical directional probe is retired
- `third_path`, `conflict`, `reject_source`, and untested messages remain eligible for the appropriate continued work
- no Dragon-specific strings or assumptions were added to generic compiler code

The RED/GREEN contract remains in `tests.test_story_sync_constraint_response_evidence`.

## Verification authority

Verified on branch head `c568e1be16b8d45c240ade57448dedf1b9614d1d` through GitHub Actions STORY SYNC run `34135646199`:

- focused STORY SYNC/runtime suite: **71 tests, green**
- full repository suite: **527 tests, 6 skipped, green**
- CI remained read-only validation

The handoff count of 68 focused / 523 full was superseded by concurrent generic fixture-contract additions before final verification. The current counts above are the observed authority.

## Observed Cycle 2 result

The post-fix Cycle 2 produced **17 REHEARSAL targets**.

Experiment modes:

- counterfactual branch comparison: 2
- forward consequence test: 1
- PERFORMANCE: 1
- plausibility probe: 6
- state transition test: 2
- temporal-distance rehearsal: 1
- trajectory/worldline test: 4
- backward prerequisite test: 0

The four directional messages supported in Cycle 2 were:

- `a1-to-a3-reciprocity-politics`
- `first-bargain-reciprocity-forward`
- `a4-to-a1-earned-recognition`
- `a4-to-a2-public-risk`

Observed post-fix retirement:

- `supported_directional_targets_still_scheduled`: **[]**
- the four identical directional probes disappeared
- the prior `third_path` collision around `a4-to-a1-earned-recognition` disappeared after the newer supported response became the latest response
- constraint collisions: **1 → 0**
- unresolved long-range messages: **5 → 1**
- open temporal pressure: **9 → 4**

This is real directional closure. The messages remain derived open story-state constraints; only redundant experiment selection retired.

## Branch movement across the two cycles

Cycle 1 remains the only branch-pruning cycle so far.

Act I first-bargain branches:

- `first-bargain.land-restoration`: **active / viable**
- `first-bargain.relic-restitution`: **active / viable**
- `first-bargain.protocol-only`: **superseded / redundant**
- `first-bargain.reckless-improvisation`: **superseded / redundant**

Cycle 1 moved open branch count **13 → 11**.

Cycle 2 branch count stayed **11 → 11** with branch delta **0**. Cycle 2 intentionally made no branch updates, so its convergence came from constraint closure rather than artificial branch pruning.

Land-restoration and relic-restitution remain legitimately live.

## STORY SYNC state after Cycle 2

Cycle 1 strengthened `mutual-indispensability`:

- evidence count: **2 → 3**
- maturity: **repeated_signal → strong_thread**

Cycle 2 did not add discovery evidence and did not promote anything further.

Current repeated signals:

- `heat-through-competence`

Current strong threads:

- `gift-reciprocity`
- `improvisation-is-competence-path`
- `mutual-indispensability`

Current story truths: **none**.

Creator taste remains heuristic only. `gift.scale-token` search priority had moved low → medium under creator taste in Cycle 1 while branch survival/action remained unchanged.

Shared unresolved contradictions remain:

- `first-gift-form`
- `ending-office-role`

Each act still has one local unresolved question. STORY SYNC still has two unresolved shared questions.

## Remaining temporal pressure

The trajectory remains **open**.

After Cycle 2:

- adjacent boundary pairs: 3
- boundary contradictions: **3**
- unresolved long-range messages: **1**
- constraint collisions: **0**
- open temporal pressure count: **4**

The three remaining adjacent boundary contradictions are:

1. **Act II → Act III `professional_role`**  
   `political-liability` → `needed-envoy`  
   Keep this a development-level structural/state-transition experiment.

2. **Act II → Act III `romantic_trust`**  
   `guarded-respect` → `mutual-reliance`  
   This remains the single high-heat embodied PERFORMANCE bridge. Do not close it from summary evidence or abstract interpolation.

3. **Act III → Act IV `public_identity`**  
   `contested-human-interlocutor` → `dragon-recognized-interlocutor`  
   Keep this structural unless evidence shows the transition depends on embodied relationship behavior.

## Exact next edge

The next meaningful Dragon work is the **three boundary contradictions**, with priority on the untouched Act II → III `romantic_trust` high-heat PERFORMANCE bridge.

Do not write sustained prose yet.

For the next bounded REHEARSAL slice:

- preserve the four persistent temporal act channels
- perform or derive real evidence for the Act II → III romantic-trust bridge rather than narrating the answer
- keep the `professional_role` and `public_identity` bridges cheaper unless their evidence demands escalation
- preserve land-restoration, relic-restitution, `first-gift-form`, and `ending-office-role` while still live
- measure whether boundary contradictions actually close, split, or generate a defensible third path
- watch whether major novelty continues slowing while existing threads deepen
- do not force entropy reduction or story-truth promotion

Current research question remains:

**Do four persistent temporal perspectives + REHEARSAL + STORY SYNC converge on one coherent Dragon Spotter trajectory without prematurely collapsing useful alternatives?**
