"""Benchmark four local instruction-tuned LLMs for openLCA process matching.

It evaluates LLM performance on the tasks requested for the paper:

1. Material normalization.
2. Candidate openLCA process retrieval/ranking.
3. Final openLCA process selection.
4. Run-to-run repeatability.

The script does NOT ask the LLM to invent or estimate emission factors. It uses the
fixed openLCA process catalog exported separately from ELCD 3.2 and evaluates the
models against a manually verified benchmark workbook.

Default repository paths
------------------------
Benchmark dataset:
   LLM/Four_Models/input/LLM_Model_Evaluation_Reference_Set.xlsx

Outputs:
    LLM/Four_Models/output/

Default models
--------------
- meta-llama/Llama-3.1-8B-Instruct
- Qwen/Qwen2.5-7B-Instruct
- mistralai/Mistral-7B-Instruct-v0.3
- deepseek-ai/deepseek-llm-7b-chat

Recommended execution environment
---------------------------------
Google Colab with an NVIDIA T4 or better GPU. Models are loaded one at a time and
4-bit quantization is enabled by default to reduce GPU-memory requirements.

Example
-------
    scripts/benchmark_four_llms.py --model llama

Optional example
----------------
    scripts/benchmark_four_llms.py --model qwen --limit 2 --runs 1

Benchmark workbook
------------------
The script automatically recognizes common aliases, but the preferred columns are:

    sample_id
    material_description
    quantity                       (optional)
    unit                           (optional)
    ground_truth_normalized_material
    ground_truth_process_uuid      (recommended)
    ground_truth_process_name      (recommended)
    ground_truth_unresolved        (optional; TRUE/FALSE)

At least one ground-truth process identifier (UUID or process name) is required for
matched rows. Rows explicitly marked unresolved are evaluated as unresolved cases.
"""

from __future__ import annotations

import argparse
import gc
import json
import math
import os
import platform
import random
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
import torch
from rapidfuzz import fuzz, process as rf_process
from sklearn.metrics import f1_score
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    set_seed,
)


SCRIPT_VERSION = "1.1.0"
DATABASE_LABEL = "ELCD 3.2"
SEED = 42
DEFAULT_RUNS = 5
DEFAULT_CANDIDATE_POOL_SIZE = 20
DEFAULT_TOP_K = 10
DEFAULT_MAX_NEW_TOKENS = 384
DEFAULT_TEMPERATURE = 0.1

DEFAULT_CATALOG_PATH = Path(
    "research_artifacts/openlca/openlca_process_catalog.xlsx"
)
DEFAULT_BENCHMARK_PATH = Path(
    "research_artifacts/model_benchmark/input/LLM_Model_Evaluation_Step1_Reference_Set.xlsx"
)
DEFAULT_OUTPUT_ROOT = Path("research_artifacts/model_benchmark/output")

MODEL_SPECS: dict[str, dict[str, str]] = {
    "llama": {
        "display_name": "Llama 3.1 8B Instruct",
        "model_id": "meta-llama/Llama-3.1-8B-Instruct",
    },
    "qwen": {
        "display_name": "Qwen2.5 7B Instruct",
        "model_id": "Qwen/Qwen2.5-7B-Instruct",
    },
    "mistral": {
        "display_name": "Mistral 7B Instruct v0.3",
        "model_id": "mistralai/Mistral-7B-Instruct-v0.3",
    },
    "deepseek": {
        "display_name": "DeepSeek LLM 7B Chat",
        "model_id": "deepseek-ai/deepseek-llm-7b-chat",
    },
}

SYSTEM_PROMPT = """You are an LCA material-matching evaluator for A1-A3 screening.
Your job is limited to material interpretation and matching against the supplied
openLCA candidate processes.

Rules:
1. Use ONLY process UUIDs that appear in the supplied candidate list.
2. Do NOT invent process UUIDs, emission factors, GWP values, EPDs, citations, or data.
3. Normalize the material description into a concise engineering material name.
4. Rank up to ten candidate processes from best to worst.
5. Select one final process only when it is defensible from the supplied information.
6. If no supplied candidate is defensible, return decision = \"unresolved\".
7. Return JSON only, with no Markdown and no text outside the JSON object.

Required JSON schema:
{
  \"normalized_material\": \"string\",
  \"ranked_candidates\": [
    {
      \"process_uuid\": \"string\",
      \"process_name\": \"string\",
      \"confidence\": 0.0,
      \"rationale\": \"short string\"
    }
  ],
  \"selected_process_uuid\": \"string or empty\",
  \"selected_process_name\": \"string or empty\",
  \"decision\": \"matched or unresolved\",
  \"uncertainty_reason\": \"short string\"
}
"""

COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "sample_id": ("sample_id", "id", "item_id", "row_id", "case_id"),
    "material_description": (
        "material_description",
        "material",
        "description",
        "original_description",
        "material_name",
        "bom_description",
        "original_bom_material",
        "original bom material",
    ),
    "quantity": ("quantity", "qty", "amount"),
    "unit": ("unit", "units"),
    "ground_truth_normalized_material": (
        "ground_truth_normalized_material",
        "normalized_material",
        "reference_normalized_material",
        "expected_normalized_material",
        "target_normalized_material",
        "correct_normalized_material",
        "correct normalized material",
    ),
    "ground_truth_process_uuid": (
        "ground_truth_process_uuid",
        "reference_process_uuid",
        "expected_process_uuid",
        "target_process_uuid",
        "process_uuid",
    ),
    "ground_truth_process_name": (
        "ground_truth_process_name",
        "reference_process_name",
        "expected_process_name",
        "target_process_name",
        "process_name",
        "selected_process",
        "preferred_elcd/openlca_process",
        "preferred elcd/openlca process",
        "preferred_elcd_openlca_process",
    ),
    "case_study": ("case_study", "case study"),
    "acceptable_proxy": ("acceptable_proxy", "acceptable proxy?", "acceptable_proxy?"),
    "review_required": ("review_required", "review required?", "review_required?"),
    "reviewer_notes": ("reviewer_notes", "reviewer notes"),
    "source_location": ("source_location", "source location"),
    "ground_truth_unresolved": (
        "ground_truth_unresolved",
        "reference_unresolved",
        "expected_unresolved",
        "unresolved",
    ),
}


@dataclass
class LoadedModel:
    key: str
    display_name: str
    model_id: str
    tokenizer: Any
    model: Any
    model_revision: str
    tokenizer_revision: str


def package_version(name: str) -> str:
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return "not-installed"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9.%+\-/ ]", "", text)
    return text.strip()


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "unresolved"}


def canonical_uuid(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return str(value).strip().lower()


def safe_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark four LLMs for material normalization and openLCA process matching."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG_PATH)
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK_PATH)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    parser.add_argument(
        "--candidate-pool-size", type=int, default=DEFAULT_CANDIDATE_POOL_SIZE
    )
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--max-new-tokens", type=int, default=DEFAULT_MAX_NEW_TOKENS)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument(
        "--model",
        choices=["llama", "qwen", "deepseek", "mistral", "all"],
        default="llama",
        help=(
            "Model to benchmark. For a Colab T4, run one model per command. "
            "Use 'all' only on hardware with sufficient memory."
        ),
    )
    parser.add_argument(
        "--combine-results",
        action="store_true",
        help=(
            "Do not load a model. Combine existing per-model benchmark_results.xlsx "
            "files into output/combined/four_model_comparison.xlsx."
        ),
    )
    parser.add_argument(
        "--no-4bit",
        action="store_true",
        help="Disable 4-bit quantization. Not recommended for a Colab T4.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for a quick smoke test.",
    )
    return parser.parse_args()


