import soundfile as sf
from sys import argv
from numpy import average, hsplit, shape, split, std, reshape
from scipy import signal, stats
import re
import os

def checkspec(audio_file):

    # Find the minimum amount of samples to use without reading entirely empty data              #
    # The framecount starting value could be as low as 256, but false positives start to happen  #
    # below that.                                                                                #
    data = 0
    framecount = 5000
    while (average(data) == 0):
        data, samplerate = sf.read(audio_file, frames=framecount)
        framecount *= 2

    # Extract only one channel of the audio data, since the spectrogram can't process 2D arrays. #
    old_shape = data.shape[0]
    data_1d = reshape(data, data.shape[0]*2)[:old_shape-1]
    split_data = hsplit(data, 2)[0]
    data_one_channel = split_data.flatten()

    # Generate spectrogram.
    f, t, Sxx = signal.spectrogram(data_one_channel, samplerate, mode='magnitude')


    # Get average amplitude of each frequency band.
    averages = []
    for value in Sxx:
        averages.append(average(value))

    # The actual detector for determining transcoded FLACs.                                      #
    # Checks if the average amplitude of the 20.625 KHz band (Inside the frequency cutoff range  #
    # is significantly lower than the average of the 13.8k - 16k bands.                          #
    average_average = average(averages[80:92])
    da_secret_sauce = (average(Sxx[120])-average_average)/average_average
    if (da_secret_sauce < -0.985):
        print(audio_file)

# Check if file argument exists.
if (len(argv) == 1):
    directory = "."
else:
    directory = argv[1]

# Recursively traverse directory for FLAC files.
for root, dir, files in os.walk(directory):
    for name in files:
        result = re.search('.*\.flac$', name)
        if (result is not None):
                checkspec(os.path.join(root, name))
