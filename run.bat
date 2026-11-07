@echo off
title Multi-Tool Autonomous AI Agent
cls
echo ===================================================
echo     Multi-Tool Autonomous AI Agent Launcher
echo ===================================================
echo.
echo Select an option:
echo   [1] Start Professional Web UI (Browser Interface)
echo   [2] Start Interactive Console Agent (CLI REPL)
echo   [3] Run Multi-Tool Compound Benchmark (Offline Mock Mode)
echo   [4] Run Multi-Tool Compound Benchmark (Active LLM)
echo   [5] Run All Unit and Integration Tests
echo   [6] Exit
echo.
set /p choice="Enter choice (1-6): "

if "%choice%"=="1" (
    echo Starting Web Server...
    echo Open your browser at http://127.0.0.1:5000
    python src/web_app.py
) else if "%choice%"=="2" (
    python src/main.py
) else if "%choice%"=="3" (
    python src/main.py --mock --benchmark
) else if "%choice%"=="4" (
    python src/main.py --benchmark
) else if "%choice%"=="5" (
    echo Running standalone tool tests...
    python tests/test_tools.py
    echo.
    echo Running ReAct compound integration test...
    python tests/test_agent_flow.py
) else (
    echo Exiting...
)
pause

