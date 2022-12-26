import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

def fft(x,fs,fft_len):
    F = np.fft.fft(x,fft_len)
    F = np.abs(F)
    F = norm(F)
    Ff = (fs/2)*np.linspace(0,1,int(fft_len/2))
    Fdb = 20*np.log10(F[:int(len(F)/2)]);
    
    return F, Ff, Fdb

def norm( n ):
    return n/np.max(np.abs(n))

def gain( g ):
    return np.power(10, g / 20 )


def get_alpha( fc, fs ):
    # Wikipedia
    alpha = 1 / ( (1/(2*np.pi*(fc/fs))) + 1)
    return alpha

def ewma( alpha, length ):
    dirac = signal.unit_impulse( length )
    y = np.zeros( length )
    for i in range( length ):
        #y[i] = ( alpha*y[i-1] ) + ( dirac[i] * ( 1 - alpha ) )
        y[i] = y[i-1] + ( alpha * ( dirac[i] - y[i-1] ) )
        #y[i] = ( alpha*dirac[i] ) + ( y[i-1] * ( 1 - alpha ) )
    return y

fs = 48000
order = 1
sig_len = 4096 * 16

fc = 12000
cutoff = 1 - np.exp( -2 * np.pi * ( fc / fs ) )
#cutoff = get_alpha( fc, fs )

print("Cutoff: " + str(fc) + "Hz")
print("Alpha: " + str(cutoff) )

y = ewma( cutoff, sig_len )
Y, Yf, Ydb = fft( y, fs, sig_len)

plt.semilogx(Yf,Ydb)
plt.axvline(x=fc)
plt.axhline(y=-3)
plt.show()

