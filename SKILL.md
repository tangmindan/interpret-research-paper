---
name: interpret-research-paper
description: Deeply interpret scientific research papers from local PDFs or supplied article files; extract and embed complete paper figures in Obsidian; and produce reusable Chinese literature notes, panel-level evidence explanations, method and statistics tutorials, critical appraisals, literature-sharing PowerPoint decks, and accessible WeChat articles. Use when the user asks to 解读或精读文献、提取论文图片、制作或迭代Obsidian笔记、解释figure或方法、制作文献汇报PPT、撰写文献解读微信稿，or improve an existing research-paper artifact.
---

# Interpret Research Papers

Treat paper interpretation as an iterative evidence workflow, not a one-shot summary.

## Select an operating mode

Choose the least expensive mode that satisfies the request. Respect an explicit user choice.

- `quick`: triage or first-pass reading. Capture identity, study design, headline findings, principal figures, and the most important limitation; do not inspect every panel or supplement.
- `standard` (default): a complete reusable note. Inspect the Methods supporting major claims and all main figures; explain important panels, statistics, limitations, and code/data availability.
- `deep`: publication-, review-, or presentation-grade interpretation. Inspect every relevant main-figure panel, essential supplementary evidence, exact Methods and statistics, requested external novelty claims, and all figure candidates.

Read [references/modes.md](references/modes.md) before starting and record the mode in `paper-evidence.json`. A higher mode extends prior evidence; it must not discard verified fields or user-authored interpretations.

## Core workflow

1. Inspect the supplied PDF and existing notes before writing.
2. Build a source map: bibliographic data, study question, cohorts, methods, figures, key results, limitations, code/data availability.
3. Separate three layers in every explanation:
   - **Observation**: what the figure or analysis directly shows.
   - **Interpretation**: the biological or technical meaning supported by the observation.
   - **Boundary**: what the evidence cannot establish.
4. Produce only the artifact requested now; keep it extensible for later questions and revisions.
5. After user feedback, preserve their original insights, correct errors explicitly, and integrate additions without duplicating sections.
6. Treat existing notes, articles, and decks as source artifacts. Do not overwrite them unless the user explicitly requests in-place editing; otherwise create a versioned or purpose-specific copy.

## Source handling

- Use the PDF skill whenever layout, figures, captions, or supplementary relationships matter.
- Extract text for search, but render and inspect relevant pages before making figure-specific claims.
- Read the exact Methods paragraph before explaining an algorithm, marker definition, threshold, statistical test, or model split.
- Distinguish main-text evidence from supplementary evidence.
- Do not fill missing methodological details with plausible defaults. Label unknowns and point to the exact place that must be checked.
- If current external facts or official software behavior are needed, verify them with authoritative sources.
- Resolve a stable paper identity before creating persistent artifacts. Read [references/evidence-cache.md](references/evidence-cache.md), then run `scripts/paper_evidence.py init` or `plan`.
- Keep machine-readable evidence in `paper-evidence.json`, validated against [schemas/paper-evidence.schema.json](schemas/paper-evidence.schema.json).
- Reuse cached stages only when their fingerprints still match. Never use a timestamp alone as proof that content changed.

## Evidence state and incremental updates

Use identifiers in this priority order: DOI, PMID, arXiv ID, then SHA-256 of the supplied source. `canonical_id` identifies the logical paper; `source_sha256` identifies the exact file edition.

Before repeating work, run `python scripts/paper_evidence.py plan paper-evidence.json --source <pdf> --mode <mode>`. Follow its invalidation plan. Source changes invalidate parsing and downstream work; extractor changes invalidate figures and downstream figure interpretation; a higher mode computes missing depth; template changes invalidate only deliverables. Preserve `user_annotations` in every automated update.

After completing a stage, use `scripts/paper_evidence.py stamp` to record status, input fingerprints, outputs, and completion time. A file's existence alone does not make a stage complete.

## Default interpretation structure

Use the following order unless the user supplies a stronger structure:

