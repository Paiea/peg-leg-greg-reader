# PERFORMANCE Novelization Live Experiment Report

## Authority

- Source/current-main authority: `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`
- PERFORMANCE lab authority: `experiment/performance-lab` at `48bf312924c5d1d6836587e9cb3e21f3944a4d43`
- Expanded scope: the full displayed Chapter 1-20 Showcase sequence, with detailed round-trip evidence in `VISIBLE_001_020_ROUNDTRIP.md` and all 19 visible handoffs audited in `SHOWCASE_SEAM_AUDIT_VISIBLE_001_020.md`.

## Scene decisions

The original mixed five-scene sample remains the high-resolution script evidence inside the broader first-20 pass.

| Scene | Novelization decision | Reason |
| --- | --- | --- |
| Canon 002 / displayed Ch 2, Antonius loan | SOURCE RETAINED | The source already realizes suspicion, transaction ownership, and Greg's younger persona shift. Novelization did not earn a clear overall improvement. |
| Canon 007 / displayed Ch 5, Antonius storeroom | CHANGE | The behavioral shift from cleanup to valuation survives prose while broom, shelf, name scrap, buyer/use questions, and Greg's premature disclosure replace a shared dry-comeback ladder. |
| Canon 013 / displayed Ch 9, Arlo workshop | CHANGE | Fixture, notebook, ruined regulator, readings, and tensioner carry Arlo's process ownership more distinctly than the source refusal ladder. |
| Canon 016 / displayed Ch 12, Jorren + Alden + Greg | SOURCE RETAINED | The source already has the strongest topology: teach, test, succeed, overapply, physical correction. The candidate mainly restaged an already healthy scene. |
| Canon 018 / displayed Ch 14, Hessa beans | CHANGE | Fresh beans, waiting, the bean tap, attempt counting, and the covered bowl carry Hessa's procedure/concern while Greg retains the technical and comic interiority. |

The remaining displayed chapters were reduced through dramatic structure and comparative PERFORMANCE, then retained where the explicit-script stage did not expose an improvement strong enough to survive back into Greg's first-person prose.

## Literary validation

- Dramatic truth: PASS. No scene outcome, debt term, magic result, object, timeline fact, relationship state, or knowledge ceiling is changed.
- Speaker ownership: PASS by construction. Dialogue remains in its speaker's paragraph or is paired only with that speaker's action.
- Action ownership: PASS by construction. Antonius owns broom/shelf/valuation behavior, Arlo owns workshop objects/process, Hessa owns exercise access/control, Greg owns Greg actions and interpretation.
- POV/interiority: PASS. Only Greg receives narrated internal cognition.
- Character performance: PASS. The novelization preserves the tested behavior rather than translating it back into explanatory banter.
- Greg narrator voice: PASS. Source interior beats are retained whenever they outperform script compression; new Greg lines remain analytical, self-aware, and comic without shifting him into neutral stage prose.
- Mundane/domain texture: PASS. Storeroom sorting/ownership, workshop apparatus/readings, and beans/procedure remain concrete.
- Explanatory smoothing: PASS. The three changed scenes use physical behavior as an answer where PERFORMANCE earned that change.
- Source-wins rule: PASS. No chapter is changed merely to prove the intermediate representation exists.

## Exact PERFORMANCE patch IDs applied

- `007-value-shift`
- `007-valuation-exit`
- `013-process-ownership`
- `018-bean-instruction`
- `018-fresh-bean`
- `018-placement`
- `018-anchor-wait`
- `018-no-dry-correction`
- `018-bean-redirect`
- `018-one-finger`
- `018-covered-bowl`

## Conservative attribution hardening

PASS. Novel prose was re-anchored for instantaneous first-read speaker recognition. Ordinary `said` / `asked` tags are intentionally repeated after narration, action beats, and speaker changes. An action beat is allowed to carry attribution only when the acting character is unquestionably the speaker in that same paragraph. The changed spans do not rely on another character's separate action to imply who spoke.

## Replacement seam audit

PASS. Entry and exit seams around all three surviving PERFORMANCE replacements were reread against their untouched neighboring prose. The cleanup removes one redundant same-paragraph Antonius tag, explicitly re-anchors dialogue immediately after replacement spans, and repairs an Arlo/Greg handoff where `"I know," I said.` incorrectly broke the alternating speaker pattern. No scene facts or outcomes changed.

## Showcase handoff audit

PASS with one repair. All 19 visible-to-visible handoffs in displayed Chapters 1-20 were checked independently of canon adjacency.

- 14 handoffs are CLEAN.
- 4 are SOFT but self-contained enough to retain without intervention.
- 1 handoff required a patch: displayed Chapter 2 -> 3, canon 002 -> 004.

The displayed sequence skips canon 003, so canon 004 now re-establishes the shale-test antecedent before Greg reasons from the result. The repair preserves the hidden-canon facts: the sixth disk first beat the control, later tests reached closer to twenty percent, and the project remained promising rather than proven. No hidden chapter is restored and no scene outcome changes.

## Validation

The implementation was developed test-first. The new Showcase seam test failed on run 11 before `clean_004` existed. After the minimal cleaner and bounded workflow update were added, run 13 passed:

- focused PERFORMANCE experiment tests
- conservative attribution hardening
- replacement and Showcase seam cleanup
- full repository unit-test discovery
- `git diff --check`
- reader-frontier verification
- no-em-dash checks for affected prose
- required attribution/seam anchors
- bounded generated prose diff

Validated branch head after the generated prose commit: `2ae6a6fcd0e6b15049ac8f32d4482471c3162c6a`.

## Publish boundary

This report authorizes the validated first-20 experiment candidate only. It does not authorize manuscript-wide PERFORMANCE rollout. The hidden dramatic/PERFORMANCE/script layers remain derived editorial machinery and do not become manuscript authority.
