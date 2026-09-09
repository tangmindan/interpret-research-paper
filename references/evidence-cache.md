# Evidence cache and incremental updates

## Identity

Use `canonical_id` for the logical work and `source_sha256` for the exact source edition. Select identity in order: normalized DOI, PMID digits, normalized arXiv ID without version suffix, then source SHA-256.

## Layout

Default to a project-local cache:

```text
.paper-cache/<safe-canonical-key>/
  paper-evidence.json
  parsed/
  figures/
  deliverables/
```

Do not copy copyrighted full text beyond the user-authorized project or library.

## Fingerprints

Record source SHA-256, schema and skill versions, parser config/version, figure extractor config/version, interpretation profile, and deliverable template hashes. Timestamps are audit metadata, not cache keys.

Depth and narrative are independent. `mode` records evidence depth; `narrative` records requested and completed views. `result_units` store reusable scientific reasoning, while `presentation_plans` store audience-specific ordering.

## Dependencies

```text
identity -> bibliography
source -> parse -> source_map -> interpretation -> reasoning -> deliverables
                -> figures -> figure_qa -> interpretation
mode -------------------------------------> interpretation
narrative ------------------------------------------------------> deliverables
templates ------------------------------------------------------> deliverables
```

Invalidate a changed node and descendants only. Never replace verified evidence with unverified evidence. Preserve `user_annotations`, append history events, and keep conflicts explicit until reviewed.

Changing narrative should normally reuse parsed evidence and result units and rebuild only deliverables. Enrich an older manifest without replacing annotations:

```text
python scripts/paper_evidence.py migrate paper-evidence.json --narrative logic-chain
```

Plan a depth or narrative change explicitly:

```text
python scripts/paper_evidence.py plan paper-evidence.json --source paper.pdf --mode deep --narrative presentation
```