def set_reproducibility(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    set_seed(seed)
    if hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True


def load_catalog(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"openLCA catalog not found: {path}\n"
            "Run scripts/export_openlca_process_catalog.py first."
        )

    catalog = pd.read_excel(path, sheet_name="Processes")
    required = {"process_uuid", "process_name"}
    missing = required.difference(catalog.columns)
    if missing:
        raise ValueError(f"Catalog is missing required columns: {sorted(missing)}")

    for col in ["process_uuid", "process_name", "category", "location", "process_type"]:
        if col not in catalog.columns:
            catalog[col] = ""
        catalog[col] = catalog[col].fillna("").astype(str)

    catalog["_uuid_key"] = catalog["process_uuid"].map(canonical_uuid)
    catalog["_name_key"] = catalog["process_name"].map(normalize_text)
    catalog["_search_text"] = (
        catalog["process_name"]
        + " | "
        + catalog["category"]
        + " | "
        + catalog["location"]
    ).map(normalize_text)

    return catalog.reset_index(drop=True)


def _find_alias(columns: Iterable[str], aliases: tuple[str, ...]) -> str | None:
    normalized = {normalize_text(c).replace(" ", "_"): c for c in columns}
    for alias in aliases:
        key = normalize_text(alias).replace(" ", "_")
        if key in normalized:
            return normalized[key]
    return None


def load_benchmark(path: Path, catalog: pd.DataFrame) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Benchmark workbook not found: {path}\n"
            "Place the manually verified benchmark workbook at this path or pass --benchmark."
        )

    excel = pd.ExcelFile(path)
    sheet_name = "Reference_Set" if "Reference_Set" in excel.sheet_names else excel.sheet_names[0]
    df = pd.read_excel(path, sheet_name=sheet_name)
    rename_map: dict[str, str] = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        found = _find_alias(df.columns, aliases)
        if found is not None:
            rename_map[found] = canonical

    df = df.rename(columns=rename_map).copy()

    if "material_description" not in df.columns:
        raise ValueError(
            "Benchmark workbook must contain a material description column. "
            f"Recognized aliases: {COLUMN_ALIASES['material_description']}"
        )

    if "sample_id" not in df.columns:
        df["sample_id"] = [f"S{i:04d}" for i in range(1, len(df) + 1)]

    for optional in [
        "quantity",
        "unit",
        "ground_truth_normalized_material",
        "ground_truth_process_uuid",
        "ground_truth_process_name",
        "ground_truth_unresolved",
        "case_study",
        "acceptable_proxy",
        "review_required",
        "reviewer_notes",
        "source_location",
    ]:
        if optional not in df.columns:
            df[optional] = ""

    df["material_description"] = df["material_description"].fillna("").astype(str)
    df["ground_truth_process_uuid"] = df["ground_truth_process_uuid"].map(canonical_uuid)
    df["ground_truth_process_name"] = (
        df["ground_truth_process_name"].fillna("").astype(str).str.strip()
    )
    df["ground_truth_normalized_material"] = (
        df["ground_truth_normalized_material"].fillna("").astype(str).str.strip()
    )
    df["ground_truth_unresolved"] = df["ground_truth_unresolved"].map(as_bool)
    df["review_required"] = df["review_required"].map(as_bool)

    # If expert reviewers explicitly flag an item for review and provide no preferred
    # ELCD process, treat it as an unresolved reference case rather than forcing a match.
    no_preferred_process = (
        df["ground_truth_process_uuid"].astype(str).str.len().eq(0)
        & df["ground_truth_process_name"].astype(str).str.len().eq(0)
    )
    df.loc[df["review_required"] & no_preferred_process, "ground_truth_unresolved"] = True

    uuid_to_name = dict(zip(catalog["_uuid_key"], catalog["process_name"]))
    name_to_uuid = dict(zip(catalog["_name_key"], catalog["_uuid_key"]))

    for idx, row in df.iterrows():
        gt_uuid = canonical_uuid(row["ground_truth_process_uuid"])
        gt_name = str(row["ground_truth_process_name"]).strip()

        if not gt_uuid and gt_name:
            matched_uuid = name_to_uuid.get(normalize_text(gt_name), "")
            if matched_uuid:
                df.at[idx, "ground_truth_process_uuid"] = matched_uuid
                gt_uuid = matched_uuid

        if gt_uuid and not gt_name:
            matched_name = uuid_to_name.get(gt_uuid, "")
            if matched_name:
                df.at[idx, "ground_truth_process_name"] = matched_name

    matched_rows = ~df["ground_truth_unresolved"]
    resolved_ground_truth = df["ground_truth_process_uuid"].astype(str).str.len().gt(0)
    bad = df[matched_rows & ~resolved_ground_truth]
    if not bad.empty:
        details = "; ".join(
            f"{r['sample_id']}: {r['ground_truth_process_name'] or '[blank]'}"
            for _, r in bad.head(10).iterrows()
        )
        raise ValueError(
            "Every matched reference row must resolve to an exact process UUID in the "
            "exported ELCD catalog. Copy the preferred process name exactly from the "
            "Processes sheet of openlca_process_catalog.xlsx, or mark the item for review "
            "with no preferred process. Unresolved sample(s): " + details
        )

    return df.reset_index(drop=True)


def retrieve_candidate_pool(
    row: pd.Series,
    catalog: pd.DataFrame,
    pool_size: int,
) -> list[dict[str, Any]]:
    description = str(row.get("material_description", "")).strip()
    unit = str(safe_value(row.get("unit", ""))).strip()
    query = normalize_text(f"{description} {unit}")

    choices = catalog["_search_text"].tolist()
    matches = rf_process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        limit=min(pool_size, len(catalog)),
    )

    candidates: list[dict[str, Any]] = []
    for _, score, index in matches:
        process_row = catalog.iloc[index]
        candidates.append(
            {
                "process_uuid": process_row["process_uuid"],
                "process_name": process_row["process_name"],
                "category": process_row.get("category", ""),
                "location": process_row.get("location", ""),
                "process_type": process_row.get("process_type", ""),
                "lexical_score": round(float(score), 2),
            }
        )
    return candidates


def build_user_prompt(row: pd.Series, candidates: list[dict[str, Any]]) -> str:
    material_payload = {
        "sample_id": str(row.get("sample_id", "")),
        "material_description": str(row.get("material_description", "")),
        "quantity": safe_value(row.get("quantity", "")),
        "unit": safe_value(row.get("unit", "")),
    }

    payload = {
        "material": material_payload,
        "candidate_processes": candidates,
    }

    return (
        "Evaluate the material below using only the supplied candidate processes. "
        "Return the required JSON object.\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def load_model(model_key: str, use_4bit: bool) -> LoadedModel:
    spec = MODEL_SPECS[model_key]
    model_id = spec["model_id"]
    token = os.getenv("HF_TOKEN") or None

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        token=token,
        use_fast=True,
        trust_remote_code=False,
    )

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_kwargs: dict[str, Any] = {
        "device_map": "auto",
        "token": token,
        "trust_remote_code": False,
        "low_cpu_mem_usage": True,
    }

    if use_4bit:
        if not torch.cuda.is_available():
            raise RuntimeError(
                "4-bit benchmark mode requires a CUDA GPU. "
                "Use Google Colab GPU runtime or pass --no-4bit."
            )
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        model_kwargs["quantization_config"] = quant_config
        model_kwargs["torch_dtype"] = torch.float16
    else:
        model_kwargs["torch_dtype"] = (
            torch.float16 if torch.cuda.is_available() else torch.float32
        )

    model = AutoModelForCausalLM.from_pretrained(model_id, **model_kwargs)
    model.eval()

    model_revision = str(getattr(model.config, "_commit_hash", "") or "")
    tokenizer_revision = str(
        getattr(tokenizer, "init_kwargs", {}).get("_commit_hash", "") or ""
    )

    return LoadedModel(
        key=model_key,
        display_name=spec["display_name"],
        model_id=model_id,
        tokenizer=tokenizer,
        model=model,
        model_revision=model_revision,
        tokenizer_revision=tokenizer_revision,
    )


