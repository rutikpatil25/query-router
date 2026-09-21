@echo off
setlocal

rem Start the FastAPI backend and Streamlit frontend.
rem The PowerShell launcher handles process cleanup when it exits.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0launch.ps1"

if errorlevel 1 (
    echo.
    echo The project launcher exited with an error.
    pause
)

endlocal
