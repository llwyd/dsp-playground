import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp
import q_arithmetic as q_math


num_samples = 40 * 10
fs = 44100



A = np.int16(0x7e66)
y = np.zeros(3,dtype=np.int32)
z = np.zeros(num_samples,dtype=np.int32)

y[0] = 0x0
y[1] = 0x1404
y[2] = 0x0


for i in range(num_samples):

    y[0] = (((A*y[1])>>15) + ((A*y[1])>>15)) - y[2]

    y[2] = y[1]
    y[1] = y[0]
    
    z[i] = y[0]


plt.subplot(2,1,1)
plt.plot(z)
plt.show()

