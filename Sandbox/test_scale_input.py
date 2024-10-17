import numpy as np
import sys

if len(sys.argv) < 2:
    print("Please provide a file path as an argument.")
    sys.exit(1)

file_path = sys.argv[1]

try:
    with open(file_path, 'r') as file:
        content = file.read().strip().split(';')
        print(content)
except FileNotFoundError:
    print(f"File not found: {file_path}")

notes = []
if content[1].upper() == "chromatic".upper():
    notes = [ 'A', 'A#', 'B','C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
elif content[1].upper() == "pentatonic".upper():
    notes = [ 'A', 'C', 'D', 'E', 'G']
else:
    print(len(content))
    print(content[1])
    notes = content[1].strip('[]').replace("'", "").split(',')
    #notes = content[1].strip('[]').replace("'", "").split(',')

octaves = np.arange(0, 9)
frequencies = []

for octave in octaves:
    for note in notes:
        frequency = 440 * (2 ** (octave - 4 + (notes.index(note) / 12)))
        frequencies.append(frequency)

note_freq_array = np.array(frequencies)
note_freq_array_2 = list(zip(9*notes,note_freq_array))

print(note_freq_array)

note_freq_array = np.append(note_freq_array,0)

print(note_freq_array_2)