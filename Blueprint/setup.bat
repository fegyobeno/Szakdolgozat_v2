@echo off
@REM Adatok beolvasása a fileból
setlocal enabledelayedexpansion

set "nodelist=nodelist.txt"
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

set REPO_URL=https://github.com/fegyobeno/Szakdolgozat_v2.git

@REM Bróker beállítása
@REM A broker be van állítva
@REM for /f "tokens=1,2,3 delims=|" %%a in ("%broker%") do (
@REM     echo "Entering broker with the following credentials:"
@REM     echo "%%b"
@REM     echo "%%a"
@REM     echo "%%c"
@REM     (
@REM         echo "Executing multiple commands on broker VM..."
@REM         plink %%b -l %%a -pw %%c "echo 'First command on broker VM' && echo 'Second command on broker VM' && echo 'Third command on broker VM'"
@REM     )
@REM     echo "Exiting broker VM..."
@REM )

@REM ControlNode beállítása
@REM https://dev.to/arc42/enable-ssh-access-to-multipass-vms-36p7
@REM ssh vmuser@172.27.135.229 -i Virtual_ENV/multipass-ssh-key
for /f "tokens=1,2,3 delims=|" %%a in ("%control_node%") do (
    echo "Entering ControlNode with the following credentials:"
    echo "%%b"
    echo "%%a"
    echo "%%c"
    (
        echo "Executing multiple commands on control node VM..."
        ssh %%a@%%b -i ../Virtual_ENV/multipass-ssh-key "if [ -d 'Szakdolgozat_v2' ]; then rm -rf Szakdolgozat_v2; fi && git clone %REPO_URL% && cd Szakdolgozat_v2 && chmod +x Blueprint/control_node_setup.sh && ./Blueprint/control_node_setup.sh"
    )
    echo "Exiting control node VM..."
    
)

@REM Node-ok beállítása
for %%n in (%nodes:;= %) do (
    for /f "tokens=1,2,3 delims=|" %%a in ("%%n") do (
        echo "Entering node with the following credentials:"
        echo "%%b"
        echo "%%a"
        echo "%%c"
        (
            echo "Executing multiple commands on node VM..."
            ssh %%a@%%b -i ../Virtual_ENV/multipass-ssh-key "if [ -d 'Szakdolgozat_v2' ]; then rm -rf Szakdolgozat_v2; fi && git clone %REPO_URL% && cd Szakdolgozat_v2 && chmod +x Blueprint/node_setup.sh && ./Blueprint/node_setup.sh"
        )
        echo "Exiting node VM..."
    )
)


endlocal