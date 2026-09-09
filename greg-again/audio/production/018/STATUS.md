# Greg, Again Chapter 18 Audio Status

Chapter identity: `ga-018` / numeric Chapter 18
Current title metadata: **Six Weeks**
Voice: `deep`
Take count: **34**
Final duration: **790.128s**
Final asset: `greg-again/audio/assets/chapter-018.mp3`
Durable chunks: `greg-again/audio/assets/chunks/018/01.mp3` through `34.mp3`
Take map: `greg-again/audio/takes/018.json`

## State

**COMPLETE — RECOVERED EXISTING PROVIDER WORK FOR PUBLICATION**

The Chapter 18 claim already contained thirty-four captured provider artifacts plus a stitched chapter MP3. This publication transaction reuses that completed work and does not regenerate synthesis.

The capture workflow verified every take with `ffprobe`, required positive duration, stitched all thirty-four takes with ffmpeg concat copy, verified the final chapter with `ffprobe`, required exactly thirty-four chunk MP3s, and required a final file larger than 1 MB before committing the durable audio artifacts.

Chapter title is treated as mutable metadata. Ownership and publication identity are `ga-018` + numeric Chapter 18.

Registry reconciliation in this transaction also corrects Chapter 22 to `audio: published`, matching the already-published `ga-022` manifest entry and merged audio asset.

## Next handshake

After this chapter is merged, rescan actual written chapter files from low to high. Preserve the real provider work on legacy Chapters 15–17 and the durable Chapter 20 ownership/work. Recover existing artifacts before any synthesis. Do not use historical titles to decide whether audio is missing.
