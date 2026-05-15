@echo off
setlocal
cd /d "%~dp0"
.venv\Scripts\python.exe src\launch_war3_windowed.py %*
