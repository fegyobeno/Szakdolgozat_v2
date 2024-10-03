import paho.mqtt.client as mqtt
import os
import sys

BROKER = "MosquittoBroker"
TOPIC = f"system/{sys.argv[1]}/+"
OUTPUT_TOPIC = f"ControlNode/{sys.argv[1]}"
watching = False

SAVE_DIR = "TMP"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global watching
    if msg.topic == f"system/{sys.argv[1]}/end" or msg.topic == f"system/{sys.argv[1]}/start":
        message = msg.payload.decode()
        print(f"{message} {msg.topic}")    
        if message == "start" and not watching:
            print("Received start message, starting to watch for files...")
            watching = True
        elif message == "end" and watching: 
            print("Received end message, stopping...")
            watching = False
            client.disconnect()
    else:
        if watching:
            topic = msg.topic   
            payload = msg.payload
            file_path = os.path.join(SAVE_DIR, topic.replace('/', '_'))
            print(f"{topic} {file_path}")
            with open(file_path, 'wb') as f:
                f.write(payload)
        else:
            pass


def publish_file(client, file):
    with open(file, 'rb') as f:
        file_content = f.read()
    client.publish(OUTPUT_TOPIC, file_content)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
