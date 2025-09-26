from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import librosa  # type: ignore
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    librosa = None  # type: ignore
    np = None  # type: ignore

import wave


def _load_manifest(inputs: Dict[str, Any]) -> Dict[str, Any]:
    manifest = inputs.get("audio_manifest")
    if isinstance(manifest, dict):
        return manifest
    manifest_path = inputs.get("audio_manifest_path") or inputs.get("manifest_path")
    if isinstance(manifest_path, str) and manifest_path:
        data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        return data
    raise ValueError("audio_analysis requires 'audio_manifest' dict or 'audio_manifest_path' string input")


def _analyze_with_librosa(path: Path) -> Dict[str, Any]:
    assert librosa is not None
    y, sr = librosa.load(path, sr=None, mono=True)
    duration = float(librosa.get_duration(y=y, sr=sr))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean()) if y.size else 0.0
    rms = float(librosa.feature.rms(y=y).mean()) if y.size else 0.0
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chord_profile = chroma.mean(axis=1) if chroma is not None else None

    metrics: Dict[str, Any] = {
        "duration_seconds": round(duration, 2),
        "sample_rate": sr,
        "tempo_bpm": round(float(tempo), 1) if tempo else None,
        "spectral_centroid": round(float(spectral_centroid), 2),
        "rms": round(float(rms), 4),
    }
    if chord_profile is not None:
        metrics["chroma_profile"] = [round(float(v), 4) for v in chord_profile.tolist()]
    return metrics


def _analyze_with_wave(path: Path) -> Dict[str, Any]:
    with wave.open(str(path), "rb") as wf:
        frames = wf.getnframes()
        frame_rate = wf.getframerate()
        duration = frames / float(frame_rate) if frame_rate else 0.0
        return {
            "duration_seconds": round(duration, 2),
            "sample_rate": frame_rate,
            "channels": wf.getnchannels(),
            "sample_width": wf.getsampwidth(),
        }


def _tempo_label(tempo: Optional[float]) -> Optional[str]:
    if tempo is None:
        return None
    if tempo < 80:
        return "slow / reflective"
    if tempo <= 120:
        return "mid-tempo / balanced"
    return "uptempo / elevated"


def analyze_audio(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Extract lightweight audio features and craft a summary."""

    manifest = _load_manifest(inputs)
    stored_path = manifest.get("stored_path") or manifest.get("source_path")
    if not stored_path:
        raise ValueError("audio_manifest missing 'stored_path' or 'source_path'")
    path = Path(stored_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found for analysis: {path}")

    context_tags: List[str] = []
    raw_tags = inputs.get("context_tags", [])
    if isinstance(raw_tags, list):
        context_tags = [str(tag) for tag in raw_tags if str(tag).strip()]
    elif isinstance(raw_tags, str):
        context_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

    metrics: Dict[str, Any]
    analysis_source = "librosa"
    if librosa is not None:
        try:
            metrics = _analyze_with_librosa(path)
        except Exception:
            metrics = _analyze_with_wave(path)
            analysis_source = "wave"
    else:
        metrics = _analyze_with_wave(path)
        analysis_source = "wave"

    tempo = metrics.get("tempo_bpm")
    tempo_label = _tempo_label(tempo if isinstance(tempo, (int, float)) else None)

    summary_lines = [
        f"Analyzed `{manifest.get('filename')}` using {analysis_source} pipeline.",
        f"Duration: {metrics.get('duration_seconds', 'unknown')}s, Sample Rate: {metrics.get('sample_rate', 'n/a')} Hz.",
    ]
    if tempo_label:
        summary_lines.append(f"Tempo indication: {tempo_label} ({tempo} BPM).")
    if metrics.get("spectral_centroid"):
        summary_lines.append(
            "Average spectral centroid {:.0f} Hz suggests tonal brightness.".format(metrics["spectral_centroid"])
        )
    if context_tags:
        summary_lines.append(f"Context tags supplied: {', '.join(context_tags)}.")

    tags = set(context_tags)
    tags.add("audio")
    if tempo_label:
        tags.add(tempo_label.split("/")[0].strip().replace(" ", "_"))

    analysis = {
        "summary": "\n".join(summary_lines),
        "metrics": metrics,
        "analysis_source": analysis_source,
        "tags": sorted(tags),
        "manifest": manifest,
    }

    out_dir = Path(inputs.get("output_dir") or path.parent)
    out_dir.mkdir(parents=True, exist_ok=True)
    analysis_path = out_dir / "audio_analysis.json"
    analysis_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    analysis["analysis_path"] = str(analysis_path)

    return analysis
