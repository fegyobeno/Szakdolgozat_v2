#!/usr/bin/env python3
#pip install paho-mqtt
import paho.mqtt.client as mqtt
import sys

# MQTT broker details
#TODO: Somehow get the adress of the broker automatically from multipass list
broker = f"MosquittoBroker"  # Replace with your broker address
port = 1883  # Default MQTT port

# Define the MQTT client
client = mqtt.Client()

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("True")
    else:
        print("False", rc)


# Assign the callback functions
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker, port)

# Start the network loop
client.loop_start()


# Stop the network loop and disconnect
client.loop_stop()
client.disconnect()


