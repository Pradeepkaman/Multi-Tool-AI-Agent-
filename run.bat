@echo off
title Multi-Tool Autonomous AI Agent
cls
echo ===================================================
echo     Multi-Tool Autonomous AI Agent Launcher
echo ===================================================
echo.
echo Select an option:
echo   [1] Start Interactive Console Agent
echo   [2] Run Multi-Tool Compound Benchmark (Offline Mock Mode)
echo   [3] Run Multi-Tool Compound Benchmark (Active LLM)
echo   [4] Run All Unit and Integration Tests
echo   [5] Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    python src/main.py
) else if "%choice%"=="2" (
    python src/main.py --mock --benchmark
) else if "%choice%"=="3" (
    python src/main.py --benchmark
) else if "%choice%"=="4" (
    echo Running standalone tool tests...
    python tests/test_tools.py
    echo.
    echo Running ReAct compound integration test...
    python tests/test_agent_flow.py
) else (
    echo Exiting...
)
pause
