import paho.mqtt.client as mqtt
import os
import sys

with open("../Blueprint/nodelist.txt", "r") as file:
    first_line = file.readline().strip()
    broker_ip = first_line.split('|')[1]

BROKER = broker_ip
TOPIC = "Result"

SAVE_DIR = "TMP"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
        topic = msg.topic   
        payload = msg.payload
        file_path = os.path.join(SAVE_DIR, topic.replace('/', '_'))+".musicxml"
        print(f"{topic} {file_path}")
        with open(file_path, 'wb') as f:
            f.write(payload)

        client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
