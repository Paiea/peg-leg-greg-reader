# R2 Chapter 3 Image Transaction Claim

Status: CLAIMED
Chapter: R2 Chapter 3 only
Branch: `image/r2-ch003-borrower`
Base authority at claim: `418b080295f349a5dcbc5d47b42699cff83debe9`

This branch is the durable ownership lock for the Chapter 3 image transaction under `r2/IMAGE_WORKER.md`.

Chapters 1 and 2 were already owned by active image claims at claim time. This worker must read the exact current Chapter 3 source before selecting scenes, generate only source-grounded Chapter 3 work, preserve newer authority, stage only approved binaries when safe bytes are available, record the transaction, leave the next handshake, and stop without claiming another chapter.
