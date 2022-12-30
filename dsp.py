import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

class LPF():
    def __init__( self, order, cutoff, raw_gain, fs, sig_len ):
        self.fs = fs
        self.cutoff = cutoff
        self.order = order
        self.gain = raw_gain
        self.sig_len = sig_len
        self.filter = signal.butter( self.order, self.cutoff, 'lp', fs = self.fs, output = 'sos' )

        dirac = signal.unit_impulse( self.sig_len )
        self.ir = signal.sosfilt( self.filter, dirac ) * gain( raw_gain )

        self.FFT, self.FFTf, self.FFTdb = fft( self.ir, self.fs, self.sig_len )

class SinglePoleLPF():
    def __init__( self, order, cutoff, raw_gain, fs, sig_len ):
        self.fs = fs
        self.cutoff = cutoff
        self.order = order
        self.gain = raw_gain
        self.sig_len = sig_len

        self.ir = ewma( self.cutoff, self.sig_len) * gain( raw_gain )

        self.FFT, self.FFTf, self.FFTdb = fft( self.ir, self.fs, self.sig_len )

def fft(x,fs,fft_len,norm=None):
    F = np.fft.fft(x,fft_len,norm=norm)
    F = np.abs(F)
    Ff = (fs/2)*np.linspace(0,1,int(fft_len/2))
    Fdb = 20*np.log10(F[:int(len(F)/2)]);
    
    return F, Ff, Fdb

def fft_norm(x,fs,fft_len):
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
    #alpha = 1 / ( (1/(2*np.pi*(fc/fs))) + 1)
    alpha = 1 - np.exp( -2 * np.pi * ( fc / fs ) )
    return alpha

def ewma( alpha, length ):
    dirac = signal.unit_impulse( length )
    y = np.zeros( length )
    for i in range( length ):
        y[i] = y[i-1] + ( alpha * ( dirac[i] - y[i-1] ) )
    return y

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
