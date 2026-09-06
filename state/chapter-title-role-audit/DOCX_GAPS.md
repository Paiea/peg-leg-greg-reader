# Canonical DOCX Title Metadata Gaps

During title integration, the Book II canonical DOCX was inspected directly.

It contains chapter boundaries 83-99, then resumes at 106-137. It has no explicit chapter-boundary/title metadata for Chapters 100-105. The prose in that region is preserved untouched because reconstructing boundaries from prose would be speculative.

Approved title renames inside that pre-existing metadata gap are:

- Chapter 102: `The Pivot` -> `The Trainee`
- Chapter 104: `The Second Opinion` -> `The Adviser`
- Chapter 105: `The Control` -> `The Subject`

Those titles are normalized on reader/index surfaces. The canonical DOCX prose is not altered or repartitioned for them.

Separately, Book I Chapter 51 had an explicit `CHAPTER FIFTY-ONE` boundary but no following title paragraph. Because the boundary itself was unambiguous, integration inserts the approved `THE SIGNALMAN` title paragraph there without changing chapter prose.
