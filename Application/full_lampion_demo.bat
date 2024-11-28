@echo off
@REM Adatok beolvasása a fileból
setlocal enabledelayedexpansion

pip install -r requirements.txt

python3 collect_ip_addresses.py

set "nodelist=..\Blueprint\nodelist.txt"
set "broker="
set "control_node="
set "nodes="

for /f "tokens=1,2,3 delims=|" %%a in ('type "%nodelist%"') do (
    if not defined broker (
        set "broker=%%a|%%b|%%c"
    ) else if not defined control_node (
        set "control_node=%%a|%%b|%%c"
    ) else (
        set "nodes=!nodes!%%a|%%b|%%c;"
    )
)

echo "Broker: %broker%"
echo "Control Node: %control_node%"
echo "Nodes: %nodes%"

@REM ssh vmuser@172.27.135.229 -i Virtual_ENV/multipass-ssh-key
for /f "tokens=1,2,3 delims=|" %%a in ("%control_node%") do (
    echo "Entering ControlNode with the following credentials:"
    echo "%%b"
    echo "%%a"
    echo "%%c"
    (
        start %%c cmd /c ssh %%a@%%b -i ../Virtual_ENV/multipass-ssh-key "cd Szakdolgozat_v2 && cd Application && chmod +x control_node_action.sh && ./control_node_action.sh"
    )
    echo "Exiting control node VM..."
    
)

set "nodes=%nodes:;= %"
set "nodes=%nodes:|=@%"

for %%n in (%nodes%) do (
    for /f "tokens=1,2,3 delims=@" %%a in ("%%n") do (
        echo "Entering node with the following credentials:"
        echo "%%b"
        echo "%%a"
        echo "%%c"
        (
            start %%c cmd /c ssh %%a@%%b -i ../Virtual_ENV/multipass-ssh-key "cd Szakdolgozat_v2 && cd Application && chmod +x node_action.sh && ./node_action.sh"
        )
        echo "Exiting node VM..."
    )
)

python3 lampion.py

python3 listen_user.py

endlocal