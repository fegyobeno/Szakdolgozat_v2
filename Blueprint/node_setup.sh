#!/bin/bash

sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

#sudo apt update

sudo apt install mosquitto-clients -y

sudo apt install python3-pip -y

pip install --upgrade tensorflow
pip install crepe
pip install music21

mkdir TMP
cd TMP
touch out.txt
cd ..