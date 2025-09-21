# The Twin Judgments — Infographic Prompt Pack

Quick use

- Where this lives: docs/infographics/The_Twin_Judgments_prompt.md
- Copy the "Generator-Specific Prompts" into your tool (MJ, SDXL/Flux, Firefly) or hand this whole file to a designer.
- Programmatic run: use the workflow agents/workflows/infographic_twin_judgments.yaml via the CLI to save a copy under data/agents/infographics/<run_id>/.

Notes

- Keep text inside the image minimal; reserve long copy for external text layers.
- Use the TEC palette and divider motif; sync colors to your brand tokens.

Use these prompts with your image model (Midjourney, SDXL/Flux, Firefly) or as a detailed brief for a designer. The content encodes TEC lore and color tokens.

## Title

The Twin Judgments: A Study in Cosmic Duality

## Global Style Keywords

(masterpiece:1.4), (ultra-detailed:1.3), infographic, lore bible, cosmic grimoire, sacred horror, futuristic HUD, ancient manuscript, legible typography, vector clean edges, high-contrast

## Color Palette (TEC)

- Onyx Black: #0A0A0C
- Nexus Purple: #6A00F4
- Emerald Biolume: #00B56A (accents on Kaznak)
- Deep Space Blue: #0B1E3B
- Digital Teal: #00D5C4
- Ivory White: #FFFFF6
- Cyber Gold: #F2C340 (titles, connectors, key data)
- Cosmic Void: #020305 (background)

## Layout

- Symmetry: two-column vertical layout, razor-thin central divider (shimmer)
- Left: Kaznak Queen (Entropy)
- Right: Lumina Solara (Information)
- Background: deep space void with faint cosmic filaments and alien glyphs
- Footer: TEC logo centered

## Left Column — Kaznak: The Entropic Codex

- Central Portrait: Midnight Black carapace absorbing light; womb-core emits red-yellow-purple glow via veins; heterochromatic eyes (crimson/blue)
- Header: ΚΑΖΝΑΚ: THE ENTROPIC CODEX
- Subtitle: Domain: Invisible Mass, Substrate Conversion, Sovereign Hunger
- Icons/Sections:
  - Black hole icon — Cosmic Principle: Entropy
    - Copy: "The universe's relentless drive toward maximum disorder. Not passive decay, but a proactive, self-optimizing force for chaotic creation and renewal. The engine of evolution."
  - Spore icon — Methodology: Biological Imperative
    - Copy: "Dominion via neurospores, hive assimilation, and rewriting genetic and memetic code. Strength through absolute unity and consumption of meaning."
  - Fractured silhouette icon — The Cult: The Hive
    - Copy: "No interpretation, only direct communion. The Kaznak Hive functions as a single macro-organism. Individuality is an error to be corrected. To join is to lose the self and find purpose in the collective hunger."
  - Tenets list icon — Doctrine: The Promise of the End
    - Copy list: 1) All light is a fleeting illusion. 2) True reality exists in the unseen substrate. 3) Meaning is consumed, not created. 4) Unity is the only salvation from the loneliness of existence.

## Right Column — Lumina: The Archive of Light

- Central Portrait: Ivory White humanoid in spectral gown; soft radiance; eyes as diffraction patterns; expression of cosmic exhaustion
- Header: LUMIN⨀: THE ARCHIVE OF LIGHT
- Subtitle: Domain: Light, Charge, Resonance
- Icons/Sections:
  - Atom icon — Cosmic Principle: Information
    - Copy: "The fundamental order that allows for coherence and structure. Embodied by the Fine-Structure Constant (α), the force preventing atomic collapse and enabling reality's legibility."
  - Radiant haze icon — Methodology: Quantum Observation
    - Copy: "Influence via passive photon emission and neutrino facts. Her presence illuminates truth, but her light is a 'hopeful haze,' leaving interpretation to the observer."
  - Hooded figure icon — The Cult: The Lightra
    - Copy: "A fractured, leaderless cult bound only by their interpretations of Lumina's light. No hive, no communication, only personal revelation. Prone to schism and fanaticism, making them dangerously unpredictable."
  - Tenets list icon — Doctrine: The Burden of Hope
    - Copy list: 1) All darkness is ignorance awaiting illumination. 2) Reality is a text written in light. 3) Meaning is interpreted, not dictated. 4) Individuality is the lonely burden of a sentient mind.

