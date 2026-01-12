import dsp
import fp_dsp as fp
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import q_arithmetic as qmath
from scipy.io.wavfile import write

order = 1
fs = 48000
sig_len = fs
q = 30

t = np.linspace(0,sig_len - 1, sig_len)
x = np.sin(np.pi * 2 * 1 * 1/fs * t)


x_q = qmath.to_q32(x,30)
write('test.wav',fs,x_q)
plt.plot(x)
plt.show()
