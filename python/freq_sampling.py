import numpy as np
import matplotlib.pyplot as plt
import dsp
from scipy import signal


sig_len = 513
fs = 44100

ideal_mag = np.zeros(sig_len)
ideal_phase = np.zeros(sig_len)
f= (fs/2)*np.linspace(0,1,int(sig_len))

ideal_mag[:] = 1.0
#ideal_mag = ideal_mag / f
ideal_mag[1:] = ideal_mag[1:] / f[1:]
mag = 20*np.log10(ideal_mag)


# Convert to rectangular form
rect = np.zeros(sig_len,dtype=np.complex128)
for i in range(sig_len):
    real = ideal_mag[i] * np.cos(ideal_phase[i])
    imag = ideal_mag[i] * np.sin(ideal_phase[i])
    
    comp = real + (imag * 1j)
    rect[i] = comp

raw_impulse = np.fft.ifft(rect, 1024)

filt = np.abs(raw_impulse)
#filt = raw_impulse.real


N = 400
# Shift
filt = np.roll(filt,int(N/2))

# Truncate
h = filt[:N+1]
h = dsp.norm(h)

h0 = h

# Window
w = np.blackman(N+1)
h = h * w

x = np.zeros(1024)
x[0] = 1.0

y = np.convolve(x, h,mode='same')

Y,Yf,Ydb = dsp.fft(y,fs, 1024,norm='ortho')

plt.semilogx(Yf,Ydb);
plt.semilogx(f,mag);
plt.show()





