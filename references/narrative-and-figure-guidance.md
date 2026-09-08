# Narrative and Figure Guidance

## Contents

1. Research story
2. Terminology
3. Combined results and figure evidence
4. Figure roles
5. Technical-paper emphasis
6. WeChat adaptation
7. Artifact preservation

## 1. Research story

Start with the field-level challenge, state one central research gap, and derive a small set of progressive questions. Use this technical-paper arc:

```text
field/data problem → design requirements → model and dataset
→ representation validation → cross-domain benchmark
→ biomedical application → innovation and boundary
```

## 2. Terminology

At first occurrence, write `中文名称（English full name, ABBR）`, then reuse the abbreviation. Give unfamiliar infrastructure such as protein language models a short purpose-oriented introduction; move secondary details to a glossary, appendix, or further reading.

## 3. Combined results and figure evidence

Use a single section titled `主要结果与逐图解读`. Organize it by Figure, not as a summary section followed by a repeated figure section.

For each result figure, split the panels into one or more coherent question blocks. Use:

```text
Key question
→ key strategy, comparison, and metric
→ series-level conclusion with representative numbers
→ figure image and reading order
→ panel-by-panel evidence
→ Extended Data / Supplementary support
→ strategy discussion
→ evidence boundary
```

Place the key question, strategy, and series-level conclusion before the figure image or at the beginning of the image explanation. The conclusion must synthesize the complete panel group, not merely restate a caption. Include representative author-level quantitative results and benchmark comparisons without copying the author's wording.

For every relevant subpanel, specify:

- what data and visual encoding appear;
- which groups or conditions are compared;
- the direct numerical or visual observation;
- how it supports the series-level conclusion;
- what cannot be inferred.

Explain why major choices were made: masking task, marker grouping, transfer type, comparator, metric, threshold, clustering resolution, or validation design. State what an alternative choice could change.

## 4. Figure roles

### Orientation figure

For workflow, cohort map, architecture, or study design figures, explain purpose, components, and reading order. Point to later figures that test the design. Do not force a result-style conclusion or causal claim.

### Evidence figure

Use the combined result framework above. If the figure supports multiple arguments, split it into question blocks while keeping all blocks under the same Figure heading.

## 5. Technical-paper emphasis

Always synthesize method innovation, benchmark by task and domain-shift difficulty, stable strengths, failures or non-significant comparisons, comparison fairness, application prospects, and validation required before translation.

## 6. WeChat adaptation

Write for an educated life-science audience. Keep the combined result-and-figure narrative: introduce the question, strategy, and conclusion, then walk through the relevant panels in readable prose. Avoid clickbait, poster slogans, childish analogies, and note-like bullet dumping. Preserve exact representative numbers and evidence boundaries.

## 7. Artifact preservation

Keep source notes, prior articles, template decks, and previous PPT versions. Create a purpose-specific filename or increment `_v1`, `_v2`, and so on unless the user explicitly requests in-place replacement. Keep builders, renders, and QA files outside the final Obsidian output folder.