import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
from scipy.io import wavfile
import dsp


fs = 48000
sig_len = 8192

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')

plt.show()