1. 一句话理解
2. 文献信息与阅读目的
3. 背景、研究空白与核心问题
4. 研究设计和数据地图
5. 关键方法
6. 主要结果与逐图解读（按Figure组织结论和证据链）
7. 核心结论与创新点
8. 批判性评价与证据强度
9. 可复用方法、待确认问题和复习问题
10. 数据、代码和参考链接

Read [references/analysis-framework.md](references/analysis-framework.md) when performing a full interpretation, a figure/method deep dive, or a critical review. Read [references/narrative-and-figure-guidance.md](references/narrative-and-figure-guidance.md) when drafting or revising a full note, figure evidence chain, WeChat article, or presentation narrative.

## Method and statistics explanations

Explain from concrete inputs to outputs:

```text
raw data → preprocessing → feature construction → model/test → output → biological meaning
```

Always state:

- unit of observation;
- variables and matrix dimensions;
- null hypothesis when a significance test is used;
- parameter choices and thresholds;
- how clusters or model outputs receive biological labels;
- independence, nesting, multiple-testing, and causal assumptions;
- at least one robustness check that would strengthen the conclusion.

Prefer formulas or minimal pseudocode when they materially clarify the method. Do not substitute jargon for mechanics.

## Terminology and narrative

- Introduce a technical term at first occurrence as Chinese name + English full name + abbreviation. Reuse the abbreviation afterward. Do not assume terms such as CNN, ViT, ESM-2, IMC, CODEX, macro-F1, or AUROC are self-explanatory.
- State the field-level challenge before listing technical limitations. Consolidate the research gap into one central problem, then derive two to four progressive core questions.
- Introduce key methods from their objective: obstacle → design choice → mechanics → output → why it solves the obstacle. Keep secondary technical background concise and move it to a glossary or further-reading section when it would interrupt the story.
- For computational or technical papers, explicitly summarize method innovation, benchmark against mainstream methods, application prospects, and the conditions required for translation.

## Merge main results with figure interpretation

Use one combined section titled `主要结果与逐图解读`. Do not write a standalone main-results summary followed by another figure-by-figure section; that structure creates repetition. Organize the combined section by figure and, within complex result figures, by the key questions answered by groups of panels.

For each result question block, use this order:

1. **Key question**: state the biological or technical question in one sentence.
2. **Key strategy**: explain the experimental or computational strategy, comparison, and metric.
3. **Series-level conclusion**: synthesize what the complete panel group establishes, including representative author-level quantitative results. Place this conclusion before the figure image or at the beginning of the figure explanation.
4. **Figure image and reading order**: show the complete figure or a legible panel group and state how to read it.
5. **Panel-by-panel evidence**: explain every relevant subpanel concretely—encoding, comparison, direct observation, and its role in the conclusion.
6. **Supporting evidence**: list essential Extended Data or Supplementary Figures with the panel they support.
7. **Strategy discussion**: explain why the authors chose the task, grouping, masking, transfer setting, metric, comparator, threshold, or clustering resolution, and what alternatives could change the result.
8. **Evidence boundary**: state what the panel group cannot establish.

Do not force this result framework onto orientation figures. For workflow, cohort-map, architecture, or study-design figures, explain only the figure purpose, reading order, relevant panels, and where later performance evidence appears.
## Figure-by-figure interpretation

Classify the figure before writing. Treat workflow, cohort-map, architecture, and study-design figures as orientation figures: explain purpose, components, and reading order without forcing a result-style conclusion. Treat result figures as evidence figures: place the integrated conclusion before the image or panel explanation.

For each result figure, answer:

- What question does this figure address?
- What does each relevant panel encode?
- In what order should it be read?
- Which comparison supports the headline?
- What can and cannot be concluded?
- Which supplementary figure or method validates it?

For every relevant subpanel, state what it encodes, the comparison, the direct observation, and its role in the series-level conclusion. Do not use a generic framework in place of concrete panel content. If one figure answers multiple questions, divide it into question blocks: **key question → strategy → series-level conclusion → panels → strategy discussion → boundary**. Explain why major design choices were made, what alternatives could change the result, and why the chosen metric is informative.

