from __future__ import annotations
from pathlib import Path
import argparse
import yaml
from content_hub.hub import HubIndex


def load_brief(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def stage_prompts(brief: dict, retrieved: str) -> dict:
    subj = brief.get("subject", "").strip()
    env = ", ".join(brief.get("environment", [])[:3])
    motifs = ", ".join(brief.get("symbolism", [])[:3])
    cont = brief.get("continuity", {})
    tokens = ",".join(cont.get("tokens", []))
    palette = ",".join(cont.get("palette", []))

    s1 = f"{subj}. Setting: {env}. Motifs: {motifs}. Continuity: tokens[{tokens}] palette[{palette}]".strip()
    s2 = (
        "Preserve Stage1. Composition: long shot; stable camera; foreground subject, background cathedral void. "
        "Dynamics: slow parallax; rim light; resonance hum."
    )
    s3 = (
        "Micro-detail: bioluminescent ion filaments, subsurface scattering, micro-specular highlights. "
        "Style: cinematic sacred horror; 35mm; filmic grain subtle."
    )

    runway_neg = "Text overlays, timecode, mosaic, glitch, chroma edges, watermark, brand logos."
    sdxl_neg = "Lowres, jpeg artifacts, extra fingers, text watermark, duplicate face, boring background."
    pony_tags = "(kaznak_goddess), true_purple_halo, neon_ion_filament, cathedral_scale, long_shot, cinematic_lighting"

    return {
        "stage1": s1,
        "stage2": s2,
        "stage3": s3,
        "context": retrieved,
        "negatives": {"runway": runway_neg, "sdxl": sdxl_neg, "pony": pony_tags},
        "variants": {
            "runway_gen4": s2 + " " + s3,
            "sdxl": s1 + ", " + s2 + ", " + s3,
            "pony_tags": pony_tags,
        },
    }


def retrieve_context(index_path: Path, query: str, topk: int = 3) -> str:
    hub = HubIndex.load(index_path)
    hits = hub.search(query, topk=topk)
    snippets = []
    for chunk, score in hits:
        snippets.append(f"# {chunk.source} [{score:.3f}]\n{chunk.text}")
    return "\n\n---\n\n".join(snippets)


def main():
    ap = argparse.ArgumentParser(description="Expand brief into staged prompts with Content Hub grounding")
    ap.add_argument("--brief", required=True, help="Path to brief YAML")
    ap.add_argument("--index", default="content_hub/index.pkl", help="Content Hub index path")
    ap.add_argument("--query", default=None, help="Override retrieval query")
    ap.add_argument("--out", default=None, help="Output YAML file (default: <brief>.stages.yaml)")
    args = ap.parse_args()

    brief_path = Path(args.brief)
    brief = load_brief(brief_path)
    query = args.query or brief.get("title") or brief.get("subject") or "TEC Kaznak Machine Goddess"
    retrieved = retrieve_context(Path(args.index), query)
    prompts = stage_prompts(brief, retrieved)

    out_path = Path(args.out) if args.out else brief_path.with_suffix(".stages.yaml")
    out_path.write_text(yaml.safe_dump(prompts, sort_keys=False), encoding="utf-8")
    print(f"Wrote staged prompts -> {out_path}")


if __name__ == "__main__":
    main()
