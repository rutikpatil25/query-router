# Launches the FastAPI backend and Streamlit frontend in separate terminals.
# Press Enter or Ctrl+C in this window to stop both applications.

$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $projectDir
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Virtual environment not found: $python"
}

function Get-DescendantProcessIds {
    param([int]$ParentId)

    $children = Get-CimInstance Win32_Process -Filter "ParentProcessId = $ParentId"
    foreach ($child in $children) {
        $child.ProcessId
        Get-DescendantProcessIds -ParentId $child.ProcessId
    }
}

function Stop-ProcessTree {
    param([System.Diagnostics.Process]$Process)

    if ($null -eq $Process -or $Process.HasExited) {
        return
    }

    $descendants = @(Get-DescendantProcessIds -ParentId $Process.Id)
    foreach ($processId in ($descendants | Sort-Object -Descending)) {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
    Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
}

$backend = $null
$frontend = $null

try {
    $backendArguments = "-NoProfile -NoExit -Command `"Set-Location -LiteralPath '$projectDir'; & '$python' -m uvicorn main:app --host 127.0.0.1 --port 8000`""
    $frontendArguments = "-NoProfile -NoExit -Command `"Set-Location -LiteralPath '$projectDir'; & '$python' -m streamlit run app.py --server.port 8501`""

    $backend = Start-Process -FilePath "powershell.exe" -ArgumentList $backendArguments -WorkingDirectory $projectDir -PassThru
    $frontend = Start-Process -FilePath "powershell.exe" -ArgumentList $frontendArguments -WorkingDirectory $projectDir -PassThru

    Write-Host "FastAPI:   http://127.0.0.1:8000"
    Write-Host "Swagger:   http://127.0.0.1:8000/docs"
    Write-Host "Streamlit: http://127.0.0.1:8501"
    Write-Host ""
    Write-Host "Press Enter or Ctrl+C to stop both applications."
    Read-Host
}
finally {
    Stop-ProcessTree -Process $backend
    Stop-ProcessTree -Process $frontend
    Write-Host "Backend and frontend stopped."
}
