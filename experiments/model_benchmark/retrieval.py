"""Deterministic candidate retrieval for the Comment 5 benchmark.

Every evaluated model receives exactly the same candidate list for a given BOM
item.  Retrieval is deliberately simple and auditable: normalized token overlap
plus a small construction-material synonym map.  Geography is not used as a
ranking bonus, so the ELCD catalog is treated neutrally.

The retriever is evaluated separately (top-k recall) after the expert reference
is frozen.  It is not presented as an LLM capability.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Descriptive/specification terms that should not dominate process retrieval.
STOPWORDS = {
    "a", "an", "and", "at", "for", "from", "in", "of", "on", "the", "to",
    "ordinary", "clean", "well", "graded", "natural", "local", "commercial",
    "external", "internal", "wall", "walls", "thick", "thickness", "gauge",
    "soft", "annealed", "minimum", "post", "purlin", "rafter", "column",
    "binding", "layer", "bmt", "mm", "nos", "no", "grade", "tmt", "fe500",
    "m10", "1", "3", "4", "6", "7", "10", "15", "18", "19", "24", "43",
    "0", "45",
}


@dataclass(frozen=True)
class CatalogProcess:
    uuid: str
    name: str
    location: str = ""
    process_type: str = ""
    category: str = ""


def normalize_text(value: str) -> str:
    return " ".join(_TOKEN_RE.findall((value or "").lower()))


def tokens(value: str, *, remove_stopwords: bool = False) -> set[str]:
    result = set(_TOKEN_RE.findall((value or "").lower()))
    if remove_stopwords:
        return {token for token in result if token not in STOPWORDS and not token.isdigit()}
    return result


# Query key -> process-name evidence terms.  These terms are used only to build
# the deterministic candidate set; the LLM never sees hidden reference labels.
SYNONYM_GROUPS: dict[str, set[str]] = {
    "cement": {"cement", "portland", "clinker"},
    "sand": {"sand", "silica"},
    "gravel": {"gravel", "aggregate", "stone"},
    "stone": {"stone", "rock", "limestone"},
    "concrete": {"concrete"},
    "rebar": {"steel", "rebar", "reinforcing", "reinforcement", "bar"},
    "reinforcing": {"steel", "rebar", "reinforcing", "reinforcement", "bar"},
    "wire": {"steel", "wire"},
    "cgi": {"steel", "sheet", "galvanized", "galvanised", "zinc", "coil"},
    "galvanized": {"steel", "sheet", "galvanized", "galvanised", "zinc", "coil"},
    "galvanised": {"steel", "sheet", "galvanized", "galvanised", "zinc", "coil"},
    "iron": {"steel", "iron", "sheet", "coil"},
    "timber": {"wood", "timber", "softwood", "sawn", "spruce", "pine"},
    "wood": {"wood", "timber", "softwood", "sawn", "spruce", "pine"},
    "plywood": {"plywood", "wood", "timber", "board"},
    "bamboo": {"bamboo"},
    "soil": {"soil", "earth"},
    "earth": {"soil", "earth"},
    "block": {"block", "blocks", "brick"},
    "plaster": {"plaster"},
    "mortar": {"mortar", "plaster"},
    "nail": {"nail", "steel"},
}


def query_terms(query: str) -> tuple[set[str], set[str]]:
    base = tokens(query, remove_stopwords=True)
    expanded = set(base)
    normalized = normalize_text(query)

    # "PCC" in this BOM means plain cement concrete because the full phrase is
    # present; do not expand the acronym toward precipitated calcium carbonate.
    if "plain cement concrete" in normalized:
        base.discard("pcc")
        expanded.discard("pcc")

    for key, values in SYNONYM_GROUPS.items():
        if key in base or key in normalized:
            expanded.update(values)
    return base, expanded


def _concept_bonus(query: str, candidate_tokens: set[str]) -> int:
    q = normalize_text(query)
    score = 0

    if "cement" in q:
        score += 55 if "cement" in candidate_tokens else 0
        if "portland" in q and "portland" in candidate_tokens:
            score += 35
    if "sand" in q and "sand" in candidate_tokens:
        score += 65
        if "silica" not in q and "silica" in candidate_tokens:
            score -= 20
        if "plaster" in candidate_tokens:
            score -= 35
    if "gravel" in q and "gravel" in candidate_tokens:
        score += 65
    if q.strip() == "stone" or " stone " in f" {q} ":
        if "stone" in candidate_tokens:
            score += 55
        if "crushed" in candidate_tokens:
            score += 25
    if "concrete" in q and "concrete" in candidate_tokens:
        score += 75
        if "block" not in q and ("block" in candidate_tokens or "blocks" in candidate_tokens):
            score -= 25
    if "block" in q and ("block" in candidate_tokens or "blocks" in candidate_tokens):
        score += 55
    if "rebar" in q:
        if "rebar" in candidate_tokens:
            score += 110
        elif "steel" in candidate_tokens:
            score += 50
    if "wire" in q:
        if "wire" in candidate_tokens:
            score += 55
        if "steel" in candidate_tokens:
            score += 45
        if "copper" in candidate_tokens:
            score -= 70
    if any(term in q for term in ("cgi", "galvanized", "galvanised")):
        if "steel" in candidate_tokens:
            score += 50
        if "galvanized" in candidate_tokens or "galvanised" in candidate_tokens:
            score += 95
        if "sheet" in candidate_tokens or "coil" in candidate_tokens:
            score += 35
        if "aluminium" in candidate_tokens or "copper" in candidate_tokens or "lead" in candidate_tokens:
            score -= 60
    if "timber" in q or re.search(r"\bwood\b", q):
        if "wood" in candidate_tokens or "timber" in candidate_tokens:
            score += 80
        if "incineration" in candidate_tokens or "landfill" in candidate_tokens:
            score -= 120
    if "plywood" in q:
        if "plywood" in candidate_tokens:
            score += 120
        elif "wood" in candidate_tokens or "timber" in candidate_tokens:
            score += 55
        if "corrugated" in candidate_tokens or "cartonboard" in candidate_tokens:
            score -= 80
        if "incineration" in candidate_tokens or "landfill" in candidate_tokens:
            score -= 120
    if "plaster" in q and "plaster" in candidate_tokens:
        score += 85
    if "nail" in q:
        if "nail" in candidate_tokens:
            score += 100
        elif "steel" in candidate_tokens:
            score += 35
        if "copper" in candidate_tokens:
            score -= 60
    if "bamboo" in q and "bamboo" in candidate_tokens:
        score += 120
    if "soil" in q or "earth" in q:
        if "soil" in candidate_tokens or "earth" in candidate_tokens:
            score += 100
        # For "soil blocks", block products remain possible proxies even when
        # no earthen process exists in the catalog, but they receive no soil bonus.
        if {"anchor", "nailing", "shotcrete", "sprayed"} & candidate_tokens:
            score -= 120
    return score


def score_process(query: str, process: CatalogProcess) -> int:
    query_norm = normalize_text(query)
    base_terms, expanded_terms = query_terms(query)
    candidate_norm = normalize_text(process.name)
    candidate_tokens = tokens(process.name)

    score = 0
    if query_norm and query_norm == candidate_norm:
        score += 220
    elif query_norm and query_norm in candidate_norm:
        score += 90

    # Only substantive BOM terms receive direct token weight.
    score += 20 * len(base_terms & candidate_tokens)
    score += 7 * len(expanded_terms & candidate_tokens)
    score += _concept_bonus(query, candidate_tokens)

    # Tiny neutral preference for production/manufacturing records.
    if "production" in candidate_tokens or "manufacturing" in candidate_tokens:
        score += 2

    # Require at least some material evidence. This prevents incidental words
    # such as "grade" or numbers from surfacing unrelated plastics/metals.
    material_evidence = (base_terms | expanded_terms) & candidate_tokens
    if not material_evidence:
        return 0
    return score


def retrieve_candidates(
    query: str,
    catalog: list[CatalogProcess],
    *,
    limit: int = 10,
) -> list[CatalogProcess]:
    scored: list[tuple[int, str, CatalogProcess]] = []
    for process in catalog:
        score = score_process(query, process)
        if score > 0:
            scored.append((score, normalize_text(process.name), process))
    scored.sort(key=lambda item: (-item[0], item[1], item[2].uuid))
    return [item[2] for item in scored[:limit]]
