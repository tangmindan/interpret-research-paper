# Changelog

This project follows Semantic Versioning.

## [Unreleased]

## [1.1.0] - 2026-09-09

### Added

- Independent `figure`, `logic-chain`, and `presentation` narrative views alongside evidence-depth modes.
- Reusable scientific `result_units` connecting prior finding, question, experimental rationale, strategy, answer, evidence, boundary, and next question.
- Audience-specific `presentation_plans` with source order, presentation order, reorder rationale, and multi-slide result modules.
- A separate incremental `reasoning` stage and a backward-compatible `migrate` command that preserves user annotations.

### Changed

- Result interpretation is no longer structurally rooted in Figure order.
- Presentation guidance treats a major result as a slide module rather than forcing one result onto one slide.

## [1.0.2] - 2026-09-08

### Changed

- Reduced `SKILL.md` from 238 lines to a 65-line routing entrypoint.
- Split scientific interpretation, figure handling, Obsidian output, and accessible-article guidance into conditionally loaded references.
- Consolidated duplicated results/Figure guidance and aligned the note template.
- Removed organization-specific presentation assets and fonts from public defaults.
- Added size-budget and broken-reference checks for the Skill entrypoint.

## [1.0.1] - 2026-09-08

### Fixed

- Removed the original author's personal Obsidian and PPT paths from public instructions.
- Added explicit output parameters and an ignored project-local configuration file.
- Added validation preventing common personal absolute paths from entering public guidance.

## [1.0.0] - 2026-09-08

### Added

- `quick`, `standard`, and `deep` operating modes.
- `paper-evidence.json` Draft 2020-12 schema.
- DOI/PMID/arXiv/content-hash paper identity.
- Content-addressed source fingerprints and scoped incremental invalidation.
- Deterministic manifest initialization, planning, and stage stamping.
- Unit tests, repository validation, and GitHub Actions CI.
- MIT license, contribution policy, security policy, and example evidence manifest.
