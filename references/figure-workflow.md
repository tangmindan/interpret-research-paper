# Figure workflow

Read this when figures, captions, panels, significance markers, or image extraction matter.

## Organize the evidence

Use one combined section titled `主要结果与逐图解读`; do not write a results summary and then repeat it figure by figure.

Classify each figure first:

- **Orientation figure:** workflow, cohort map, architecture, or study design. Explain purpose, components, reading order, and where later evidence tests the design.
- **Evidence figure:** organize by one or more scientific question blocks.

For each evidence question block use:

```text
key question → strategy/comparison/metric → series-level conclusion
→ complete figure or legible panel group and reading order
→ panel-level evidence → supplementary support
→ design-choice discussion → evidence boundary
```

For every relevant panel, state its encoding, compared groups, direct numerical or visual observation, role in the integrated conclusion, and what it cannot establish. Explain why important metrics, thresholds, masking tasks, comparators, transfer settings, or clustering resolutions were chosen and what alternatives could change.

When interpreting a caption or significance marker, locate the brackets/stars visually and read the exact statistical description first.

## Extract original figures

For a new PDF-based note, extract main figures unless the user opts out:

```text
python scripts/extract_pdf_figures.py <pdf> <figure-output-dir> --keep-candidates
```

The script combines PDF image objects, vector drawings, positioned text, and caption proximity; caption position alone is insufficient.

1. Read `figure-manifest.json`.
2. Inspect every extracted image and candidate-page render.
3. Confirm all panel labels, axes, legends, scale bars, brackets, and sample-size annotations are present and unrelated body text is excluded.
4. Compare same-, previous-, and next-page candidates near page boundaries.
5. If boundaries are wrong, regenerate from a visually inspected rectangle; prefer a slightly generous rectangular crop over lost evidence.
6. Do not embed `low_confidence` or visually unchecked output as verified.

Extract Extended Data only when requested or essential to a claim. Preserve rectangular aspect ratio and avoid decorative crops. When a full figure is unreadable, retain a complete reference and use additional panel zooms without removing required context.

Record figure ID, source/caption page, crop, file, extractor version, QA status, panels, related claims, and supporting supplements in `paper-evidence.json` when persistent evidence state is in scope.
