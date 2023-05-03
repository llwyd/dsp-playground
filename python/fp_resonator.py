import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp
import q_arithmetic as q_math


num_samples = 4096 * 10
fs = 44100
f = 100
A = 0.94;

q = 15

w = ( 2*np.pi*f )/ fs

b0 = A*np.sin(w)
a1 = -1 * np.cos(w)
a2 = 0.5

w_q = q_math.float_to_q16bit(w,q,True)
b0_q = q_math.float_to_q16bit(b0,q,True)
a1_q = q_math.float_to_q16bit(a1,q,True)
a2_q = q_math.float_to_q16bit(a2,q,True)

x = signal.unit_impulse(num_samples)
y = np.zeros(num_samples)

x_q = q_math.float_to_q16bit(x,q)
y_q = q_math.float_to_q16bit(y,q)

y_q[0] = b0_q
y[0] = b0
for i in range(1,num_samples):
    y[i] = ( x[i] * b0 ) - ( (a1*y[i-1]) +  (a1*y[i-1])) - ((a2 * y[i-2]) + (a2 * y[i-2]))

    temp_0 = q_math.mul16(x_q[i],b0_q,q)
    temp_11 = q_math.mul16(y_q[i-1],a1_q,q)
    temp_12 = q_math.mul16(y_q[i-1],a1_q,q)
    
    temp_21 = q_math.mul16(y_q[i-2],a2_q,q)
    temp_22 = q_math.mul16(y_q[i-2],a2_q,q)

    temp_1 = np.int32(temp_11) + np.int32(temp_11)
    temp_2 = np.int32(temp_21) + np.int32(temp_22)

    temp_3 = temp_0 - temp_1
    temp_4 = temp_3 - temp_2
    y_q[i] = np.int16(temp_4)

Y,Yf,Ydb = dsp.fft(y,fs,num_samples,norm='ortho')
#lazy
Yq,Yqf,Yqdb = dsp.fft(dsp.norm(y_q),fs,num_samples,norm='ortho')

fig, ax1 = plt.subplots()

ax1.plot(y,color='tab:blue')
ax1.set_ylabel('Amplitude (float)')
ax1.set_xlabel('Samples')

ax2 = ax1.twinx()
ax2.plot(y_q,color='tab:red')
ax2.set_ylabel('Amplitude (int16)')

plt.figure(2)
plt.semilogx(Yf,Ydb)
plt.semilogx(Yqf,Yqdb)

plt.ylabel('Magnitude (dB)')
plt.xlabel('Frequency (Hz)')
plt.show()

