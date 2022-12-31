import numpy as np
import matplotlib.pyplot as plt
import noise


fs = 48000
sig_len = 4096

white_u32 = noise.U32BitNoiseGenerator(seed=0x87654321)
noise_u32 = noise.U32BitNoiseGenerator(seed=0x12345678)

y_u32 = np.zeros(sig_len,dtype=np.uint32)
x_u32 = np.zeros(sig_len,dtype=np.uint32)
z_u32 = np.zeros(sig_len,dtype=np.uint32)

y_u64 = np.zeros(sig_len, dtype=np.uint64)


for i in range(sig_len):
    white_u32.Update()
    noise_u32.Update()
    x_u32[i] = noise_u32.value
    y_u32[i] = white_u32.value

    y_u64[i] = np.uint64(x_u32[i]) + np.uint64(y_u32[i])
    y_shifted = y_u64[i] >> np.uint64(1)

    z_u32[i] = np.uint32(y_shifted)



plt.subplot(2,1,1)
plt.plot(y_u32)
plt.plot(x_u32)
plt.subplot(2,1,2)
plt.plot(y_u64)
plt.plot(z_u32)
plt.show()
