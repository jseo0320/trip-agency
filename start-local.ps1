$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$runtimeDirectory = Join-Path $projectRoot '.local-logs'
$pythonExecutable = Join-Path $projectRoot 'backend\.venv\Scripts\python.exe'
$nodeExecutable = (Get-Command node.exe -ErrorAction Stop).Source
New-Item -ItemType Directory -Path $runtimeDirectory -Force | Out-Null
$env:USE_MOCK_DATA = 'true'
$backend = Start-Process -FilePath $pythonExecutable -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000' -WorkingDirectory (Join-Path $projectRoot 'backend') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtimeDirectory 'backend.log') -RedirectStandardError (Join-Path $runtimeDirectory 'backend-error.log') -PassThru
$frontend = Start-Process -FilePath $nodeExecutable -ArgumentList 'node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','5173','--strictPort' -WorkingDirectory (Join-Path $projectRoot 'frontend') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtimeDirectory 'frontend.log') -RedirectStandardError (Join-Path $runtimeDirectory 'frontend-error.log') -PassThru
@{backend=$backend.Id;frontend=$frontend.Id} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runtimeDirectory 'local-processes.json')
Write-Output 'Frontend: http://localhost:5173'
Write-Output 'Backend: http://localhost:8000/docs'
