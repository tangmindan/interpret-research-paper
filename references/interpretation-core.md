# Interpretation core

Read this for standard or deep interpretation, method/statistics teaching, or critical appraisal.

## Narrative and structure

Start with the field-level challenge, consolidate one central research gap, and derive two to four progressive questions. Introduce methods as obstacle → design choice → mechanics → output → why it addresses the obstacle.

Default note order:

1. 一句话理解
2. 文献信息与阅读目的
3. 背景、研究空白与核心问题
4. 研究设计和数据地图
5. 关键方法
6. 主要结果与逐图解读
7. 核心结论与创新点
8. 批判性评价与证据强度
9. 可复用方法、待确认问题和复习问题
10. 数据、代码和参考链接

For computational papers, summarize method innovation, benchmark difficulty and fairness, stable strengths, failures or nonsignificant comparisons, applications, and validation needed for translation.

At first occurrence, write technical terms as Chinese name + English full name + abbreviation. Explain unfamiliar infrastructure briefly by purpose; move secondary background to a glossary or further reading.

## Evidence map

Create a compact internal map before drafting:

| Claim | Direct evidence | Figure/table/method | Validation | Boundary |
|---|---|---|---|---|

Keep claims close to this evidence in the final artifact.

## Study design audit

Record discovery, training, validation, and treatment cohorts; patients, specimens, sections, regions, spots/cells, and derived objects; prospective versus retrospective and public versus in-house data; inclusion and quality-control rules; batch/platform/tissue/center differences; and independent versus nested observations. Never report “sample size” without naming its unit.

## Method reconstruction

Explain concrete inputs to outputs:

```text
raw data → preprocessing → feature construction → model/test → output → biological meaning
```

State the observation unit, variables or matrix dimensions, parameters and thresholds, biological labeling procedure, independence and causal assumptions, and at least one useful robustness check. For unsupervised results, separate data-driven structure, prior-driven marker choice, fixed resolution/cluster count, and post-hoc naming.

For predictive or image models, check split unit, leakage, class imbalance, internal/external validation, preprocessing, augmentation, domain shift, error propagation, threshold locking, and recalibration.

## Statistical interpretation

For each inferential result, identify the observation unit, variables, null hypothesis, global versus pairwise comparison, multiplicity correction, effect size and uncertainty, and independence/nesting assumptions.

Common failures include treating cells or image patches as independent patients, reading a global test as proof of every pairwise contrast, selecting and testing a cutoff in one cohort, treating spatial correlation as causality, and ignoring compositional constraints. Mention patient-level aggregation, hierarchical models, patient-level resampling, locked external validation, or sensitivity analysis when they materially improve the design.

## Critical appraisal

Organize material limitations into measurement, sampling, inference, and translation. Differentiate biological association, prognostic association, predictive biomarker evidence, treatment-effect modification, and clinical utility. A separated survival curve alone does not establish clinical readiness.

## Evidence language

- Use **shows/demonstrates** only for direct evidence.
- Use **is associated with/correlates with** for observational relationships.
- Use **suggests/is consistent with** for mechanistic interpretation.
- Use **causes/drives** only with an appropriate perturbation or causal design.
