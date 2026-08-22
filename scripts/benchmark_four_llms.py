"""Controlled four-model benchmark for LLM-assisted openLCA process matching.

This experiment is intentionally aligned with the language-model role in the
paper. It evaluates:

1. material normalization;
2. deterministic character n-gram TF-IDF ELCD/openLCA candidate retrieval;
3. LLM ranking of supplied candidate processes;
4. final process selection or Review Required routing;
5. Direct / Proxy / Review Required classification; and
6. run-to-run repeatability.

The benchmark never asks an LLM to invent an emission factor, GWP value, EPD,
or process UUID. Every selectable process comes from the fixed exported catalog.

Run from any directory, for example:

    python scripts/benchmark_four_llms.py --model llama
    python scripts/benchmark_four_llms.py --model qwen
    python scripts/benchmark_four_llms.py --model deepseek
    python scripts/benchmark_four_llms.py --model mistral
    python scripts/benchmark_four_llms.py --combine-results

For a quick smoke test:

    python scripts/benchmark_four_llms.py --model llama --limit 2 --runs 1

Important
---------
The benchmark input must be a *frozen expert reference set*. Create it from the
reconciled human workbook before model scoring:

    python scripts/prepare_benchmark_reference.py

Then validate the complete benchmark inputs without loading a model:

    python scripts/benchmark_four_llms.py --check-inputs

The benchmark refuses to score unfinished or internally inconsistent labels.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import platform
import random
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
import torch
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score


SCRIPT_VERSION = "2.0.0"
DATABASE_LABEL = "ELCD 3.2"
SEED = 42
DEFAULT_RUNS = 5
DEFAULT_CANDIDATE_POOL_SIZE = 20
DEFAULT_TOP_K = 10
DEFAULT_MAX_NEW_TOKENS = 384
DEFAULT_TEMPERATURE = 0.0

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG_PATH = REPO_ROOT / "ELCD_Check" / "ELCD_Process_Catalog.xlsx"
DEFAULT_BENCHMARK_PATH = (
    REPO_ROOT / "Four_Models" / "Input" / "LLM_Model_Evaluation_Reference_Set.xlsx"
)
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "Four_Models" / "Output"

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

SYSTEM_PROMPT = """You are an LCA material-normalization and ELCD process-matching evaluator for A1-A3 screening.

Your task is deliberately limited to language interpretation and process matching.
You are NOT calculating embodied carbon and you are NOT generating environmental
factors. Use only the candidate processes supplied in the prompt.

Study definitions:
- direct: a selected ELCD process sufficiently represents the BOM material/product.
- proxy: an ELCD process is selected as a technically defensible substitute because
  an exact/direct representation is not available.
- review_required: no supplied ELCD candidate is usable enough to select. This is
  reserved for an unmatched material. Do NOT use review_required merely because a
  selected process is imperfect, geographically different, or requires judgment;
  if you select an ELCD substitute, classify it as proxy.

Rules:
1. Use ONLY process UUIDs that appear in the supplied candidate list.
2. Do NOT invent process UUIDs, emission factors, GWP values, EPDs, citations,
   or any environmental data.
3. Normalize the original BOM description into a concise engineering material name.
4. Rank the most defensible supplied candidates from best to worst, up to the
   requested top-k.
5. If at least one candidate is defensible, select exactly one supplied process and
   classify it as direct or proxy.
6. Use review_required only when no supplied candidate is defensible.
7. For review_required, selected_process_uuid and selected_process_name MUST both be
   empty strings.
8. The selected process must also appear in ranked_candidates.
9. Return JSON only, with no Markdown and no text outside the JSON object.

Required JSON schema:
{
  "normalized_material": "string",
  "ranked_candidates": [
    {
      "process_uuid": "string",
      "process_name": "string",
      "confidence": 0.0,
      "rationale": "short string"
    }
  ],
  "selected_process_uuid": "string or empty",
  "selected_process_name": "string or empty",
  "match_type": "direct or proxy or review_required",
  "selection_confidence": 0.0,
  "uncertainty_reason": "short string"
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
    "ground_truth_match_type": (
        "ground_truth_match_type",
        "reference_match_type",
        "match_type",
        "final_decision",
        "final decision",
    ),
    "ground_truth_unresolved": (
        "ground_truth_unresolved",
        "reference_unresolved",
        "expected_unresolved",
        "unresolved",
    ),
    "reference_status": (
        "reference_status",
        "ground_truth_status",
        "reference status",
    ),
    "case_study": ("case_study", "case study"),
    "reviewer_notes": ("reviewer_notes", "reviewer notes", "notes"),
    "source_location": ("source_location", "source location"),
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


@dataclass
class CatalogRetriever:
    """Deterministic model-independent candidate retriever.

    Character n-gram TF-IDF is used because BOM descriptions and process names
    often differ in word form, abbreviations, or descriptive suffixes. The
    retriever is fit only on the exported catalog text and never on expert labels.
    """

    vectorizer: Any
    matrix: Any


def package_version(name: str) -> str:
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return "not-installed"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9.%+\-/ ]", "", text)
    return text.strip()


