# Infographics assets

This folder contains:

- `The_Twin_Judgments_prompt.md` — full copy and generator-ready prompts
- `palette.json` — TEC color tokens used in prompts/designs
- `twin_judgments_wireframe.svg` — a simple layout wire for designers (SVG)

Usage

- Designers: open the SVG in Figma/Illustrator and swap zones with final art.
- Prompt runs: copy from the prompt doc, keep text minimal inside the image; keep paragraphs outside as text layers.
- Agents: use `agents/workflows/infographic_twin_judgments.yaml` to save the prompt doc to a run-scoped folder under `data/agents/infographics/<run_id>` and log a Memory note.
