import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy import stats
import random
import dsp
from tqdm import trange
import noise

# A 1/f/sup gamma / power spectrum noise sequence generator
# G. Corsini; R. Saletti
# 10.1109/19.9825

# y[n] = x[n] - (b * x[n-1]) + (a * y[n-1])
def first_order_lpf(x, b, a):
    y = np.zeros(len(x))

    for n in range(len(y)):
        y[n] = x[n] - (b * x[n - 1]) + (a * y[n - 1])
    return y


def get_slope(x, y):
    slope, _, _, _, _ = stats.linregress(x, y)
    return slope


def generate_pole(i, N, h, gamma, c):
    return np.exp(-2 * np.pi * np.power(10, (((i - N) / h) - (gamma / (2 * h)) - c)))


def generate_zero(i, N, h, gamma, c):
    return np.exp(-2 * np.pi * np.power(10, ((i - N) / h) - c))


fc = fs = 1000

n = 4  # number of decades
h = 3  # number of poles per decade
N = n * h  # number of first order sections
gamma = 1
c = 0

a = []
b = []


for i in range(N):
    a.append(generate_pole(i, N, h, gamma, c))
    b.append(generate_zero(i, N, h, gamma, c))

num_samples = 32768
ir = signal.unit_impulse(num_samples)

ideal_db, ideal_f = dsp.generate_decade_line(-23.8, 100000)
y = ir

for i in range(N):
    y = first_order_lpf(y, b[i], a[i])

Y, Yf, Ydb = dsp.fft(y, fs, len(y), norm="ortho")

plt.semilogx(Yf, Ydb)
plt.semilogx(ideal_f, ideal_db)
plt.xlim(0.031, int(fs / 2))
plt.ylabel("Magnitude (dB)")
plt.xlabel("Frequency (Hz)")
plt.grid(which="both")
plt.show()
