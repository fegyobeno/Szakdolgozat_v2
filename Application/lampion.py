from instrument import Instrument
import os
import platform
import threading
import subprocess

def get_number_of_instruments() -> int:
    while True:
        try:
            t = int(input("PLEASE ENTER THE NUMBER OF INSTRUMENTS [Integer]:\n"))
            if t > 0:
                return t
            else:
                return 0 
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

with open("../Blueprint/nodelist.txt", "r") as file:
    first_line = file.readline().strip()
    broker_ip = first_line.split('|')[1]

print(f"Broker IP: {broker_ip}")

print(chr(sum(range(ord(min(str(not()))))))) # prints char 3486
clear_console() # clears the console
print("WELCOME TO LAMPION - A MULTI PITCH SOUND RECOGNITION SOFTWARE")
print("-------------------------------------------------------------")
print("IN THE FIRST STEP YOU CAN SET UP EACH INSTRUMENT INDIVIDUALLY")
print("or")
print("YOU CAN USE A GENERAL INSTRUMENT FOR A QUICKER SETUP BUT GENERALLY WORSE RESULTS")

number_of_instruments = get_number_of_instruments()
instruments = []

# Main loop for setting up the instruments
for i in range(number_of_instruments):
    clear_console()
    while True:
        clear_console()
        print(f"INSTRUMENT {i + 1} SETUP")
        print("-------------------")
        print("PLEASE ENTER THE NAME OF THE INSTRUMENT")
        instrument_name = input().upper()
        print("PLEASE ENTER THE SCALE OF THE INSTRUMENT[pentatonic,chromatic,custom]")
        instrument_scale = input().upper()
        if instrument_scale == "CUSTOM":
            print("PLEASE ENTER THE PITCHES OF THE INSTRUMENT SEPERATED BY COMMAS")
            pitches = input().split(",")
            instrument_scale = [pitch.upper() for pitch in pitches]

        #Ask for the location of the wav file corresponding to the instrument
        while True:
            print("PLEASE ENTER THE LOCATION OF THE WAV FILE (relative to the pitches folder):")
            wav_file_location = input()+".wav"
            full_path = os.path.join("pitches", wav_file_location)
            if os.path.isfile(full_path):
                break
            else:
                print("The file does not exist. Please enter a valid file location.")

        temp_instrument = Instrument(instrument_name, i, instrument_scale, wav_file_location)
    
        print(f"The instrument defined is {temp_instrument}")
        print("CONFIRM THE INSTRUMENT SETUP! THIS CANNOT BE CHANGED LATER [Y/N]")
        confirmation = input().upper()
        if confirmation == "Y":
            print(f"{i + 1}. INSTRUMENT: {instrument_name} -> SETUP COMPLETED")
            instruments.append(temp_instrument)
            print("-------------------")
            break
        else:
            print("INSTRUMENT SETUP CANCELLED - PLEASE TRY AGAIN")
clear_console()
print("---------------ALL INSTRUMENTS ARE SET UP---------------")
print("Initiating the recognition process...")


#Send a message for the controll node as to how many instruments are connected
def initiate_controll_node():
    #os.system(f"python3 mqtt_publis_message.py pitches/initiate_control_node {len(instruments)}")
    subprocess.run(["python3", "mqtt_publish_message.py", broker_ip, "ControlNode/initiate_control_node", str(len(instruments))])

control_thread = threading.Thread(target=initiate_controll_node)
control_thread.start()

#Send the files to the nodes usingn mqtt 
def start_instrument_node(instrument, node):
    subprocess.run(["python3", "mqtt_publish_message.py",broker_ip, f"system/{node}/start", f"start"])
    temp_file_path = os.path.join(os.getenv('TEMP'), f"{instrument.name}_{instrument.id}.txt")
    with open(temp_file_path, 'w') as temp_file:
        print(f"Writing the scale of {instrument.name} to {temp_file_path}")
        temp_file.write(str(instrument.name))
        temp_file.write(";")
        temp_file.write(str(instrument.scale))

    subprocess.run(["python3", "mqtt_publish_file.py",broker_ip, f"system/{node}/{instrument.name}_{instrument.id}.txt", temp_file_path])
    subprocess.run(["python3", "mqtt_publish_file.py",broker_ip, f"system/{node}/{instrument.wav_file}", f"pitches/{instrument.wav_file}"])    
    
    subprocess.run(["python3", "mqtt_publish_message.py",broker_ip, f"system/{node}/end", f"end"])

threads = []
node = ["Node1", "Node2", "Node3", "Node4"]
for i in range(0,len(instruments)):
    thread = threading.Thread(target=start_instrument_node, args=(instruments[i],node[i],))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

control_thread.join()