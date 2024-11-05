@echo off
setlocal

REM Get the input parameters
set USER=%1
set HOST=%2
set SSH_KEY_PATH=%3

REM Command to check MQTT connection
REM Copy the local script to the remote machine
scp -i %SSH_KEY_PATH% connect_to_broker.py %USER%@%HOST%:/tmp/script.py

REM Execute the script on the remote machine
ssh -i %SSH_KEY_PATH% %USER%@%HOST% "python3 /tmp/script.py"

endlocal