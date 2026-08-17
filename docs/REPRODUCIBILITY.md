# Reproducibility notes

This document records the reproducibility workflow used during the reviewer
revision of the LLM-assisted embodied-carbon screening study.

## 1. Scope

The application is intended for preliminary A1-A3 embodied-carbon screening.
The LLM assists with material interpretation and process selection. When no
usable database value is available, the current implementation can produce an
explicitly labeled provisional estimate; such a value should not be treated as
verified LCI data.

All numerical quantity conversion, multiplication, aggregation, and building
summation are performed by deterministic application code after the relevant
inputs have been resolved.

## 2. openLCA environment

The Python application communicates with the database currently active in
openLCA through its IPC server, normally on port 8080.

For a reproducible run, record at minimum:

- openLCA version;
- database name and exact release/version;
- LCIA method and version;
- process UUID selected for each database-grounded material;
- Python version;
- `olca-ipc` and `olca-schema` versions; and
- operating system.

The repository contains `research_artifacts/openlca/ELCD_Process_Catalog.xlsx`,
which currently records 608 process descriptors from the active database used
for the August 2026 revision workflow. The exact database release/version still
needs to be entered in the metadata before final publication.

## 3. Expert reference-set workflow

The evaluation uses the 35 BOM entries from the three Nepal demonstration case
studies. Two LCA experts should label the entries independently.

For each item, each expert records:

- normalized material name;
- best available openLCA/ELCD process;
- exact process UUID;
- match classification: Direct, Proxy, or Review Required;
- confidence; and
- a short rationale when appropriate.

The experts should not see the model outputs or each other's labels during the
initial review. Disagreements are reconciled before model scoring. Ambiguous LLM
alternatives may be adjudicated afterward as acceptable alternatives, incorrect
matches, or review-required cases.

The working template is:

`research_artifacts/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx`

## 4. Controlled LLM evaluation protocol (Reviewer Comment 5)

The preliminary manuscript compared models by asking them to predict GWP values.
That comparison is replaced by a controlled experiment aligned with the actual
language-model role in the screening workflow.

The executable experiment is located at:

`experiments/model_benchmark/`

The four default checkpoints are:

- `meta-llama/Llama-3.1-8B-Instruct`;
- `Qwen/Qwen2.5-7B-Instruct`;
- `deepseek-ai/deepseek-llm-7b-chat`; and
- `mistralai/Mistral-7B-Instruct-v0.3`.

For each of the 35 BOM entries, a deterministic retriever generates the same
fixed top-k process candidates from the 608-process ELCD/openLCA catalog before
any model is called. Every model then receives the same BOM description,
declared unit, candidate list, system prompt, and output schema. In one model
call it must return: (1) a normalized material name, (2) the selected candidate
index or `-1`, and (3) Direct, Proxy, or Review Required. The model is not asked
to generate an emission factor or GWP value in this benchmark.

Candidate retrieval is therefore model-independent and can be evaluated as a
separate deterministic stage. After the expert reference is frozen, report at
minimum:

- material-normalization agreement (with lexical metrics plus human semantic
  adjudication where needed);
- candidate-retrieval recall at the declared k;
- end-to-end exact process UUID accuracy;
- process-selection accuracy conditional on the expert reference process being
  present in the candidate set;
- Direct/Proxy/Review Required decision accuracy;
- Review Required binary accuracy; and
- repeatability across five repeated runs.

The final protocol uses greedy decoding (`do_sample=False`; temperature treated
as 0 rather than sampled), a fixed seed, the same candidate count, and the same
prompt for all four models. Four-bit NF4 quantization is available for a Colab
T4 run and must be reported if used. The runtime writes the resolved Hugging
Face checkpoint SHA, prompt, software versions, GPU information, seed,
quantization, per-call inference time, parse failures, and raw response text to
`run_manifest.json` / `raw_results.*`.

The benchmark does not silently force a process assignment. A valid
`selected_candidate=-1` remains Review Required. Invalid indices or malformed
JSON are recorded as failures rather than replaced with candidate 0.

The repository currently defaults to `meta-llama/Llama-3.1-8B-Instruct`. The
manuscript's existing phrase “LLaMA 3.2 8B” should be corrected before final
submission if this benchmark is the reported experiment.

## 5. Ablation comparison

Using the same expert reference set and the same 35 BOM items, compare:

1. dictionary-only matching;
2. dictionary + fuzzy/database search; and
3. dictionary + fuzzy/database search + LLM-assisted selection.

This isolates the incremental contribution of the LLM without conflating the
experiment with the final whole-building GWP comparison.

## 6. Current LLM implementation

The code currently defaults to:

`meta-llama/Llama-3.1-8B-Instruct`

through the `LLAMA_MODEL_ID` environment variable. The in-process model loader
uses GPU inference when available and does not silently fall back to CPU.

Any model benchmark reported in the manuscript should be based on the actual
model-evaluation experiment and should not be inferred from this default alone.
