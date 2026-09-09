# Scientific logic chain

Read this when the user wants the paper's reasoning, a result-led note, a journal-club narrative, or a presentation storyboard.

## Separate evidence from narrative

Use three layers:

```text
source evidence → scientific result units → deliverable-specific order
```

- Evidence records what the paper directly contains: panels, tables, Methods, observations, statistics, and boundaries.
- A result unit records one inferential advance in the paper's argument.
- A narrative view orders result units for a particular reader or audience without changing the evidence.

Do not make Figure the root of the reasoning model. One result may require several figures; one figure may support several results. Preserve source order separately from narrative order.

## Result unit

Give each major scientific advance a stable `result_id` and record:

- `previous_finding`: established premise needed for this step.
- `current_question`: uncertainty addressed now.
- `why_this_experiment`: why the existing evidence cannot answer it and why this design is informative.
- `strategy`: experiment, comparison, model, and decisive readout.
- `main_answer`: narrow answer directly supported by the cited evidence.
- `evidence`: figure, panel, table, method, or supplement references and the role each plays.
- `boundary`: what the result does not establish.
- `what_this_leads_to_next`: the next uncertainty created or enabled by this answer.

Avoid circular transitions. `previous_finding` must already be supported by an earlier result unit or explicitly marked as prior/background knowledge. `what_this_leads_to_next` should explain a scientific dependency, not merely say that the authors next performed an experiment.

## Narrative views

### figure

Follow the source Figure order for panel-level reading, reproduction, or audit. Group panels by the questions they answer, but do not reorder the paper silently.

### logic-chain

Order result units by scientific dependency:

```text
gap → question → discriminating experiment → answer
    → new uncertainty → next experiment → synthesis
```

Make inferential jumps and missing links visible. A source-order transition may be retained when it is already the clearest dependency path.

### presentation

Order result units around audience prerequisites and the presentation goal. Prefer the smallest background needed to understand the decisive results. Record both `source_order` and `presentation_order`, plus a reason for every material reorder.

Do not strengthen a claim to make a better headline. A slide headline is the result unit's supported `main_answer`; causal wording still requires causal evidence.

## Quality checks

- Every result unit has evidence and a boundary.
- Every major transition follows from the preceding answer or is labeled as a deliberate presentation bridge.
- Reordering changes exposition, never provenance or claimed chronology.
- Contradictory, null, or limiting evidence stays attached to the affected result unit.
- Design/orientation figures may remain context nodes instead of being forced into result units.
