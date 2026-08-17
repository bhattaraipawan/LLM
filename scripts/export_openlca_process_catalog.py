"""Export process descriptors from the database currently active in openLCA.

This script is intentionally independent of the FastAPI application. It uses the
same openLCA IPC connection as the application and writes a CSV catalog plus a
small JSON metadata file for reproducibility.

Example:
    python scripts/export_openlca_process_catalog.py --database-label "ELCD"

Requirements:
    pip install olca-ipc olca-schema

Before running, start openLCA, activate the intended database, and start the IPC
server (default port 8080).
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import olca_ipc as ipc
import olca_schema as o


def _text(value: Any) -> str:
    if value is None:
        return ""
    return getattr(value, "value", str(value))


def _category_path(value: Any) -> str:
    if not value:
        return ""
    return " > ".join(str(part) for part in value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export process descriptors from the active openLCA database."
    )
    parser.add_argument("--port", type=int, default=8080, help="openLCA IPC port")
    parser.add_argument(
        "--database-label",
        default="active-openLCA-database",
        help="Human-readable database label recorded in metadata",
    )
    parser.add_argument(
        "--output-dir",
        default="research_artifacts/openlca",
        help="Directory for catalog and metadata outputs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ipc.Client(args.port)
    descriptors = list(client.get_descriptors(o.Process))

    rows: list[dict[str, str]] = []
    for process in descriptors:
        rows.append(
            {
                "process_uuid": _text(getattr(process, "id", "")),
                "process_name": _text(getattr(process, "name", "")),
                "category": _category_path(getattr(process, "category_path", None)),
                "location": _text(getattr(process, "location", "")),
                "library": _text(getattr(process, "library", "")),
                "process_type": _text(getattr(process, "process_type", "")),
            }
        )

    rows.sort(key=lambda row: row["process_name"].lower())

    catalog_path = output_dir / "openlca_process_catalog.csv"
    with catalog_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "process_uuid",
                "process_name",
                "category",
                "location",
                "library",
                "process_type",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "exported_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "database_label": args.database_label,
        "ipc_host": "localhost",
        "ipc_port": args.port,
        "process_count": len(rows),
        "note": (
            "The IPC export reflects the database active in openLCA at export time. "
            "Record the exact database release/version separately for publication."
        ),
    }
    metadata_path = output_dir / "openlca_process_catalog_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(f"Exported {len(rows)} processes")
    print(f"Catalog:  {catalog_path.resolve()}")
    print(f"Metadata: {metadata_path.resolve()}")


if __name__ == "__main__":
    main()
