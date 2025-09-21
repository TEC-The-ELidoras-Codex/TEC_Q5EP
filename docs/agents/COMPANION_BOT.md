# Companion Bot (TEC)

This companion aggregates your creative memories (storyboards, prompt packs, videos) and exposes them to a chat interface. It’s designed to plug into Microsoft Copilot Studio or any chat runtime.

## Goals

- Pull latest memories by tag/time range from the local Memory API
- Package JSON + readable MD for quick review
- Provide safety rails and tone (supportive, myth-science, non-clinical)

## Architecture

- Data source: FastAPI Memory API (see docs/MEMORY.md)
- Agent runner: agents/cli.py executing YAML workflows
- Bundles: data/agents/companion/<run_id>/recent_memories.{json,md}

## Workflow

1) Run `agents/workflows/companion_pull_recent.yaml`
   - Searches memory for tags: storyboard, infographic, video, prompt-pack (limit 50)
   - Saves JSON summary and Markdown digest
   - Logs a Memory note with paths

## Copilot Studio integration (outline)

1. Create a Custom connector (HTTPS)
   - Operations: GET /memory, POST /memory/search
   - Authentication: None (local) or API key (if added later)
2. Create a Bot flow
   - Trigger: user asks for “recent creative assets”
   - Action: call connector POST /memory/search with tags and limit
   - Response: render a Markdown card of results
3. Guardrails
   - Non-clinical support language; escalate to resources when asked
   - No PII storage; redact sensitive content before saving memories

## Safety notes

- This bot is not a therapist. Keep tone supportive and myth-focused.
- Offer break prompts and grounding tips if the user expresses distress.

## Next steps

- Add date filters in memory_search
- Add “pin” tag to keep favorites at top
- Optional: MCP adapter for direct memory access from IDE
