# Research artifacts for reviewer revision

This folder contains the transparent reference-set and openLCA process-catalog
assets used during the manuscript revision. These files are intentionally kept
separate from the application source code so that the evaluation workflow can
be inspected without changing the runtime implementation.

## Contents

### `openlca/ELCD_Process_Catalog.xlsx`

A catalog of **608 process descriptors** exported through the openLCA IPC server
from the database active during the August 2026 revision workflow. The catalog
contains process UUIDs, process names, locations, process types, categories, and
library fields where available.

This file is a process-search catalog, not a redistribution of the complete LCI
database. It does not contain the full process exchanges, product systems, or
impact results.

The exact database release/version should be recorded in the manuscript and in
`openlca/CATALOG_METADATA.md` before final publication. The IPC export itself
identifies the active processes but does not reliably encode the human-readable
database release name.

### `expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx`

Workbook prepared for independent expert review of the **35 BOM entries** used
in the three demonstration case studies.

The intended sequence is:

1. Expert A independently normalizes each BOM material and selects the best
   available process from the exported catalog.
2. Expert B performs the same task independently.
3. The two expert sheets are reconciled into a final expert reference.
4. Only after reconciliation are LLM outputs compared against the reference.

The workbook intentionally does **not** expose LLM answers to the experts during
initial labeling, reducing anchoring bias. It also records the exact process UUID
for selected database processes.

> Status: this workbook is an evaluation template / in-progress reference set.
> Blank expert cells must not be interpreted as completed ground-truth labels.

## Why these artifacts are included

They support a more reproducible evaluation of the actual role of the LLM in
this study: material normalization, candidate-process interpretation, final
process selection, and review-required decisions. They are not evidence of
building-level validation by themselves.

## Related controlled model benchmark

The executable Reviewer Comment 5 experiment is kept under
`experiments/model_benchmark/`. It uses these 35 BOM items and this exported
608-process catalog as fixed benchmark inputs. Model outputs should not be
scored as accuracy results until the expert reference workbook has been fully
reconciled.
