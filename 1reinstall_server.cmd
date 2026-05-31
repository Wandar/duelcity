@echo off

echo delete ./scripts and ./server
if exist scripts rd /s /q scripts
if exist server rd /s /q server

echo Start downloading server.zip
set url=https://d2jy77o3yhb82u.cloudfront.net/server.zip
.\wget.exe %url% -O server.zip
IF %ERRORLEVEL% NEQ 0 (
    start %url%
    echo =========================================
    echo Browser has been invoked for download. Please unzip the downloaded zip file into this folder.
    echo 已调用浏览器进行下载,请把下载完成的zip文件解压到此文件夹内.
    echo =========================================
    pause
    exit
)
echo The download is complete, please wait for unzipping...

unzip.exe -o -q server.zip
echo Successfully downloading and unzipping server,press any key to exit

pause