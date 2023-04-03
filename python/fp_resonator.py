import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp
import q_arithmetic as q_math


num_samples = 4096
fs = 44100
f = 100
A = 0.9999;

q = 14

w = ( 2*np.pi*f )/ fs

b0 = A*np.sin(w)
a1 = -2 * np.cos(w)
a2 = 1

w_q = q_math.float_to_q16bit(w,q,True)
b0_q = q_math.float_to_q16bit(b0,q,True)
a1_q = q_math.float_to_q16bit(a1,q,True)
a2_q = q_math.float_to_q16bit(a2,q,True)

x = signal.unit_impulse(num_samples)
y = np.zeros(num_samples)

x_q = q_math.float_to_q16bit(x,q)
y_q = q_math.float_to_q16bit(y,q)

for i in range(num_samples):
    y[i] = ( x[i] * b0 ) - (a1*y[i-1]) - (a2 * y[i-2])

    temp_0 = np.int16((np.int32(x_q[i]) * np.int32(b0_q)) >> q)
    temp_1 = np.int16((np.int32(y_q[i-1]) * np.int32(a1_q)) >> q)
    temp_2 = np.int16((np.int32(y_q[i-2]) * np.int32(a2_q)) >> q)

    y_q[i] = temp_0 - temp_1
    y_q[i] = y_q[i] - temp_2

plt.subplot(2,1,1)
plt.plot(y)
plt.subplot(2,1,2)
plt.plot(y_q)
plt.show()

