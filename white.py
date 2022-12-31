import numpy as np
import matplotlib.pyplot as plt
import noise


fs = 48000
sig_len = 4096
white = noise.NoiseGenerator()
white_u32 = noise.U32BitNoiseGenerator()

y = np.zeros(sig_len)
y_u32 = np.zeros(sig_len,dtype=np.uint32)

for i in range(sig_len):
    white.Update()
    white_u32.Update()
    y[i] = white.value
    y_u32[i] = white_u32.value

plt.plot(y_u32)
plt.show()
