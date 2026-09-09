# PEG-LEG GREG — IMAGE BINARY HANDOFF

Durable transport rule for R2 and all PLG visual production.

## Core rule

Generated image binaries are not trusted merely because a GitHub write succeeds.

When direct AI → GitHub binary transport is unreliable:

**AI owns planning, prompt/scene selection, filenames, deterministic destination paths, manifests, registry state, reader code, staging, and verification. Keoni owns the final approved image-file drop into the named repository path.**

This rule exists because a generated R2 site hero reached GitHub as a valid-looking binary object but rendered visibly corrupted on the deployed site. Treat that as evidence about the transport path, not as an image-model failure.

## Default visual handoff

1. Resolve current GitHub authority and the exact visual job.
2. Generate or edit the image.
3. Review and approve useful output before integration.
4. Assign a stable filename and exact repository-relative destination.
5. Stage approved safe binaries in the project-approved handoff surface when available.
6. Consolidate multi-worker output into a clean release ZIP when that reduces human handling.
7. Keoni performs the final approved binary drop into the repository.
8. Re-read the repository and verify that every expected asset exists.
9. Decode/open the actual repository file. Do not infer validity from blob existence or file size.
10. Only after binary verification update chapter manifests, gallery mappings, illustration registry state, or live reader references.
11. After merge/deploy, verify highly visible assets on the actual public page.

## R2 ChatGPT Library staging

R2 parallel image workers use ChatGPT Library as the shared binary warehouse between generation and large manual repository drops.

Current R2 Library shelf:

```text
/Peg-Leg Greg Image Integration/R2/
  00 Canon/
  01 Incoming/
  02 Approved/
  03 Releases/
  04 Released/
```

This staging surface changes the **size of the human handoff**, not the authority model.

- GitHub still owns story/visual authority, claims, intended paths, manifests, and integration state.
- Library stores actual image binaries between disposable workers.
- Normal chapter workers should stage approved keepers rather than making Keoni download a tiny ZIP after every chapter.
- A separate release worker packages approved unreleased binaries into one large repo-mirrored ZIP, normally around 50 to 100 useful images or when Keoni asks.
- Only after the release ZIP is safely stored should included Library source binaries move from `02 Approved/` to `04 Released/`.

See `r2/IMAGE_SYSTEM.md`, `r2/IMAGE_WORKER.md`, and `r2/IMAGE_RELEASES.md`.

If a generated image is not exposed as a safe file reference that can be stored in Library, mark it `library_stage_pending`. Do not claim staging success from a visible image alone.

## ZIP handoff

For R2, prefer a release archive shaped like:

```text
r2-image-release-<nnn>/
  README.md
  manifest.json
  release-map.json
  r2/
    assets/
      images/
        <approved production images only at final repo-relative paths>
```

For other PLG multi-image production that does not use the R2 release engine, a smaller handoff may still use:

```text
plg-r2-image-handoff-<batch>/
  README.md
  manifest.json
  assets/
    <approved production images only>
```

Do not include rejected generations, scratch exports, full contact-sheet workspaces, or unrelated source material in the final handoff ZIP.

If safe image bytes are unavailable to the AI, still provide `README.md` + `manifest.json` with exact destinations and let Keoni supply the approved binaries manually.

## Per-asset contract

Each record should carry at least:

- `image_id`
- `filename`
- `destination_path`
- `role`
- `chapter_id` / `scene_id` when relevant
- `approval_status`
- `authority_role`: for example `site_mood`, `chapter_art`, `character_reference`, `location_reference`, `source_evidence`
- `library_path` or `library_stage_pending` for R2 staged production
- `release_id` when packaged
- `replace_asset` when superseding a known bad file
- verification action after upload

## R2 site assets

Site mood art belongs under a deterministic R2 site-art path and does **not** become chapter or character canon merely because it appears prominently.

Prefer:

```text
r2/assets/images/site/
```

for R2 homepage/branding mood art.

Chapter images belong in chapter-specific production paths and are referenced by chapter manifests only after approval and binary verification.

## Verification failure

If an uploaded image is corrupted, visually wrong, undecodable, or mismatched:

- mark the transport/integration attempt failed
- remove or stop referencing the bad live asset
- preserve the approved visual intent
- do not regenerate merely to solve a transport problem if the approved source output still exists
- re-run the handoff using Library source or manual binary placement

## Project isolation

This file governs PLG/R2 transport only. It does not authorize borrowing visual identity from Hawaiʻi Archive, Pidgin → ʻŌlelo, or any other project. Shared Image OS process and handoff logic do not create shared visual canon.
