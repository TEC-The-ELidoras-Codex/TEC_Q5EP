# VS Code Copilot Guide — ROM + Prompt Goddess

Use these lightweight scaffolds while editing briefs, prompts, and scripts. Keep it terse; prefer concrete tokens and palettes.

## Snippets

/// plan
Goal: <what outcome looks like>
Inputs: <files, tokens, palette>
Stages: 1) Coarse 2) Structure 3) Detail
Risks: <ambiguity, token drift>
Done-when: <motif recurrence >= 0.7, alignment >= 0.8>

/// prompt stage1
Subject: <one line>
Setting: <time/space/light>
Motifs: <3 keywords>
Continuity: <tokens/palette>
Keep it under 30 words.

/// prompt stage2
Composition: <shot/pose/scale>
Dynamics: <verbs/forces>
Blocking: <foreground/background>
Preserve Stage1 text verbatim; add only structure.

/// prompt stage3
Micro-detail: <materials, textures>
Style cues: <genre, lenses>
Model-specific: <Runway/SDXL/Pony>
Avoid adding new entities; amplify Stage2.

/// negatives sdxl
Lowres, jpeg artifacts, extra fingers, text watermark, duplicate face, boring background.

/// negatives runway
Text overlays, timecode, mosaic, glitch, chroma edges, watermark, brand logos.

/// pony tags
(kaznak_goddess), true_purple_halo, neon_ion_filament, cathedral_scale, long_shot, cinematic_lighting

/// eval
Alignment: <CLIP/VQA prompt>
Motif recurrence: <describe visual regex or color cluster>
Continuity: <palette delta, token hit rate>

## Tips

- Lock continuity tokens early; don’t mutate names or palette codes.
- Order matters: subject → environment → symbolism → rendering.
- Prefer short Stage1; never repeat nouns across stages.
- Use BREAK to separate unrelated clauses in SDXL.
