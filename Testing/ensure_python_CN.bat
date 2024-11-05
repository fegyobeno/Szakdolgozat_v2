@echo off
setlocal

REM Check if the correct number of parameters are provided
if "%~3"=="" (
    echo Usage: %0 username ip_address ssh_key
    exit /b 1
)

set "USERNAME=%~1"
set "IP_ADDRESS=%~2"
set "SSH_KEY=%~3"
REM Check if paho-mqtt, music21, and mosquitto_clients are installed
ssh -i "%SSH_KEY%" "%USERNAME%@%IP_ADDRESS%" "pip show paho-mqtt && pip show music21 && (command -v mosquitto_sub --version >nul 2>&1 && echo True || echo False)"

endlocal