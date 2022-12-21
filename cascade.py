import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

def pink_filter():
	# Taken from http://www.firstpr.com.au/dsp/pink-noise/
	# Filter design by Robert Bristow-Johnson
	p = [0.99572754,0.94790649,0.53567505] 
	z = [0.98443604,0.83392334,0.07568359] 
	k = 1

	# This converts to poles and zeros into second order sections
	sos = signal.zpk2sos( z, p, k );
	
	return sos

def unit_impulse_filter():
    p = [0]
    z = [1]
    k = 1

    sos = signal.spk2sos( z, p, k )
    return sos

def voss_algorithm( bands, n ):
	pink = np.zeros(n)
	noise = np.zeros(bands)
	
	for i in range(n):
		pink[i] = 0
		for j in range(bands):
			if((i+1)%np.power(2,j)==0):
				noise[j]=(r.random()*2)-1;

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

cutoff = [5.859375,23.4375,93.75,375,1500,6000,12000,16000,20000]
current_gain = -6

lpf = []
for i in range( len( cutoff ) ):
    lpf.append( LPF(order, cutoff[i], current_gain, fs, sig_len ) )
    current_gain = current_gain -6

dirac = signal.unit_impulse(sig_len)

p = signal.sosfilt( pink_filter(), dirac )
p = norm( p ) * gain( -27)

x = []
for i in range( len( cutoff ) ):
    x.append( signal.sosfilt( lpf[i].filter, dirac ) * gain( lpf[i].gain ) )


y = np.zeros(sig_len)
#y = signal.unit_impulse(sig_len)
for i in range( len( cutoff ) ):
    y = y + x[i]

ref  = [ 0, -10, -20, -30, -40]
reff = [ 10, 100, 1000, 10000, 100000]

Y, Yf, Ydb = fft( y, fs, sig_len)
P, Pf, Pdb = fft( p, fs, sig_len)
PINK, PINKf, PINKdb = fft( wav_pink, wav_fs, len(wav_pink))

plt.semilogx( PINKf, PINKdb )
plt.semilogx( Yf, Ydb )
plt.semilogx( Pf, Pdb )
plt.semilogx( reff, ref )
plt.legend(['Audacity', 'cascade approach','RBJ','reference'])
plt.ylim( -150, 10 )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')

plt.figure(2)
plt.semilogx( Yf, Ydb )
for i in range( len( cutoff ) ):
    plt.semilogx( lpf[i].FFTf, lpf[i].FFTdb )
plt.ylim( -150, 10 )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')

plt.show()




