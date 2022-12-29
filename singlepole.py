import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp

fs = 48000
order = 1
sig_len = 4096 * 16

fc = 200
cutoff = dsp.get_alpha( fc, fs )

print("Cutoff: " + str(fc) + "Hz")
print("Alpha: " + str(cutoff) )

y = dsp.ewma( cutoff, sig_len )
x = dsp.ewma( dsp.get_alpha( 2000, fs ), sig_len )

z = dsp.norm( x + y )
Y, Yf, Ydb = dsp.fft( y, fs, sig_len, norm=None)
X, Xf, Xdb = dsp.fft( x, fs, sig_len, norm=None)
Z, Zf, Zdb = dsp.fft( z, fs, sig_len, norm=None)

plt.semilogx(Yf,Ydb)
plt.semilogx(Xf,Xdb)
plt.semilogx(Zf,Zdb)
plt.axvline(x=fc)
plt.axhline(y=-3)
plt.show()

