import numpy as np
import matplotlib.pyplot as plt
import dsp
from scipy import signal


fft_len = 4096
fs = 44100

ideal_mag = np.zeros(fft_len)
ideal_phase = np.zeros(fft_len)
f= (fs/2)*np.linspace(0,1,int(fft_len))

ideal_mag[:] = 1.0
ideal_mag[1:] /= f[1:]

# Convert to rectangular form

