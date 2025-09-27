# TEC_Q5EP VS Code Runbook

This drop-in guide keeps the project running smoothly from VS Code when cloned at the canonical path:

```
C:\Users\Ghedd\OneDrive - TEC - The Elidoras Codex\Projects\TEC\TEC_Q5EP
```

It covers:

1. One-time setup commands.
2. Copy-paste VS Code configs (settings, tasks, launch).
3. A quick PowerShell bootstrap script.
4. Fast diagnostics when something refuses to run.

---

## 0) Verify you’re at the right folder

Open an integrated terminal in VS Code and run:

```powershell
Get-Location; git rev-parse --show-toplevel; $env:VIRTUAL_ENV
```

You should see the **TEC OneDrive path** above. If not, close this window and open the folder from the path shown at the top of this doc.

---

## 1) One-time setup (PowerShell)

Run these **inside the repo root**. They’re idempotent.

```powershell
# Allow local scripts
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force

# Create a virtual env (tries python, then py launcher)
if (-not (Test-Path .venv)) {
  try { python -m venv .venv } catch { py -3.12 -m venv .venv }
}

# Upgrade pip + install deps
.\.venv\Scripts\pip.exe install -U pip
.\.venv\Scripts\pip.exe install -r requirements.txt

# Optional UI deps (only if you’ll use /ui)
if (Test-Path .\ui\package.json) { npm install --prefix ui }

# Create a local .env if missing
if (-not (Test-Path .env) -and (Test-Path .env.example)) { Copy-Item .env.example .env }
```

> **Tip:** if you’re using Bitwarden Secrets Manager, generate `.env` with your secrets and **do not commit it**.

---

## 2) VS Code configs (copy into `.vscode/`)

### `.vscode/settings.json`

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "files.eol": "\n",
  "editor.formatOnSave": true
}
```

### `.vscode/tasks.json`

These give you one-click actions: setup, start API, run tests, build the Copilot agent zip.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "py: setup venv",
      "type": "shell",
      "command": "if (!(Test-Path .venv)) { py -3.12 -m venv .venv }; .\\.venv\\Scripts\\pip.exe install -U pip; .\\.venv\\Scripts\\pip.exe install -r requirements.txt",
      "problemMatcher": []
    },
    {
      "label": "api: start (uvicorn)",
      "type": "shell",
      "command": ".\\.venv\\Scripts\\python.exe -m uvicorn server.app:app --reload --host 0.0.0.0 --port 8000",
      "isBackground": true,
      "problemMatcher": {
        "owner": "custom",
        "fileLocation": ["relative", "${workspaceFolder}"],
        "pattern": [{"regexp": ".*", "file": 1, "location": 2, "message": 0}],
        "background": {"activeOnStart": true, "beginsPattern": ".*Reloading.*|.*Started server process.*", "endsPattern": ".*Application startup complete.*"}
      }
    },
    {
      "label": "tests: pytest",
      "type": "shell",
      "command": ".\\.venv\\Scripts\\python.exe -m pytest -q",
      "problemMatcher": []
    },
    {
      "label": "agent: build zip",
      "type": "shell",
      "command": ".\\.venv\\Scripts\\python.exe tools\\package_agent_manifest.py",
      "problemMatcher": []
    }
  ]
}
```

### `.vscode/launch.json`

Debug the API with F5.

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug API (uvicorn)",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}\\.venv\\Scripts\\uvicorn.exe",
      "args": ["server.app:app", "--reload", "--port", "8000"],
      "cwd": "${workspaceFolder}",
      "envFile": "${workspaceFolder}\\.env"
    }
  ]
}
```

---

## 3) One-button runner (optional) — `run_me.ps1`

Save this at the repo root and run it when you just want things to “go.”

```powershell
Param([int]$Port=8000)
Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) { py -3.12 -m venv .venv }
.\.venv\Scripts\pip.exe install -U pip
.\.venv\Scripts\pip.exe install -r requirements.txt
$env:PYTHONPATH = "$PWD"
.\.venv\Scripts\python.exe -m uvicorn server.app:app --reload --host 0.0.0.0 --port $Port
```

---

## 4) How to run (fast path)

1. **Terminal → Run Task →** `py: setup venv` (first run only).
2. **Terminal → Run Task →** `api: start (uvicorn)`.
3. Open [http://localhost:8000/health](http://localhost:8000/health) — you should see `{ "ok": true }`.
4. **Terminal → Run Task →** `agent: build zip` if you’re packaging the Copilot agent.
5. (Optional) **Run Task →** `tests: pytest`.

---

## 5) If it still won’t run — Quick diagnostics

```powershell
# 1) Are we in the right place?
Get-Location; git rev-parse --show-toplevel

# 2) Does Python exist?
python --version; if ($LASTEXITCODE -ne 0) { py -3.12 --version }

# 3) Is the venv active / correct interpreter?
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"

# 4) Missing deps?
.\.venv\Scripts\pip.exe install -r requirements.txt

# 5) Port already in use?
netstat -ano | findstr :8000   # then kill the PID with: taskkill /PID <pid> /F
```

**Common fixes**

- `ModuleNotFoundError`: you’re not using the project’s venv → select interpreter: **Ctrl+Shift+P → Python: Select Interpreter → .venv**.
- `PermissionError` on scripts: run the Set-ExecutionPolicy line in section 1.
- Spaces in path: our tasks use `${workspaceFolder}` so quoting is handled; avoid hard-coding absolute paths.

---

## 6) Copilot Agent zip → where to upload

Use the `agent: build zip` task, then go to **Microsoft 365 admin center → Copilot → Agents → Deploy new agent → Upload** and select `tec_rd_queen_agent.zip`.

> If you were trying to drop the zip into **Dataverse** directly, that won’t work. Dataverse needs a table + File column or a Notes attachment. Use Power Automate to ingest files from OneDrive into Dataverse if needed.

---

## 7) Safety checklist

- `.env` is present locally (or generated), but listed in `.gitignore`.
- `requirements.txt` is up to date.
- You opened VS Code from the **TEC OneDrive path**, not the Personal one.
- Azure permissions for Foundry agents are set (data-plane **OpenAI User** role) if you call those APIs.

Once these pieces are in place, **VS Code → Run Task → api: start** will bring the server up every time. If something misbehaves, copy the failing output into chat and we’ll target the exact fix.
