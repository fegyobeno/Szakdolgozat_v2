@echo off
set vmuser=%1
set ipaddress=%2
set brokeraddress=%3

if "%vmuser%"=="" (
    echo Usage: %0 vmuser ipaddress brokeraddress
    exit /b 1
)

if "%ipaddress%"=="" (
    echo Usage: %0 vmuser ipaddress brokeraddress
    exit /b 1
)

set success=true

start cmd /c ssh %vmuser%@%ipaddress% -i ../Virtual_ENV/multipass-ssh-key "cd Szakdolgozat_v2 && cd Application && python3 listen_node.py testingTopic "
if errorlevel 1 (
    set success=false
)

start cmd /c python3 C:\Users\Benedek\Documents\ELTE\Szakdolgozat_v2\Application\mqtt_publish_message.py %brokeraddress% system/testingTopic/start start
if errorlevel 1 (
    set success=false
)

start cmd /c python3 C:\Users\Benedek\Documents\ELTE\Szakdolgozat_v2\Application\mqtt_publish_message.py %brokeraddress% system/testingTopic/end end
if errorlevel 1 (
    set success=false
)

if "%success%"=="true" (
    echo true
) else (
    echo false
)