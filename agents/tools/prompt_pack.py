from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import json


def load_prompt_pack(md_path: str) -> Dict[str, Any]:
    p = Path(md_path)
    text = p.read_text(encoding="utf-8")
    return {"path": str(p), "text": text}


def save_text(out_path: str, content: str) -> Dict[str, Any]:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return {"saved": str(p), "bytes": len(content.encode("utf-8"))}


def save_json(out_path: str, data: Any) -> Dict[str, Any]:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    p.write_text(text, encoding="utf-8")
    return {"saved": str(p), "bytes": len(text.encode("utf-8"))}