If the user asks about a caption or significance marker, locate the visual placement of brackets/stars and the exact statistical description before interpreting it.

## Obsidian notes

- Resolve output locations from explicit user parameters or project configuration. Read [references/configuration.md](references/configuration.md) before writing persistent notes, figures, archived PDFs, slides, or articles.
- Accept `vault_root`, `note_dir`, `source_dir`, `figure_dir`, and `ppt_dir` as parameters. A user-supplied value for the current request takes precedence over configuration.
- If no persistent destination is configured, write ordinary artifacts in the current task workspace. If the user explicitly requests an Obsidian-vault or final-PPT delivery and its destination cannot be discovered safely, ask for that destination; never guess a personal path.
- Use YAML properties, stable headings, Obsidian embeds, callouts, and wiki-links where useful.
- Format all LaTeX for Obsidian with dollar delimiters. Use `$...$` for inline math and `$$...$$` for display math. Never use `\(...\)` or `\[...\]` in Obsidian Markdown. Before delivery, scan the note and convert any such delimiters while preserving existing valid `$$...$$` blocks.
- Use [assets/literature-note-template.md](assets/literature-note-template.md) as the starting structure for a new note.
- Preserve existing image embeds and user-written interpretations during edits.
- Back up an existing note before a substantial rewrite.
- Keep each claim near its figure, evidence, or caveat instead of collecting all caveats at the end.

### Literature library layout and naming

When `vault_root` is configured, use this relative structure unless the user overrides it:

```text
<vault_root>/
  <paper note>.md
  source\
    <FirstAuthor>_<YYYY>_<Journal>_<ShortTopic>.pdf
  图片\
    <FirstAuthor>_<YYYY>_<Journal>_<ShortTopic>\
      Fig_01.png
      Fig_02.png
      candidates\
      figure-manifest.json
```

Apply these rules:

1. Read the first author, publication year, journal, and a concise topic from the paper itself before naming files.
2. Name the archived PDF `<FirstAuthor>_<YYYY>_<Journal>_<ShortTopic>.pdf`. Example: `Wang_2026_NatureImmunology_Airway-immunity-in-tuberculosis.pdf`.
3. Use the same stem for the paper-specific image subfolder. Never place figures directly under `图片`.
4. Sanitize Windows-invalid characters (`< > : " / \\ | ? *`), collapse repeated spaces/separators, and keep the filename concise. Prefer the official journal abbreviation only when it is unambiguous.
5. Copy the supplied PDF into `source` under its normalized name; do not delete or move the user's original file unless explicitly requested.
6. Before overwriting, compare the existing target. If names collide but files differ, append a short DOI suffix or `-2`; never silently replace a different paper.
7. Store the normalized PDF path and image directory in the note YAML, for example `pdf:` and `figure_dir:`.
8. Embed figures from the note with vault-relative paths such as `![[图片/<paper-folder>/Fig_01.png]]` so links remain stable.
9. Keep temporary renders and rejected candidates out of the note body. Retain them under the paper's `candidates` subfolder only while review is needed.
### Automatically extract and embed paper figures

For a new PDF-to-Obsidian workflow, extract main figures by default unless the user opts out.

