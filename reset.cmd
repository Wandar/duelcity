@echo off

echo reset > "%~dp0msg.txt"


timeout /t 1 /nobreak >nul

if exist msg.txt (
    echo ErrorConnecting
    pause
) else (
    echo StartReset
    timeout /t 3 /nobreak >nul
    exit
)