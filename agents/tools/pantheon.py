from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import json, math


def load_pantheon(path: str = "data/pantheon/entries.json") -> Dict[str, Any]:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    index = {e["name"].lower(): e for e in data}
    return {"entries": data, "index": index}


def find_by_name(state: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    return state.get("index", {}).get(name.lower())


def _ang_dist(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    # approximate small-angle distance in degrees on celestial sphere
    # convert to radians
    r1, d1, r2, d2 = map(math.radians, (ra1, dec1, ra2, dec2))
    cos_c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    cos_c = max(-1.0, min(1.0, cos_c))
    return math.degrees(math.acos(cos_c))


def find_nearest(state: Dict[str, Any], ra: float, dec: float, k: int = 3) -> List[Tuple[float, Dict[str, Any]]]:
    entries: List[Dict[str, Any]] = state.get("entries", [])
    scored = [(_ang_dist(ra, dec, e.get("ra_deg", 0.0), e.get("dec_deg", 0.0)), e) for e in entries]
    scored.sort(key=lambda x: x[0])
    return scored[:k]


def render_archetype_card(e: Dict[str, Any]) -> str:
    lines = [
        f"# {e.get('name')} ({e.get('type')})",
        "",
        f"RA {e.get('ra_deg')}°, Dec {e.get('dec_deg')}°",
        f"Tags: {', '.join(e.get('tags', []))}",
        f"Domain: {', '.join(e.get('domain', []))}",
        f"Symbols: {', '.join(e.get('symbols', []))}",
        "",
        e.get("lore", ""),
        "",
        "Traits:",
        f"- Light: {e.get('traits', {}).get('light', '')}",
        f"- Shadow: {e.get('traits', {}).get('shadow', '')}",
        f"- Guidance: {e.get('traits', {}).get('guidance', '')}",
        "",
        "Prompt:",
        e.get("prompts", {}).get("text", ""),
    ]
    return "\n".join(lines)
