import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy import stats
import random
import dsp
from tqdm import trange
import noise
import random
from enum import Enum

num_samples = 8192
num_sources = 12
offset = num_sources / 2
fs = 48000

x = np.zeros(num_samples,dtype=np.float32)
y = np.zeros(num_samples,dtype=np.float32)
white = 0.0

for i in range(num_samples):
    white = 0.0
    for j in range(num_sources):
        white += random.random()
    x[i] = ( white - offset )


top = np.max(x)
for i in range(num_samples):
    y[i] = ( random.random() * top * 2 ) - (top)

X, Xf, Xdb = dsp.fft(x, fs, len(x),norm='ortho' )
Y, Yf, Ydb = dsp.fft(y, fs, len(x),norm='ortho' )

bins = 40
plt.figure(1)
plt.subplot(2,1,2)
plt.hist(x, density=True,bins=bins,histtype='step')
plt.hist(y, density=True,bins=bins,histtype='step')
plt.subplot(2,2,1)
plt.semilogx(Xf,Xdb)
plt.subplot(2,2,2)
plt.semilogx(Yf,Ydb)

plt.show()

