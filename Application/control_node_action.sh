#!/bin/bash
rm -rf messages
mkdir messages
rm -rf musescore
mkdir musescore

python3 listen_control_node.py

python3 unification.py

rm -rf messages