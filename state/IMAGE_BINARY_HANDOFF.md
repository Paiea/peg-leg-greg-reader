# PEG-LEG GREG — IMAGE BINARY HANDOFF

Durable transport rule for R2 and all PLG visual production.

## Core rule

Generated image binaries are not trusted merely because a GitHub write succeeds.

When direct AI → GitHub binary transport is unreliable:

**AI owns planning, prompt/scene selection, filenames, deterministic destination paths, manifests, registry state, reader code, and verification. Keoni owns the final approved image-file drop into the named repository path.**

This rule exists because a generated R2 site hero reached GitHub as a valid-looking binary object but rendered visibly corrupted on the deployed site. Treat that as evidence about the transport path, not as an image-model failure.

## Default visual handoff

1. Resolve current GitHub authority and the exact visual job.
2. Generate or edit the image.
3. Review and approve useful output before integration.
4. Assign a stable filename and exact repository-relative destination.
5. Prepare a handoff manifest/README. For a batch, package approved safe binaries in a ZIP when possible.
6. If the generated binary cannot safely be packaged by the AI, Keoni manually saves/uploads the approved image into the exact destination path.
7. Re-read the repository and verify that every expected asset exists.
8. Decode/open the actual repository file. Do not infer validity from blob existence or file size.
9. Only after binary verification update chapter manifests, gallery mappings, illustration registry state, or live reader references.
10. After merge/deploy, verify highly visible assets on the actual public page.

## ZIP handoff

For multi-image production, prefer:

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
- re-run the handoff using manual binary placement

## Project isolation

This file governs PLG/R2 transport only. It does not authorize borrowing visual identity from Hawaiʻi Archive, Pidgin → ʻŌlelo, or any other project. Shared Image OS process and handoff logic do not create shared visual canon.
