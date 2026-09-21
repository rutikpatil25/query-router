@echo off
setlocal EnableExtensions

set "PROJECT_DIR=%~dp0"
set "PYTHON=%PROJECT_DIR%..\.venv\Scripts\python.exe"
set "TRAIN_SCRIPT=%PROJECT_DIR%train.py"

if not exist "%PYTHON%" (
    echo.
    echo Python virtual environment not found:
    echo %PYTHON%
    echo.
    pause
    exit /b 1
)

:menu
cls
echo.
echo ==================================================
echo                 TOOLS PANEL
echo ==================================================
echo.
echo   1] Train model
echo   2] Clear routing_history database
echo   3] Exit
echo.
choice /C 123 /N /M "Select an option: "

if errorlevel 3 goto :exit
if errorlevel 2 goto :clear_history
if errorlevel 1 goto :train_model

:train_model
cls
echo.
echo ==================================================
echo                 TRAINING MODEL
echo ==================================================
echo.
if not exist "%PROJECT_DIR%" (
    echo ERROR: Project directory not found:
    echo %PROJECT_DIR%
    echo.
    pause
    goto :menu
)

if not exist "%TRAIN_SCRIPT%" (
    echo ERROR: Training script not found:
    echo %TRAIN_SCRIPT%
    echo.
    echo Check that the training file is named train.py.
    echo.
    pause
    goto :menu
)

pushd "%PROJECT_DIR%"
if errorlevel 1 (
    echo ERROR: Could not open the project directory:
    echo %PROJECT_DIR%
    echo.
    pause
    goto :menu
)

"%PYTHON%" "%TRAIN_SCRIPT%"
set "TRAIN_EXIT=%ERRORLEVEL%"
popd
echo.
if not "%TRAIN_EXIT%"=="0" (
    echo Training failed with exit code %TRAIN_EXIT%.
) else (
    echo Training completed successfully.
)
pause
goto :menu

:clear_history
cls
echo.
echo ==================================================
echo             CLEAR ROUTING HISTORY
echo ==================================================
echo.
echo This will permanently remove all saved routing history.
choice /C YN /N /M "Continue? [Y/N]: "
if errorlevel 2 goto :menu

pushd "%PROJECT_DIR%"
"%PYTHON%" -c "from pathlib import Path; Path('routing_history.csv').write_text('timestamp,query,route,method,confidence\r\n', encoding='utf-8')"
set "CLEAR_EXIT=%ERRORLEVEL%"
popd
echo.
if not "%CLEAR_EXIT%"=="0" (
    echo Could not clear routing history.
) else (
    echo Routing history cleared. The CSV header was preserved.
)
pause
goto :menu

:exit
echo.
echo Exiting Tools Panel.
endlocal
exit /b 0
