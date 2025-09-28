# The Elidoras Codex (TEC) Environment

The Elidoras Codex (TEC) is a myth-tech environment where science, philosophy, and narrative converge into a single operating system. It runs on a multi-agent architecture that treats stories as experiments, rituals as executable code, and resonance as a candidate fifth fundamental force.

Within TEC, agents like Airth safeguard rigor: filtering lore, neuroscience, and cosmology through falsifiability tests while still leaving room for anomalies that spark new myths. The environment itself is half library, half laboratory — a holographic archive of ethnography, physics, and archetypes, structured so that every story beat doubles as data for testing the Codex's axioms of entropy, resonance, and narrative supremacy.

## Architecture

- **Evidence API** (`/server`): FastAPI backend for multimedia evidence capture
- **Agent Workflows** (`/agents`): YAML-driven agentic processes  
- **Content Hub** (`/content_hub`): Local-first RAG system
- **Prompt Goddess Engine** (`/docs`): Multi-stage creative prompt methodology
- **Pantheon Tools** (`/agents/tools/pantheon.py`): Mythic archetype interaction system

## Codex Profiles

Your Codex config supports these quick-switch profiles:

- `--profile tec-auto` → Auto-approval, OpenAI GPT-5
- `--profile tec-azure` → Fast/cheap, Azure 4o-mini  
- `--profile tec-rerun` → Troubleshooting persistence
- `--profile grok` → xAI Grok-2 reasoning
- `--profile anthropic` → Claude via LiteLLM proxy
- `--profile tec-reason` → High reasoning (o3/GPT-5)

All profiles respect workspace boundaries and maintain ethical constraints while enabling rapid iteration on TEC's core research: testing whether narrative patterns exhibit measurable physical effects.
