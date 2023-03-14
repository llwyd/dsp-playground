import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp


num_samples = 4096
fs = 48000
f = 1000
A = 1;

w = ( 2*np.pi*f )/ fs

b0 = A*np.sin(w)
a1 = -2 * np.cos(w)
a2 = 1

x = signal.unit_impulse(num_samples)
y = np.zeros(num_samples)

for i in range(num_samples):
    y[i] = ( x[i] * b0 ) - (a1*y[i-1]) - (a2 * y[i-2])

plt.plot(y)
plt.show()

