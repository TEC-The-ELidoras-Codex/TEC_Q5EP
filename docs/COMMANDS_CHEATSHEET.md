# TEC_Q5EP Command Cheatsheet

> PowerShell-flavored commands for daily ops. Activate the virtual environment first unless noted.

## Environment Setup

```powershell
# create venv (first time)
python -m venv .venv

# activate venv (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# install python deps
pip install -r requirements.txt

# install UI deps
npm install --prefix ui
```

## Quality Gates

```powershell
# run pytest suite
.\.venv\Scripts\python.exe -m pytest -q

# lint-only fast check (if ruff installed)
.\.venv\Scripts\python.exe -m ruff check .
```

## Core Services

```powershell
# start FastAPI backend
.\.venv\Scripts\python.exe -m uvicorn server.app:app --reload

# launch UI (Vite dev server)
npm run dev --prefix ui

# combined dev task (if using VS Code task runner)
code --command workbench.action.tasks.runTask "dev:all"
```

## AI Evidence Ops

```powershell
# quick sanity test against Azure OpenAI deployment
.\.venv\Scripts\python.exe tools\test_ai.py

# backfill AI analysis for recent evidence runs
.\.venv\Scripts\python.exe tools\ai_processor.py

# list available Azure AI models / deployments
.\.venv\Scripts\python.exe tools\list_models.py
.\.venv\Scripts\python.exe tools\check_deployments.py
```

## Agent Workflows

```powershell
# run Twin Judgments infographic agent
.\.venv\Scripts\python.exe -m agents.cli agents/workflows/infographic_twin_judgments.yaml --base-url http://127.0.0.1:8000

# run media companion (audio prototype)
.\.venv\Scripts\python.exe -m agents.cli agents/workflows/media_companion_agent.yaml --var audio_path="C:\\path\\to\\track.wav" --var context_tags="resonance,lumina"

# generic agent run passing variables
.\.venv\Scripts\python.exe -m agents.cli agents/workflows/<workflow>.yaml --var key=value
```

## Data & Packaging

```powershell
# build evidence pack for run <id>
Invoke-WebRequest -OutFile data/evidence_packs/<id>_bundle.zip "http://127.0.0.1:8000/pack/<id>"

# export runs to CSV
.\.venv\Scripts\python.exe analysis\export_csv.py
```

## Housekeeping

```powershell
# format JSON/Markdown using Prettier (requires npm install --prefix ui already)
npx prettier --write "docs/**/*.md"

# clean transient data (keep canonical runs)
powershell -Command "Remove-Item -Recurse -Force data\runs\temp_*"
```

> Keep large SDK archives (e.g., JDK zips) outside the repo or add explicit ignore rules before copying into the workspace.
