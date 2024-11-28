#!/bin/bash
rm -rf messages
mkdir messages
rm -rf musescore
mkdir musescore

python3 listen_control_node.py

python3 unification.py

mosquitto_pub -h MosquittoBroker -t "ControlNode/result" -f musescore/*.musicxml

rm -rf messages