# Controlled LLM Model Benchmark — Reviewer Comment 5

This experiment replaces the preliminary GWP-prediction comparison with a
benchmark aligned to the actual language-model role in the workflow.

## What is evaluated

Each of the four models receives the **same 35 BOM descriptions**, the **same
fixed top-k candidate processes** retrieved from the exported 608-process
ELCD/openLCA catalog, the **same prompt**, and the **same deterministic decoding
settings**.

For each BOM item the model must:

1. normalize the material description;
2. select the best candidate process, or explicitly return `-1` when no
   candidate is defensible; and
3. classify its choice as `Direct`, `Proxy`, or `Review Required`.

The LLM is **not** asked to estimate GWP or an emission factor in this benchmark.
Candidate retrieval itself is deterministic and model-independent so the final
process-selection comparison is not confounded by different search spaces.

## Default models

The registry intentionally uses similarly sized 7–8B instruction/chat models:

| Alias | Hugging Face model ID | Size class |
|---|---|---|
| `llama` | [`meta-llama/Llama-3.1-8B-Instruct`](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 8B |
| `qwen` | [`Qwen/Qwen2.5-7B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 7B |
| `deepseek` | [`deepseek-ai/deepseek-llm-7b-chat`](https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat) | 7B |
| `mistral` | [`mistralai/Mistral-7B-Instruct-v0.3`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | 7B |

**Important manuscript correction:** the current manuscript says “LLaMA 3.2
8B.” Meta's Llama 3.2 text-only instruction models are 1B and 3B; the real 8B
instruction model used by the current application repository is Llama 3.1 8B.
If this benchmark is used for the revision, the manuscript should report
`meta-llama/Llama-3.1-8B-Instruct` exactly.

The script records the resolved Hugging Face commit SHA at runtime in
`run_manifest.json`, so the exact checkpoint revision can be reported even if
`model_registry.json` leaves `revision` as `null`.

## Recommended Colab setup

Use a Google Colab T4 runtime for model testing. Install:

```bash
pip install -r requirements-benchmark.txt
```

The Llama model is gated. Log into Hugging Face using an account with approved
Meta Llama access before running it.

For a quick smoke test before the final experiment:

```bash
python experiments/model_benchmark/benchmark_models.py \
  --model qwen \
  --repeats 1 \
  --top-k 10 \
  --load-in-4bit \
  --limit-items 2 \
  --run-name qwen_smoke
```

For the final Comment 5 experiment, run each model separately:

```bash
python experiments/model_benchmark/benchmark_models.py --model llama    --repeats 5 --top-k 10 --load-in-4bit --run-name llama_comment5
python experiments/model_benchmark/benchmark_models.py --model qwen     --repeats 5 --top-k 10 --load-in-4bit --run-name qwen_comment5
python experiments/model_benchmark/benchmark_models.py --model deepseek --repeats 5 --top-k 10 --load-in-4bit --run-name deepseek_comment5
python experiments/model_benchmark/benchmark_models.py --model mistral  --repeats 5 --top-k 10 --load-in-4bit --run-name mistral_comment5
```

If a run is interrupted, rerun the same command with `--resume`. Completed
`(BOM ID, repeat)` combinations are skipped.

## Controlled decoding

The benchmark uses greedy deterministic decoding:

- `do_sample=False`;
- temperature conceptually `0.0` (temperature is not passed to `generate()`
  when sampling is disabled);
- fixed seed;
- identical prompt and candidate list for every model; and
- five repeated runs by default.

This intentionally replaces the preliminary manuscript's temperature `2.0`
configuration, which is not appropriate for a stability-focused engineering
matching task.

## Output files

Each model run produces a separate directory under `results/` containing:

- `run_manifest.json` — exact model ID/revision, prompt, decoding settings,
  quantization, software versions, GPU, seed, and run counts;
- `candidate_retrieval.csv` — deterministic top-k candidate list for every BOM
  item;
- `raw_results.jsonl` — incrementally written raw model outputs for recovery and
  auditability;
- `raw_results.csv` — flattened results table including the exact prompt text,
  raw response, input/output token counts, selected UUID, and inference time; and
- `repeatability_summary.csv` — whether each BOM item produced the same
  normalized material, selected process UUID, and decision across all repeats.

No invalid `-1` response is silently converted to candidate 0. `-1` is retained
as `Review Required`, addressing a weakness in the preliminary application
logic without changing the production application during this controlled
experiment.

## Scoring after the experts finish

Do not score model accuracy until Expert A and Expert B have completed and
reconciled the reference workbook. Once the final reference is frozen, run:

```bash
python experiments/model_benchmark/score_benchmark.py
```

If the final expert labels are still blank, the scoring script stops rather
than treating blank cells as ground truth.

The automated scoring output includes:

- canonical normalization exact-match;
- normalization token-F1;
- deterministic candidate-retrieval top-k recall;
- end-to-end exact process UUID accuracy;
- conditional process-selection accuracy when the reference process is present
  in the candidate set;
- Direct/Proxy/Review Required decision accuracy; and
- binary Review Required accuracy.

Because semantically equivalent normalized names can differ lexically, the
final paper may additionally report expert-adjudicated normalization equivalence
rather than relying only on exact string matching.
