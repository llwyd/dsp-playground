import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp
import q_arithmetic as q_math


num_samples = 4096
fs = 44100
f = 100

phi = 0.5
delta = 0.1

s = np.sin(phi)
c = np.cos(phi)

s_delta = np.sin(delta)
c_delta = np.cos(delta)

# 0.5 + 0.1
y = s*c_delta + c*s_delta

