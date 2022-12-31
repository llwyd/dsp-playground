import numpy as np
import matplotlib.pyplot as plt
import noise


fs = 48000
sig_len = 4096
white = noise.NoiseGenerator()

y = np.zeros(sig_len)

for i in range(sig_len):
    white.Update()
    y[i] = white.value

plt.plot(y)
plt.show()
