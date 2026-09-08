# Scientific Paper Analysis Framework

## Contents

1. Evidence map
2. Study design audit
3. Method reconstruction
4. Statistical interpretation
5. Figure analysis
6. Critical appraisal
7. Translational claims

## 1. Evidence map

Create a compact internal table before drafting:

| Claim | Main evidence | Figure/table | Validation | Caveat |
|---|---|---|---|---|

Use it to prevent conclusions from drifting away from their evidence.

## 2. Study design audit

Record separately:

- discovery, training, validation, and treatment cohorts;
- patients, samples, sections, regions, spots/cells, and derived objects;
- prospective versus retrospective collection;
- public versus in-house data;
- inclusion/exclusion and quality-control rules;
- batch, platform, tissue-preservation, and center differences;
- which observations are independent and which are nested.

Never use “sample size” without clarifying its unit.

## 3. Method reconstruction

Reconstruct each major method using six questions:

1. What is the raw input?
2. What preprocessing or normalization is applied?
3. What features are constructed?
4. What algorithm or test is run, with which parameters?
5. How is the numeric output converted into a biological label?
6. How is the output validated independently?

For unsupervised classifications, distinguish data-driven separation from prior-driven marker selection, fixed cluster number, and post-hoc biological naming.

For image models, check:

- split by image, object, specimen, or patient;
- class imbalance;
- internal versus external validation;
- preprocessing and augmentation;
- domain shift across staining, scanner, center, and tissue type;
- error propagation in multistage pipelines;
- threshold locking and recalibration.

## 4. Statistical interpretation

For every P value, identify:

- unit of observation;
- tested variables;
- null and alternative hypotheses;
- global versus pairwise test;
- multiple-testing correction;
- effect size and uncertainty;
- independence and nesting assumptions.

### Common pitfalls

- Treating cells, spots, TLSs, ROIs, or image patches from one patient as independent replicates.
- Reporting significance without the comparison represented by brackets or stars.
- Interpreting a global chi-square P value as proof that every category differs.
- Selecting a cut point and evaluating it in the same cohort.
- Treating correlation across spatial distance as causal regulation.
- Ignoring compositional constraints when category proportions sum to one.

### Better alternatives to mention when relevant

- patient-level aggregation;
- mixed-effects or hierarchical models;
- patient-level permutation/bootstrap;
- multinomial or Dirichlet-multinomial models;
- locked external validation;
- sensitivity analyses over thresholds and parameter choices.

## 5. Figure analysis

Use this micro-template:

```markdown
### Figure N：takeaway-style title

- **问题**：
- **数据与编码**：
- **读图顺序**：
- **关键比较**：
- **直接结论**：
- **不能推出**：
- **验证/补充证据**：
```

When a full multi-panel figure is unreadable on a slide or note, crop only for explanatory zooms and keep a full-figure reference nearby. Never crop away axes, legends, group labels, significance brackets, or sample-size annotations needed for interpretation.

## 6. Critical appraisal

Organize limitations into four layers:

### Measurement

Resolution, marker specificity, imputation, segmentation, assay sensitivity, image quality, or annotation error.

### Sampling

Cohort size, selection bias, tissue region, two-dimensional sectioning, missing longitudinal samples, or uneven cancer-type representation.

### Inference

Confounding, reverse causation, pseudoreplication, multiple testing, model overfitting, unstable thresholds, or incompatible units of analysis.

### Translation

External generalizability, calibration, clinical utility, locked algorithms, incremental value over standard biomarkers, prospective validation, cost, and workflow integration.

## 7. Translational claims

Differentiate:

- biological association;
- prognostic association;
- predictive biomarker evidence;
- treatment-effect modification;
- clinical utility.

A biomarker is not clinically ready merely because it separates Kaplan-Meier curves. Ask whether the model is locked, externally validated, calibrated, compared with standard predictors, and evaluated for decision benefit.

