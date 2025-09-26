# Infographics assets

This folder contains:

- `The_Twin_Judgments_prompt.md` — full copy and generator-ready prompts (Canon v1.1 · automation ready)
- `Cosmic_Duality_Comparison_v7_1.md` — master brief for the Unseen vs Manifest side-by-side
- `Pantheon_Incarnations_v8_master.md` — consolidated v8.1/v8.2/v8.3 prompt pack (character ≤512s, grand-format, titan-scale)
- `palette.json` — TEC color tokens used in prompts/designs
- `twin_judgments_wireframe.svg` — a simple layout wire for designers (SVG)

## Canon Kits

- **Twin Judgments** — Prompt pack + `twin_judgments_wireframe.svg` (Canon). Use the agent workflow to pull both assets into `data/agents/infographics/<run_id>/` with a Memory receipt.
- **Cosmic Duality Comparison** — Prompt-only Canon brief for contrasting the Unseen vs Manifest.
- **Pantheon Incarnations v8** — Canon master pack (character, grand-format, titan-scale prompts).

## Usage

- Designers: open the SVG in Figma/Illustrator and swap zones with final art.
- Prompt runs: copy from the prompt doc, keep text minimal inside the image; keep paragraphs outside as text layers.
- Agents: `agents/workflows/infographic_twin_judgments.yaml` now saves the prompt pack **and** the wireframe into a run-scoped folder (`data/agents/infographics/<run_id>/`) and logs a Memory note for traceability.
  - For Cosmic Duality, use `agents/workflows/infographic_cosmic_duality.yaml`.
  - For Pantheon Incarnations, use `agents/workflows/infographic_pantheon_incarnations.yaml`.

### Automation Quickstart

```powershell
.\.venv\Scripts\python.exe -m agents.cli agents/workflows/infographic_twin_judgments.yaml
```

The workflow copies `The_Twin_Judgments_prompt.md` and `twin_judgments_wireframe.svg` into a timestamped folder under `data/agents/infographics/`, then logs the run in memory for later retrieval.
  