def canonical_uuid(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return str(value).strip().lower()


def safe_value(value: Any) -> Any:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return value


def optional_bool(value: Any) -> bool | None:
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "unresolved", "review required", "review_required"}:
        return True
    if text in {"0", "false", "no", "n", "resolved", "matched"}:
        return False
    if text == "":
        return None
    raise ValueError(f"Cannot interpret boolean value: {value!r}")


def canonical_match_type(value: Any) -> str:
    text = normalize_text(value).replace("-", " ").replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if text in {"direct", "direct match", "exact", "exact match"}:
        return "direct"
    if text in {"proxy", "proxy match", "documented proxy"}:
        return "proxy"
    if text in {
        "review required",
        "reviewrequired",
        "review",
        "unresolved",
        "no match",
        "no defensible match",
    }:
        return "review_required"
    return ""


def canonical_reference_status(value: Any) -> str:
    text = normalize_text(value).replace("-", " ").replace("_", " ")
    if text in {"final", "frozen", "complete", "completed", "ready", "approved"}:
        return "FINAL"
    if text in {"pending", "pending reconciliation", "pendingreconciliation", "draft", "in progress", "incomplete"}:
        return "PENDING_RECONCILIATION"
    return str(value).strip().upper() if str(value).strip() else ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark four LLMs for material normalization and ELCD/openLCA process matching."
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
        help="Model to benchmark. 'all' runs the four models sequentially.",
    )
    parser.add_argument(
        "--combine-results",
        action="store_true",
        help="Combine existing per-model benchmark_results.xlsx files without loading an LLM.",
    )
    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help="Validate the ELCD catalog and frozen reference set, print diagnostics, and exit without loading an LLM.",
    )
    parser.add_argument(
        "--no-4bit",
        action="store_true",
        help="Disable 4-bit NF4 quantization.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for a smoke test.",
    )
    return parser.parse_args()


