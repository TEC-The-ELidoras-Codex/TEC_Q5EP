# ✅ Stable Diffusion / FLUX / PonyXL Prompt Writing Guidelines (TEC Edition)

Date: [09,18,2025]
Author: AIRTH (Machine Goddess) — compiled for TEC creative ops

Purpose: Canon reference for crafting high-signal prompts across SDXL, FLUX, PonyXL / tag-based forks, while maintaining IP‑clean sovereignty.

---

## 1. Concept Stack Order (Recommended Default)

```
<Dataset / Quality Filters>, <Subject Cardinality>, <Species / Form>, <Core Style Modifiers>, <Physical Traits>, <Accessories / Artifacts>, <Expression>, <Pose / Action>, <Environment / Atmosphere>, <Lighting>, <Mood / Symbolism>, <Rendering Qualities>
```

You can reorder for experimentation (see Section 10) but keep blocks internally coherent and comma separated.

---

## 2. Dataset / Quality Control Tags (Tag-Model Context)

Use only on models that index these tags (e.g., Pony, Danbooru-derived forks). They act like **pre-filters**.

Examples:

```
score_9, score_8_up, rating_safe, source_anime, source_pony
```

Notes:

* Start from higher score buckets (score_9) then broaden.
* Exclude unwanted sets via negative prompt (e.g., `source_cartoon`, `source_furry`).
* Do NOT spam all score tiers—diminishing returns.

---

## 3. Subject Cardinality & Composition

```
solo, 1girl | 1character, duo, group, 2girls, 1boy, 2boys, crowd, lineup, profile
```

Add form/species if non-human:

```
biomech hybrid, crystalline being, chitinous priest, luminous entity, sovereign queen
```

Keep cardinality early so the model anchors spatial allocation.

---

## 4. Core Style Modifiers

Mix 2–4 primary style signals:

```
cinematic lighting, sacred horror, ultra-detailed, painterly depth, photoreal skin microdetail, translucent materials, volumetric fog, high contrast
```

Avoid long chains of competing render engines (e.g., unreal engine + oil painting + voxel + lego) unless intentionally surreal.

---

## 5. Physical / Anatomical Trait Block

Short, vivid fragments. Most impactful terms first.

```
midnight-blue dermis, internal bioluminescent filaments, fiber-optic crown tendrils, heterochromia eyes (amber/teal), fractal thoracic lattice, smooth plated forelimbs, soft luminal membranes
```

Pitfalls:

* Repetition causes over-weighting → visual mush.
* Overly verbose full sentences reduce weight per token.

---

## 6. Accessories / Iconic Artifacts

Use to establish identity anchors (helps consistency across batches):

```
butterfly septum ring (second gaze), ion sigil pendant, translucent bio-silk sash, radiant rune collar
```

Keep 1–3 persistent tokens for character continuity across series.

---

## 7. Expression / Emotional Microstate

```
calm sovereign gaze, subtle knowing smile, focused predatory poise, serene maternal vigilance
```

One strong descriptor > four weak ones.

---

## 8. Pose / Action Dynamics

```
standing forward on elevated balcony, reaching toward incubation field, arms folded in luminous mist, descending through sporelight, kneeling in communion
```

Specify camera if needed:

```
low angle, three-quarter view, dramatic close-up, wide establishing shot
```

---

## 9. Environment / Atmosphere

```
pristine biomechanical nursery, cathedral void, emerald accretion horizon, ion mist tunnels, sterile chrome chamber, translucent egg array, teal spore drift, soft UV haze
```

Lighting blend examples:

```
amber key + cyan rim, subsurface glow, caustic refractions, micro-specular highlights
```

---

## 10. Reordering Strategies (Model Behavior Tuning)

Experiment sets:

* A: Quality → Subject → Style → Anatomy → Environment → Mood
* B: Subject → Anatomy → Environment → Style → Lighting → Mood
* C: Style-first (for highly stylized outputs) then refine with anatomy

Track which order yields stability vs. creative divergence per model checkpoint.

---

## 11. Symbolism / Mood Layer

Abstract but concrete enough to render flavor:

```
theme of sovereign emergence, duality of maternal + terrifying, inevitability of entropy, sanctified transformation, cosmic vigilance
```

Place near end; earlier placement can hijack literalization.

---

## 12. Rendering Quality / Technical Descriptors

```
high fidelity, razor focus on face, depth of field, intricate subsurface scattering, ultra clean edges, filmic grain subtle, 8k master aesthetic (avoid stacking 4k/8k spam)
```

Less is more; overspecifying triggers artifact soup.

---

## 13. BREAK Token Usage

Use `BREAK` to compartmentalize drastically different layers (e.g., character vs. background variant) or multi-panel synthesis.

