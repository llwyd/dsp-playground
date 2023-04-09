import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp
import q_arithmetic as q_math


num_samples = 400
fs = 44100
f = 100

phi = 0.0
delta = 0.4

s = np.sin(phi)
c = np.cos(phi)

s_delta = np.sin(delta)
c_delta = np.cos(delta)

# 0.5 + 0.1
x_s = s*c_delta + c*s_delta
x_c = c*c_delta - s*s_delta

y_s = np.zeros(num_samples)
y_c = np.zeros(num_samples)

y_s[0] = x_s
y_c[0] = x_c

for i in range(1,num_samples):

    y_s[i] = y_s[i-1]*c_delta + y_c[i-1]*s_delta
    y_c[i] = y_c[i-1]*c_delta - y_s[i-1]*s_delta


