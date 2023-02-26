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

def first_order_iir(x, xz_1, yz_1, b, a):
    y = x - (b * xz_1) + (a * yz_1)
    return y

def get_slope(x, y):
    slope, _, _, _, _ = stats.linregress(x, y)
    return slope


def generate_pole(i, N, h, gamma, c):
    return np.exp(-2 * np.pi * np.power(10, (((i - N) / h) - (gamma / (2 * h)) - c)))


def generate_zero(i, N, h, gamma, c):
    return np.exp(-2 * np.pi * np.power(10, ((i - N) / h) - c))

num_samples = 32768
fc = fs = 1000
n = 4  # number of decades
h = 3  # number of poles per decade
N = n * h  # number of first order sections
gamma = 1
c = 0

print("Corsini and Saletti Pinking filter")
print(f"Sample Rate: {fs}Hz")
print(f"Poles per decade: {h}")
print(f"Number of decades: {n}")
print(F"Number of First-Order-Sections: {N}")

a = []
b = []

x = np.zeros([N,num_samples])

def pink_filter(b,a,num_samples):
    assert len(b) == len(a)
    pz_pairs = len(b)
    x = signal.unit_impulse(num_samples)
    y = np.zeros(num_samples)

    history = np.zeros(pz_pairs)
    
    for i in range(num_samples):
        y[i] = x[i]
        for j in range(pz_pairs):
            y[i] = first_order_iir( y[i], y[i-1],history[j],b[j],a[j])
            history[j] = y[i]

    return y


def pink_filter_debug(b,a,num_samples):
    assert len(b) == len(a)
    pz_pairs = len(b)
    x = signal.unit_impulse(num_samples)

    z = np.zeros([pz_pairs, 2])
    y = np.zeros(num_samples)
    
    history = np.zeros(pz_pairs)
    
    for i in range(num_samples):
        
        z[0][0] = z[0][1]
        z[0][1] = x[i]

        y[i] = first_order_iir( z[0][1], z[0][0],history[0],b[0],a[0])
        history[0] = y[i]
        for j in range(1, pz_pairs):
            z[j][0] = z[j][1]
            z[j][1] = y[i]

            y[i] = first_order_iir( z[j][1], z[j][0],history[j],b[j],a[j])
            history[j] = y[i]


    return y

for i in range(N):
    
    a.append(generate_pole(i, N, h, gamma, c))
    b.append(generate_zero(i, N, h, gamma, c))

ir = signal.unit_impulse(num_samples)

ideal_db, ideal_f = dsp.generate_decade_line(-23.8, 100000)
y = ir

for i in range(N):
    y = first_order_lpf(y, b[i], a[i])


z = pink_filter_debug(b,a,num_samples)
Y, Yf, Ydb = dsp.fft(y, fs, len(y), norm="ortho")
Z, Zf, Zdb = dsp.fft(z, fs, len(z), norm="ortho")

plt.semilogx(Yf, Ydb)
plt.semilogx(Zf, Zdb)
plt.semilogx(ideal_f, ideal_db)
plt.xlim(0.031, int(fs / 2))
plt.ylabel("Magnitude (dB)")
plt.xlabel("Frequency (Hz)")
plt.grid(which="both")
plt.show()
