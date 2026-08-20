@echo off
title PF BRIDGE - visible command console
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0pf_bridge.ps1"
echo.
echo [PF BRIDGE stopped]
pause
