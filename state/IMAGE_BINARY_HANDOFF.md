# PEG-LEG GREG — IMAGE BINARY HANDOFF

Durable transport rule for R2 and all PLG visual production.

## Core rule

Generated image binaries are not trusted merely because a GitHub write succeeds.

Drive is the default working and routing layer for generated image files. GitHub is an additional publication layer only when the deliverable is actually a repository or website asset.

For R2 production, use this state model:

1. `CHAT CANDIDATE` — generated or edited, not durably routed yet.
2. `DRIVE INBOX` — safe working copy exists in the R2 Drive inbox.
3. `DRIVE APPROVED` — selected keeper exists under the appropriate approved Drive path.
4. `GITHUB PUBLISHED` — exact accepted web/repository binary is committed at its deterministic repository path.
5. `LIVE VERIFIED` — the deployed public asset has been fetched or opened and verified.

If a worker cannot identify the current state, the asset is not complete.

## Drive-first routing

Normal visual flow:

**GENERATE → DRIVE INBOX → REVIEW / CURATE → DRIVE APPROVED**

If the file itself is the final deliverable, stop at the correct durable Drive destination. Do not add GitHub merely because GitHub is available.

Only site-facing or repository-owned assets continue:

**DRIVE APPROVED → WEB DERIVATIVE → READY FOR GITHUB → GITHUB PUBLISHED → LIVE VERIFIED**

For R2, Drive is the human-facing binary warehouse and GitHub is the accepted publication authority. Public reader pages must never depend on Drive URLs.

A repo-mirrored Drive handoff is preferred when it makes the final publication step obvious, for example:

```text
R2/Images/Ready for GitHub/
  r2/
    assets/
      images/
        <exact final repository filenames>
```

This keeps a fallback handoff to one dumb file drop rather than requiring Keoni to rename files, reconstruct paths, edit manifests, or assemble repeated tiny ZIPs.

## Direct AI → GitHub binary transport

Small optimized web assets may be transferred directly when the binary can be verified deterministically.

Before accepting a direct blob transfer:

1. Compute the local Git blob SHA from the exact source bytes: `SHA1("blob <byte_length>\\0" + bytes)`.
2. Create the GitHub blob from those exact bytes.
3. Require the returned GitHub blob SHA to match the local expected SHA exactly.
4. Attach only matching blobs to the repository tree.
5. Re-read repository path metadata and verify the committed blob SHA and byte size.
6. After deployment, fetch or open the public asset and verify that it decodes and is the intended image.

A successful API response without a matching blob SHA is a failed transport attempt.

Large image payloads may be unreliable through chat-scale binary calls. When a payload is too large or hash verification fails, keep the approved master in Drive and use a filesystem-capable publication path such as Work/Codex or a single manual file drop into the already-prepared repo-mirrored destination. Do not repeatedly fight an unreliable binary transport path.

## Default visual handoff

1. Resolve current GitHub authority and the exact visual job.
2. Generate or edit the image.
3. Route useful production output to Drive rather than leaving it trapped in chat.
4. Review and approve useful output before integration.
5. Assign a stable filename and exact repository-relative destination when the asset is site-facing.
6. Preserve a full-quality approved Drive master.
7. Derive appropriately sized web assets for publication.
8. Prefer direct hash-verified GitHub blob transfer for small optimized site assets.
9. If direct transfer is unsuitable, stage exact final filenames under a repo-mirrored `Ready for GitHub` Drive path and use the smallest practical filesystem/manual handoff.
10. Re-read the repository and verify that every expected asset exists with the expected blob SHA and size.
11. Decode/open the actual repository or deployed file. Do not infer validity from blob existence or file size alone.
12. Only after binary verification update chapter manifests, gallery mappings, illustration registry state, or live reader references.
13. After merge/deploy, verify highly visible assets on the actual public page.

## R2 Drive staging

Current preferred R2 Drive surface:

```text
/Google Drive/02 PROJECTS/R2/Images/
  00 Inbox/
  Approved/
  Ready for GitHub/
```

`00 Inbox` holds candidates and working assets. `Approved` holds selected full-quality masters organized by role. `Ready for GitHub` holds optimized publication derivatives with exact repository-relative filenames and, when useful, repo-mirrored folder structure.

Drive create/copy operations may be used to promote a keeper when mounted Google Drive move/rename operations are unavailable. Duplicate working copies are acceptable when the Approved copy is clearly named and the publication path is unambiguous.

This staging surface changes the size of the human handoff, not the authority model.

- GitHub still owns accepted story/visual authority, intended paths, manifests, and integration state.
- Drive stores actual working and approved image binaries between disposable workers.
- Normal image workers should stage useful keepers rather than making Keoni download a tiny ZIP after every image.
- ZIPs remain useful for genuinely large release batches, but they are not the default for one or a few assets.

See `r2/IMAGE_SYSTEM.md`, `r2/IMAGE_WORKER.md`, and `r2/IMAGE_RELEASES.md` where applicable.

If a generated image is not exposed as a safe file reference that can be stored in Drive or Library, mark staging pending. Do not claim staging success from a visible image alone.

## ZIP handoff

For a large R2 batch where a release archive is still the cheapest safe transport, prefer:

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

## Per-asset contract

Each record should carry at least:

- `image_id`
- `filename`
- `destination_path`
- `role`
- `chapter_id` / `scene_id` when relevant
- `approval_status`
- `authority_role`: for example `site_mood`, `chapter_art`, `character_reference`, `location_reference`, `source_evidence`
- Drive or Library staging path, or a clear staging-pending status
- `release_id` when packaged
- `replace_asset` when superseding a known bad file
- verification action after upload

## R2 site assets

Site mood art belongs under a deterministic R2 site-art path and does **not** become chapter or character canon merely because it appears prominently.

Prefer:

```text
r2/assets/images/site/
```

for new R2 homepage/branding mood art when the current reader architecture allows it. Existing named live hero/cover slots may be replaced in place when that is the smallest safe change and current page references already point there.

Chapter images belong in chapter-specific production paths and are referenced by chapter manifests only after approval and binary verification.

## Verification failure

If an uploaded image is corrupted, visually wrong, undecodable, hash-mismatched, or otherwise mismatched:

- mark the transport/integration attempt failed
- remove or stop referencing the bad live asset
- preserve the approved visual intent and Drive master
- do not regenerate merely to solve a transport problem if the approved source output still exists
- re-run the handoff using the Drive source, a filesystem-capable worker, or manual binary placement

## Project isolation

This file governs PLG/R2 transport only. It does not authorize borrowing visual identity from Hawaiʻi Archive, Pidgin → ʻŌlelo, or any other project. Shared Image OS process and handoff logic do not create shared visual canon.
