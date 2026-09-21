@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "PYTHON=%PROJECT_DIR%..\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Virtual environment not found:
    echo %PYTHON%
    echo.
    echo Create or restore the project environment before starting v2.
    pause
    exit /b 1
)

start "Query Router Backend" /D "%PROJECT_DIR%" cmd /k ""%PYTHON%" -m uvicorn main:app --host 127.0.0.1 --port 8000"
start "Query Router Frontend" /D "%PROJECT_DIR%" cmd /k ""%PYTHON%" -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501"

echo FastAPI backend: http://127.0.0.1:8000
echo Swagger docs:    http://127.0.0.1:8000/docs
echo Streamlit UI:    http://127.0.0.1:8501
echo.
echo Backend and frontend are starting in separate windows.

endlocal
