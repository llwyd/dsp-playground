import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp
import q_arithmetic as q_math


def coeff_calculator(f,fs):
    y = np.zeros(4)

    for i in range(4):
        y[i] = np.sin(2 * np.pi * (f/fs) * i )
        print(f'y[{i}] = {y[i]})')


    A = y[2] / y[1]

    B = (y[3]-(A * y[2])) / y[1]

    print(f'A: {A}')
    print(f'B: {B}')

    return A, B, y[1]

num_samples = 4096
f = 18000
fs = 44100
max_val = (1<<31) - 1

a,b,c = coeff_calculator(f,fs)

A = np.int32( (a / 2) * max_val)
B = np.int32( b * max_val)
y = np.zeros(3,dtype=np.int32)
z = np.zeros(num_samples,dtype=np.int64)

y[0] = 0x0
y[1] = np.int32(c*max_val)
y[2] = 0x0


for i in range(num_samples):

    temp_0 = np.int64((np.int64(A) * np.int64(y[1]))  >> 31)

    temp_1 = np.int64(temp_0 + temp_0)

    temp_2 = np.int64(temp_1 - np.int64(y[2]))

    y[0] = np.int32(temp_2)

    y[2] = y[1]
    y[1] = y[0]
    
    z[i] = y[0]

Y,Yf,Ydb = dsp.fft(z,fs,num_samples,norm='ortho')

plt.subplot(2,1,1)
plt.plot(z)
plt.subplot(2,1,2)
plt.semilogx(Yf,Ydb)
plt.show()

