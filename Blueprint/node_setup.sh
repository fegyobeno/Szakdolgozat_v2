#!/bin/bash

sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

#sudo apt update

sudo apt install mosquitto-clients -y

sudo apt install python3-pip -y

sudo pip install --upgrade tensorflow
sudo pip install crepe
sudo pip install music21
suod pip install paho-mqtt

mkdir TMP
cd TMP
touch out.txt
cd ..