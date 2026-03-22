@echo off
chcp 65001 >nul
title System Dashboard Server
echo.
echo  ==========================================
echo     System Dashboard Server
echo  ==========================================
echo.
echo  正在启动服务...
echo.
cd /d "%~dp0"
python server.py
pause
