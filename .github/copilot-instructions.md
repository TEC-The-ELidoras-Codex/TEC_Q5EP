
# Copilot instructions for TEC_Q5EP

This repo powers TEC_Q5EP — a FastAPI backend + minimal TS UI, plus docs, agents, and a local RAG scaffold. Follow these patterns to stay productive and on‑brand.

## Architecture (big picture)
- Backend: `server/` (FastAPI). Endpoints in `server/app.py`, data models in `server/models.py`. Test clients in `server/tests/*`.
- UI: `ui/` is a lightweight TS/Vite front end (dev via `npm run dev --prefix ui`).
- Content + Agents: `content_hub/` (local retrieval TF‑IDF style), `agents/prompt_agent.py` (staged prompt generator scaffold).
- Docs: `docs/` holds Prompt Goddess engine, ROM theory, CPP pitch, and guides referenced from README.
- Data flow: POST `/submit` writes a run under `data/runs/<id>` (note.txt, optional photo, metadata.json). GET `/pack/{id}` zips the run to `data/evidence_packs/<id>_bundle.zip` and streams it back.

## Developer workflow
- Python 3.13 with a local venv at `.venv`.
  - Tests: run `& .\.venv\Scripts\python.exe -m pytest -q` or VS Code task "tests:server".
  - Server: `& .\.venv\Scripts\python.exe -m uvicorn server.app:app --reload` or task "server:run".
  - UI: `npm run dev --prefix ui` or task "ui:dev".
- Combined dev: task "dev:all" (compound) runs API + UI together.
- Tests rely on `conftest.py` making repo root importable and `server/__init__.py` to make `server` a package.
- Git hygiene: large binaries and transient outputs are ignored. Evidence packs live under `data/evidence_packs/`.

## Conventions & patterns
- API contracts
  - Submit: `POST /submit` accepts multipart form: `photo?`, `note`, `timestamp`, `user_id?`, `consent`, `tags (csv)`, `gps json?`, `device json?`, `context json?`. Returns `"OK <run_id>"`.
  - Runs: `GET /runs` → `[RunSummary]` with `id, timestamp, tags, has_photo, note_chars`.
  - Pack: `GET /pack/{run_id}` → application/zip; also persists a copy under `data/evidence_packs/`.
- Filesystem layout: `data/runs/<id>/metadata.json|note.txt|photo.jpg` is canonical. Avoid changing names without updating tests.
- Models: see `server/models.py` (Pydantic v2). Prefer `model_validate_json`/`model_dump_json` used in the app.
- RAG: `content_hub/` is local-first (no external services by default). Keep it deterministic and small until a switch to a hosted search.
- Prompting: See `docs/PROMPT_GODDESS_README.md` and `docs/COPILOT_ROM_PROMPT_GUIDE.md` for staged prompt structure and evaluation cues.

## Examples to follow
- Writing run metadata: `server/app.py` `submit()` uses a small helper to parse optional JSON fields safely. Mirror this pattern for new fields.
- Packing artifacts: `pack_run()` writes ZIPs to `data/evidence_packs/` and returns `FileResponse`. Ensure parent dirs exist before writing.
- Tests: `server/tests/test_pack_endpoint.py` shows a full flow: submit → list → pack. Use `TestClient(app)` for API tests.

## External deps & integration
- Python: fastapi, uvicorn[standard], pydantic v2, httpx, pandas/numpy, scikit-learn. Install via `pip install -r requirements.txt`.
- Node: UI `ui/package.json` (Vite). Dev only — no build pipeline required unless extended.
- No cloud services required to run. Azure/Runway/Blender are discussed in docs but optional.

## When adding code
- Keep endpoints idempotent when possible and persist under `data/` using clear, human-legible files.
- Update or add tests under `server/tests/` for any new API or changed behavior.
- Avoid large binaries in Git; drop outputs in `data/` and keep `.gitignore` rules intact.
- Align prompts/agents with the staged pattern in `docs/*` and keep agent scaffolds deterministic.

If anything here is unclear or missing, leave a note in an issue or ask for an update to this file.
