from instrument import Instrument
import os
import platform
import threading

print("WELCOME TO LAMPION - A MULTI PITCH SOUND RECOGNITION SOFTWARE")
print("-------------------------------------------------------------")
print("IN THE FIRST STEP YOU CAN SET UP EACH INSTRUMENT INDIVIDUALLY")
print("or")
print("YOU CAN USE A GENERAL INSTRUMENT FOR A QUICKER SETUP BUT GENERALLY WORSE RESULTS")

def get_number_of_instruments() -> int:
    while True:
        try:
            return int(input("PLEASE ENTER THE NUMBER OF INSTRUMENTS [Integer]:\n"))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


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
        if instrument_scale == "custom":
            print("PLEASE ENTER THE PITCHES OF THE INSTRUMENT SEPERATED BY COMMAS")
            pitches = input().split(",")
            instrument_scale = [float(pitch) for pitch in pitches]

        #TODO: Ask for the location of the wav file corresponding to the instrument
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
            #TODO: Launch the client for the instrument
            print("-------------------")
            break
        else:
            print("INSTRUMENT SETUP CANCELLED - PLEASE TRY AGAIN")
clear_console()
print("---------------ALL INSTRUMENTS ARE SET UP---------------")
print("Initiating the recognition process...")


#TODO: send a message for the controll node as to how many instruments are connected
def initiate_controll_node():
    os.system(f"initiate_controll_node.bat {len(instruments)}")

control_thread = threading.Thread(target=initiate_controll_node)
control_thread.start()
#os.system(f"initiate_controll_node.bat {len(instruments)}")

#TODO: start a new thread for each instrument
def start_instrument_client(instrument):
    temp_file_path = os.path.join(os.getenv('TEMP'), f"{instrument.name}_{instrument.id}.txt")
    with open(temp_file_path, 'w') as temp_file:
        print(f"Writing the scale of {instrument.name} to {temp_file_path}")
        temp_file.write(str(instrument.name))
        temp_file.write(",")
        temp_file.write(str(instrument.scale))
    os.system(f"node_setup.bat {instrument.name}{instrument.id} pitches\\{instrument.wav_file} {temp_file_path}")

threads = []
for instrument in instruments:
    thread = threading.Thread(target=start_instrument_client, args=(instrument,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# for instrument in instruments:
#     temp_file_path = os.path.join(os.getenv('TEMP'), f"{instrument.name}_{instrument.id}.txt")
#     with open(temp_file_path, 'w') as temp_file:
#         print(f"Writing the scale of {instrument.name} to {temp_file_path}")
#         temp_file.write(str(instrument.name))
#         temp_file.write(",")
#         temp_file.write(str(instrument.scale))
#     #Launch and configure the client with node_setup.bat
#     #make sure to start each client with a different id
#     os.system(f"node_setup.bat {instrument.name}{instrument.id} pitches\{instrument.wav_file} {temp_file_path}")
        


#This part is not necessary anymore as instruments can be reused
#Multipass delete insturment.name
#multipass purge
control_thread.join()