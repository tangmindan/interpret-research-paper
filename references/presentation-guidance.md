# Literature Presentation Guidance

## Recommended narrative

Use the paper's evidence density rather than a fixed slide count. A detailed technical-paper journal club may need 18–30 slides when dense figures must be split for legibility.

Default sequence:

1. Minimal cover
2. Contents
3. One-sentence paper
4. Background and field-level research gap
5. Progressive core questions
6. Study design and data map
7. Key methods from objective to mechanics
8. Combined main-results and figure-evidence section
9. Core conclusions and method innovations
10. Benchmark against mainstream methods
11. Application prospects and evidence boundaries
12. Closing synthesis and discussion question

Build a cumulative story, not a figure inventory.

## Combined results and figure walkthrough

Use one section named `主要结果与逐图解读`. Organize it by Figure and, for complex figures, by question blocks. Do not add a separate main-results overview that repeats the later figure section.

Each result question block should appear in this order:

```text
key question → strategy/metric → series conclusion
→ figure or panel group → panel evidence
→ supplementary support → strategy discussion → boundary
```

Put the question, strategy, and integrated conclusion before the figure or at the beginning of the figure explanation. Include representative quantitative results. Then explain every relevant panel concretely. Split a dense figure across multiple slides when necessary, but keep the slides under the same Figure-level result story.

## Figure roles

### Design and orientation figures

For workflow, cohort-map, data-overview, and architecture figures, state the purpose and reading order, explain each relevant panel as part of the design, and point forward to the result figures. Do not force a result-style conclusion.

### Result figures

Use the complete original figure with `contain`. If labels are too small, add dedicated panel zooms while preserving a full-figure reference. Never crop away axes, legends, sample sizes, scale bars, or significance annotations.

## Scientific copy

- Define technical terms at first occurrence as Chinese name + English full name + abbreviation.
- Introduce unfamiliar infrastructure such as ESM-2 briefly; move secondary detail to notes, appendix, glossary, or further reading.
- Use restrained takeaway titles; avoid poster slogans, exaggerated type, clickbait, and repeated formulaic headlines.
- Distinguish observation, interpretation, and evidence boundary.
- For technical papers, summarize method innovation, benchmark strengths and failures, comparison fairness, applications, and translation requirements.

## Brand and files

- Use the resolved `ppt_dir` for final decks. If it is unset, follow [configuration.md](configuration.md); never infer a personal absolute path.
- Use organization-specific templates, logos, and fonts only when the user supplies or configures them for the current project.
- Preserve logo aspect ratio and brand colors; do not infer a private asset path or organization identity.
- Prefer broadly available CJK fonts when no typography system is supplied, and verify glyph rendering on every slide.
- Do not overwrite an existing deck unless explicitly requested. Increment `_v1`, `_v2`, or another version suffix.

## QA

- Render and inspect every slide.
- Confirm `主要结果与逐图解读` is one combined section organized by Figure and question block.
- Confirm the question, strategy, and series conclusion precede the corresponding figure evidence.
- Confirm every relevant subpanel and essential supplementary figure is explained.
- Confirm design figures remain descriptive rather than result-driven.
- Check figure labels, axes, sample sizes, title wrapping, overflow, logo placement, page numbers, and source notes.
- Keep only the verified `.pptx` in the final PPT directory.
