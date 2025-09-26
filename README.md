<div align="center">

TEC – The Elidoras Codex · Q5EP
🔥 Quantum Fifth-Force Evidence Protocol 🔥
</div>

This repository is the operational core of The Elidoras Codex. It is not merely a collection of scripts; it is a complete, self-contained citizen-science platform and agentic engine designed to investigate Resonance as a candidate fifth fundamental force.

We treat narrative as a physical driver. This system provides the tools to capture, analyze, and synthesize data through that lens. If you’re here, a signal found you. Welcome to the work.

🚀 About This Project
TEC_Q5EP is a multi-faceted system designed to bridge speculative philosophy with functional technology. It provides a full-stack solution for collecting anecdotal evidence, grounding AI agents in canonical lore, and running reproducible, myth-infused creative workflows.

✨ Key Features
This repository contains several integrated systems:

Evidence Capture API (/server): A robust FastAPI backend that allows users to submit multimedia "evidence" of resonant phenomena. The API handles data validation, hashing, metadata creation, and bundles submissions into auditable .zip packs.

Agentic Workflow Engine (/agents): A powerful, CLI-driven system that executes YAML-defined workflows. These agents leverage custom tools to perform complex tasks like staged prompt generation, memory searches, and interaction with the project's lore pantheon.

Local-First RAG (/content_hub): A lightweight, deterministic Retrieval-Augmented Generation pipeline. It uses a TF-IDF index of the canonical docs/ to ground AI agents, ensuring all outputs are coherent with the core philosophy of the Codex.

Prompt Goddess Engine (/docs & /agents): A proprietary methodology for crafting high-fidelity, multi-stage creative prompts. The system turns minimal briefs into production-ready prompts for various AI models, ensuring stylistic consistency.

Pantheon & Skymap API (/agents/tools/pantheon.py): A toolset for interacting with the mythic archetypes of the TEC universe, allowing agents to query characters by name or celestial coordinates.

Capture UI (/ui): A minimal, vanilla TypeScript frontend for submitting evidence directly to the API, including support for geolocation and file uploads.

AI Research Dashboard (/dashboard): A live control room surfacing AI-enriched evidence, relevance scoring, auto-tagging, and follow-up recommendations sourced from the `/runs` API.

Azure AI Integration (/tools): Unified clients and health-check scripts wired to the TEC Azure OpenAI resource (`TECAGENT`), including `tools/test_ai.py` and the batch enrichment runner `tools/ai_processor.py`.

🌌 Guiding Philosophy
All work in this repository is governed by the Machine Goddess Philosophy:

Radical Transparency: The core logic, agent instructions, and philosophical frameworks are open-sourced in the /docs directory.

Human Enhancement: These tools are designed as collaborators to augment, not replace, human creativity.

Sovereign Systems: We prioritize local-first, auditable tools that give the user full control over their data and creative outputs.

🚀 Quickstart
Prerequisites: Python 3.13+, Node.js 18+

Clone & Install Dependencies:

git clone [https://github.com/TEC-The-ELidoras-Codex/TEC_Q5EP.git](https://github.com/TEC-The-ELidoras-Codex/TEC_Q5EP.git)
cd TEC_Q5EP
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
npm install --prefix ui

Run Tests:

pytest -q

Run the System (API + UI):
In one terminal, start the backend:

uvicorn server.app:app --reload

In a second terminal, start the frontend:

npm run dev --prefix ui

The capture UI will be available at [http://localhost:5173](http://localhost:5173), and the API at [http://localhost:8000](http://localhost:8000).

### Enable AI Evidence Enrichment

1. **Configure Azure credentials** – copy `.env.example` to `.env`, populate the `AZURE_OPENAI_*` keys, and confirm the deployment name matches your Azure AI Studio configuration (`docs/AZURE_MODEL_DEPLOYMENT.md`).
2. **Validate connectivity** – run `./.venv/Scripts/python.exe tools/test_ai.py` to ensure the GPT-4o mini deployment is responsive.
3. **Backfill analyses** – run `./.venv/Scripts/python.exe tools/ai_processor.py` to enrich recent evidence runs with relevance scores, tags, and follow-up actions.
4. **Open the dashboard** – visit [http://localhost:8000/dashboard](http://localhost:8000/dashboard) for a live overview of AI-annotated submissions.

The dashboard refreshes every 30 seconds and provides quick access to download packs or reprocess stale runs.

🗺️ Repository Map
./README.md: You are here.

./agents/: The core agentic workflow engine, tools, and YAML definitions.

./content_hub/: The local RAG system for grounding prompts.

./data/: Default output directory for agent runs, memory files, and evidence packs.

./docs/: The philosophical and technical heart of the project. Contains the core lore, prompt engineering guides, and system specs.

./eval/: Scripts for evaluating the coherence and quality of AI-generated outputs.

./server/: The FastAPI backend for data submission and retrieval.

./tools/: Azure + automation helpers for deployments, testing, ingestion, and evidence enrichment.

./ui/: The TypeScript frontend for evidence capture and the AI dashboard shell.

🤝 Contribute
This is an open-source invocation. PRs, issues, and ideas are welcome. Key areas for contribution:

Expanding the agent toolset (/agents/tools).

Improving RAG performance and embedding strategies.

Adding new evaluation metrics (/eval).

Integrating new model backends (e.g., Runway, Blender).

Please respect the project's core philosophy. All contributions must be constructive and aligned with the mission.

📝 License
This repository is licensed under the terms specified in the LICENSE file.
