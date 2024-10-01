import numpy as np

notes = [ 'A', 'A#', 'B','C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
octaves = np.arange(0, 9)
frequencies = []

for octave in octaves:
    for note in notes:
        frequency = 440 * (2 ** (octave - 4 + (notes.index(note) / 12)))
        frequencies.append(frequency)

note_freq_array = np.array(frequencies)
note_freq_array_2 = list(zip(9*notes,note_freq_array))

note_freq_array = np.append(note_freq_array,0)

# Read the file
data = np.loadtxt('TMP/out.txt')
#data = np.fromfile('TMP/out.bin', dtype=np.float32)
#data = data.reshape(-1, 3)

# Filter rows based on confidence
#data = data[data[:, 2] != 0]

def find_closest_frequency(number):
    absolute_diff = np.abs(note_freq_array - number)
    closest_index = np.argmin(absolute_diff)
    closest_frequency = note_freq_array[closest_index]
    return closest_frequency


# Update frequency values if confidence is low
for i in range(0, len(data)):

    if (data[i, 2] < 0.5 and i != 0) :
        data[i, 1] = data[i-1, 1]  # Set frequency to the previous value
    elif data[i, 2] < 0.5 :
        data[i, 1] = data[i+1, 1]
        #print(data[i,1])

    closest_freq = find_closest_frequency(data[i,1])
    data[i,1] = closest_freq



count=0
sum = 0
confidence = 0
last_value = -1
data_2 = np.array([])

for i in range(0, len(data)):
    value = data[i,1]
    time = data[i,0]
    confidence_tmp = data[i,2]
    if value == last_value or last_value == -1:
        sum+=time
        confidence += confidence_tmp
        count += 1
        last_value = value
    else:
        data_2 = np.append(data_2,[last_value, sum, (confidence / count)],axis = 0)
        count=0
        sum = 0
        confidence = 0
        last_value = -1


#stacked_array = np.vstack((array1, array2))

# #print(data_2.shape)
data_2 = data_2.reshape(int(len(data_2)/3),3)
#data_2 = data_2[:,0:2] # kiszedi a confidence-t
#0 hang 1 idő 2 confidence
to_delete = []
for i in range(1,len(data_2)-1):
    if((data_2[i, 1] < 0.1) and (data_2[i-1, 0] == data_2[i+1, 0])):
        data_2[i-1, 1] += data_2[i, 1]
        data_2[i-1, 1] += data_2[i+1, 1]
        to_delete.append(i)
        to_delete.append(i+1)
    elif((data_2[i, 1] < 0.05)): to_delete.append(i) #0.1 > s
    elif(data_2[i, 2] < 0.70 and round(data_2[i,0]) != 0):
         to_delete.append(i)


data_2 = np.delete(data_2,to_delete, axis = 0)
#print(to_delete)
# a = np.array([1,2,3,4,5,6])
# print(a)
# print(a.reshape(2,3))
data_2 = data_2[:,0:2]
np.savetxt('TMP/processed.txt', data_2, fmt='%.3f', delimiter='\t')