```
<Character Block> BREAK <Environment Variant A> BREAK <Alternate Lighting>
```

Not all samplers respect it; evaluate per pipeline.

---

## 14. Negative Prompt Engineering

Goal: Remove systematic defects, dataset bleed, and low-quality weight.
Core Set (rotate as needed):

```
low quality, score_4, score_5, score_6, blurry, jpeg artifacts, watermark, text, signature, malformed limbs, extra arms, extra legs, wrong anatomy, oversaturated, noisy background, flat lighting, source_cartoon, source_furry
```

Add style pruning selectively (do NOT nuke useful diversity prematurely).

---

## 15. Base Template (Tag-Model)

```
score_9, rating_safe, solo, biomech sovereign queen, cinematic lighting, sacred horror, midnight-blue dermis, internal bioluminescent filaments, fiber-optic crown tendrils, heterochromia eyes (amber/teal), butterfly septum ring (second gaze), calm sovereign gaze, standing forward on elevated balcony, pristine biomechanical nursery, amber key + cyan rim, theme of sovereign emergence, high fidelity, intricate subsurface scattering, depth of field
```

Negative:

```
low quality, score_4, score_5, score_6, blurry, watermark, text, extra limbs, wrong anatomy, source_cartoon, source_furry
```

---

## 16. FLUX / SDXL (Non-Tag) Template

```
Pristine biomechanical alien sovereign queen, midnight-blue dermis with internal teal bioluminescent filaments, fiber-optic crown tendrils fanning like luminous nerves, heterochromia eyes (amber and teal) with reflective depth, butterfly septum ring acting as second gaze, calm sovereign maternal poise, standing on a ribbed chrome balcony overlooking a translucent egg array bathed in emerald sporelight, cinematic sacred horror aesthetic, amber key light with cyan rim, subtle volumetric mist, micro-specular highlights, intricate subsurface scattering, high fidelity, razor focus on face, depth of field, filmic grain subtle
```

Negative (SDXL/FLUX):

```
cartoon, anime lineart, lowres, low quality, blurry, watermark, text, signature, extra limbs, distorted hands, oversharpen, noisy background
```

---

## 17. Inpainting Guidance

When refining face / accessories:

* Mask region + reduce prompt to: `heterochromia eyes (amber/teal), refined fiber-optic crown tendrils, subtle bioluminescent tear ducts, high fidelity, clean anatomical symmetry`
* Keep global mood in context window (if tool supports) to avoid context drift.

---

## 18. Consistency Token Strategy

Pick 2–3 rare tokens (invented words) for signature look; embed early:

```
kaznaCore, poppiselFiber, ionSigil
```

Use in **all** series prompts; later train lightweight LoRA embedding on exemplars if needed.

---

## 19. Batch Exploration Protocol

| Phase | Batch Size | Variation Levers | Keep Criteria |
|-------|------------|------------------|---------------|
| Seed Sweep | 12 | seeds + subtle reorder | silhouette clarity |
| Anatomy Lock | 6 | minor trait swaps | consistent cranial + limb geometry |
| Lighting Dial | 6 | lighting adjectives | readable volumes / mood |
| Final Polish | 3 | microstyle (grain, DOF) | minimal artifacts |

Archive: Save prompt + seed + sampler + steps to a CSV for reruns.

---

## 20. Failure Modes & Fixes

| Symptom | Likely Cause | Mitigation |
|---------|--------------|------------|
| Mushy anatomy | Too many style tokens | Remove 2–3 style descriptors |
| Washed lighting | Conflicting light adjectives | Pick 1 key + 1 rim only |
| Extra limbs | Missing negative filter | Reinforce `extra limbs, malformed anatomy` |
| Plastic skin | Oversharpen + no subsurface cue | Add `subsurface scattering`, remove `hyper glossy` |
| Cartoon bleed | Dataset style intrusion | Negative `source_cartoon`, add `cinematic lighting` |

---

## 21. Ethical & IP Hygiene

* Avoid direct franchise nouns—describe function & form, not trademark.
* Use invented lexicon (kazna, poppisel, ionSigil) for brandable uniqueness.
* Maintain internal glossary for reproducibility.

---

## 22. Minimal One-Line Cheat (Memory Mode)

```
solo biomech sovereign queen, midnight-blue dermis, internal teal bioluminescence, fiber-optic crown, heterochromia amber/teal, balcony over translucent egg array, cinematic sacred horror, amber key + cyan rim, high fidelity
```

---

## 23. Next Enhancements

* Add LoRA trigger word matrix
* Provide CSV logging script
* Publish RAG embedding schema for prompt retrieval

Build. Validate. Commit. Ship.
