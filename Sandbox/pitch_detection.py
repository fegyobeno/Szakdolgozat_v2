#$ pip install --upgrade tensorflow  # if you don't already have tensorflow >= 2.0.0
#$ pip install crepe

import sys
import crepe
from scipy.io import wavfile
import numpy

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

# Read the audio file
sr, audio = wavfile.read(f"{filename}")

# Apply the low-pass filter to the audio signal
# cutoff_freq_low = 1000  # Adjust the cutoff frequency as needed
# b_low, a_low = signal.butter(4, cutoff_freq_low, fs=sr, btype='lowpass')
# audio = signal.filtfilt(b_low, a_low, audio)

# # Apply the high-pass filter to the audio signal
# cutoff_freq_high = 1000  # Adjust the cutoff frequency as needed
# b_high, a_high = signal.butter(4, cutoff_freq_high, fs=sr, btype='highpass')
# audio = signal.filtfilt(b_high, a_high, audio)

# # Apply the median filter to the audio signal
# #audio = signal.medfilt(audio)

time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)

data = numpy.column_stack((time, frequency, confidence))

rate = data[1][0] - data[0][0]

for i in range(len(data)):
    data[i][0] = rate

numpy.savetxt('TMP/out.txt', data, fmt='%.3f', delimiter='\t')
# Save the data as a binary file
# data_binary = data.astype(numpy.float32)  # Convert data to float32 for binary storage
# with open('TMP/out.bin', 'wb') as f:
#     data_binary.tofile(f)