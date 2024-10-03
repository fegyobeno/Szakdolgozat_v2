import paho.mqtt.client as mqtt
import os

BROKER = "MosquittoBroker"
TOPIC = "system/Node"
OUTPUT_TOPIC = "pitches/Node"
watching = False

SAVE_DIR = "TMP"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global watching
    message = msg.payload.decode()
    print(f"{message} {msg.topic}")
    if watching and message != "start" and message != "end":
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        file_path = os.path.join(SAVE_DIR, topic.replace('/', '_'))
        with open(file_path, 'a') as f:
            f.write(payload + '\n')
    if message == "start" and not watching:
        print("Received start message, starting to watch for files...")
        watching = True
    elif message == "end" and watching: 
        print("Received end message, stopping...")
        watching = False
        client.disconnect()

def publish_file(client, file):
    with open(file, 'rb') as f:
        file_content = f.read()
    client.publish(OUTPUT_TOPIC, file_content)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
