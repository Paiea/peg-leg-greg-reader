# PEG-LEG GREG - EXTERNAL HANDOFF CLEANUP AUDIT

This audit classifies filename families and generations. It is not a fabricated
inventory of external files and does not authorize blind deletion.

GitHub now preserves accepted project evolution and current exact story
authority. Historical ZIPs that contain only an old Git checkout are redundant
once their identity is confirmed. Git cannot recover material that was never
committed.

## Safe to remove after name match

These are high-confidence candidates only when the archive is visibly a full
repository/reader checkpoint at or before the named generation and does not
contain extra top-level source material:

- `Peg_Leg_Greg_GitHub_Ch137.zip`
- `Peg_Leg_Greg_GitHub_Reader_Ch113*.zip`
- `Peg_Leg_Greg_reader_ch82_*`
- `Peg_Leg_Greg_reader_ch92_*`
- `Peg_Leg_Greg_reader_ch97_*`
- `Peg_Leg_Greg_reader_ch105_*`
- `Peg_Leg_Greg_reader_ch123_checkpoint.zip`
- `peg-leg-greg-reader-v*`
- exact `(1)` / `(2)` duplicate uploads after matching file size or hash

Before deletion, inspect the archive listing. If it is simply a repository
checkout containing the same project families now in Git history, Git is the
better archive. If it contains an extra manuscript, editor artifact, or visual
source outside the checkout, move it to VERIFY.

## Verify then remove

- `Peg_Leg_Greg_Ch105_harvest_with_photos*.zip`: check for images not present
  in `harvested_photos/`, `visual/chapter_art/`, or Git history.
- `PEG_LEG_GREG_illustrated_reader_batch*.zip`: check whether generated
  candidates or sources exist outside the committed reader paths.
- `Peg_Leg_Greg_Editor_to_Codex_*`: check for edited prose, editorial notes,
  or a heavy-edit revision absent from the living artifact.
- `Peg_Leg_Greg_Book2_Handoff_*`: compare exact chapter ranges against
  current DOCX/Markdown authorities before removal.
- visual production, curation, and intake ZIPs: check for unique high-quality
  source images, accepted crops, prompts/metadata, or uncommitted manifests.
- Codex checkpoints without a clear chapter label: verify whether their branch
  or accepted changes exist in Git history.

Rejected candidates do not automatically deserve permanent storage. Preserve a
failed generation only when it has real recovery, reference, prompt, or
high-quality source value.

## Keep / archive

- Deliberate offline backups the user actually wants.
- Exact missing manuscript recovery packages not yet verified against GitHub.
- Unique source-art packages intentionally excluded from GitHub.
- A verified latest export used for disaster recovery, if the user wants one.

## Do not delete

- `Peg_Leg_Greg_Heavy_Edit.md`

It is active unique editorial work. Forward manuscript authority does not
replace it.

## Unknown

Any archive whose contents cannot be inspected, whose generation cannot be
matched to Git history, or whose name implies editing/recovery rather than a
plain repository snapshot.

## Git-history pressure test

Git history contains the accepted reader, manuscript, state, recovered-prose,
visual, Light Reader, and lane-brain evolution through current `main`.
Checking out a historical commit recovers committed code/state/assets without a
full-project attachment.

Git history does not prove recovery of:

- uncommitted generated candidates;
- local-only editorial prose;
- rejected/contact-sheet source material never committed;
- exact files removed before they entered Git;
- external binary/source artifacts intentionally kept elsewhere.

The correct cleanup test is:

**WAS THE VALUABLE CONTENT COMMITTED OR INTENTIONALLY PRESERVED ELSEWHERE?**

not:

**DOES THE ZIP LOOK OLD?**
