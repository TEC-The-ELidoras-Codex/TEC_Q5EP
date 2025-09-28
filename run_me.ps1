Param([int]$Port = 8000)
Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) { py -3.12 -m venv .venv }
.\.venv\Scripts\pip.exe install -U pip
.\.venv\Scripts\pip.exe install -r requirements.txt
$env:PYTHONPATH = "$PWD"
.\.venv\Scripts\python.exe -m uvicorn server.app:app --reload --host 0.0.0.0 --port $Port