1. Create the note-specific image directory at `<figure_dir>/<FirstAuthor>_<YYYY>_<Journal>_<ShortTopic>/`. When only `vault_root` is configured, `figure_dir` defaults to `<vault_root>/图片`.
2. Run `scripts/extract_pdf_figures.py <pdf> <image-dir> --keep-candidates` using PyMuPDF and Pillow. Combine PDF image objects, vector drawings, positioned text, and caption proximity; do not infer the crop from caption position alone.
3. Read `figure-manifest.json` and insert each `![[图片/<paper-folder>/Fig_NN.png]]` immediately after the matching result or figure-analysis section.
4. Inspect every candidate-page render and extracted image. Check that all panel labels, axes, legends, scale bars, and significance annotations are present and surrounding article text is excluded. Treat every automatic selection as unverified until this inspection passes.
5. Compare same-page, previous-page, and next-page candidates whenever captions occur near a page boundary. A caption may precede a figure on the following page; never assume that a top-of-page caption belongs only to the previous page.
6. If automatic boundaries are wrong, create an overrides JSON with the verified source page and rectangle, then rerun with `--overrides <file>`. Prefer a slightly generous rectangular crop over truncating any scientific content.
7. Do not insert or replace Obsidian embeds when `low_confidence` is true or visual review is incomplete. Never silently deliver a truncated figure or a text-only crop.
8. Extract main figures by default. Include Extended Data only when requested or essential to a claim.
9. Preserve the original rectangular aspect ratio. Do not apply rounded masks or decorative cropping.
10. Keep the manifest beside the images only when useful for traceability; keep the note embeds clean.
### Presentation storage

Resolve the final slide destination from `ppt_dir`. When only `vault_root` is configured, `ppt_dir` defaults to `<vault_root>/PPT`; otherwise use the current task workspace unless the user requested a persistent destination.

1. Create the `PPT` directory when it does not exist.
2. Store only the final verified `.pptx` there; keep builders, renders, montages, and QA files in the task workspace or temporary directory.
3. Use a concise paper-specific filename ending in `_文献分享.pptx`.
4. Before overwriting, compare the existing target. Back up or suffix a different file; never silently replace it.
5. Deliver the final vault path in the completion message.
6. Unless in-place replacement is explicitly requested, add `_v1`, a date, or another purpose suffix. If a target already exists, increment the version instead of overwriting it.

## WeChat literature articles

- Create a separate Markdown file; never overwrite the deep-reading note by default.
- Build a readable long-form narrative from the note rather than copying note bullets or callouts verbatim.
- Preserve scientific accuracy, key numbers, figure order, and evidence boundaries while translating specialized mechanics into clear mid-level language.
- Avoid poster-style slogans, exaggerated section headings, clickbait, and oversimplified analogies. Use restrained headings and connective paragraphs.
- Treat Figure 1-like design figures as orientation; explain result figures through question, strategy, evidence, conclusion, and boundary.
- Embed the verified Obsidian figures using the same vault-relative paths and include the paper citation at the end.

## Literature-sharing slides

When the user requests slides, also use the presentations skill and read [references/presentation-guidance.md](references/presentation-guidance.md).

- Build a cumulative scientific story, not a figure inventory.
- Default narrative: cover → contents → one-sentence paper → background and field-level gap → core questions → study design → key methods → result evidence chains → innovations → benchmark → applications and boundaries → closing synthesis.
- Keep design figures descriptive and orienting; do not force takeaway conclusions. Put the integrated series-level conclusion above result figures, then explain each relevant panel and its evidence role.
- Use paper figures as evidence and retain their original aspect ratio with `contain` fitting.
- Do not apply rounded-rectangle image masks or decorative cropping unless explicitly requested.
- Keep figure labels legible; split a dense figure across slides when necessary.
- End with evidence boundaries and discussion questions, not a generic thank-you page.

## Evidence language

Use calibrated verbs:

- **shows/demonstrates** only for direct evidence;
- **is associated with/correlates with** for observational relationships;
- **suggests/is consistent with** for mechanistic interpretation;
- **causes/drives** only when supported by appropriate perturbation or causal design.

Explicitly identify pseudoreplication when multiple cells, spots, TLSs, images, or samples come from the same patient.

## Completion checks

- Verify all reported sample sizes and percentages against the paper.
- Ensure figure numbers match their described results.
- Remove duplicated result sections and placeholder text.
- Preserve user-authored content and embedded assets.
- Confirm that limitations distinguish measurement, sampling, inference, and translation.
- For slides, render every page and check cropping, overlap, wrapping, and image legibility.
- Deliver links to the final artifacts and state what was changed.
- Confirm that no existing artifact was overwritten unless explicitly authorized.



