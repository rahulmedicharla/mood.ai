from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np

fs, amplitude = read('audio_file.wav')


avg_amplitude = np.mean(np.abs(amplitude))
print(avg_amplitude)