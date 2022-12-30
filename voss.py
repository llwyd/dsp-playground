import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy import stats
import random
import dsp
from tqdm import trange



class NoiseGenerator():
    def Update(self):
        self.prev_value = self.value
        self.value = (random.random() * 2) - 1

    def __init__(self):
        self.value = 0
        self.prev_value = 0

def trailing_bits(num):
    bits = bin(num)
    return len(bits) - len(bits.rstrip('0'))

def get_slope( x, y ):
    slope, _, _, _, _ = stats.linregress( x, y )
    return slope

def voss(num_samples):
    generators = 16
    rollover = 2**( generators - 1 )
    noise = []
    x = np.zeros(num_samples)
    white = 0.0

    white_noise = NoiseGenerator()
    white_noise.Update()

    for i in range(generators):
        noise.append(NoiseGenerator())
        noise[i].Update()
        white = white+noise[i].value

    white = white+white_noise.value

    # Voss-McCartney pink noise algorithm
    counter = 1
    indices = np.zeros(num_samples)
    for i in range(num_samples):
        index = trailing_bits(counter)
        indices[i] = index
    
        noise[index].Update()
        white_noise.Update()

        white = white - white_noise.prev_value
        white = white + white_noise.value

        white = white - noise[index].prev_value;
        white = white + noise[index].value;
        x[i] = white

        counter = ( counter & (rollover - 1) )
        counter = counter + 1

    x = dsp.norm(x)
    return x, indices

def generate_decade_line(start_mag, end_freq):
    iterations = int(np.log10( end_freq ) )
    iterations += 1

    mags = np.zeros(iterations)
    freqs = np.zeros(iterations)

    for i in range( iterations ):
        mags[i] = start_mag
        freqs[i] = ( 10 ** i )

        start_mag -= 10

    return mags, freqs


fs = 48000
num_samples = 4096 * 4
num_tests = 1

Ydb = np.zeros(int(num_samples/2))
Yf = []
for i in trange(num_tests):
    x, indices = voss(num_samples)
    X, Xf, Xdb = dsp.fft(x, fs, len(x),norm='ortho' )
    Ydb = np.add(Ydb,Xdb)

Zdb = Ydb / num_tests

ideal_db, ideal_f = generate_decade_line(20, 100000)

ideal_slope = get_slope(ideal_f, ideal_db )
Zdb_slope = get_slope( Xf, Zdb )

print("Ideal Slope: " + str( ideal_slope ) )
print("  Zdb Slope: " + str( Zdb_slope ) )

plt.figure(1)
plt.semilogx( Xf, Xdb )
plt.semilogx( Xf, Zdb )
plt.semilogx( ideal_f, ideal_db )

plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')
#plt.figure(2)
#plt.stem(indices)
plt.show()

