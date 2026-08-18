LLM-Assisted Upfront Embodied-Carbon Screening

Open-source workflow for BOM interpretation, openLCA process matching, and A1-A3 screening

This repository contains the application code and reproducibility assets for a
research workflow that uses a locally deployable large language model (LLM) to
assist with construction-material interpretation and environmental-process
matching for upfront embodied-carbon screening.

The repository should be treated as a research and screening workflow, not a
certified LCA tool. Database-grounded results, documented proxies, and any
provisional LLM-supported values used by the main application must remain
visibly distinguishable in the manuscript and outputs.

The controlled four-model benchmark in this repository is intentionally narrower:
it evaluates the LLM on material normalization and ELCD/openLCA process
matching, not on direct GWP-value guessing.

Repository status

The August 2026 reviewer-revision package contains:

35 BOM entries from three Nepal demonstration case studies;

an exported ELCD/openLCA process catalog containing 608 process descriptors;

a two-expert review and reconciliation workbook;

a controlled four-model benchmark for Llama, Qwen, DeepSeek, and Mistral;

strict safeguards preventing unfinished expert labels from being scored as
ground truth; and

per-model and combined Excel outputs containing predictions, metrics, prompt,
runtime configuration, hardware information, and raw responses.

The current expert-review workbook has not yet been completed. Therefore,
Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx is presently marked
PENDING_RECONCILIATION. The benchmark will refuse to run until the expert
reference is frozen.

See docs/REPRODUCIBILITY.md for the full protocol.

Assessment scope

The broader application focuses on upfront embodied carbon within product-stage
modules A1-A3.

Module

Product-stage activity

A1

Raw-material supply

A2

Transportation to manufacturing

A3

Material manufacturing

The controlled four-model benchmark does not calculate building GWP. Its
purpose is to evaluate the language-model stages separately and reproducibly.

Controlled four-model benchmark

Models

The default checkpoints are:

meta-llama/Llama-3.1-8B-Instruct

Qwen/Qwen2.5-7B-Instruct

deepseek-ai/deepseek-llm-7b-chat

mistralai/Mistral-7B-Instruct-v0.3

The benchmark records the resolved model/checkpoint revision at runtime.

What is evaluated

For each frozen expert-reference BOM row, the experiment evaluates:

material normalization;

deterministic candidate-pool retrieval from the exported ELCD/openLCA
catalog;

LLM ranking of the supplied candidate processes;

final process selection;

Direct / Proxy / Review Required classification; and

run-to-run repeatability.

The LLM is restricted to the supplied process candidates. It is not allowed to
invent process UUIDs, emission factors, GWP values, EPDs, or citations.

Important methodological separation

Candidate-pool retrieval is deterministic and identical for all four models.
The benchmark therefore reports both:

candidate-pool recall — whether the expert process was available to the
LLM at all; and

conditional process-selection accuracy — how often the LLM selected the
expert process when that process was actually present in the candidate pool.

This prevents a retrieval failure from being incorrectly attributed entirely to
the LLM selection stage.

Decoding

The final benchmark default is greedy decoding:

temperature = 0.0
do_sample = False
runs per sample = 5
base seed = 42

Five repeated runs are retained to document repeatability. Four-bit NF4
quantization is enabled by default for CUDA execution and is written to the
output metadata.

Expert reference-set workflow

The expert workbook is located at:

ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx

It contains:

Expert_A

Expert_B

Reconciliation

ELCD_Catalog

Expert A and Expert B should label the 35 BOM entries independently before
reconciliation. Initial reviewers should not see the model outputs.

For each row, the final reconciliation must contain:

final normalized material;

final reference process, when a defensible process exists;

exact process UUID;

final decision: Direct, Proxy, or Review Required; and

notes where needed.

A Review Required row intentionally has no final process UUID.

Freeze the expert reference

After reconciliation is complete, run:

python scripts/prepare_benchmark_reference.py

The script validates all 35 rows against the exported catalog and creates/finalizes:

Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx

If any expert row is incomplete or inconsistent, the script stops and lists the
problem rows. It does not create artificial ground truth.

ELCD/openLCA process catalog

The fixed process catalog used by the benchmark is:

ELCD_Check/ELCD_Process_Catalog.xlsx

