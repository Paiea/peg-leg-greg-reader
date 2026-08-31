# GitHub-First Asset Archaeology Design

## Goal

Make GitHub sufficient for routine Peg-Leg Greg handoffs, prove which historical external checkpoint families are redundant, and add non-destructive repository, manuscript, reader, and image diagnostics.

## Authority and safety

- Current GitHub `main` remains accepted repository authority.
- Exact manuscript prose outranks summaries and filenames.
- No manuscript or image source deletion occurs in this work.
- `Peg_Leg_Greg_Heavy_Edit.md` remains protected external editorial authority.
- External ZIP families are classified by evidence, not guessed file contents.
- Git history is treated as recovery evidence only for committed material.

## Architecture

One standard-library Python audit module will inventory repository files, extract chapter/image relationships from reader HTML, inspect image metadata, hash duplicate assets, and report manuscript ranges. A thin command wrapper will expose manuscript, reader, asset, and complete checks. Generated JSON/CSV data will feed durable Markdown audits and later image-replacement work.

Reader presentation changes will stay in the existing static-reader architecture. They may improve intrinsic sizing, layout reservation, lazy loading, and image-role limits, but will not redesign the reader or destructively replace source art.

## Durable outputs

- `state/REPOSITORY_ASSET_AUDIT.md`
- `state/EXTERNAL_HANDOFF_CLEANUP_AUDIT.md`
- `state/CHATGPT_LIBRARY_CLEANUP_HANDOFF.md`
- `publishing/repository_inventory.json`
- `publishing/image_asset_manifest.json`
- `publishing/chapter_art_coverage.json`

## Handoff policy

Routine work uses current GitHub authority, branches or PRs, durable state, and compact re-prompts. Full repository ZIPs are exceptional recovery or deliberate offline archives. Targeted external artifacts remain valid when their unique contents are not intentionally held in GitHub.

## Pull-request boundary

This PR contains audits, tests, reusable diagnostics, compact workflow guidance, and evidence-backed reader presentation improvements. It contains no mass deletion, manuscript rewrite, image generation, destructive image conversion, or Git-history rewriting.
