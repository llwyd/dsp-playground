import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy import stats
import random
import dsp
from tqdm import trange
import noise
from enum import Enum


class Mode(Enum):
    Float = "Float"
    FloatStoch = "Float-Stochastic"
    Fixed = "Fixed Point"

class Stochastic():
    def __init__(self,p):
        self.default_p = p
        self.p = p
        self.noise = noise.NoiseGenerator()
    def Update(self):
        self.p = self.p / 2
    def Reset(self):
        self.p = self.p * 2
        if( self.p > self.default_p):
            self.p = self.default_p

def trailing_bits(num):
    bits = bin(num)
    return len(bits) - len(bits.rstrip('0'))

def get_slope( x, y ):
    slope, _, _, _, _ = stats.linregress( x, y )
    return slope

def voss(num_samples,generators):
    assert ( (generators+1) & ((generators+1) - 1) ) == 0
    shift = np.uint32(np.log2(generators+1))
    rollover = 2**( generators-1 )
    assert trailing_bits(rollover) == (generators-1)
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

        x[i] = x[i] / (generators+1)

        counter = ( counter & (rollover - 1) )
        counter = counter + 1

    return x, indices

def generate_p(generators):
    x = np.linspace(1,generators,generators)
    return 1 - np.power( 0.5, x )

def voss_stoch(num_samples,generators):
    assert ( (generators+1) & ((generators+1) - 1) ) == 0
    shift = np.uint32(np.log2(generators+1))
    rollover = 2**( generators-1 )
    assert trailing_bits(rollover) == (generators-1)
    noise_array = []
   
    p = generate_p(generators)
    previous_index = generators - 1

    x = np.zeros(num_samples)
    white = 0.0
    white_noise = noise.NoiseGenerator()
    white_noise.Update()

    for i in range(generators):
        noise_array.append(Stochastic(p[i]))
        noise_array[i].noise.Update()
        white = white+noise_array[i].noise.value

    white = white+white_noise.value

    # Voss-McCartney pink noise algorithm
    counter = 1
    indices = np.zeros(num_samples)
    for i in range(num_samples):
        index = generators - 1

        r = random.random()
        for j in range(len(noise_array)):
            if r < noise_array[j].p:
                index = j
                previous_index = j
                break

        #index = trailing_bits( int(r*(rollover)) )
        indices[i] = index
    
        noise_array[index].noise.Update()
        white_noise.Update()

        white = white - white_noise.prev_value
        white = white + white_noise.value

        white = white - noise_array[index].noise.prev_value;
        white = white + noise_array[index].noise.value;
        x[i] = white

        x[i] = x[i] / (generators+1)

        counter = ( counter & (rollover - 1) )
        counter = counter + 1

    return x, indices

def voss32(num_samples,generators):
    assert ( (generators+1) & ((generators+1) - 1) ) == 0
    shift = np.uint32(np.log2(generators+1))
    rollover = 2**( generators-1 )
    assert trailing_bits(rollover) == (generators-1)
    noise_array = []
    
    x = np.zeros(num_samples, dtype=np.uint32)
    pink = np.uint64(0)

    white_noise = noise.U32BitNoiseGenerator(seed=random.getrandbits(32))
    white_noise.Update()

    for i in range(generators):
        noise_array.append(noise.U32BitNoiseGenerator(seed=random.getrandbits(32)))
        noise_array[i].Update()
        pink = pink + np.uint64( noise_array[i].value )

    pink = pink + np.uint64( white_noise.value )
    
    counter = 1
    indices = np.zeros(num_samples)
    for i in range(num_samples):
        index = trailing_bits(counter)
        indices[i] = index
    
        noise_array[index].Update()
        white_noise.Update()

        pink = pink - np.uint64(white_noise.prev_value)
        pink = pink + np.uint64(white_noise.value)

        pink = pink - np.uint64(noise_array[index].prev_value);
        pink = pink + np.uint64(noise_array[index].value);
        pink_shifted = pink >> np.uint64(shift)

        x[i] = np.uint32(pink_shifted)

        counter = ( counter & (rollover - 1) )
        counter = counter + 1

    assert np.max(np.abs(x))<= np.uint32(0xFFFFFFFF) 
    return x, indices


fs = 48000
num_samples = 4096 * 8
num_tests = 250
generators = 15
mode = Mode.FloatStoch

print(f'Voss-McCartney Pink Noise Generator')
print(f'    Sample Rate: {fs}') 
print(f'         Length: {num_samples} Samples ({num_samples*(1/fs):.2f}s)') 
print(f'  Noise sources: {generators}')
print(f'Test iterations: {num_tests}')
print(f'Generation mode: {mode.value}')
print(f'Generating...')

Ydb = np.zeros(int(num_samples/2))
Ydb_32 = np.zeros(int(num_samples/2))
Yf = []

for i in trange(num_tests):
    if mode == Mode.Fixed:
        x, indices = voss32(num_samples,generators)
        x = dsp.norm(x)
    elif mode == Mode.Float:
        x, indices = voss(num_samples,generators)
        x = dsp.norm(x)
    elif mode == Mode.FloatStoch:
        x, indices = voss_stoch(num_samples,generators)
        x = dsp.norm(x)
    else:
        assert False

    X, Xf, Xdb = dsp.fft(x, fs, len(x),norm='ortho' )
    Ydb = np.add(Ydb,Xdb)

Zdb = Ydb / num_tests

ideal_db, ideal_f = dsp.generate_decade_line(10, 100000)

X_slope, _, _, _, _ = stats.linregress( np.log10( Xf, where=Xf > 0 ), np.log10( dsp.gain( Xdb ) ) )
ideal_slope, _, _, _, _ = stats.linregress( np.log10(ideal_f), np.log10( dsp.gain(ideal_db) ) )

indices_used, instances = np.unique(indices, return_counts=True)

print(f'\nIndex Analysis')
for i in range(len(indices_used)):
    print(f'{indices_used[i]} = {instances[i]} ({instances[i]/num_samples:.5f}%)')
print(f'\nGradient Analysis')
print(f' Pink Slope: {X_slope:.2f}')
print(f'Ideal Slope: {ideal_slope:.2f}')

#plt.figure(1)
#plt.semilogx( Xf, Xdb )
#plt.semilogx( Xf, Zdb )
#plt.semilogx( ideal_f, ideal_db )

#plt.xlim( 1, int(fs / 2 ) )
#plt.grid(which='both')

plt.figure(2)
plt.semilogx( Xf, Xdb )
plt.semilogx( Xf, Zdb )
plt.semilogx( ideal_f, ideal_db )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')

#plt.figure(2)
#plt.stem(indices)
plt.show()