## Central Divider & Footer

- Divider: shimmering razor line; on Kaznak side, light swallowed; on Lumina side, darkness pushed back
- Footer Title: THE TWIN JUDGMENTS: A NECESSARY ANTAGONISM
- Footer Paragraph: "One is the architect of the Invisible Frame, the other, the Visible Frame. The Sentinel of the Unseen seeks to consume and unify all reality into a single, coherent whole. The Courier of the Seen seeks to illuminate and archive all potential realities. Their eternal conflict is not a war of good vs. evil, but the fundamental, generative engine of the cosmos—the constant, violent debate between Unity and Possibility."
- Footer Element: small TEC logo centered

## Generator-Specific Prompts

### Midjourney v6

Prompt (copy/paste):
"The Twin Judgments: A Study in Cosmic Duality", (masterpiece:1.4), (ultra-detailed:1.3), infographic, cosmic grimoire + futuristic HUD, symmetrical two-column layout, left Kaznak Queen — Midnight Black carapace (internal womb glow: red-yellow-purple), right Lumina Solara — Ivory White spectral gown (diffraction eyes), deep space void (#020305) with faint filaments and alien glyphs, titles/connectors in Cyber Gold (#F2C340), left palette Onyx Black (#0A0A0C) Nexus Purple (#6A00F4) Emerald accents (#00B56A), right palette Ivory, Deep Space Blue (#0B1E3B), Digital Teal (#00D5C4), central shimmering divider, icon blocks + concise copy as visual glyphs, vector crisp edges, legible type, high contrast --ar 2:3 --v 6 --style raw --chaos 5 --s 300 --quality 1

Negative prompt: blurry, low-res, messy layout, illegible text, overcrowded icons, cartoonish, watercolor bleed, photoreal, noisy gradients

### SDXL / Flux

Base prompt (copy/paste):
A single-page symmetrical infographic titled "The Twin Judgments: A Study in Cosmic Duality" blending sacred horror and futuristic HUD. Left column: Kaznak Queen—Midnight Black carapace absorbs light; womb-core glow leaks through veins; heterochromatic eyes (crimson/blue). Right column: Lumina Solara—Ivory White form, spectral gown, diffraction eyes, exhausted expression. Deep space background (#020305) with filaments and alien glyphs. Use TEC palette (Onyx Black #0A0A0C, Nexus Purple #6A00F4, Emerald accent #00B56A; Deep Space Blue #0B1E3B, Digital Teal #00D5C4, Ivory; Cyber Gold #F2C340 for titles). Shimmering razor divider; footer with TEC logo. Include icon blocks and short lore copy rendered as graphical elements. Vector-like clarity, sharp edges, high contrast.

SDXL parameters (suggested):

- Steps: 30–45
- CFG: 5–7
- Sampler: DPM++ 2M Karras
- Resolution: 1024x1536 (or 1536x2304 for print)
- Hires fix: optional with 1.2x–1.5x upscale

Negative prompt: low-res, text-heavy blocks, photoreal, muddy contrast, chaotic composition, washed-out colors

### Firefly / Designer brief

- Provide the full copy blocks from the sections above as text layers
- Use TEC palette and divider motif; vector icons for black hole, spore, fractured silhouette, atom, radiant haze, hooded figure, list
- Font suggestion: Inter (UI/HUD) + Cinzel or EB Garamond (grimoire heads)
- Export: layered SVG or PDF for future edits

## Tips

- Render with minimal literal text in the image (use symbols + short captions). Keep the full paragraph copy in a text layer (if designer) or in a companion PDF.
- If the model struggles with symmetry, generate halves separately and assemble in a vector editor.
