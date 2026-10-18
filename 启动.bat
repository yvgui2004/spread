@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
python main.py
if %errorlevel% neq 0 pause
