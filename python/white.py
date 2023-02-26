import numpy as np
import matplotlib.pyplot as plt
import noise
import random

fs = 48000
sig_len = 4096

white_u32 = noise.U32BitNoiseGenerator(seed=random.getrandbits(32))
noise_u32 = noise.U32BitNoiseGenerator(seed=random.getrandbits(32))

num_sources = 4
shift = int(np.log2(num_sources))
white32 = []
for i in range(num_sources):
    white32.append(noise.U32BitNoiseGenerator(seed=random.getrandbits(32)))


x32 = np.zeros((num_sources,sig_len),dtype=np.uint32)
y64 = np.zeros(sig_len, dtype=np.uint64)

for i in range(sig_len):
    y64[i] = np.uint64(0)
    for j in range(num_sources):
        white32[j].Update()
        x32[j][i] = white32[j].value

        y64[i] = y64[i] + x32[j][i]

y32 = y64 >> shift

plt.figure(1)

plt.subplot(2,1,1)
for i in range(num_sources):
    plt.plot(x32[i])
plt.subplot(2,1,2)
plt.plot(np.int32(y32))

plt.figure(2)
plt.plot(y64)
plt.plot(y32)
plt.show()
