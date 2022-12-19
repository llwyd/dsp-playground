import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile


def fft(x,fs,fft_len):
    F = np.fft.fft(x,fft_len)
    F = np.abs(F)
    #F = norm(F)
    Ff = (fs/2)*np.linspace(0,1,int(fft_len/2))
    Fdb = 20*np.log10(F[:int(len(F)/2)]);
    
    return F, Ff, Fdb

def norm( n ):
    return n/np.max(np.abs(n))

def gain( g ):
    return np.power(10, g / 20 )

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

fs = 48000
order = 1
sig_len = 8192 * 8

[wav_fs, wav_pink] = wavfile.read("pink.wav")
wav_pink = norm(wav_pink) * gain ( -50 )


cutoff = [4, 32, 256, 2048, 16384 ]
current_gain = -6

lpf = []
for i in range( len( cutoff ) ):
    lpf.append( LPF(order, cutoff[i], current_gain, fs, sig_len ) )
    current_gain = current_gain -6

dirac = signal.unit_impulse(sig_len)

x = []
for i in range( len( cutoff ) ):
    x.append( signal.sosfilt( lpf[i].filter, dirac ) * gain( lpf[i].gain ) )


y = np.zeros(sig_len)
for i in range( len( cutoff ) ):
    y = y + x[i]


Y, Yf, Ydb = fft( y, fs, sig_len)
P, Pf, Pdb = fft( wav_pink, wav_fs, len(wav_pink))

plt.semilogx( Yf, Ydb )
for i in range( len( cutoff ) ):
    plt.semilogx( lpf[i].FFTf, lpf[i].FFTdb )

plt.semilogx( Pf, Pdb )
plt.ylim( -150, 10 )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')
plt.show()




