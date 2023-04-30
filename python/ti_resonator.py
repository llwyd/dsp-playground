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
f = 500
fs = 44100

a,b,c = coeff_calculator(f,fs)

A = np.int16( (a / 2) * 32767)
B = np.int16( b * 32767)
y = np.zeros(3,dtype=np.int16)
z = np.zeros(num_samples,dtype=np.int32)

y[0] = 0x0
y[1] = np.int16(c*32767)
y[2] = 0x0


for i in range(num_samples):

    temp_0 = np.int32((np.int32(A) * np.int32(y[1]))  >> 15)

    temp_1 = np.int32(temp_0 + temp_0)

    temp_2 = np.int32(temp_1 - np.int32(y[2]))

    y[0] = np.int16(temp_2)

    y[2] = y[1]
    y[1] = y[0]
    
    z[i] = y[0]

Y,Yf,Ydb = dsp.fft(z,fs,num_samples,norm='ortho')

plt.subplot(2,1,1)
plt.plot(z)
plt.subplot(2,1,2)
plt.semilogx(Yf,Ydb)
plt.show()

