import os
import sys
import paho.mqtt.client as mqtt

# Define the MQTT broker details
BROKER = 'MosquittoBroker'
PORT = 1883
TOPIC = 'pitches/+'
#MAX_MESSAGES = 10  # Set the maximum number of messages to rec eive

# Initialize a counter for the number of received messages
number_of_messages = 0

# Define the directory to save the messages
SAVE_DIR = 'messages'

# Ensure the save directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
first = True
def on_message(client, userdata, msg):
    global first
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    global number_of_messages  # Declare the variable as global
    if first:
        number_of_messages = int(payload)
        print(f"Expecting {number_of_messages} messages...")
        first = False

    else:

        file_path = os.path.join(SAVE_DIR, topic.replace('/', '_') + '.musicxml')
    
        with open(file_path, 'a') as f:
            f.write(payload + '\n')
    
        print(f"Message received on topic {topic}: {payload}")
    
        # Increment the message count
        number_of_messages -= 1
    
        # Stop the loop if the desired number of messages has been received
        if number_of_messages == 0:
            print(f"Received all the message(s). Disconnecting...")
            client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# This will keep the script running to listen for incoming messages until MAX_MESSAGES is reached.
client.loop_forever()
