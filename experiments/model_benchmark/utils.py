"""Utility helpers for benchmark JSON parsing, canonicalization, and metadata."""

from __future__ import annotations

import json
import os
import platform
import re
import sys
from importlib import metadata as importlib_metadata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_CANON_RE = re.compile(r"[a-z0-9]+")


def canonical_text(value: str) -> str:
    return " ".join(_CANON_RE.findall((value or "").lower()))


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract the first balanced JSON object from model output.

    Handles ordinary model chatter or fenced JSON without silently inventing
    missing fields. Raises ValueError when no valid object can be parsed.
    """
    if not text:
        raise ValueError("empty model output")

    start = text.find("{")
    while start >= 0:
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            ch = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start : index + 1]
                    try:
                        value = json.loads(candidate)
                    except json.JSONDecodeError:
                        break
                    if isinstance(value, dict):
                        return value
                    break
        start = text.find("{", start + 1)
    raise ValueError("no valid JSON object found")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def environment_metadata(torch_module=None, transformers_module=None) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "timestamp_utc": utc_now_iso(),
        "python": sys.version,
        "platform": platform.platform(),
        "os": os.name,
        "machine": platform.machine(),
    }
    if transformers_module is not None:
        metadata["transformers_version"] = getattr(transformers_module, "__version__", None)
    package_versions = {}
    for package in ("accelerate", "bitsandbytes", "huggingface_hub", "safetensors", "openpyxl"):
        try:
            package_versions[package] = importlib_metadata.version(package)
        except importlib_metadata.PackageNotFoundError:
            package_versions[package] = None
    metadata["package_versions"] = package_versions
    if torch_module is not None:
        metadata["torch_version"] = getattr(torch_module, "__version__", None)
        cuda_available = bool(torch_module.cuda.is_available())
        metadata["cuda_available"] = cuda_available
        metadata["cuda_version"] = getattr(torch_module.version, "cuda", None)
        if cuda_available:
            metadata["gpu_name"] = torch_module.cuda.get_device_name(0)
            props = torch_module.cuda.get_device_properties(0)
            metadata["gpu_total_memory_gib"] = round(props.total_memory / (1024**3), 3)
    return metadata


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