def unload_model(loaded: LoadedModel | None) -> None:
    if loaded is not None:
        try:
            del loaded.model
            del loaded.tokenizer
        except Exception:
            pass
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def model_input_device(model: Any) -> torch.device:
    try:
        return model.get_input_embeddings().weight.device
    except Exception:
        return next(model.parameters()).device


def generate_response(
    loaded: LoadedModel,
    user_prompt: str,
    max_new_tokens: int,
    temperature: float,
) -> tuple[str, float]:
    # Use a single user-role message for every model. This keeps the benchmark
    # prompt content identical across model families and is compatible with
    # DeepSeek LLM 7B Chat, whose model card does not recommend a system prompt.
    messages = [
        {"role": "user", "content": SYSTEM_PROMPT + "\n\n" + user_prompt},
    ]

    tokenizer = loaded.tokenizer
    model = loaded.model

    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    device = model_input_device(model)
    input_ids = input_ids.to(device)
    attention_mask = torch.ones_like(input_ids)

    generate_kwargs: dict[str, Any] = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "max_new_tokens": max_new_tokens,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id,
        "use_cache": True,
    }

    if temperature > 0:
        generate_kwargs.update(
            {
                "do_sample": True,
                "temperature": temperature,
                "top_p": 1.0,
            }
        )
    else:
        generate_kwargs["do_sample"] = False

    if torch.cuda.is_available():
        torch.cuda.synchronize()
    start = time.perf_counter()

    with torch.inference_mode():
        output = model.generate(**generate_kwargs)

    if torch.cuda.is_available():
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    generated = output[0, input_ids.shape[-1] :]
    text = tokenizer.decode(generated, skip_special_tokens=True).strip()
    return text, elapsed


