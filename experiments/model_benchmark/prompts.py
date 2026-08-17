"""Standardized prompts for the controlled LLM material-matching benchmark."""

from __future__ import annotations

SYSTEM_PROMPT = """You are participating in a controlled engineering benchmark for an
LLM-assisted life-cycle assessment screening workflow. Your role is limited to
material-name normalization and selection among a fixed list of environmental
database process candidates. Do not estimate emission factors, carbon values,
densities, or quantities. Do not invent database processes. Use only the
candidates supplied in the prompt.

Decision definitions:
- Direct: the selected process represents the same material/process closely
  enough to be used without a substantive material substitution.
- Proxy: the selected process is a defensible related substitute, but it is not
  an exact/direct representation of the BOM material.
- Review Required: none of the supplied candidates is defensible. In this case,
  selected_candidate must be -1.

For normalized_material, preserve technically relevant information present in
the BOM description, but do not invent grades, compositions, locations, or
manufacturing routes that were not provided.

Return one JSON object only. No markdown and no text outside the JSON object."""


def build_prompt(*, bom_id: str, description: str, unit: str, candidates: list[dict]) -> str:
    lines = []
    for index, candidate in enumerate(candidates):
        location = candidate.get("location") or "unspecified"
        process_type = candidate.get("process_type") or "unspecified"
        lines.append(
            f"{index}: {candidate['name']} | location={location} | type={process_type}"
        )
    candidate_text = "\n".join(lines) if lines else "(no candidates returned)"

    return f"""{SYSTEM_PROMPT}

BOM item ID: {bom_id}
Original BOM description: {description}
Declared unit: {unit}

Fixed ELCD/openLCA candidate processes:
{candidate_text}

Perform both benchmark tasks:
1. Normalize the BOM material description into a concise standardized material
   name without adding unsupported information.
2. Select the best candidate process by its integer index, or select -1 when no
   candidate is defensible. Classify the decision as Direct, Proxy, or Review Required.

Return ONLY this JSON structure:
{{
  "normalized_material": "standardized material name",
  "selected_candidate": 0,
  "decision": "Direct",
  "reason": "brief technical justification"
}}

If no candidate is defensible, selected_candidate must be -1 and decision must
be "Review Required"."""