The current file contains 608 process descriptors with UUID and process-name
information plus available category, location, library, and process-type fields.
It is a process-search/reference catalog, not the complete LCI database.

To regenerate a catalog from the database currently active in openLCA:

python scripts/export_openlca_process_catalog.py --database-label "ELCD <exact version>"

Record the exact openLCA version, database release, and LCIA configuration used
for the final paper.

Running the four-model benchmark

1. Install benchmark dependencies

pip install -r requirements-benchmark.txt

For gated Hugging Face models such as Llama, make sure the account has model
access and set/login with a valid Hugging Face token before loading the model.

2. Smoke test

After the expert reference is FINAL:

python scripts/benchmark_four_llms.py --model llama --limit 2 --runs 1

3. Run each model

Running models separately is convenient on Google Colab because each result is
saved before the next model is loaded.

python scripts/benchmark_four_llms.py --model llama
python scripts/benchmark_four_llms.py --model qwen
python scripts/benchmark_four_llms.py --model deepseek
python scripts/benchmark_four_llms.py --model mistral

Alternatively, the four models can be run sequentially with:

python scripts/benchmark_four_llms.py --model all

4. Combine the four completed results

python scripts/benchmark_four_llms.py --combine-results

The combined workbook is written to:

Four_Models/Output/combined/four_model_comparison.xlsx

Benchmark outputs

Each model creates:

Four_Models/Output/<model>/benchmark_results.xlsx

with these sheets:

Predictions — row/run-level model outputs and scoring fields;

Metrics — model-level benchmark statistics;

Metadata — model ID/revision, prompt settings, seed, quantization, software,
GPU, and timing information; and

Prompt — the exact system prompt and user-prompt template.

The benchmark reports, among other fields:

valid/failed response rate;

normalization exact accuracy;

mean normalization similarity;

candidate-pool recall;

Top-1 / Top-3 / Top-5 / Top-10 ranking performance;

mean reciprocal rank;

final process-selection accuracy for matched rows;

process-selection accuracy conditional on the ground-truth process being in
the candidate pool;

Direct / Proxy / Review Required accuracy;

Review Required binary accuracy;

end-to-end reference accuracy;

macro F1; and

run-to-run selection, normalization, and match-type agreement.

Malformed JSON, invalid candidate UUIDs, inconsistent rankings, and other schema
violations are recorded as failures. A failed response is never rewarded as a
correct Review Required prediction.

Project layout

.
├── app/
│   ├── controllers/
│   ├── core/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── utils/
├── docs/
│   └── REPRODUCIBILITY.md
├── ELCD_Check/
│   ├── ELCD_Process_Catalog.xlsx
│   ├── README.md
│   └── expert_reference/
│       └── LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx
├── Four_Models/
│   ├── README.md
│   ├── Input/
│   │   └── LLM_Model_Evaluation_Reference_Set.xlsx
│   └── Output/
│       └── README.md
├── scripts/
│   ├── benchmark_four_llms.py
│   ├── prepare_benchmark_reference.py
│   └── export_openlca_process_catalog.py
├── tests/
│   └── test_model_benchmark.py
├── main.py
├── requirements.txt
├── requirements-llama.txt
└── requirements-benchmark.txt

The main application and its embodied-carbon calculation workflow are separate
from this controlled benchmark and can be revised independently without changing
the frozen benchmark protocol.

Main application

Install the main application requirements and start FastAPI with:

pip install -r requirements.txt
python main.py

The application uses the database currently active in openLCA through its IPC
server. The main application logic is not used to manufacture benchmark ground
truth.

Tests

Run repository tests with:

python -m unittest discover -s tests -v

The benchmark-specific tests include checks that:

deterministic candidate retrieval is stable;

the selected process is not silently inserted into the model's returned
ranking;

malformed responses are not counted as correct unresolved predictions; and

conditional process-selection scoring is separated from candidate retrieval.

Research-use notes

The three Nepal buildings are demonstration cases rather than comprehensive
external validation cases.

The expert reference set must be frozen before model scoring.

Commercial-platform comparisons should be described as reference/comparative
comparisons rather than absolute ground truth.

Database-backed coverage and successful numerical BOM processing are separate
concepts.

Exact model IDs/revisions, prompt, decoding settings, number of runs,
quantization, hardware, software versions, openLCA version, database release,
and LCIA method should be reported in the final paper.
