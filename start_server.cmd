@echo off
set KBE_SCRIPT=%cd%
set KBE_ROOT=%cd%/server
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%KBE_SCRIPT%/;%KBE_SCRIPT%/scripts/;%KBE_SCRIPT%/game_logic/;%KBE_SCRIPT%/res/;
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/
set IS_BH_VER=1



if defined UID (
    set uid=%UID%
    echo UID found in environment: %uid%
) else (
    set /a uid=%RANDOM% %% 30000 + 1
    echo UID not found, generated random UID: %uid%
)


echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%
echo uid=%uid%


SET status=1
(TASKLIST|FIND /I "machine.exe"||SET status=0) 2>nul 1>nul
IF %status% EQU 1 (
	@echo off
    taskkill /f /t /im baseapp.exe
    taskkill /f /t /im cellapp.exe
    taskkill /f /t /im logger.exe
    taskkill /f /t /im machine.exe
    taskkill /f /t /im dbmgr.exe
    taskkill /f /t /im baseappmgr.exe
    taskkill /f /t /im cellappmgr.exe
    taskkill /f /t /im interfaces.exe
    taskkill /f /t /im loginapp.exe
)

if "%1"=="1" (
  set HIDE=0
) else (
  set HIDE=1
)


::Create localip.txt in the current directory and write the local machine's internal IP address to force specify the internal IP
set INTERNAL_IP=

if exist "%KBE_SCRIPT%\localip.txt" (
    for /f "usebackq delims=" %%i in ("%KBE_SCRIPT%\localip.txt") do set INTERNAL_IP=%%i
)

:: copy and replace IP
powershell -Command "(Get-Content '.\res\server\kbengineOrigin.xml') -replace '(<internalInterface>).*?(</internalInterface>)', '${1}%INTERNAL_IP%${2}' -replace '(<externalInterface>).*?(</externalInterface>)', '${1}%INTERNAL_IP%${2}' | Set-Content '.\res\server\kbengine.xml' -Encoding UTF8"

echo xml set IP:%INTERNAL_IP%



start /MIN /HIGH "logger" %KBE_BIN_PATH%/logger.exe --cid=1000 --gus=100 --hide=0
start /MIN /HIGH "machine" %KBE_BIN_PATH%/machine.exe --cid=2000 --gus=200 --hide=%HIDE%
start /MIN /HIGH "dbmgr" %KBE_BIN_PATH%/dbmgr.exe --cid=4000 --gus=400 --hide=0
start /MIN /HIGH "baseappmgr" %KBE_BIN_PATH%/baseappmgr.exe --cid=5000 --gus=500 --hide=%HIDE%
start /MIN /HIGH "cellappmgr" %KBE_BIN_PATH%/cellappmgr.exe --cid=6000 --gus=600 --hide=%HIDE%
start /MIN /HIGH "interfaces" %KBE_BIN_PATH%/interfaces.exe --cid=3000 --gus=300 --hide=%HIDE%
start /MIN /HIGH "loginapp" %KBE_BIN_PATH%/loginapp.exe --cid=9000 --gus=900 --hide=%HIDE%
start /MIN /HIGH "baseapp" %KBE_BIN_PATH%/baseapp.exe --cid=1 --gus=1 --hide=0
start /MIN /HIGH "cellapp" %KBE_BIN_PATH%/cellapp.exe --cid=8000 --gus=800 --hide=0



SET hasguiconsole=1
(TASKLIST|FIND /I "guiconsole.exe"||SET hasguiconsole=0) 2>nul 1>nul
IF %hasguiconsole% EQU 0 (
	@echo off
	start %KBE_ROOT%/kbe/tools/server/guiconsole/guiconsole.exe
)

exit