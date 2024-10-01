@echo off
@rem Létrehozza a brokert

multipass list | findstr /C:"MosquittoBroker" >nul
if %errorlevel% neq 0 (
    multipass launch appliance:mosquitto -n MosquittoBroker

    multipass transfer mosquitto_broker_setup.sh MosquittoBroker:/home/ubuntu/mosquitto_broker_setup.sh

    multipass exec MosquittoBroker -- chmod +x /home/ubuntu/mosquitto_broker_setup.sh

    multipass exec MosquittoBroker -- /home/ubuntu/mosquitto_broker_setup.sh

    @rem plink <IP> -l <user> -pw <password>

) else (
    multipass start MosquittoBroker
)

set controlNode=ControlNode
set node1=Node1
set node2=Node2

@rem Launch or start control node
multipass list | findstr /C:"%controlNode%" >nul
if %errorlevel% neq 0 (
    multipass launch jammy -n %controlNode% --cloud-init cloud-init.yaml

) else (
    multipass start %controlNode%
)

@rem Launch or start node1s
multipass list | findstr /C:"%node1%" >nul
if %errorlevel% neq 0 (
    multipass launch jammy -n %node1% --cloud-init cloud-init.yaml --disk 10G --memory 2G

) else (
    multipass start %node1%
)

@rem Launch or start node2
multipass list | findstr /C:"%node2%" >nul
if %errorlevel% neq 0 (
    multipass launch jammy -n %node2% --cloud-init cloud-init.yaml --disk 10G --memory 2G

) else (
    multipass start %node2%
)