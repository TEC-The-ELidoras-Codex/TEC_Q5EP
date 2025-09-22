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

The capture UI will be available at http://localhost:5173, and the API at http://localhost:8000.

🗺️ Repository Map
./README.md: You are here.

./agents/: The core agentic workflow engine, tools, and YAML definitions.

./content_hub/: The local RAG system for grounding prompts.

./data/: Default output directory for agent runs, memory files, and evidence packs.

./docs/: The philosophical and technical heart of the project. Contains the core lore, prompt engineering guides, and system specs.

./eval/: Scripts for evaluating the coherence and quality of AI-generated outputs.

./server/: The FastAPI backend for data submission and retrieval.

./ui/: The TypeScript frontend for evidence capture.

🤝 Contribute
This is an open-source invocation. PRs, issues, and ideas are welcome. Key areas for contribution:

Expanding the agent toolset (/agents/tools).

Improving RAG performance and embedding strategies.

Adding new evaluation metrics (/eval).

Integrating new model backends (e.g., Runway, Blender).

Please respect the project's core philosophy. All contributions must be constructive and aligned with the mission.

📝 License
This repository is licensed under the terms specified in the LICENSE file.
