import paho.mqtt.client as mqtt
import sys

# Define the MQTT broker details
broker = f'{sys.argv[1]}' 
port = 1883
topic = f'{sys.argv[2]}' 

# Define the file to be published
file_path = f'{sys.argv[3]}'

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    with open(file_path, 'rb') as file:  # Open the file in binary mode
        file_content = file.read()
        client.publish(topic, file_content)
        print(f"Published file content to topic {topic}")
    client.disconnect()

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_connect callback function
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Start the loop to process network traffic and dispatch callbacks
client.loop_forever()
