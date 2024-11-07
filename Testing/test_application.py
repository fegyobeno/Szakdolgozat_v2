import subprocess
import time
from termcolor import colored
import sys
import threading
import numpy as np
import music21
import os
from music21 import converter


ALL_TESTS = 6
TESTS_PASSED = 0

def get_number_of_instruments(t) -> int:
    while True:
        try:
            #t = int(input("PLEASE ENTER THE NUMBER OF INSTRUMENTS [Integer]:\n"))
            t = int(t)
            if t > 0:
                return t
            else:
                return 0 
        except ValueError:
            return -1

def check_user_input_number_of_instruments() -> bool:
    try:
        assert get_number_of_instruments(5) == 5
        assert get_number_of_instruments(0) == 0
        assert get_number_of_instruments(-30) == 0
        assert get_number_of_instruments("almafa") == -1
        assert get_number_of_instruments("") == -1
        print(colored('The handling of user input is correct', 'green'))
        return True
    except AssertionError:
        print(colored("The handling of user input is not correct", 'red'))
        return False

#
#python3 ../Application/mqtt_publish_message.py 172.29.130.221 system/testingTopic/start start
#python3 ../Application/mqtt_publish_message.py 172.29.130.221 system/testingTopic/end end 
def check_sending_message_to_nodes(host, ip, broker_ip) -> bool:
    try:
        result = subprocess.run([".\check_messaging.bat", line[1], line[0], lines[0][1]], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        result = result.stdout.strip().split('\n')
        #print(result)
        if result[-1] == "true":
            print(colored(f"Messaging works correctly on {host}@{ip}", 'green'))
            return True
        else:
            print(colored(f"Messaging does not work correctly on {host}@{ip}", 'red'))
            return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def check_recogniser():
    try:
        result = subprocess.run([".\check_recogniser.bat"], check=True, timeout=1000)
        result.check_returncode()  # Ensure the subprocess completed successfully
        
        with open('TMP/out.txt', 'r') as file:
            lines = file.readlines()
            lines = [x.strip().split() for x in lines]
            if len(lines[0]) == 3 and all(all(is_float(element) for element in line) for line in lines):
                print(colored("The output of the recogniser is correct", 'green'))
                return True
            else:
                print(colored("The output of the recogniser is incorrect", 'red'))
                return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def check_processer(config_file) -> bool:
    notes = [ 'A', 'A#', 'B','C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    octaves = np.arange(0, 9)
    frequencies = []

    for octave in octaves:
        for note in notes:
            frequency = 440 * (2 ** (octave - 4 + (notes.index(note) / 12)))
            frequencies.append(frequency)

    note_freq_array = np.round(np.array(frequencies),1)
    note_freq_array_2 = list(zip(9*notes,note_freq_array))
    #print(note_freq_array)
    try:
        result = subprocess.run(["python3", "../Application/process.py",config_file], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully

        with open(config_file, "r") as c_file:
            lines = c_file.readlines()
            lines = [x.strip().split(";") for x in lines]
            #print(lines)

        with open('TMP/processed.txt', 'r') as file:
            processed_lines = file.readlines()
            processed_lines = [x.strip().split() for x in processed_lines]
            processed_lines = [(np.round(float(x[0]),1), float(x[1])) for x in processed_lines]

        if lines[0][1].upper() == "chromatic".upper():
            return all([x[0] in note_freq_array for x in processed_lines])
        elif lines[0][1].upper() == "pentatonic".upper():
            t_notes = [ 'A', 'C', 'D', 'E', 'G']
            note_freq_array_2 = [item for item in note_freq_array_2 if item[0][0:] in t_notes]
            note_freq_array = np.array([freq for note, freq in note_freq_array_2])
            return all([x[0] in note_freq_array for x in processed_lines])
        else:
            t_notes = lines[0][1].strip('[]').replace("'", "").split(',')
            note_freq_array_2 = [item for item in note_freq_array_2 if item[0][0:] in t_notes]
            note_freq_array = np.array([freq for _, freq in note_freq_array_2])
            return all([x[0] in note_freq_array for x in processed_lines])

    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def check_converting_to_musescore() -> bool:
    try:
        result = subprocess.run(["python3", "../Application/convert_to_musescore.py"], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        try:
            score = music21.converter.parse('TMP/output.musicxml')
            if score:
                print(colored("The generated MusicXML is valid", 'green'))
                return True
            else:
                print(colored("The generated MusicXML is invalid", 'red'))
            return False
        except Exception as e:
            print(colored(f"An error occurred while validating MusicXML: {e}", 'red'))
            return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def check_combining_sheets() -> bool:
    try:
        result = subprocess.run(["python3", "../Application/unification.py"], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        # Calculate the number of files in the messages folder ending with .musicxml
        messages_folder = 'messages'
        musicxml_files = [f for f in os.listdir(messages_folder) if f.endswith('.musicxml')]
        num_files = len(musicxml_files)

        # Check if the musescore/combined_sheet.musicxml has that many parts
        combined_sheet = converter.parse('musescore/combined_sheet.musicxml')
        if len(combined_sheet.parts) == num_files:
            print(colored("The combined sheet has the correct number of parts", 'green'))
            return True
        else:
            print(colored("The combined sheet does not have the correct number of parts", 'red'))
            return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

if __name__ == "__main__":
    with open('../Blueprint/nodelist.txt', 'r') as _file:
        lines = _file.readlines()
        lines = [x.split('|') for x in lines]
    
    #check_user_input_number_of_instruments()
    for line in lines[:2]:
        pass
        if check_sending_message_to_nodes(line[0], line[1], lines[0][1]):
           TESTS_PASSED += 1

    if check_recogniser():
        TESTS_PASSED += 1

    if check_processer("TMP/config_chromatic.txt") and check_processer("TMP/config_pentatonic.txt") and check_processer("TMP/config_custom.txt"):
        print(colored("The processer works correctly", 'green'))
        TESTS_PASSED += 1

    if check_combining_sheets():
        TESTS_PASSED += 1

    if check_converting_to_musescore():
        TESTS_PASSED += 1

    print(colored("----------------------Testing The Application : completed----------------------", 'blue'))
    if TESTS_PASSED == ALL_TESTS:
        print(colored("All tests passed", 'green'))
    elif TESTS_PASSED == 0:
        print(colored("All tests failed", 'red'))
    else:
        print(colored(f"{TESTS_PASSED}/{ALL_TESTS} tests passed", 'yellow'))
        print(colored(f"{ALL_TESTS - TESTS_PASSED}/{ALL_TESTS} tests failed", 'red'))
    