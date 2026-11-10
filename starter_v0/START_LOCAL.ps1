param([int]$Port = 8501)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$labPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $labPython)) {
    throw 'Create .venv and install requirements.txt first. See RUN_LOCAL.md.'
}
& $labPython -X utf8 -m streamlit run app.py --server.address 127.0.0.1 --server.port $Port --server.headless true