def extract_json(text: str) -> tuple[dict[str, Any] | None, str]:
    if not text:
        return None, "empty_response"

    cleaned = text.strip()
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, flags=re.S | re.I)
    candidates = fenced + [cleaned]

    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first != -1 and last > first:
        candidates.append(cleaned[first : last + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed, "ok"
        except json.JSONDecodeError:
            continue

    return None, "json_parse_error"


def validate_prediction(
    parsed: dict[str, Any] | None,
    candidates: list[dict[str, Any]],
    parse_status: str,
    top_k: int,
) -> dict[str, Any]:
    valid_by_uuid = {
        canonical_uuid(c["process_uuid"]): c for c in candidates if c.get("process_uuid")
    }

    if parsed is None:
        return {
            "parse_status": parse_status,
            "normalized_material": "",
            "decision": "unresolved",
            "selected_process_uuid": "",
            "selected_process_name": "",
            "ranked_process_uuids": [],
            "ranked_process_names": [],
            "confidence": "",
            "uncertainty_reason": "",
        }

    normalized_material = str(parsed.get("normalized_material", "")).strip()
    decision = str(parsed.get("decision", "")).strip().lower()
    if decision not in {"matched", "unresolved"}:
        decision = "unresolved" if not parsed.get("selected_process_uuid") else "matched"

    ranked = parsed.get("ranked_candidates", [])
    if not isinstance(ranked, list):
        ranked = []

    valid_ranked_uuids: list[str] = []
    valid_ranked_names: list[str] = []
    first_confidence: Any = ""

    for item in ranked:
        if not isinstance(item, dict):
            continue
        uid = canonical_uuid(item.get("process_uuid", ""))
        if uid in valid_by_uuid and uid not in valid_ranked_uuids:
            valid_ranked_uuids.append(uid)
            valid_ranked_names.append(valid_by_uuid[uid]["process_name"])
            if first_confidence == "":
                first_confidence = safe_value(item.get("confidence", ""))
        if len(valid_ranked_uuids) >= top_k:
            break

    selected_uuid = canonical_uuid(parsed.get("selected_process_uuid", ""))
    status = parse_status
    if decision == "matched":
        if selected_uuid not in valid_by_uuid:
            selected_uuid = ""
            status = "invalid_selected_candidate"
            decision = "unresolved"

    if decision == "unresolved":
        selected_uuid = ""
        selected_name = ""
    else:
        selected_name = valid_by_uuid[selected_uuid]["process_name"]
        if selected_uuid and selected_uuid not in valid_ranked_uuids:
            valid_ranked_uuids.insert(0, selected_uuid)
            valid_ranked_names.insert(0, selected_name)
            valid_ranked_uuids = valid_ranked_uuids[:top_k]
            valid_ranked_names = valid_ranked_names[:top_k]

    return {
        "parse_status": status,
        "normalized_material": normalized_material,
        "decision": decision,
        "selected_process_uuid": selected_uuid,
        "selected_process_name": selected_name,
        "ranked_process_uuids": valid_ranked_uuids,
        "ranked_process_names": valid_ranked_names,
        "confidence": first_confidence,
        "uncertainty_reason": str(parsed.get("uncertainty_reason", "")).strip(),
    }


def evaluate_record(
    row: pd.Series,
    candidates: list[dict[str, Any]],
    prediction: dict[str, Any],
    top_k: int,
) -> dict[str, Any]:
    gt_uuid = canonical_uuid(row.get("ground_truth_process_uuid", ""))
    gt_name = str(row.get("ground_truth_process_name", "")).strip()
    gt_norm = str(row.get("ground_truth_normalized_material", "")).strip()
    gt_unresolved = as_bool(row.get("ground_truth_unresolved", False))

    pool_uuids = [canonical_uuid(c.get("process_uuid", "")) for c in candidates]
    ranked = prediction["ranked_process_uuids"]
    selected = prediction["selected_process_uuid"]
    predicted_unresolved = prediction["decision"] == "unresolved"

    if gt_unresolved:
        # Retrieval metrics are undefined when the expert reference says no defensible
        # ELCD process exists. These rows are scored only on unresolved-item routing.
        final_correct = predicted_unresolved
        top1_correct: Any = ""
        top3_correct: Any = ""
        top5_correct: Any = ""
        top10_correct: Any = ""
        topk_correct: Any = ""
        pool_contains_gt: Any = ""
    else:
        final_correct = bool(gt_uuid and selected == gt_uuid)
        top1_correct = bool(gt_uuid and gt_uuid in ranked[:1])
        top3_correct = bool(gt_uuid and gt_uuid in ranked[:3])
        top5_correct = bool(gt_uuid and gt_uuid in ranked[:5])
        top10_correct = bool(gt_uuid and gt_uuid in ranked[:10])
        topk_correct = bool(gt_uuid and gt_uuid in ranked[:top_k])
        pool_contains_gt = bool(gt_uuid and gt_uuid in pool_uuids)

    normalization_exact: Any = ""
    normalization_similarity: Any = ""
    if gt_norm:
        normalization_exact = normalize_text(prediction["normalized_material"]) == normalize_text(
            gt_norm
        )
        normalization_similarity = round(
            fuzz.ratio(
                normalize_text(prediction["normalized_material"]), normalize_text(gt_norm)
            )
            / 100.0,
            4,
        )

    return {
        "ground_truth_process_uuid": gt_uuid,
        "ground_truth_process_name": gt_name,
        "ground_truth_normalized_material": gt_norm,
        "ground_truth_unresolved": gt_unresolved,
        "candidate_pool_contains_ground_truth": pool_contains_gt,
        "normalization_exact": normalization_exact,
        "normalization_similarity": normalization_similarity,
        "top1_retrieval_correct": top1_correct,
        "top3_retrieval_correct": top3_correct,
        "top5_retrieval_correct": top5_correct,
        "top10_retrieval_correct": top10_correct,
        "topk_retrieval_correct": topk_correct,
        "final_selection_correct": final_correct,
        "unresolved_routing_correct": predicted_unresolved == gt_unresolved,
    }


def bool_mean(series: pd.Series) -> float | None:
    vals = [x for x in series.tolist() if isinstance(x, (bool, np.bool_))]
    if not vals:
        return None
    return float(np.mean(vals))


def compute_metrics(predictions: pd.DataFrame, runs: int) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    metrics["n_samples"] = int(predictions["sample_id"].nunique())
    metrics["n_runs_per_sample"] = runs
    metrics["n_prediction_rows"] = int(len(predictions))

    metrics["normalization_exact_accuracy"] = bool_mean(
        predictions["normalization_exact"]
    )

    similarity_values = pd.to_numeric(
        predictions["normalization_similarity"], errors="coerce"
    ).dropna()
    metrics["mean_normalization_similarity"] = (
        float(similarity_values.mean()) if len(similarity_values) else None
    )

    metrics["candidate_pool_recall"] = bool_mean(
        predictions["candidate_pool_contains_ground_truth"]
    )
    metrics["top1_retrieval_accuracy"] = bool_mean(
        predictions["top1_retrieval_correct"]
    )
    metrics["top3_recall"] = bool_mean(predictions["top3_retrieval_correct"])
    metrics["top5_recall"] = bool_mean(predictions["top5_retrieval_correct"])
    metrics["top10_recall"] = bool_mean(predictions["top10_retrieval_correct"])
    metrics["configured_top_k_recall"] = bool_mean(predictions["topk_retrieval_correct"])
    metrics["final_selection_accuracy"] = bool_mean(
        predictions["final_selection_correct"]
    )
    metrics["unresolved_routing_accuracy"] = bool_mean(
        predictions["unresolved_routing_correct"]
    )

    failed = predictions["parse_status"].ne("ok")
    metrics["failed_response_rate"] = float(failed.mean())

    durations = pd.to_numeric(predictions["generation_seconds"], errors="coerce").dropna()
    metrics["mean_generation_seconds"] = float(durations.mean()) if len(durations) else None
    metrics["median_generation_seconds"] = (
        float(durations.median()) if len(durations) else None
    )

    y_true: list[str] = []
    y_pred: list[str] = []
    for _, row in predictions.iterrows():
        true_label = (
            "__UNRESOLVED__"
            if as_bool(row["ground_truth_unresolved"])
            else canonical_uuid(row["ground_truth_process_uuid"])
        )
        pred_label = (
            "__UNRESOLVED__"
            if str(row["decision"]).lower() == "unresolved"
            else canonical_uuid(row["selected_process_uuid"])
        )
        if true_label:
            y_true.append(true_label)
            y_pred.append(pred_label or "__INVALID__")

    metrics["macro_f1_final_selection"] = (
        float(f1_score(y_true, y_pred, average="macro", zero_division=0))
        if y_true
        else None
    )

    strict_selection_agreement: list[bool] = []
    strict_normalization_agreement: list[bool] = []

    for _, group in predictions.groupby("sample_id", sort=False):
        selection_labels = [
            "__UNRESOLVED__"
            if str(v_dec).lower() == "unresolved"
            else canonical_uuid(v_uid)
            for v_dec, v_uid in zip(
                group["decision"].tolist(), group["selected_process_uuid"].tolist()
            )
        ]
        strict_selection_agreement.append(len(set(selection_labels)) == 1)

        norms = [normalize_text(v) for v in group["normalized_material"].tolist()]
        strict_normalization_agreement.append(len(set(norms)) == 1)

    metrics["run_to_run_selection_agreement"] = (
        float(np.mean(strict_selection_agreement)) if strict_selection_agreement else None
    )
    metrics["run_to_run_normalization_agreement"] = (
        float(np.mean(strict_normalization_agreement))
        if strict_normalization_agreement
        else None
    )

    return metrics


def metadata_rows(
    loaded: LoadedModel | None,
    args: argparse.Namespace,
    status: str,
    error_message: str = "",
) -> list[dict[str, Any]]:
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No CUDA GPU"
    gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    cuda_version = torch.version.cuda or ""

    values: list[tuple[str, Any]] = [
        ("script_version", SCRIPT_VERSION),
        ("exported_at_utc", utc_now()),
        ("benchmark_status", status),
        ("error_message", error_message),
        ("database_label", DATABASE_LABEL),
        ("model_key", loaded.key if loaded else ""),
        ("model_display_name", loaded.display_name if loaded else ""),
        ("model_id", loaded.model_id if loaded else ""),
        ("model_revision", loaded.model_revision if loaded else ""),
        ("tokenizer_revision", loaded.tokenizer_revision if loaded else ""),
        ("base_seed", SEED),
        ("repeat_seeds", f"{SEED}..{SEED + args.runs - 1}"),
        ("runs_per_sample", args.runs),
        ("candidate_pool_size", args.candidate_pool_size),
        ("reported_top_k", args.top_k),
        ("max_new_tokens", args.max_new_tokens),
        ("temperature", args.temperature),
        ("decoding", "greedy" if args.temperature <= 0 else "sampling"),
        ("quantization", "none" if args.no_4bit else "4-bit NF4"),
        ("python_version", sys.version.replace("\n", " ")),
        ("platform", platform.platform()),
        ("gpu_name", gpu_name),
        ("gpu_count", gpu_count),
        ("cuda_version", cuda_version),
        ("torch_version", torch.__version__),
        ("transformers_version", package_version("transformers")),
        ("accelerate_version", package_version("accelerate")),
        ("bitsandbytes_version", package_version("bitsandbytes")),
        ("pandas_version", pd.__version__),
        ("rapidfuzz_version", package_version("rapidfuzz")),
        ("scikit_learn_version", package_version("scikit-learn")),
        ("openpyxl_version", package_version("openpyxl")),
        ("catalog_path", str(args.catalog)),
        ("benchmark_path", str(args.benchmark)),
    ]
    return [{"field": field, "value": value} for field, value in values]


def prompt_sheet() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"prompt_part": "system_prompt", "text": SYSTEM_PROMPT},
            {
                "prompt_part": "user_prompt_template",
                "text": (
                    "Evaluate the material below using only the supplied candidate "
                    "processes. The runtime payload contains sample_id, material_description, "
                    "quantity, unit, and the lexically retrieved openLCA candidate list."
                ),
            },
        ]
    )


