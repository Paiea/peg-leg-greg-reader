# Peg-Leg Greg Visual Production Workflow

Use the existing visual-production folders and records. This is an asset-lifecycle clarification, not a new subsystem.

## Asset states

### DEVELOPMENT
Contact sheets, experiments, alternate compositions, failed attempts, and unapproved images. Contact sheets are always DEVELOPMENT and are never published directly. Development assets may also carry `RE-PROMPT REQUIRED`, `REJECTED`, or `SUPERSEDED` when useful.

### STANDALONE READY
A deliberate standalone image exists, has a searchable project filename, and has passed basic visual QA. Record chapter, scene, source/contact-sheet panel when applicable, continuity notes, and intended prose anchor. The art exists and is ready, but it is **not reader-facing yet**.

### READER PROMOTED
Only explicit user approval promotes a STANDALONE READY asset. Use the exact approved standalone file at its recorded story anchor. Existing reader art remains stable unless the user explicitly instructs replacement. Record the final placement anchor.

## Normal lifecycle

Image-production room selects / curates / regenerates art → Codex records the asset as DEVELOPMENT or STANDALONE READY → user gives promotion approval → Codex places the exact approved asset and marks it READER PROMOTED.

A concise image-agent manifest containing asset filename, chapter, scene, status, source, reader status, and anchor is sufficient. Repository architecture does not need to be repeated in each handoff.

## Promotion command

Commands such as `PROMOTE svgPLG_Ch48_HR_Stove-at-the-Turn.png` or `PROMOTE CH48 STOVE` are sufficient when unambiguous. Codex should confirm the STANDALONE READY file exists, place that exact file at the recorded story anchor, update tracking, and report the result. Do not regenerate, crop a contact sheet, substitute another image, redesign the reader, or move stable existing art without instruction.

## Current example

`svgPLG_Ch48_HR_Stove-at-the-Turn.png` is **STANDALONE READY** and **NOT READER PROMOTED**. Its intended anchor is the Chapter 48 Stove at the Turn maneuver passage.
## Current coverage-mode authorization

The user has explicitly authorized a coverage push. During this phase, existing **STANDALONE READY** assets already classified as reader-eligible may move to **READER PROMOTED** without an individual `PROMOTE` command when the recorded scene/anchor is supported, the image is readable, stylistically compatible, continuity-safe, and improves chapter coverage. Contact sheets remain DEVELOPMENT and are never published as whole sheets. During the authorized coverage-harvest phase, a strong individual panel may be cleanly cropped into a separate standalone asset when its manuscript scene is correct, readable, stylistically compatible, continuity-safe, and useful for coverage. The source sheet remains unchanged and traceable. RE-PROMPT, rejected, unresolved, or scene-mismatched panels remain outside the reader. Existing reader art is not replaced merely because another asset exists.

