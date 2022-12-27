import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import random
import dsp

def fft(x,fs,fft_len):
    F = np.fft.fft(x,fft_len,norm='ortho')
    F = np.abs(F)
    #F = norm(F)
    Ff = (fs/2)*np.linspace(0,1,int(fft_len/2))
    Fdb = 20*np.log10(F[:int(len(F)/2)]);
    
    return F, Ff, Fdb

def norm( n ):
    return n/np.max(np.abs(n))

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

    x = norm(x)
    return x, indices

fs = 48000
num_samples = 4096

[wav_fs, wav_pink] = wavfile.read("pink.wav")
wav_pink = norm(wav_pink)

x, indices = voss(num_samples)
X, Xf, Xdb = fft(x, fs, len(x) )
PINK, PINKf, PINKdb = fft( wav_pink, wav_fs, len(wav_pink))

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(x)
plt.subplot(2,1,2)
plt.semilogx( PINKf, PINKdb )
plt.semilogx( Xf, Xdb )
#plt.ylim( -150, 10 )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')
plt.figure(2)
plt.stem(indices)
plt.show()

