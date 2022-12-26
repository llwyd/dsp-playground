import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import dsp

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

fs = 48000
order = 1
sig_len = 4096 * 16

[wav_fs, wav_pink] = wavfile.read("pink.wav")
wav_pink = dsp.norm(wav_pink) * dsp.gain ( -50 )

cutoff = [15,42,205,1300,10300]
gains = [-6,-6,-6,-6,-6,-6]
current_gain = 0

lpf = []
for i in range( len( cutoff ) ):
    lpf.append( dsp.LPF(order, cutoff[i], current_gain, fs, sig_len ) )
    #current_gain = current_gain - 6
    current_gain = current_gain + gains[i]

dirac = signal.unit_impulse(sig_len)

p = signal.sosfilt( pink_filter(), dirac )
p = dsp.norm( p ) * dsp.gain(-70)

x = []
for i in range( len( cutoff ) ):
    x.append( signal.sosfilt( lpf[i].filter, dirac ) * dsp.gain( lpf[i].gain ) )


y = np.zeros(sig_len)
#y = signal.unit_impulse(sig_len)
for i in range( len( cutoff ) ):
    y = y + x[i]

y = dsp.norm(y)

ref  = [ 0, -10, -20, -30, -40]
reff = [ 10, 100, 1000, 10000, 100000]

Y, Yf, Ydb = dsp.fft_norm( y, fs, sig_len)
P, Pf, Pdb = dsp.fft_norm( p, fs, sig_len)
PINK, PINKf, PINKdb = dsp.fft_norm( wav_pink, wav_fs, len(wav_pink))

#plt.semilogx( PINKf, PINKdb )
plt.semilogx( Yf, Ydb )
#plt.semilogx( Pf, Pdb )
plt.semilogx( reff, ref )
plt.legend(['Audacity', 'cascade approach','RBJ','reference'])
plt.ylim( -50, 10 )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')

#plt.figure(2)
#plt.semilogx( Yf, Ydb )
#for i in range( len( cutoff ) ):
#    plt.semilogx( lpf[i].FFTf, lpf[i].FFTdb )
#plt.ylim( -150, 10 )
#plt.xlim( 1, int(fs / 2 ) )
#plt.grid(which='both')

plt.show()




