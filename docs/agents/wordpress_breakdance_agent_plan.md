# WordPress Breakdance Automation Agent — Concept Plan

## Why the "WordPress Agent" is Missing

The current TEC agent catalog focuses on FastAPI-driven workflows (e.g., `agents/workflows/*`) and does not ship an out-of-the-box WordPress automation profile. Microsoft Copilot Studio and the VS Code Copilot Agents preview center the GitHub/VS Code ecosystem and do not expose a prebuilt WordPress/BREAKDANCE specialist. To control Breakdance from our environment we need to build a **custom agent** that bridges:

1. **WordPress REST APIs (and custom endpoints).**  
2. **Breakdance Builder hooks** for section/box creation.  
3. **Our TEC knowledge base** (symbol table, runbook, narrative assets).  
4. **An orchestration layer** capable of invoking GPT-4/ GPT-4.1/ GPT-5 (when available) with structured prompts.

## High-Level Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                         TEC_Q5EP Agent Orchestrator                        │
│  (FastAPI service + workflow YAML)                                         │
├───────────────────────────────────────────────────────────────────────────┤
│         WordPress Automation Plugin (deployed inside target sites)         │
│  • Auth: JWT Application Passwords or OAuth2                               │
│  • Endpoints: /tec-ai/layout, /tec-ai/content, /tec-ai/assets              │
│  • Breakdance integration: PHP hooks & Breakdance API classes              │
└───────────────────────────────────────────────────────────────────────────┘
                 ▲                               ▲
                 │                               │
        GPT-4/ GPT-4.1/ GPT-5 via Azure/OpenAI   │
                 │                               │
                 ▼                               ▼
      Prompt templates in `agents/prompt_agent.py`        TEC symbol table & lore assets
```

## Functional Requirements

1. **Layout synthesis** — draft Breakdance sections/containers, matching TEC glyph boxes and resonance motifs. Output JSON (Breakdance layout schema) or PHP arrays.  
2. **Content authoring** — generate copy aligned with the symbol table, contextual energy theory, and story beats.  
3. **Asset wiring** — attach glyph icons, resonance gradients, and metadata (ALT text, OG tags).  
4. **Preview & rollback** — sandbox changes before publishing; maintain backups of previous Breakdance layouts.  
5. **Human-in-the-loop** — allow manual review and final approval via agent CLI or VS Code task.

## Technical Implementation Roadmap

### Phase 0 — Prerequisites

- Provision API credentials on target WordPress instance (Application Password or OAuth2).  
- Confirm Breakdance version and available PHP/JS APIs.  
- Mirror staging site for safe testing.

### Phase 1 — WordPress Plugin Skeleton (`wp-content/plugins/tec-ai-agent`)

- Register REST namespace `tec-ai/v1`.  
- Endpoints:  
  - `POST /layout`: accepts JSON describing page sections and Breakdance components.  
  - `POST /content`: stores rendered copy, headings, and metadata.  
  - `POST /task`: triggers pipeline actions (publish/draft, rollback).  
- Use Breakdance's `
Breakdance\Elements\...` classes to assemble DOM trees.  
- Implement nonce + capability checks (limit to custom role `tec_orchestrator`).

### Phase 2 — TEC Agent Workflow

- Add a YAML workflow under `agents/workflows/wordpress_breakdance.yaml` describing steps:  
  1. Gather intents (page goal, glyph set, CTA).  
  2. Query local knowledge (symbol table, lore docs).  
  3. Call GPT-4.1/5 with structured prompt to produce layout + copy.  
  4. POST results to WordPress plugin endpoints.  
  5. Poll status and surface preview link.  
- Extend `agents/prompt_agent.py` with prompt templates referencing TEC symbology tokens and contextual energy equation.

### Phase 3 — Tooling & Tasks

- VS Code task: `agents:wordpress:deploy` → pushes plugin ZIP to site via SSH/SFTP (use `tools/package_agent_manifest.py`).  
- CLI command: `python -m agents.cli agents/workflows/wordpress_breakdance.yaml --base-url https://example.com`.

### Phase 4 — Safety & Rollback

- Every run writes a backup of the Breakdance layout to `/tec-ai/logs/YYYYMMDD_HHMM.json`.  
- Maintain checksum map (reuse `analysis/verify_hashes.py`).  
- Provide `DELETE /layout/{id}` endpoint to restore from prior revision.

## Prompting Strategy for GPT-4/5

- **System rail:** embed TEC axioms (Narrative Supremacy, Duality Principle, Flawed Hero Doctrine) + formatting requirements for Breakdance schema.  
- **User rail:** page brief (goal, audience, CTA, glyph set).  
- **Developer rail:** injection of unified symbol table entries, equation legend, and palette directives from the TEC Brand Guide.  
- **Critic rail (optional):** request structural validation before publishing (e.g., ensure hero + proof + CTA + lore capsule).

## Security Checklist

- Restrict plugin endpoints to HTTPS and application passwords.  
- Enforce nonce/capability checks in WordPress plugin.  
- Rotate credentials through Azure Key Vault / GitHub Secrets.  
- Log all agent actions with timestamps and operator identity.  
- Provide kill-switch flag in plugin to disable remote changes quickly.

## Stretch Goals

- **Two-way sync:** fetch current Breakdance layouts and auto-generate documentation/diagrams in the TEC content hub.  
- **Live preview:** embed WordPress preview iframe inside VS Code WebView for instant review.  
- **Asset generation:** integrate Stable Diffusion / DALL·E tasks for glyph-infused imagery tied to TEC symbol IDs.  
- **Citizen editing:** build a simplified UI panel leveraging TEC glyph tagging for non-technical collaborators.

## Next Steps

1. Approve plugin namespace and authentication approach.  
2. Draft the WordPress plugin (PHP) scaffold with the REST endpoints listed above.  
3. Extend the TEC agent orchestration with the new workflow YAML and prompt templates.  
4. Pilot on a staging WordPress + Breakdance site, validate rollback protections, and iterate.  
5. Once stable, document the workflow in the runbook and add a dedicated VS Code task for one-click deployment.
