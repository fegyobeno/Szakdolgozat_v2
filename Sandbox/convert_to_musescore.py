from music21 import stream, note, duration, converter
import numpy as np
import sys

#optional initial parameter
if len(sys.argv) < 2:
    print("Default: %s => <output.musicxml>" % sys.argv[0])
    #sys.exit(1)
    outfile = 'TMP/output.musicxml'

else:
    outfile = 'TMP/' + sys.argv[1] 

durations = [1/32, 1/16, 1/8, 1/4, 1/2, 1, 2, 4, 8, 16]  # Available durations

with open('TMP/processed.txt', 'r') as file:
    lines = file.readlines()

updated_lines = []

# Process each line in the file
for line in lines:
    parts = line.strip().split('\t')
    frequency = parts[0]
    timestamp = float(parts[1])

    # Find the closest duration value
    closest_duration = min(durations, key=lambda x: abs(x - timestamp))

    # Update the timestamp with the closest duration value
    updated_line = f"{frequency}\t{closest_duration}\n"
    updated_lines.append(updated_line)

# Write the updated lines back to the file
with open('TMP/processed_mscx.txt', 'w') as file:
    file.writelines(updated_lines)
file.close()


def generate_musicxml(durations, frequencies, output_file):
    # Create a music21 Stream object to store the musical elements
    score = stream.Score()

    # Create a Part object to hold the notes
    part = stream.Part()
    score.append(part)

    # Iterate over the durations and frequencies arrays
    for dur, freq in zip(durations, frequencies):
        if freq == 0:
            # Create a Rest object for the pause
            r = note.Rest()

            # Create a Duration object with the corresponding duration value
            d = duration.Duration(dur)

            # Set the quarter length of the Rest object
            r.quarterLength = d.quarterLength

            # Add the Rest object to the Part object
            part.append(r)
        else:
            # Create a Note object with the corresponding frequency
            n = note.Note()
            n.pitch.frequency = freq

            # Create a Duration object with the corresponding duration value
            d = duration.Duration(dur)

            # Set the quarter length of the Note object
            n.quarterLength = d.quarterLength

            # Add the Note object to the Part object
            part.append(n)

    # Convert the score to MusicXML format and save to file
    score.write('musicxml', fp=output_file)

# Read the data from the file
with open('TMP/processed_mscx.txt', 'r') as file:
    lines = file.readlines()

frequencies = []
durations_beats = []

for line in lines:
    parts = line.strip().split('\t')
    frequency = float(parts[0])
    beat = float(parts[1])

    frequencies.append(frequency)
    durations_beats.append(beat)

# Calculate the durations in seconds based on a fixed tempo (e.g., 120 beats per minute)
tempo = 60
durations_seconds = [dur * (120/tempo) for dur in durations_beats]

# Convert the lists to NumPy arrays
frequencies = np.array(frequencies)
durations = np.array(durations_seconds)

# Generate the MusicXML file
generate_musicxml(durations, frequencies, outfile)
file.close()
