#!/usr/bin/env python3
#pip install paho-mqtt
import paho.mqtt.client as mqtt
import sys

# MQTT broker details
#TODO: Somehow get the adress of the broker automatically from multipass list
broker = "172.27.85.49"  # Replace with your broker address
port = 1883  # Default MQTT port
topic = f"{sys.argv[1]}"  # Replace with your topic
message = f"{sys.argv[2]}"  # Message to publish

# Define the MQTT client
client = mqtt.Client()

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed with code", rc)

def on_publish(client, userdata, mid):
    print("Message published")

# Assign the callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(broker, port)

# Start the network loop
client.loop_start()

# Publish the message
result = client.publish(topic, message)

# Wait for the message to be published
result.wait_for_publish()

# Stop the network loop and disconnect
client.loop_stop()
client.disconnect()