def sanitize_sheet_value(value: Any) -> Any:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def prepare_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        out[col] = out[col].map(sanitize_sheet_value)
    return out


def format_workbook(writer: pd.ExcelWriter) -> None:
    workbook = writer.book
    for sheet_name in workbook.sheetnames:
        ws = workbook[sheet_name]
        ws.freeze_panes = "A2"
        if ws.max_row >= 1 and ws.max_column >= 1:
            ws.auto_filter.ref = ws.dimensions
        for column_cells in ws.columns:
            letter = column_cells[0].column_letter
            max_len = 0
            for cell in column_cells[:200]:
                value = "" if cell.value is None else str(cell.value)
                max_len = max(max_len, len(value))
            ws.column_dimensions[letter].width = min(max(max_len + 2, 12), 60)


def write_model_workbook(
    output_path: Path,
    predictions: pd.DataFrame,
    metrics: dict[str, Any],
    metadata: list[dict[str, Any]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_df = pd.DataFrame(
        [{"metric": key, "value": value} for key, value in metrics.items()]
    )
    metadata_df = pd.DataFrame(metadata)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        prepare_for_excel(predictions).to_excel(
            writer, sheet_name="Predictions", index=False
        )
        metrics_df.to_excel(writer, sheet_name="Metrics", index=False)
        metadata_df.to_excel(writer, sheet_name="Metadata", index=False)
        prompt_sheet().to_excel(writer, sheet_name="Prompt", index=False)
        format_workbook(writer)


def write_combined_workbook(
    output_path: Path,
    summary_rows: list[dict[str, Any]],
    all_predictions: list[pd.DataFrame],
    configuration_rows: list[dict[str, Any]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df = pd.DataFrame(summary_rows)
    predictions_df = (
        pd.concat(all_predictions, ignore_index=True) if all_predictions else pd.DataFrame()
    )
    config_df = pd.DataFrame(configuration_rows)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="ModelComparison", index=False)
        prepare_for_excel(predictions_df).to_excel(
            writer, sheet_name="AllPredictions", index=False
        )
        config_df.to_excel(writer, sheet_name="RunConfiguration", index=False)
        prompt_sheet().to_excel(writer, sheet_name="Prompt", index=False)
        format_workbook(writer)


def benchmark_model(
    loaded: LoadedModel,
    benchmark_df: pd.DataFrame,
    catalog: pd.DataFrame,
    args: argparse.Namespace,
) -> pd.DataFrame:
    records: list[dict[str, Any]] = []

    total = len(benchmark_df) * args.runs
    counter = 0

    for _, row in benchmark_df.iterrows():
        candidates = retrieve_candidate_pool(row, catalog, args.candidate_pool_size)
        candidate_ids = [canonical_uuid(c["process_uuid"]) for c in candidates]
        user_prompt = build_user_prompt(row, candidates)

        for run_number in range(1, args.runs + 1):
            counter += 1
            run_seed = SEED + run_number - 1
            set_reproducibility(run_seed)
            print(
                f"[{loaded.key}] {counter}/{total} | sample={row['sample_id']} | "
                f"run={run_number} | seed={run_seed}"
            )

            raw_text = ""
            generation_seconds: Any = ""
            parse_status = "generation_error"
            parsed: dict[str, Any] | None = None
            error_message = ""

            try:
                raw_text, generation_seconds = generate_response(
                    loaded,
                    user_prompt,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                )
                parsed, parse_status = extract_json(raw_text)
            except Exception as exc:
                error_message = f"{type(exc).__name__}: {exc}"

            prediction = validate_prediction(
                parsed,
                candidates,
                parse_status=parse_status,
                top_k=args.top_k,
            )
            evaluation = evaluate_record(
                row,
                candidates,
                prediction,
                top_k=args.top_k,
            )

            record = {
                "model_key": loaded.key,
                "model_name": loaded.display_name,
                "model_id": loaded.model_id,
                "sample_id": str(row["sample_id"]),
                "run_number": run_number,
                "run_seed": run_seed,
                "case_study": safe_value(row.get("case_study", "")),
                "material_description": str(row["material_description"]),
                "quantity": safe_value(row.get("quantity", "")),
                "unit": safe_value(row.get("unit", "")),
                "acceptable_proxy": safe_value(row.get("acceptable_proxy", "")),
                "review_required": as_bool(row.get("review_required", False)),
                "reviewer_notes": safe_value(row.get("reviewer_notes", "")),
                "source_location": safe_value(row.get("source_location", "")),
                "candidate_pool_size": len(candidates),
                "candidate_pool_uuids": candidate_ids,
                "candidate_pool_names": [c["process_name"] for c in candidates],
                "normalized_material": prediction["normalized_material"],
                "decision": prediction["decision"],
                "selected_process_uuid": prediction["selected_process_uuid"],
                "selected_process_name": prediction["selected_process_name"],
                "ranked_process_uuids": prediction["ranked_process_uuids"],
                "ranked_process_names": prediction["ranked_process_names"],
                "reported_confidence": prediction["confidence"],
                "uncertainty_reason": prediction["uncertainty_reason"],
                "parse_status": prediction["parse_status"],
                "generation_seconds": generation_seconds,
                "error_message": error_message,
                "raw_model_output": raw_text,
                **evaluation,
            }
            records.append(record)

    return pd.DataFrame(records)


def combine_existing_results(args: argparse.Namespace) -> None:
    """Combine the four per-model result workbooks without loading any LLM."""
    summary_rows: list[dict[str, Any]] = []
    all_predictions: list[pd.DataFrame] = []
    configuration_rows: list[dict[str, Any]] = []
    missing: list[str] = []

    for model_key in ["llama", "qwen", "deepseek", "mistral"]:
        path = args.output_root / model_key / "benchmark_results.xlsx"
        if not path.exists():
            missing.append(str(path))
            continue

        predictions = pd.read_excel(path, sheet_name="Predictions")
        metrics_df = pd.read_excel(path, sheet_name="Metrics")
        metadata_df = pd.read_excel(path, sheet_name="Metadata")
        metrics = dict(zip(metrics_df["metric"], metrics_df["value"]))
        meta = dict(zip(metadata_df["field"], metadata_df["value"]))

        all_predictions.append(predictions)
        summary_rows.append(
            {
                "model_key": model_key,
                "model_name": meta.get("model_display_name", MODEL_SPECS[model_key]["display_name"]),
                "model_id": meta.get("model_id", MODEL_SPECS[model_key]["model_id"]),
                "model_revision": meta.get("model_revision", ""),
                **metrics,
            }
        )
        configuration_rows.extend(
            [{"model_key": model_key, **row} for row in metadata_df.to_dict("records")]
        )

    if missing:
        raise FileNotFoundError(
            "Cannot combine results because these model workbooks are missing:\n  - "
            + "\n  - ".join(missing)
        )

    combined_path = args.output_root / "combined" / "four_model_comparison.xlsx"
    write_combined_workbook(
        combined_path,
        summary_rows=summary_rows,
        all_predictions=all_predictions,
        configuration_rows=configuration_rows,
    )
    print(f"Combined comparison saved: {combined_path.resolve()}")


def main() -> None:
    args = parse_args()

    if args.runs < 1:
        raise ValueError("--runs must be at least 1")
    if args.candidate_pool_size < 5:
        raise ValueError("--candidate-pool-size must be at least 5")
    if args.top_k < 1 or args.top_k > args.candidate_pool_size:
        raise ValueError("--top-k must be between 1 and candidate-pool-size")
    if args.temperature < 0:
        raise ValueError("--temperature cannot be negative")

    selected_keys = (
        ["llama", "qwen", "deepseek", "mistral"]
        if args.model == "all"
        else [args.model]
    )

    set_reproducibility(SEED)

    if args.combine_results:
        combine_existing_results(args)
        return

    print("Loading ELCD process catalog...")
    catalog = load_catalog(args.catalog)
    print(f"Catalog processes: {len(catalog):,}")

    print("Loading benchmark dataset...")
    benchmark_df = load_benchmark(args.benchmark, catalog)
    if args.limit is not None:
        benchmark_df = benchmark_df.head(args.limit).copy()
    print(f"Benchmark samples: {len(benchmark_df):,}")

    args.output_root.mkdir(parents=True, exist_ok=True)

    all_predictions: list[pd.DataFrame] = []
    summary_rows: list[dict[str, Any]] = []
    configuration_rows: list[dict[str, Any]] = []

    for model_key in selected_keys:
        loaded: LoadedModel | None = None
        model_output_dir = args.output_root / model_key
        model_output_path = model_output_dir / "benchmark_results.xlsx"

        try:
            print("\n" + "=" * 80)
            print(f"Loading {MODEL_SPECS[model_key]['display_name']}")
            print(MODEL_SPECS[model_key]["model_id"])
            print("=" * 80)

            loaded = load_model(model_key, use_4bit=not args.no_4bit)
            predictions = benchmark_model(
                loaded=loaded,
                benchmark_df=benchmark_df,
                catalog=catalog,
                args=args,
            )
            metrics = compute_metrics(predictions, args.runs)
            metadata = metadata_rows(loaded, args, status="completed")
            write_model_workbook(model_output_path, predictions, metrics, metadata)

            all_predictions.append(predictions)
            summary_rows.append(
                {
                    "model_key": model_key,
                    "model_name": loaded.display_name,
                    "model_id": loaded.model_id,
                    "model_revision": loaded.model_revision,
                    **metrics,
                }
            )
            configuration_rows.extend(
                [{"model_key": model_key, **row} for row in metadata]
            )

            print(f"Saved: {model_output_path}")

        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            print(f"ERROR for {model_key}: {error}", file=sys.stderr)
            failed_meta = metadata_rows(loaded, args, status="failed", error_message=error)
            configuration_rows.extend(
                [{"model_key": model_key, **row} for row in failed_meta]
            )
            summary_rows.append(
                {
                    "model_key": model_key,
                    "model_name": MODEL_SPECS[model_key]["display_name"],
                    "model_id": MODEL_SPECS[model_key]["model_id"],
                    "benchmark_status": "failed",
                    "error_message": error,
                }
            )

        finally:
            unload_model(loaded)

    print("\nBenchmark complete.")
    if args.model == "all":
        combined_path = args.output_root / "combined" / "four_model_comparison.xlsx"
        write_combined_workbook(
            combined_path,
            summary_rows=summary_rows,
            all_predictions=all_predictions,
            configuration_rows=configuration_rows,
        )
        print(f"Combined comparison: {combined_path.resolve()}")
    else:
        print(
            "After all four model runs finish, create the paper comparison workbook with:\n"
            "  python scripts/benchmark_four_llms.py --combine-results"
        )


if __name__ == "__main__":
    main()