def set_reproducibility(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True


def load_catalog(path: Path) -> pd.DataFrame:
    path = path.expanduser().resolve()
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
        catalog[col] = catalog[col].fillna("").astype(str).str.strip()

    catalog = catalog[catalog["process_uuid"].ne("") & catalog["process_name"].ne("")].copy()
    if catalog["process_uuid"].duplicated().any():
        dupes = catalog.loc[catalog["process_uuid"].duplicated(), "process_uuid"].head(5).tolist()
        raise ValueError(f"Catalog contains duplicate process UUIDs, e.g. {dupes}")

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
    """Load and strictly validate the frozen expert reference set.

    Pending expert rows are rejected. An unfinished row is never silently
    converted to Review Required/unresolved.
    """
    path = path.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(
            f"Benchmark workbook not found: {path}\n"
            "Use scripts/prepare_benchmark_reference.py after expert reconciliation."
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
        raise ValueError("Benchmark workbook must contain a material_description column.")
    if "sample_id" not in df.columns:
        df["sample_id"] = [f"S{i:04d}" for i in range(1, len(df) + 1)]

    for optional in [
        "quantity",
        "unit",
        "ground_truth_normalized_material",
        "ground_truth_process_uuid",
        "ground_truth_process_name",
        "ground_truth_match_type",
        "ground_truth_unresolved",
        "reference_status",
        "case_study",
        "reviewer_notes",
        "source_location",
    ]:
        if optional not in df.columns:
            df[optional] = ""

    df["sample_id"] = df["sample_id"].fillna("").astype(str).str.strip()
    if df["sample_id"].eq("").any():
        raise ValueError("Every benchmark row must have a nonblank sample_id.")
    if df["sample_id"].duplicated().any():
        dupes = df.loc[df["sample_id"].duplicated(), "sample_id"].tolist()
        raise ValueError(f"Duplicate sample_id values in benchmark workbook: {dupes}")

    df["material_description"] = df["material_description"].fillna("").astype(str).str.strip()
    df["ground_truth_normalized_material"] = (
        df["ground_truth_normalized_material"].fillna("").astype(str).str.strip()
    )
    df["ground_truth_process_uuid"] = df["ground_truth_process_uuid"].map(canonical_uuid)
    df["ground_truth_process_name"] = (
        df["ground_truth_process_name"].fillna("").astype(str).str.strip()
    )
    df["ground_truth_match_type"] = df["ground_truth_match_type"].map(canonical_match_type)
    df["reference_status"] = df["reference_status"].map(canonical_reference_status)

    pending = df[df["reference_status"].ne("FINAL")]
    if not pending.empty:
        ids = ", ".join(pending["sample_id"].head(12).tolist())
        more = " ..." if len(pending) > 12 else ""
        raise ValueError(
            "Benchmark reference set is not frozen. "
            f"{len(pending)} row(s) are not reference_status=FINAL: {ids}{more}.\n"
            "Complete Expert A/B reconciliation first, then run:\n"
            "  python scripts/prepare_benchmark_reference.py\n"
            "Do not mark unfinished rows as unresolved merely to make the benchmark run."
        )

    uuid_to_name = dict(zip(catalog["_uuid_key"], catalog["process_name"]))
    name_to_uuid = dict(zip(catalog["_name_key"], catalog["_uuid_key"]))

    unresolved_values: list[bool] = []
    validation_errors: list[str] = []

    for idx, row in df.iterrows():
        sid = row["sample_id"]
        gt_norm = str(row["ground_truth_normalized_material"]).strip()
        gt_name = str(row["ground_truth_process_name"]).strip()
        gt_uuid = canonical_uuid(row["ground_truth_process_uuid"])
        match_type = canonical_match_type(row["ground_truth_match_type"])
        explicit_unresolved = optional_bool(row["ground_truth_unresolved"])

        if not gt_norm:
            validation_errors.append(f"{sid}: missing ground_truth_normalized_material")

        if match_type == "review_required":
            unresolved = True
        elif match_type in {"direct", "proxy"}:
            unresolved = False
        elif explicit_unresolved is not None:
            unresolved = explicit_unresolved
            match_type = "review_required" if unresolved else ""
        else:
            validation_errors.append(
                f"{sid}: missing/invalid ground_truth_match_type (Direct, Proxy, or Review Required)"
            )
            unresolved = False

        if not match_type:
            validation_errors.append(
                f"{sid}: ground_truth_match_type is required for final scoring"
            )

        if unresolved:
            if gt_uuid or gt_name:
                validation_errors.append(
                    f"{sid}: Review Required rows must not contain a final process UUID/name"
                )
        else:
            if not gt_uuid and gt_name:
                matched_uuid = name_to_uuid.get(normalize_text(gt_name), "")
                if matched_uuid:
                    gt_uuid = matched_uuid
                    df.at[idx, "ground_truth_process_uuid"] = matched_uuid
            if gt_uuid and not gt_name:
                matched_name = uuid_to_name.get(gt_uuid, "")
                if matched_name:
                    gt_name = matched_name
                    df.at[idx, "ground_truth_process_name"] = matched_name
            if not gt_uuid:
                validation_errors.append(
                    f"{sid}: matched row does not resolve to an exact catalog process UUID"
                )
            elif gt_uuid not in uuid_to_name:
                validation_errors.append(
                    f"{sid}: ground_truth_process_uuid is not present in the exported catalog"
                )
            elif gt_name and normalize_text(uuid_to_name[gt_uuid]) != normalize_text(gt_name):
                validation_errors.append(
                    f"{sid}: process name does not match the catalog name for its UUID"
                )

        df.at[idx, "ground_truth_match_type"] = match_type
        unresolved_values.append(bool(unresolved))

    if validation_errors:
        shown = "\n  - ".join(validation_errors[:20])
        extra = f"\n  ... plus {len(validation_errors) - 20} more" if len(validation_errors) > 20 else ""
        raise ValueError("Invalid frozen benchmark reference set:\n  - " + shown + extra)

    df["ground_truth_unresolved"] = unresolved_values
    return df.reset_index(drop=True)


def build_catalog_retriever(catalog: pd.DataFrame) -> CatalogRetriever:
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        lowercase=False,
        sublinear_tf=True,
        norm="l2",
    )
    matrix = vectorizer.fit_transform(catalog["_search_text"].tolist())
    return CatalogRetriever(vectorizer=vectorizer, matrix=matrix)


def retrieve_candidate_pool(
    row: pd.Series,
    catalog: pd.DataFrame,
    retriever: CatalogRetriever,
    pool_size: int,
) -> list[dict[str, Any]]:
    """Deterministic candidate retrieval identical for all four models.

    The query uses only the original BOM description. Human normalized material
    and reference process labels are never used for retrieval.
    """
    description = str(row.get("material_description", "")).strip()
    query = normalize_text(description)
    query_vector = retriever.vectorizer.transform([query])
    scores = (retriever.matrix @ query_vector.T).toarray().ravel()

    ranked_indices = sorted(
        range(len(catalog)),
        key=lambda i: (
            -float(scores[i]),
            str(catalog.iloc[i]["process_name"]).lower(),
            canonical_uuid(catalog.iloc[i]["process_uuid"]),
        ),
    )[: min(pool_size, len(catalog))]

    candidates: list[dict[str, Any]] = []
    for index in ranked_indices:
        process_row = catalog.iloc[index]
        candidates.append(
            {
                "process_uuid": process_row["process_uuid"],
                "process_name": process_row["process_name"],
                "category": process_row.get("category", ""),
                "location": process_row.get("location", ""),
                "process_type": process_row.get("process_type", ""),
                "retrieval_score": round(float(scores[index]), 6),
            }
        )
    return candidates


def build_user_prompt(
    row: pd.Series,
    candidates: list[dict[str, Any]],
    top_k: int,
) -> str:
    material_payload = {
        "sample_id": str(row.get("sample_id", "")),
        "material_description": str(row.get("material_description", "")),
        "quantity": safe_value(row.get("quantity", "")),
        "unit": safe_value(row.get("unit", "")),
    }
    payload = {
        "requested_top_k": top_k,
        "material": material_payload,
        "candidate_processes": candidates,
    }
    return (
        "Evaluate the material below using only the supplied candidate processes. "
        "Return exactly the required JSON object.\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def load_model(model_key: str, use_4bit: bool) -> LoadedModel:
    # Imported lazily so repository unit tests can exercise benchmark logic without
    # requiring the heavyweight inference dependencies.
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

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
                "4-bit benchmark mode requires a CUDA GPU. Use a Colab GPU runtime "
                "or pass --no-4bit for CPU/full-precision execution."
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
        model_kwargs["torch_dtype"] = torch.float16 if torch.cuda.is_available() else torch.float32

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
        try:
            torch.cuda.ipc_collect()
        except Exception:
            pass


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
    # A single user-role message keeps prompt content equivalent across model
    # families, including checkpoints that do not use a separate system role.
    messages = [{"role": "user", "content": SYSTEM_PROMPT + "\n\n" + user_prompt}]

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
            {"do_sample": True, "temperature": temperature, "top_p": 1.0}
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

    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
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
    """Validate model JSON without altering the model's returned ranking."""
    valid_by_uuid = {
        canonical_uuid(c["process_uuid"]): c for c in candidates if c.get("process_uuid")
    }

    if parsed is None:
        return {
            "parse_status": parse_status,
            "valid_response": False,
            "normalized_material": "",
            "match_type": "",
            "decision": "invalid",
            "selected_process_uuid": "",
            "selected_process_name": "",
            "ranked_process_uuids": [],
            "ranked_process_names": [],
            "selection_confidence": "",
            "uncertainty_reason": "",
        }

    status = parse_status
    normalized_material = str(parsed.get("normalized_material", "")).strip()
    match_type = canonical_match_type(parsed.get("match_type", ""))
    if not match_type:
        status = "invalid_match_type"

    ranked = parsed.get("ranked_candidates", [])
    if not isinstance(ranked, list):
        ranked = []
        status = "invalid_ranked_candidates"

    valid_ranked_uuids: list[str] = []
    valid_ranked_names: list[str] = []
    for item in ranked:
        if not isinstance(item, dict):
            continue
        uid = canonical_uuid(item.get("process_uuid", ""))
        if uid in valid_by_uuid and uid not in valid_ranked_uuids:
            valid_ranked_uuids.append(uid)
            valid_ranked_names.append(valid_by_uuid[uid]["process_name"])
        if len(valid_ranked_uuids) >= top_k:
            break

    selected_uuid = canonical_uuid(parsed.get("selected_process_uuid", ""))
    selected_name = ""

    if match_type == "review_required":
        if selected_uuid:
            status = "review_required_with_selected_process"
            selected_uuid = ""
    elif match_type in {"direct", "proxy"}:
        if selected_uuid not in valid_by_uuid:
            status = "invalid_selected_candidate"
            selected_uuid = ""
        else:
            selected_name = valid_by_uuid[selected_uuid]["process_name"]
            # Important: do not insert the selected process into the returned ranking.
            # Ranking metrics must reflect exactly what the model ranked.
            if selected_uuid not in valid_ranked_uuids:
                status = "selected_process_not_in_ranked_candidates"

    decision = (
        "unresolved"
        if match_type == "review_required"
        else "matched"
        if match_type in {"direct", "proxy"}
        else "invalid"
    )

    valid_response = status == "ok"
    return {
        "parse_status": status,
        "valid_response": valid_response,
        "normalized_material": normalized_material,
        "match_type": match_type,
        "decision": decision,
        "selected_process_uuid": selected_uuid,
        "selected_process_name": selected_name,
        "ranked_process_uuids": valid_ranked_uuids,
        "ranked_process_names": valid_ranked_names,
        "selection_confidence": safe_value(parsed.get("selection_confidence", "")),
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
    gt_match_type = canonical_match_type(row.get("ground_truth_match_type", ""))
    gt_unresolved = bool(row.get("ground_truth_unresolved", False))

    pool_uuids = [canonical_uuid(c.get("process_uuid", "")) for c in candidates]
    ranked = prediction["ranked_process_uuids"]
    selected = prediction["selected_process_uuid"]
    valid = bool(prediction["valid_response"])
    predicted_unresolved = prediction["match_type"] == "review_required"

    if gt_unresolved:
        candidate_pool_contains_gt: Any = ""
        top1_correct: Any = ""
        top3_correct: Any = ""
        top5_correct: Any = ""
        top10_correct: Any = ""
        topk_correct: Any = ""
        reciprocal_rank: Any = ""
        process_selection_correct: Any = ""
        conditional_selection_correct: Any = ""
        end_to_end_correct = valid and predicted_unresolved
    else:
        candidate_pool_contains_gt = bool(gt_uuid and gt_uuid in pool_uuids)
        top1_correct = bool(valid and gt_uuid and gt_uuid in ranked[:1])
        top3_correct = bool(valid and gt_uuid and gt_uuid in ranked[:3])
        top5_correct = bool(valid and gt_uuid and gt_uuid in ranked[:5])
        top10_correct = bool(valid and gt_uuid and gt_uuid in ranked[:10])
        topk_correct = bool(valid and gt_uuid and gt_uuid in ranked[:top_k])
        if valid and gt_uuid in ranked:
            reciprocal_rank = 1.0 / (ranked.index(gt_uuid) + 1)
        else:
            reciprocal_rank = 0.0
        process_selection_correct = bool(valid and gt_uuid and selected == gt_uuid)
        conditional_selection_correct = (
            process_selection_correct if candidate_pool_contains_gt else ""
        )
        end_to_end_correct = process_selection_correct

    normalization_exact: Any = ""
    normalization_similarity: Any = ""
    if gt_norm:
        normalization_exact = bool(
            valid
            and normalize_text(prediction["normalized_material"]) == normalize_text(gt_norm)
        )
        normalization_similarity = round(
            (
                fuzz.ratio(
                    normalize_text(prediction["normalized_material"]),
                    normalize_text(gt_norm),
                )
                / 100.0
            )
            if valid
            else 0.0,
            4,
        )

    return {
        "ground_truth_process_uuid": gt_uuid,
        "ground_truth_process_name": gt_name,
        "ground_truth_normalized_material": gt_norm,
        "ground_truth_match_type": gt_match_type,
        "ground_truth_unresolved": gt_unresolved,
        "candidate_pool_contains_ground_truth": candidate_pool_contains_gt,
        "normalization_exact": normalization_exact,
        "normalization_similarity": normalization_similarity,
        "top1_ranking_correct": top1_correct,
        "top3_ranking_correct": top3_correct,
        "top5_ranking_correct": top5_correct,
        "top10_ranking_correct": top10_correct,
        "configured_top_k_ranking_correct": topk_correct,
        "reciprocal_rank": reciprocal_rank,
        "process_selection_correct": process_selection_correct,
        "conditional_process_selection_correct": conditional_selection_correct,
        "match_type_correct": bool(valid and prediction["match_type"] == gt_match_type),
        "review_required_binary_correct": bool(
            valid and predicted_unresolved == gt_unresolved
        ),
        "unresolved_routing_correct": (
            bool(valid and predicted_unresolved) if gt_unresolved else ""
        ),
        "end_to_end_reference_correct": bool(end_to_end_correct),
    }


def bool_mean(series: pd.Series) -> float | None:
    vals = [x for x in series.tolist() if isinstance(x, (bool, np.bool_))]
    if not vals:
        return None
    return float(np.mean(vals))


def numeric_mean(series: pd.Series) -> float | None:
    vals = pd.to_numeric(series, errors="coerce").dropna()
    return float(vals.mean()) if len(vals) else None


def compute_metrics(predictions: pd.DataFrame, runs: int) -> dict[str, Any]:
    unique_reference = predictions.drop_duplicates("sample_id")
    metrics: dict[str, Any] = {
        "n_samples": int(predictions["sample_id"].nunique()),
        "n_runs_per_sample": runs,
        "n_prediction_rows": int(len(predictions)),
        "n_direct_reference_samples": int((unique_reference["ground_truth_match_type"] == "direct").sum()),
        "n_proxy_reference_samples": int((unique_reference["ground_truth_match_type"] == "proxy").sum()),
        "n_review_required_reference_samples": int((unique_reference["ground_truth_match_type"] == "review_required").sum()),
    }

    metrics["valid_response_rate"] = bool_mean(predictions["valid_response"])
    metrics["failed_response_rate"] = float((~predictions["valid_response"].astype(bool)).mean())
    metrics["normalization_exact_accuracy"] = bool_mean(predictions["normalization_exact"])
    metrics["mean_normalization_similarity"] = numeric_mean(predictions["normalization_similarity"])

    metrics["candidate_pool_recall"] = bool_mean(
        predictions["candidate_pool_contains_ground_truth"]
    )
    metrics["top1_ranking_accuracy"] = bool_mean(predictions["top1_ranking_correct"])
    metrics["top3_ranking_recall"] = bool_mean(predictions["top3_ranking_correct"])
    metrics["top5_ranking_recall"] = bool_mean(predictions["top5_ranking_correct"])
    metrics["top10_ranking_recall"] = bool_mean(predictions["top10_ranking_correct"])
    metrics["configured_top_k_ranking_recall"] = bool_mean(
        predictions["configured_top_k_ranking_correct"]
    )
    metrics["mean_reciprocal_rank"] = numeric_mean(predictions["reciprocal_rank"])
    metrics["final_process_selection_accuracy_matched_rows"] = bool_mean(
        predictions["process_selection_correct"]
    )
    metrics["conditional_process_selection_accuracy"] = bool_mean(
        predictions["conditional_process_selection_correct"]
    )
    metrics["match_type_accuracy"] = bool_mean(predictions["match_type_correct"])
    metrics["review_required_binary_accuracy"] = bool_mean(
        predictions["review_required_binary_correct"]
    )

    valid_rows = predictions[predictions["valid_response"].astype(bool)].copy()
    if len(valid_rows):
        y_true_review = valid_rows["ground_truth_unresolved"].astype(bool).to_numpy()
        y_pred_review = (valid_rows["match_type"].astype(str) == "review_required").to_numpy()
        tp = int(((y_true_review == True) & (y_pred_review == True)).sum())
        fp = int(((y_true_review == False) & (y_pred_review == True)).sum())
        fn = int(((y_true_review == True) & (y_pred_review == False)).sum())
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        metrics["review_required_precision"] = float(precision)
        metrics["review_required_recall"] = float(recall)
        metrics["review_required_f1"] = float(f1)
    else:
        metrics["review_required_precision"] = None
        metrics["review_required_recall"] = None
        metrics["review_required_f1"] = None

    matched_mask = ~predictions["ground_truth_unresolved"].astype(bool)
    metrics["direct_proxy_match_type_accuracy_matched_rows"] = bool_mean(
        predictions.loc[matched_mask, "match_type_correct"]
    )
    metrics["unresolved_routing_accuracy"] = bool_mean(
        predictions["unresolved_routing_correct"]
    )
    metrics["end_to_end_reference_accuracy"] = bool_mean(
        predictions["end_to_end_reference_correct"]
    )

    durations = pd.to_numeric(predictions["generation_seconds"], errors="coerce").dropna()
    metrics["mean_generation_seconds"] = float(durations.mean()) if len(durations) else None
    metrics["median_generation_seconds"] = float(durations.median()) if len(durations) else None

    y_true: list[str] = []
    y_pred: list[str] = []
    for _, row in predictions.iterrows():
        true_label = (
            "__REVIEW_REQUIRED__"
            if bool(row["ground_truth_unresolved"])
            else canonical_uuid(row["ground_truth_process_uuid"])
        )
        if not bool(row["valid_response"]):
            pred_label = "__INVALID__"
        elif str(row["match_type"]) == "review_required":
            pred_label = "__REVIEW_REQUIRED__"
        else:
            pred_label = canonical_uuid(row["selected_process_uuid"]) or "__INVALID__"
        if true_label:
            y_true.append(true_label)
            y_pred.append(pred_label)

    metrics["macro_f1_final_reference"] = (
        float(f1_score(y_true, y_pred, average="macro", zero_division=0)) if y_true else None
    )

    selection_agreement: list[bool] = []
    normalization_agreement: list[bool] = []
    match_type_agreement: list[bool] = []

    for _, group in predictions.groupby("sample_id", sort=False):
        if not group["valid_response"].astype(bool).all():
            selection_agreement.append(False)
            normalization_agreement.append(False)
            match_type_agreement.append(False)
            continue

        labels = [
            "__REVIEW_REQUIRED__"
            if str(mt) == "review_required"
            else canonical_uuid(uid)
            for mt, uid in zip(group["match_type"], group["selected_process_uuid"])
        ]
        selection_agreement.append(len(set(labels)) == 1)

        norms = [normalize_text(v) for v in group["normalized_material"].tolist()]
        normalization_agreement.append(len(set(norms)) == 1)

        match_types = [str(v) for v in group["match_type"].tolist()]
        match_type_agreement.append(len(set(match_types)) == 1)

    metrics["run_to_run_selection_agreement"] = (
        float(np.mean(selection_agreement)) if selection_agreement else None
    )
    metrics["run_to_run_normalization_agreement"] = (
        float(np.mean(normalization_agreement)) if normalization_agreement else None
    )
    metrics["run_to_run_match_type_agreement"] = (
        float(np.mean(match_type_agreement)) if match_type_agreement else None
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
        ("retrieval_method", "character n-gram TF-IDF"),
        ("retrieval_analyzer", "char_wb"),
        ("retrieval_ngram_range", "3-5"),
        ("retrieval_query_source", "original BOM description only"),
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
        ("catalog_path", str(Path(args.catalog).expanduser().resolve())),
        ("catalog_sha256", sha256_file(Path(args.catalog).expanduser().resolve())),
        ("benchmark_path", str(Path(args.benchmark).expanduser().resolve())),
        ("benchmark_sha256", sha256_file(Path(args.benchmark).expanduser().resolve())),
        ("system_prompt_sha256", hashlib.sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest()),
    ]
    return [{"field": field, "value": value} for field, value in values]


def prompt_sheet() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"prompt_part": "system_prompt", "text": SYSTEM_PROMPT},
            {
                "prompt_part": "user_prompt_template",
                "text": (
                    "Evaluate the material below using only the supplied candidate processes. "
                    "The runtime payload contains sample_id, material_description, quantity, "
                    "unit, requested_top_k, and the deterministic candidate list."
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
    metrics_df = pd.DataFrame([{"metric": key, "value": value} for key, value in metrics.items()])
    metadata_df = pd.DataFrame(metadata)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        prepare_for_excel(predictions).to_excel(writer, sheet_name="Predictions", index=False)
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
    predictions_df = pd.concat(all_predictions, ignore_index=True) if all_predictions else pd.DataFrame()
    config_df = pd.DataFrame(configuration_rows)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="ModelComparison", index=False)
        prepare_for_excel(predictions_df).to_excel(writer, sheet_name="AllPredictions", index=False)
        config_df.to_excel(writer, sheet_name="RunConfiguration", index=False)
        prompt_sheet().to_excel(writer, sheet_name="Prompt", index=False)
        format_workbook(writer)


def benchmark_model(
    loaded: LoadedModel,
    benchmark_df: pd.DataFrame,
    catalog: pd.DataFrame,
    retriever: CatalogRetriever,
    args: argparse.Namespace,
) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    total = len(benchmark_df) * args.runs
    counter = 0

    for _, row in benchmark_df.iterrows():
        candidates = retrieve_candidate_pool(
            row, catalog, retriever, args.candidate_pool_size
        )
        candidate_ids = [canonical_uuid(c["process_uuid"]) for c in candidates]
        user_prompt = build_user_prompt(row, candidates, args.top_k)

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
            evaluation = evaluate_record(row, candidates, prediction, top_k=args.top_k)

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
                "reviewer_notes": safe_value(row.get("reviewer_notes", "")),
                "source_location": safe_value(row.get("source_location", "")),
                "candidate_pool_size": len(candidates),
                "candidate_pool_uuids": candidate_ids,
                "candidate_pool_names": [c["process_name"] for c in candidates],
                "normalized_material": prediction["normalized_material"],
                "match_type": prediction["match_type"],
                "decision": prediction["decision"],
                "selected_process_uuid": prediction["selected_process_uuid"],
                "selected_process_name": prediction["selected_process_name"],
                "ranked_process_uuids": prediction["ranked_process_uuids"],
                "ranked_process_names": prediction["ranked_process_names"],
                "selection_confidence": prediction["selection_confidence"],
                "uncertainty_reason": prediction["uncertainty_reason"],
                "parse_status": prediction["parse_status"],
                "valid_response": prediction["valid_response"],
                "generation_seconds": generation_seconds,
                "error_message": error_message,
                "raw_model_output": raw_text,
                **evaluation,
            }
            records.append(record)

    return pd.DataFrame(records)


def combine_existing_results(args: argparse.Namespace) -> None:
    summary_rows: list[dict[str, Any]] = []
    all_predictions: list[pd.DataFrame] = []
    configuration_rows: list[dict[str, Any]] = []
    missing: list[str] = []

    for model_key in ["llama", "qwen", "deepseek", "mistral"]:
        path = Path(args.output_root) / model_key / "benchmark_results.xlsx"
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

    combined_path = Path(args.output_root) / "combined" / "four_model_comparison.xlsx"
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

    args.catalog = Path(args.catalog).expanduser().resolve()
    args.benchmark = Path(args.benchmark).expanduser().resolve()
    args.output_root = Path(args.output_root).expanduser().resolve()

    set_reproducibility(SEED)

    if args.combine_results:
        combine_existing_results(args)
        return

    print("Loading ELCD process catalog...")
    catalog = load_catalog(args.catalog)
    retriever = build_catalog_retriever(catalog)
    print(f"Catalog processes: {len(catalog):,}")
    print("Candidate retrieval: character n-gram TF-IDF (3-5), original BOM text only")

    print("Loading frozen benchmark reference set...")
    benchmark_df = load_benchmark(args.benchmark, catalog)

    if args.check_inputs:
        matched = benchmark_df[~benchmark_df["ground_truth_unresolved"].astype(bool)].copy()
        unresolved = benchmark_df[benchmark_df["ground_truth_unresolved"].astype(bool)].copy()
        retrieval_hits = 0
        for _, row in matched.iterrows():
            pool = retrieve_candidate_pool(
                row, catalog, retriever, args.candidate_pool_size
            )
            pool_ids = {canonical_uuid(c["process_uuid"]) for c in pool}
            if canonical_uuid(row["ground_truth_process_uuid"]) in pool_ids:
                retrieval_hits += 1
        print("Input validation passed.")
        print(f"Reference rows: {len(benchmark_df)}")
        print(f"Matched Direct/Proxy rows: {len(matched)}")
        print(f"Review Required rows: {len(unresolved)}")
        print(
            f"Deterministic candidate-pool recall at pool_size={args.candidate_pool_size}: "
            f"{retrieval_hits}/{len(matched)} "
            f"({(retrieval_hits / len(matched)) if len(matched) else 0:.1%})"
        )
        return

    if args.limit is not None:
        if args.limit < 1:
            raise ValueError("--limit must be at least 1")
        benchmark_df = benchmark_df.head(args.limit).copy()
    print(f"Benchmark samples: {len(benchmark_df):,}")

    args.output_root.mkdir(parents=True, exist_ok=True)
    selected_keys = (
        ["llama", "qwen", "deepseek", "mistral"] if args.model == "all" else [args.model]
    )

    all_predictions: list[pd.DataFrame] = []
    summary_rows: list[dict[str, Any]] = []
    configuration_rows: list[dict[str, Any]] = []

    for model_key in selected_keys:
        loaded: LoadedModel | None = None
        model_output_path = args.output_root / model_key / "benchmark_results.xlsx"
        try:
            print("\n" + "=" * 80)
            print(f"Loading {MODEL_SPECS[model_key]['display_name']}")
            print(MODEL_SPECS[model_key]["model_id"])
            print("=" * 80)

            loaded = load_model(model_key, use_4bit=not args.no_4bit)
            predictions = benchmark_model(
                loaded, benchmark_df, catalog, retriever, args
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
