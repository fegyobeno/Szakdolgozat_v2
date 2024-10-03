#!/bin/bash

mkdir TMP
echo $(hostname)
python3 listen_node.py $(hostname)

python3 pitch_detection.py TMP/*.wav
python3 process.py
python3 convert_to_musescore.py

hostname=$(hostname)

mosquitto_pub -h MosquittoBroker -t "ControlNode/$hostname" -f TMP/*.musicxml

rm -rf TMP