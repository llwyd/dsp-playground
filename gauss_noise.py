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

num_samples = 4096
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

bins = 40
plt.figure(1)
plt.hist(x, density=True,bins=bins,histtype='step')
plt.hist(y, density=True,bins=bins,histtype='step')
plt.show()

