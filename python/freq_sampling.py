import numpy as np
import matplotlib.pyplot as plt
import dsp
from scipy import signal


sig_len = 513
fs = 44100

ideal_mag = np.zeros(sig_len)
ideal_phase = np.zeros(sig_len)
f = (fs/2) * np.linspace(0,1,int(sig_len))

ideal_mag[:] = 1.0
ideal_mag[1:] = ideal_mag[1:] / f[1:]
mag_db = 20*np.log10(ideal_mag)


# Convert to rectangular form
rect = np.zeros(sig_len,dtype=np.complex128)
for i in range(sig_len):
    real = ideal_mag[i] * np.cos(ideal_phase[i])
    imag = ideal_mag[i] * np.sin(ideal_phase[i])
    
    comp = real + (imag * 1j)
    rect[i] = comp

fft_len = int(np.power(2, np.ceil(np.log2(sig_len))))
raw_impulse = np.fft.ifft(rect, fft_len)

filt = raw_impulse.real

# New filter len
N = 400
# Shift
filt = np.roll(filt,int(N/2))

# Truncate
h = filt[:N+1]
h0 = h

# Window
w = np.blackman(len(h))
h = h * w

sig_len = 512
x = np.zeros(sig_len)
x[0] = 1.0

y = np.convolve(x,h)

fft_len = int(np.power(2, np.ceil(np.log2(len(h)))))
H,Hf,Hdb = dsp.fft(h,fs,fft_len,norm='ortho')
H0,H0f,H0db = dsp.fft(h0,fs, fft_len,norm='ortho')

fft_len = int(np.power(2, np.ceil(np.log2(sig_len))))
Y,Yf,Ydb = dsp.fft(y,fs,fft_len,norm='ortho')

plt.semilogx(Yf,Ydb);
plt.semilogx(Hf,Hdb);
plt.semilogx(H0f,H0db);
plt.semilogx(f,mag_db);
plt.show()





