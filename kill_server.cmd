@echo off
taskkill /f /t /im machine.exe
taskkill /f /t /im logger.exe
taskkill /f /t /im dbmgr.exe
taskkill /f /t /im baseappmgr.exe
taskkill /f /t /im cellappmgr.exe
taskkill /f /t /im baseapp.exe
taskkill /f /t /im cellapp.exe
taskkill /f /t /im loginapp.exe
taskkill /f /t /im interfaces.exe
taskkill /f /t /im bots.exe
exit
