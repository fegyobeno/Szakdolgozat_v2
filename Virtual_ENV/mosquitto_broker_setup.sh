#!/bin/bash

sudo cp /var/snap/mosquitto/common/mosquitto_example.conf /var/snap/mosquitto/common/mosquitto.conf

echo "listener 1883 0.0.0.0" | sudo tee -a /var/snap/mosquitto/common/mosquitto.conf > /dev/null

echo "allow_anonymous true" | sudo tee -a /var/snap/mosquitto/common/mosquitto.conf > /dev/null

sudo systemctl restart snap.mosquitto.mosquitto.service

echo "ubuntu:pwd" | sudo chpasswd
