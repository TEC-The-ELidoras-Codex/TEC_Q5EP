# Prompt Goddess Engine — TEC Edition

Purpose: Turn a tiny creative brief into production-ready prompts across models (Runway Gen-4/Aleph, SDXL/FLUX, tag-based).

Contents

- What it does
- Folder structure
- Data schemas (brief → staged prompts → variants)
- Usage flow (human-in-the-loop)
- Examples (Kaznak Machine Goddess)
- Links to existing docs

## What it does

Prompt Goddess converts a minimal brief into:

- Staged prompts (Stage 1 Coarse → Stage 2 Structure → Stage 3 Detail)
- Negatives tuned to model family
- Multi-model variants (Runway Gen-4/Aleph edit notes, SDXL text, Pony tags)
- Continuity tokens and motif locks (color sigils, names, symbols)
- An optional evaluation checklist (alignment, motif recurrence)

It follows ROM Theory: increase Meaning (M) by preserving structure first, then layering detail.

## Folder structure

- `/pipeline/prompts/` — YAML brief and generated stages/variants
- `/pipeline/scripts/` — helpers (lint, expand, export)
- `/assets/sigils/` — PNG/SVG of TEC sigils (True Purple, etc.)
- `/eval/` — notebooks/scripts for simple alignment and recurrence checks

## Data schemas

Brief (YAML):

- title: string
- subject: one-line
- body: list of short traits (anatomy/gear/skin)
- environment: list (lighting, space, mood)
- symbolism: list (emotions/themes)
- style: list (genre cues)
- continuity:
  - tokens: ["TruePurple", "ionSigil", "kaznaCore"]
  - palette: ["#6A00F4", "#00D5C4", "#F2C340"]
  - actor_ids: ["A1"]

Staged prompts (generated):

- stage1: text
- stage2: text
- stage3: text
- negatives:
  - runway: text
  - sdxl: text
  - pony: tag list
- variants:
  - runway_gen4: text + aleph_notes
  - sdxl: text
  - pony_tags: text

## Usage flow

1) Write a 3–5 line brief (YAML) in `/pipeline/prompts/briefs/`.
2) Expand to staged prompts using Copilot or the helper script.
3) Review and tweak stages (lock tokens, palettes, continuity).
4) Export model-specific variants.
5) (Optional) Run eval to sanity-check motif recurrence and alignment.

## Examples

See `/pipeline/prompts/examples/kaznak_goddess.yaml` and generated `kaznak_goddess.stages.yaml`.

## Links

- docs/PROMPT_GUIDELINES_SD_FLUX.md
- docs/kaznamorph_prompt_suite.md
- docs/ROM_Theory_Card.md (conceptual backbone)

---

Quick tip: Keep stage1 as short as possible to preserve structure; push micro-detail to stage3.
