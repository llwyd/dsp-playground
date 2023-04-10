import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp
import q_arithmetic as q_math


num_samples = 4000
fs = 44100
f = 20

phi = 0.01
delta = 0.01

q = 15

#phi_q = q_math.float_to_q16bit(phi,q,True)
#delta_q = q_math.float_to_q16bit(delta,q,True)

s = np.sin(phi)
c = np.cos(phi)
s_delta = np.sin(delta)
c_delta = np.cos(delta)

s_q = q_math.float_to_q16bit(s,q,True)
c_q = q_math.float_to_q16bit(c,q,True)
s_delta_q = q_math.float_to_q16bit(s_delta,q,True)
c_delta_q = q_math.float_to_q16bit(c_delta,q,True)


# 0.5 + 0.1
x_s = s*c_delta + c*s_delta
x_c = c*c_delta - s*s_delta

x_s_q = q_math.mul16(s_q,c_delta_q,q) + q_math.mul16(c_q,s_delta_q,q)
x_c_q = q_math.mul16(c_q,c_delta_q,q) - q_math.mul16(s_q,s_delta_q,q)

y_s = np.zeros(num_samples)
y_c = np.zeros(num_samples)

y_s_q = np.zeros(num_samples,dtype=np.int16)
y_c_q = np.zeros(num_samples,dtype=np.int16)

y_s[0] = x_s
y_c[0] = x_c

y_s_q[0] = x_s_q
y_c_q[0] = x_c_q

for i in range(1,num_samples):

    y_s[i] = y_s[i-1]*c_delta + y_c[i-1]*s_delta
    y_c[i] = y_c[i-1]*c_delta - y_s[i-1]*s_delta

    y_s_q[i] = q_math.mul16(y_s_q[i-1],c_delta_q,q) + q_math.mul16(y_c_q[i-1],s_delta_q,q)
    y_c_q[i] = q_math.mul16(y_c_q[i-1],c_delta_q,q) - q_math.mul16(y_s_q[i-1],s_delta_q,q)

plt.plot(y_s)
plt.plot(y_c)
plt.show()

