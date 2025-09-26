from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Dict


def _compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ingest_audio(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Copy an audio asset into the run directory and emit a manifest."""

    audio_path = inputs.get("audio_path") or inputs.get("path")
    if not isinstance(audio_path, str) or not audio_path:
        raise ValueError("ingest_audio requires 'audio_path' (or 'path') string input")

    src = Path(audio_path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"Audio file not found: {src}")

    output_dir = inputs.get("output_dir") or inputs.get("dest_dir")
    if not isinstance(output_dir, str) or not output_dir:
        raise ValueError("ingest_audio requires 'output_dir' (or 'dest_dir') string input")

    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    dest = out_dir / src.name
    shutil.copy2(src, dest)

    manifest = {
        "source_path": str(src),
        "stored_path": str(dest),
        "filename": src.name,
        "extension": src.suffix.lower(),
        "bytes": dest.stat().st_size,
        "sha256": _compute_sha256(dest),
    }

    manifest_path = out_dir / "audio_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "manifest": manifest,
        "manifest_path": str(manifest_path),
    }
