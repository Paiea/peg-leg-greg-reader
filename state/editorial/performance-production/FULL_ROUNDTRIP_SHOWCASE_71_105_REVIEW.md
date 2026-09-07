# Full PERFORMANCE round trip: Showcase 71–105

Status: derived editorial evidence only. Canon prose remains sole story authority. No manuscript write is authorized by this review.

## Authority and scope

- chapter prose source authority read for this review: `72fb05930d1bddfc7b123a8d645fb77475ea12e7`
- branch base: `666cc4c554c02d9a29fd0d3f4d91369622dc738a` (tree-equivalent chapter content; only an accidental empty marker was added and immediately removed on main)
- displayed Showcase scope: 71–105
- canon scope: `88, 90, 91, 92, 93, 94, 96, 98, 99, 100, 103, 104, 105, 106, 107, 109, 110, 111, 112, 114, 115, 116, 117, 118, 120, 121, 122, 123, 124, 125, 126, 128, 129, 133, 135`
- chapters completed: 35/35

## Full stack applied to every chapter

Each chapter received:

1. locked dramatic state-in / required result / state-out
2. ownership boundaries
3. PERFORMANCE pressure, behavior, and relationship stance
4. explicit performed screenplay beats in the same beat-skeleton abstraction used by the existing first-70 PERFORMANCE production results
5. comparison back to current prose
6. speaker-ownership audit
7. rhythm/recomposition audit
8. semantic compression audit
9. final SOURCE_WIN / EDIT judgment

Evidence is stored in seven five-chapter JSONL files under `state/editorial/performance-production/full-roundtrip/`.

## Result

- 35 chapters completed
- 33 chapter-level SOURCE_WIN
- 2 chapters with surviving prose edits
- 3 exact surviving edits total
- 2 RECOMPOSE
- 1 COMPRESS
- 0 new speaker-ownership repairs
- 0 new scene-performance rewrites
- 0 canon prose changes

### Surviving edits

**Canon 92 / displayed 74 — COMPRESS**

Literal duplicate:

`Alden said, “I could.” Alden said, “I could.”`

→

`Alden said, “I could.”`

**Canon 96 / displayed 77 — RECOMPOSE**

`Same lot. Split pieces. Track ambiguity. Sample clear calls. Measure throughput. Measure Holl time.`

→

`Same lot: split pieces, track ambiguity, sample clear calls, measure throughput, measure Holl time.`

**Canon 96 / displayed 77 — RECOMPOSE**

`More columns. Bench. Reference tile. Tray condition. Dust. Wedge. Piece orientation. Time of day. Moon phase if sufficiently desperate.`

→

`More columns: bench, reference tile, tray condition, dust, wedge, piece orientation, time of day, moon phase if sufficiently desperate.`

## Comparison with the light rhythm pass

The direct rhythm pass over the same 35 chapters also produced exactly these three edits across the same two chapters.

The full dramatic → PERFORMANCE → screenplay → prose comparison did **not** add more edits. That is useful evidence rather than a null result.

The deeper representation strongly explains why many apparently clipped passages should survive:

- Hessa chapters: short units map to separate test states, stop conditions, report-versus-interpretation boundaries, and bodily observations.
- Pessa chapters: short units map to crutch placement, balance corrections, committed movement, and physical recovery.
- Theatre chapters: `Again.`, pauses, resets, prop failures, entrances, and wrong timing are performed beats; smoothing them would erase the actual mechanism of the scene.
- Canon 126 travel concerns: the rapid list is explicitly an involuntary flood of constraints, so the restart cost is part of the characterization.

The full round trip therefore reinforces the calibrated rule:

> A list is not automatically an inventory. Recompose when sentence boundaries merely separate components of one already-formed analytical object. Preserve boundaries when they perform accumulation, timing, uncertainty, observation order, physical sequence, escalation, correction, or comedy.

## Experiment conclusion

For this sample, the lightweight rhythm pass appears highly efficient at finding surface-level prose wins once the rhythm lever is calibrated. The full PERFORMANCE round trip adds value primarily as **adjudication and explanation**: it tests whether apparently choppy prose corresponds to real dramatic/performed beats and protects those beats from over-smoothing.

That suggests a useful routing strategy rather than a universal deep pass:

- cheap whole-book prose scan to generate candidates
- full PERFORMANCE round trip for ambiguous candidates, scene-level changes, dialogue ownership/timing, or calibration samples
- exact-source application only after the surviving edit still beats source in context

This review is candidate-only. `canon_write_authorized: false`.
