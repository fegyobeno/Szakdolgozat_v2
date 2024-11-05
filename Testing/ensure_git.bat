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
set "FOLDER_PATH=Szakdolgozat_v2"
set "EXPECTED_GIT_URL=https://github.com/fegyobeno/Szakdolgozat_v2.git"

REM SSH into the VM and check the folder and git source
ssh -i "%SSH_KEY%" "%USERNAME%@%IP_ADDRESS%" "if [ -d %FOLDER_PATH% ]; then echo True; else echo False; fi && cd %FOLDER_PATH% && git remote get-url origin"

endlocal