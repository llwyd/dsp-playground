import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import dsp


fs = 48000
l = 4096
cutoff = 1000

h = signal.unit_impulse(l)

lpf = signal.butter(1, cutoff, 'lowpass',fs=fs,output = 'sos')
hpf = signal.butter(1, cutoff, 'highpass',fs=fs,output = 'sos')


lpf_ir = signal.sosfilt(lpf,h)
hpf_ir = signal.sosfilt(hpf,h)

sum_ir = lpf_ir + hpf_ir

casc_ir = signal.sosfilt(lpf,h)
casc_ir = signal.sosfilt(hpf,casc_ir) + lpf_ir + hpf_ir

_, lpf_f, lpf_FFTdb = dsp.fft(lpf_ir,fs,l)
_, hpf_f, hpf_FFTdb = dsp.fft(hpf_ir,fs,l)
_, sum_f, sum_FFTdb = dsp.fft(sum_ir,fs,l)
_, casc_f, casc_FFTdb = dsp.fft(casc_ir,fs,l)

plt.semilogx(lpf_f, lpf_FFTdb)
plt.semilogx(hpf_f, hpf_FFTdb)
plt.semilogx(sum_f, sum_FFTdb)
#plt.semilogx(casc_f, casc_FFTdb)
plt.legend(['lpf','hpf','sum'])
plt.xlim(1, fs/2)
plt.ylim(-40,10)
plt.show()
