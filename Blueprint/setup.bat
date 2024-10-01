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



@REM Bróker beállítása
for /f "tokens=1,2,3 delims=|" %%a in ("%broker%") do (
    echo "Entering broker with the following credentials:"
    echo "%%b"
    echo "%%a"
    echo "%%c"
    echo "Executing command on broker VM..."
    (
        echo "Executing multiple commands on broker VM..."
        plink %%b -l %%a -pw %%c "echo 'First command on broker VM' && echo 'Second command on broker VM' && echo 'Third command on broker VM'"
    )
    echo "Exiting broker VM..."
)

@REM ControlNode beállítása

@REM Node-ok beállítása

endlocal