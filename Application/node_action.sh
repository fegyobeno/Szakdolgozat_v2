#!/bin/bash

mkdir TMP

python3 listen_node.py $(hostname)

python3 pitch_detection.py TMP/*.wav
python3 process.py
python3 convert_to_musescore.py

hostname=$(hostname)

mosquitto_pub -h MosquittoBroker -t "pitches/$hostname" -f TMP/*.musicxml

rm -rf TMP