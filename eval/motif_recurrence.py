from __future__ import annotations
import re
from typing import List, Dict


def palette_hit_rate(captions: List[str], palette: List[str]) -> float:
    if not captions or not palette:
        return 0.0
    hits = 0
    total = len(captions) * len(palette)
    for cap in captions:
        for color in palette:
            if color.lower() in cap.lower():
                hits += 1
    return hits / total if total else 0.0


def motif_token_rate(captions: List[str], tokens: List[str]) -> float:
    if not captions or not tokens:
        return 0.0
    hits = 0
    total = len(captions) * len(tokens)
    for cap in captions:
        for tok in tokens:
            if re.search(r"\b" + re.escape(tok) + r"\b", cap, re.IGNORECASE):
                hits += 1
    return hits / total if total else 0.0


def simple_eval(report: Dict) -> Dict:
    """report: { captions: [..], continuity: { tokens: [], palette: [] } }"""
    caps = report.get("captions", [])
    cont = report.get("continuity", {})
    tokens = cont.get("tokens", [])
    palette = cont.get("palette", [])
    return {
        "palette_hit_rate": palette_hit_rate(caps, palette),
        "motif_token_rate": motif_token_rate(caps, tokens),
    }
