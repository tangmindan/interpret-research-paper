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

Build a cumulative story, not a figure inventory. Construct and validate result units using [logic-chain.md](logic-chain.md) before deciding slide order.

## Storyboard before slides

Create a storyboard containing the presentation goal, audience, source result order, presentation result order, reorder rationale, and slide modules. Sort primarily by audience prerequisites, scientific dependency, importance, and evidence strength; use paper order only when it remains the clearest route.

Do not silently imply that presentation order is experimental chronology. Keep source references and chronology visible when reordering could change interpretation.

Treat one result unit as one presentation **module**, not necessarily one slide. A compact result may fit on one slide. A dense result should split into:

1. question, previous finding, rationale, and approach;
2. decisive visual evidence and main answer;
3. validation, boundary, and transition when needed.

Keep the same result label across split slides. Do not compress a complete Figure until axes, legends, labels, or the decisive comparison become unreadable.

For each result module, specify:

```text
slide headline → previous finding → current question → why this experiment
→ approach → key evidence → main answer → boundary → transition
```

The headline must not exceed what the evidence shown by that point supports. Put functional or causal language only after the corresponding perturbation or causal evidence.

## Combined results and figure walkthrough

Use one section named `主要结果与逐图解读`. In a Figure narrative, organize it by Figure and question block. In a logic-chain or presentation narrative, organize it by result unit and cite every supporting Figure or panel inside that unit. Do not add a separate main-results overview that repeats the later evidence section.

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
- Confirm `主要结果与逐图解读` is one combined section organized according to the selected narrative view.
- Confirm the question, strategy, and series conclusion precede the corresponding figure evidence.
- Confirm source order, presentation order, and material reorder reasons are recorded for a reordered deck.
- Confirm each result unit maps to a coherent slide module; do not require one result to fit one slide.
- Confirm every relevant subpanel and essential supplementary figure is explained.
- Confirm design figures remain descriptive rather than result-driven.
- Check figure labels, axes, sample sizes, title wrapping, overflow, logo placement, page numbers, and source notes.
- Keep only the verified `.pptx` in the final PPT directory.
