---
name: interpret-research-paper
description: Deeply interpret supplied scientific papers into evidence-grounded Chinese notes or derivative artifacts. Use for paper deep reading, figure or method explanation, critical appraisal, Obsidian notes, journal-club slides, or accessible literature articles; not for broad literature discovery without a target paper.
---

# Interpret Research Papers

Treat interpretation as an iterative evidence workflow, not a one-shot summary.

## Choose scope

Select the least expensive mode that satisfies the request: `quick` for triage, `standard` for a reusable complete note, or `deep` for panel-, supplement-, or presentation-grade work. Respect an explicit choice and read [references/modes.md](references/modes.md). A higher mode extends verified prior work instead of replacing it.

Choose narrative independently from depth: `figure` follows the source, `logic-chain` reconstructs scientific reasoning, and `presentation` optimizes audience understanding. Read [references/logic-chain.md](references/logic-chain.md) for logic-chain or presentation work. Do not treat Figure order as the canonical reasoning order.

Produce only the artifact requested now. Do not create notes, slides, articles, or persistent library files merely because the Skill supports them.

## Required evidence rules

- Inspect the supplied paper and existing artifacts before drafting. Use the PDF skill whenever layout, figures, captions, or supplement relationships matter.
- Separate **observation** (direct result), **interpretation** (supported meaning), and **boundary** (what cannot be established).
- Trace major claims to exact figures, panels, tables, Methods passages, or supplementary evidence.
- Read the exact Methods text before explaining an algorithm, marker definition, threshold, statistical test, model split, or labeling rule. Do not fill gaps with plausible defaults.
- Distinguish main-text from supplementary evidence. Verify sample sizes, percentages, figure numbers, and statistical comparisons against the paper.
- Use calibrated causal language and identify pseudoreplication when derived observations are nested within the same patient or experimental unit.
- Preserve user-authored interpretations and assets. Do not overwrite an existing artifact without explicit authorization; otherwise create a versioned or purpose-specific output.

## Core workflow

1. Resolve the paper identity, requested mode, requested artifact, and authorized output location.
2. Build a source map covering bibliography, question, cohorts/data, methods, figures, results, limitations, and code/data availability.
3. Extract an evidence map before writing, then construct result units and project them into the requested narrative.
4. Inspect and verify every source element required by the selected mode.
5. Deliver the requested artifact with unresolved questions and evidence boundaries visible.

For `standard` or `deep` work, method/statistics teaching, or critical appraisal, read [references/interpretation-core.md](references/interpretation-core.md).

## Route by task

- When figures, captions, panels, significance markers, or image extraction matter, read [references/figure-workflow.md](references/figure-workflow.md).
- For persistent paths or reusable project settings, read [references/configuration.md](references/configuration.md).
- For `paper-evidence.json`, caching, or a repeated/incremental run, read [references/evidence-cache.md](references/evidence-cache.md) and use `scripts/paper_evidence.py`.
- For an Obsidian note or library import, read [references/obsidian-output.md](references/obsidian-output.md) and start from [assets/literature-note-template.md](assets/literature-note-template.md).
- For a literature-sharing deck, read [references/logic-chain.md](references/logic-chain.md) and [references/presentation-guidance.md](references/presentation-guidance.md), then use the presentations skill.
- For a WeChat or accessible literature article, read [references/wechat-output.md](references/wechat-output.md).

Read only the references needed for the current request. The required evidence rules above apply in every route.

## Evidence state

For persistent or incremental work, store machine-readable evidence in `paper-evidence.json`, validated against [schemas/paper-evidence.schema.json](schemas/paper-evidence.schema.json). Prefer DOI, then PMID, arXiv ID, and finally source SHA-256 for logical identity; keep the exact source-content hash separately.

Before repeating work, run:

```text
python scripts/paper_evidence.py plan paper-evidence.json --source <paper> --mode <mode> --narrative <figure|logic-chain|presentation>
```

Follow the returned invalidation plan and preserve `user_annotations`. A file's existence or timestamp alone does not make cached evidence valid.

## Completion

- Ensure conclusions remain adjacent to supporting evidence and caveats.
- Remove duplicated result sections, placeholders, and unsupported certainty.
- Confirm limitations distinguish measurement, sampling, inference, and translation when the selected mode requires critical appraisal.
- Visually inspect every extracted figure or generated slide required by the selected mode; never present an unchecked or truncated crop as verified.
- Report the delivered artifact, changes made, unresolved gaps, and whether any existing file was replaced.
