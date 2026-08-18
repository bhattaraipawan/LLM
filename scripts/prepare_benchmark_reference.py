"""Freeze the reconciled expert labels into the four-model benchmark input.

This script intentionally refuses to create a final benchmark reference set
until every reconciliation row is complete and internally consistent.

Workflow:
    1. Experts complete the Expert_A and Expert_B sheets independently.
    2. Disagreements are resolved in the Reconciliation sheet.
    3. Run this script.
    4. Run scripts/benchmark_four_llms.py.

Default output:
    Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERT_WORKBOOK = (
    REPO_ROOT
    / "ELCD_Check"
    / "expert_reference"
    / "LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"
)
DEFAULT_CATALOG = REPO_ROOT / "ELCD_Check" / "ELCD_Process_Catalog.xlsx"
DEFAULT_OUTPUT = (
    REPO_ROOT / "Four_Models" / "Input" / "LLM_Model_Evaluation_Reference_Set.xlsx"
)
EXPECTED_ROWS = 35


def clean(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def key(value: Any) -> str:
    return " ".join(clean(value).lower().replace("_", " ").replace("-", " ").split())


def canonical_decision(value: Any) -> str:
    text = key(value)
    if text in {"direct", "direct match", "exact", "exact match"}:
        return "Direct"
    if text in {"proxy", "proxy match", "documented proxy"}:
        return "Proxy"
    if text in {
        "review required",
        "review",
        "unresolved",
        "no match",
        "no defensible match",
    }:
        return "Review Required"
    return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate expert reconciliation and freeze the benchmark reference workbook."
    )
    parser.add_argument("--expert-workbook", type=Path, default=DEFAULT_EXPERT_WORKBOOK)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_base_rows(expert_path: Path) -> pd.DataFrame:
    base = pd.read_excel(expert_path, sheet_name="Expert_A", header=6)
    base = base.rename(
        columns={
            "ID": "sample_id",
            "Case Study": "case_study",
            "Original BOM Description": "material_description",
            "Qty.": "quantity",
            "Unit": "unit",
        }
    )
    required = ["sample_id", "case_study", "material_description", "quantity", "unit"]
    missing = [c for c in required if c not in base.columns]
    if missing:
        raise ValueError(f"Expert_A sheet is missing columns: {missing}")
    base = base[required].copy()
    base = base[base["sample_id"].notna()].copy()
    base["sample_id"] = base["sample_id"].map(clean)
    return base.reset_index(drop=True)


def load_reconciliation(expert_path: Path) -> pd.DataFrame:
    rec = pd.read_excel(expert_path, sheet_name="Reconciliation", header=5)
    rec = rec.rename(
        columns={
            "ID": "sample_id",
            "Original BOM Description": "reconciliation_description",
            "Final Normalized Material": "ground_truth_normalized_material",
            "Final Reference Process": "ground_truth_process_name",
            "Final Process UUID (auto)": "ground_truth_process_uuid",
            "Final Decision": "ground_truth_match_type",
            "Notes": "reviewer_notes",
        }
    )
    required = [
        "sample_id",
        "reconciliation_description",
        "ground_truth_normalized_material",
        "ground_truth_process_name",
        "ground_truth_process_uuid",
        "ground_truth_match_type",
        "reviewer_notes",
    ]
    missing = [c for c in required if c not in rec.columns]
    if missing:
        raise ValueError(f"Reconciliation sheet is missing columns: {missing}")
    rec = rec[required].copy()
    rec = rec[rec["sample_id"].notna()].copy()
    rec["sample_id"] = rec["sample_id"].map(clean)
    return rec.reset_index(drop=True)


def load_catalog(catalog_path: Path) -> pd.DataFrame:
    catalog = pd.read_excel(catalog_path, sheet_name="Processes")
    required = ["process_uuid", "process_name"]
    missing = [c for c in required if c not in catalog.columns]
    if missing:
        raise ValueError(f"Catalog is missing columns: {missing}")
    catalog = catalog[required].copy()
    catalog["process_uuid"] = catalog["process_uuid"].map(clean)
    catalog["process_name"] = catalog["process_name"].map(clean)
    catalog = catalog[
        catalog["process_uuid"].ne("") & catalog["process_name"].ne("")
    ].copy()
    return catalog.reset_index(drop=True)


def validate_and_build(
    base: pd.DataFrame,
    rec: pd.DataFrame,
    catalog: pd.DataFrame,
    source_path: Path,
) -> pd.DataFrame:
    if len(base) != EXPECTED_ROWS:
        raise ValueError(f"Expected {EXPECTED_ROWS} BOM rows in Expert_A; found {len(base)}")
    if len(rec) != EXPECTED_ROWS:
        raise ValueError(f"Expected {EXPECTED_ROWS} reconciliation rows; found {len(rec)}")
    if base["sample_id"].duplicated().any() or rec["sample_id"].duplicated().any():
        raise ValueError("Duplicate sample IDs found in the expert workbook.")

    merged = base.merge(rec, on="sample_id", how="left", validate="one_to_one")
    if merged["reconciliation_description"].isna().any():
        missing_ids = merged.loc[
            merged["reconciliation_description"].isna(), "sample_id"
        ].tolist()
        raise ValueError(f"Reconciliation is missing sample IDs: {missing_ids}")

    name_to_uuid = {
        key(name): uuid for name, uuid in zip(catalog["process_name"], catalog["process_uuid"])
    }
    uuid_to_name = {
        clean(uuid).lower(): name for uuid, name in zip(catalog["process_uuid"], catalog["process_name"])
    }

    errors: list[str] = []
    output_rows: list[dict[str, Any]] = []

    for _, row in merged.iterrows():
        sid = clean(row["sample_id"])
        base_description = clean(row["material_description"])
        rec_description = clean(row["reconciliation_description"])
        normalized = clean(row["ground_truth_normalized_material"])
        process_name = clean(row["ground_truth_process_name"])
        process_uuid = clean(row["ground_truth_process_uuid"]).lower()
        decision = canonical_decision(row["ground_truth_match_type"])
        notes = clean(row["reviewer_notes"])

        if key(base_description) != key(rec_description):
            errors.append(f"{sid}: BOM description differs between Expert_A and Reconciliation")
        if not normalized:
            errors.append(f"{sid}: Final Normalized Material is blank")
        if not decision:
            errors.append(
                f"{sid}: Final Decision must be Direct, Proxy, or Review Required"
            )

        unresolved = decision == "Review Required"
        if decision == "":
            # Missing decision is already reported above; avoid cascading process
            # errors for an item that has not yet been reconciled.
            pass
        elif unresolved:
            if process_name or process_uuid:
                errors.append(
                    f"{sid}: Review Required row must have blank final process name/UUID"
                )
            process_name = ""
            process_uuid = ""
        else:
            if not process_name:
                errors.append(f"{sid}: {decision} row is missing Final Reference Process")
            if process_name and not process_uuid:
                process_uuid = name_to_uuid.get(key(process_name), "").lower()
            if not process_uuid:
                errors.append(
                    f"{sid}: Final Reference Process does not resolve to an exact catalog UUID"
                )
            elif process_uuid not in uuid_to_name:
                errors.append(f"{sid}: Final Process UUID is not present in the catalog")
            else:
                catalog_name = uuid_to_name[process_uuid]
                if process_name and key(catalog_name) != key(process_name):
                    errors.append(
                        f"{sid}: Final process name does not match the catalog process for its UUID"
                    )
                process_name = catalog_name

        output_rows.append(
            {
                "sample_id": sid,
                "case_study": clean(row["case_study"]),
                "material_description": base_description,
                "quantity": row["quantity"],
                "unit": clean(row["unit"]),
                "ground_truth_normalized_material": normalized,
                "ground_truth_process_name": process_name,
                "ground_truth_process_uuid": process_uuid,
                "ground_truth_match_type": decision,
                "ground_truth_unresolved": unresolved,
                "reference_status": "FINAL",
                "reviewer_notes": notes,
                "source_location": str(source_path.relative_to(REPO_ROOT))
                if source_path.is_relative_to(REPO_ROOT)
                else str(source_path),
            }
        )

    if errors:
        shown = "\n  - ".join(errors[:30])
        extra = f"\n  ... plus {len(errors) - 30} more" if len(errors) > 30 else ""
        raise ValueError(
            "Expert reconciliation is not ready to freeze. Fix these items first:\n  - "
            + shown
            + extra
        )

    return pd.DataFrame(output_rows)


def write_output(df: pd.DataFrame, output_path: Path, expert_path: Path, catalog_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = pd.DataFrame(
        [
            {"field": "reference_set_rows", "value": len(df)},
            {"field": "reference_status", "value": "FINAL"},
            {"field": "frozen_at_utc", "value": datetime.now(timezone.utc).replace(microsecond=0).isoformat()},
            {"field": "source_expert_workbook", "value": str(expert_path)},
            {"field": "catalog_path", "value": str(catalog_path)},
            {"field": "prepared_by", "value": "scripts/prepare_benchmark_reference.py"},
        ]
    )
    instructions = pd.DataFrame(
        [
            {
                "item": "Status",
                "details": "FINAL frozen expert reference set. Do not edit after model scoring begins.",
            },
            {
                "item": "Matched rows",
                "details": "Direct/Proxy rows use an exact process UUID from the exported catalog.",
            },
            {
                "item": "Unresolved rows",
                "details": "Review Required rows intentionally have blank process name/UUID.",
            },
            {
                "item": "Benchmark",
                "details": "Run scripts/benchmark_four_llms.py only after this file has been frozen.",
            },
        ]
    )

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        instructions.to_excel(writer, sheet_name="Instructions", index=False)
        df.to_excel(writer, sheet_name="Reference_Set", index=False)
        metadata.to_excel(writer, sheet_name="Metadata", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for cells in ws.columns:
                letter = cells[0].column_letter
                max_len = max(len(str(c.value or "")) for c in cells[:200])
                ws.column_dimensions[letter].width = min(max(max_len + 2, 12), 60)


def main() -> None:
    args = parse_args()
    expert_path = args.expert_workbook.expanduser().resolve()
    catalog_path = args.catalog.expanduser().resolve()
    output_path = args.output.expanduser().resolve()

    if not expert_path.exists():
        raise FileNotFoundError(f"Expert workbook not found: {expert_path}")
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catalog not found: {catalog_path}")

    base = load_base_rows(expert_path)
    rec = load_reconciliation(expert_path)
    catalog = load_catalog(catalog_path)
    frozen = validate_and_build(base, rec, catalog, expert_path)
    write_output(frozen, output_path, expert_path, catalog_path)
    print(f"Frozen benchmark reference set saved: {output_path}")
    print(f"Rows: {len(frozen)} | status: FINAL")


if __name__ == "__main__":
    main()
