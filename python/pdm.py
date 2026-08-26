import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import dsp

siglen_s = 0.1 # seconds of audio
fs = 48000
siglen = int(siglen_s * fs)

v_ref = 1.65
f = 1000
t = np.linspace(0,siglen - 1, siglen)
x_t = np.linspace(0,siglen_s, siglen)
x = np.sin(2 * np.pi * f * t/fs) * v_ref

pdm_fs = 3072000
pdm_siglen = int(pdm_fs * siglen_s)
pdm = np.zeros(pdm_siglen)
pdm_t = np.linspace(0, siglen_s,pdm_siglen)

fs_ratio = int(pdm_fs / fs)

y = np.zeros(siglen)
integrator = 0
comparator = 0
output = 0
feedback = [-v_ref,v_ref]

k = 0
for i in range(siglen):
    for j in range(fs_ratio):
        err = x[i] - output
        integrator += err
        if integrator > 0:
            comparator = 1
        else:
            comparator = 0
        pdm[k] = comparator * v_ref
        output = feedback[comparator]
        k += 1

cutoff = fs / 2
lpf = signal.butter(1, cutoff, 'lowpass',fs=pdm_fs,output = 'sos')

# LPF + decimate
z = signal.sosfilt(lpf,pdm)
z = z[::fs_ratio]

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(x_t,(x + 1) / 2)
plt.step(pdm_t,pdm)
plt.subplot(2,1,2)
#plt.plot(x_t,(x + 1) / 2)
plt.plot(x_t,x)
plt.plot(x_t,z)

plt.figure(2)
plt.step(pdm_t,pdm)
#plt.plot(x_t,(x + v_ref) / 2)
plt.plot(x_t,x)
plt.xlim(0,0.001)
plt.ylim(-v_ref - 0.01, v_ref + 0.01)
plt.legend(['PDM','Analogue signal'])
plt.title('PDM encoding of 1kHz tone')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()
