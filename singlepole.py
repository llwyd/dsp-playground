import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp

fs = 48000
order = 1
sig_len = 4096 * 16

fc = 2000
cutoff = dsp.get_alpha( fc, fs )

print("Cutoff: " + str(fc) + "Hz")
print("Alpha: " + str(cutoff) )

y = dsp.ewma( cutoff, sig_len )
Y, Yf, Ydb = dsp.fft( y, fs, sig_len)

plt.semilogx(Yf,Ydb)
plt.axvline(x=fc)
plt.axhline(y=-3)
plt.show()

