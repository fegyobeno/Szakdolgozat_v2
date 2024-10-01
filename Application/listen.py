import os
import sys
import paho.mqtt.client as mqtt

# Check if there is an argument and if it is a number
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    MAX_MESSAGES = int(sys.argv[1])
    print(f"Listening for {MAX_MESSAGES} message(s)...")
else:
    print("Please provide the number of messages to receive as an argument.")
    sys.exit(1)

# Define the MQTT broker details
BROKER = 'MosquittoBroker'
PORT = 1883
TOPIC = 'pitches/+'
#MAX_MESSAGES = 10  # Set the maximum number of messages to receive

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
def on_message(client, userdata, msg):
    global number_of_messages  # Declare the variable as global
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    file_path = os.path.join(SAVE_DIR, topic.replace('/', '_') + '.musicxml')
    
    with open(file_path, 'a') as f:
        f.write(payload + '\n')
    
    print(f"Message received on topic {topic}: {payload}")
    
    # Increment the message count
    number_of_messages += 1
    
    # Stop the loop if the desired number of messages has been received
    if number_of_messages >= MAX_MESSAGES:
        print(f"Received {MAX_MESSAGES} message(s). Disconnecting...")
        client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# This will keep the script running to listen for incoming messages until MAX_MESSAGES is reached.
client.loop_forever()
