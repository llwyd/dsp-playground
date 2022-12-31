import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy import stats
import random
import dsp
from tqdm import trange
import noise

def trailing_bits(num):
    bits = bin(num)
    return len(bits) - len(bits.rstrip('0'))

def get_slope( x, y ):
    slope, _, _, _, _ = stats.linregress( x, y )
    return slope

def voss(num_samples,generators):
    rollover = 2**( generators - 1 )
    noise_array = []
    x = np.zeros(num_samples)
    white = 0.0

    white_noise = noise.NoiseGenerator()
    white_noise.Update()

    for i in range(generators):
        noise_array.append(noise.NoiseGenerator())
        noise_array[i].Update()
        white = white+noise_array[i].value

    white = white+white_noise.value

    # Voss-McCartney pink noise algorithm
    counter = 1
    indices = np.zeros(num_samples)
    for i in range(num_samples):
        index = trailing_bits(counter)
        indices[i] = index
    
        noise_array[index].Update()
        white_noise.Update()

        white = white - white_noise.prev_value
        white = white + white_noise.value

        white = white - noise_array[index].prev_value;
        white = white + noise_array[index].value;
        x[i] = white

        counter = ( counter & (rollover - 1) )
        counter = counter + 1

    x = dsp.norm(x)
    return x, indices

fs = 48000
num_samples = 4096 * 4
num_tests = 4
generators = 16

print(f'Voss-McCartney Pink Noise Generator')
print(f'    Sample Rate: {fs}') 
print(f'         Length: {num_samples} Samples ({num_samples*(1/fs):.2f}s)') 
print(f'  Noise sources: {generators}')
print(f'Test iterations: {num_tests}')
print(f'Generating...')

Ydb = np.zeros(int(num_samples/2))
Yf = []
for i in trange(num_tests):
    x, indices = voss(num_samples,generators)
    X, Xf, Xdb = dsp.fft(x, fs, len(x),norm='ortho' )
    Ydb = np.add(Ydb,Xdb)

Zdb = Ydb / num_tests

ideal_db, ideal_f = dsp.generate_decade_line(20, 100000)

plt.figure(1)
plt.semilogx( Xf, Xdb )
plt.semilogx( Xf, Zdb )
plt.semilogx( ideal_f, ideal_db )

plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')
#plt.figure(2)
#plt.stem(indices)
plt.show()

