import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
import dsp

def calculate_bands(bands, fs):
    step = (np.log(fs/2) - np.log(20)) / (bands)
    cutoff = np.zeros(bands)
    cutoff[0] = np.exp(step)*20

    for i in range(1,bands):
        cutoff[i] = np.exp(step) * cutoff[i-1]
    cutoff = np.pad(cutoff,(1,0),'constant',constant_values=0) 

    return cutoff

num_bands = 5
fs = 48000
sig_len = fs 
fig, ax = plt.subplots(figsize=(8,6))


plt.subplots_adjust(bottom=0.35)
plt.hlines(-3,0,fs/2)
plt.xlim(20,fs/2)
plt.ylim(-30,5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')

freqs = calculate_bands(num_bands,fs)

eq_bands = []

for i in range(0,num_bands):
    eq_bands.append(dsp.EQBand(freqs[i],freqs[i+1],fs))

h = signal.unit_impulse(sig_len)
f = []
Fdb = []
Ff = []
F = []
y = np.zeros(sig_len)
for i in range(0, num_bands):
    m = signal.sosfilt(eq_bands[i].filter,h)
    y += m
    M, Mf,Mdb = dsp.fft(m, fs, sig_len)    
    f.append(m)
    F.append(M)
    Fdb.append(Mdb)
    Ff.append(Mf)
    ax.semilogx(Mf,Mdb)

Y, Yf,Ydb = dsp.fft(y, fs, sig_len)    
ax.semilogx(Yf,Ydb)

plt.show()

