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
    rollover = 2**( generators )
    assert trailing_bits(rollover) == generators
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
num_samples = 4096 * 4
num_tests = 2
generators = 15

print(f'Voss-McCartney Pink Noise Generator')
print(f'    Sample Rate: {fs}') 
print(f'         Length: {num_samples} Samples ({num_samples*(1/fs):.2f}s)') 
print(f'  Noise sources: {generators}')
print(f'Test iterations: {num_tests}')
print(f'Generating...')

Ydb = np.zeros(int(num_samples/2))
Ydb_32 = np.zeros(int(num_samples/2))
Yf = []

for i in trange(num_tests):
#    x, indices = voss(num_samples,generators)
    x_32, _ = voss32(num_samples,generators)
    x_32 = dsp.norm(x_32)
#    X, Xf, Xdb = dsp.fft(x, fs, len(x),norm='ortho' )
    X_32, Xf_32, Xdb_32 = dsp.fft(x_32, fs, len(x_32),norm='ortho')
#    Ydb = np.add(Ydb,Xdb)
    Ydb_32 = np.add( Ydb_32, Xdb_32 )

#Zdb = Ydb / num_tests
Zdb_32 = Ydb_32 / num_tests

ideal_db, ideal_f = dsp.generate_decade_line(10, 100000)

X_slope, _, _, _, _ = stats.linregress( np.log10( Xf_32, where=Xf_32 > 0 ), np.log10( dsp.gain( Xdb_32 ) ) )
ideal_slope, _, _, _, _ = stats.linregress( np.log10(ideal_f), np.log10( dsp.gain(ideal_db) ) )

print(f' Pink Slope: {X_slope:.2f}')
print(f'Ideal Slope: {ideal_slope:.2f}')

#plt.figure(1)
#plt.semilogx( Xf, Xdb )
#plt.semilogx( Xf, Zdb )
#plt.semilogx( ideal_f, ideal_db )

#plt.xlim( 1, int(fs / 2 ) )
#plt.grid(which='both')

plt.figure(2)
plt.semilogx( Xf_32, Xdb_32 )
plt.semilogx( Xf_32, Zdb_32 )
plt.semilogx( ideal_f, ideal_db )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')

#plt.figure(2)
#plt.stem(indices)
plt.show()

