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

fs = 48000
order = 1
sig_len = 8192 * 8

[wav_fs, wav_pink] = wavfile.read("pink.wav")
wav_pink = norm(wav_pink) * gain ( -50 )


lpf_0 = signal.butter(order, 4,'lp',fs=fs,output='sos')
lpf_1 = signal.butter(order, 16,'lp',fs=fs,output='sos')
lpf_2 = signal.butter(order, 64,'lp',fs=fs,output='sos')
lpf_3 = signal.butter(order, 256,'lp',fs=fs,output='sos')
lpf_4 = signal.butter(order, 1024,'lp',fs=fs,output='sos')
lpf_5 = signal.butter(order, 4096,'lp',fs=fs,output='sos')
lpf_6 = signal.butter(order, 16384,'lp',fs=fs,output='sos')

h = signal.unit_impulse(sig_len)

x_0 = signal.sosfilt(lpf_0, h ) * gain( -6 * 1 )
x_1 = signal.sosfilt(lpf_1, h ) * gain( -6 * 2 )
x_2 = signal.sosfilt(lpf_2, h ) * gain( -6 * 3)
x_3 = signal.sosfilt(lpf_3, h ) * gain( -6 * 4)
x_4 = signal.sosfilt(lpf_4, h ) * gain( -6 * 5)
x_5 = signal.sosfilt(lpf_5, h ) * gain( -6 * 6)
x_6 = signal.sosfilt(lpf_6, h ) * gain( -6 * 7)


y_0 = signal.sosfilt(lpf_0, h ) * gain( -6 * 1 ) 
y_1 = signal.sosfilt(lpf_1, h ) * gain( -6 * 2 ) 
y_2 = signal.sosfilt(lpf_2, h ) * gain( -6 * 3 ) 
y_3 = signal.sosfilt(lpf_3, h ) * gain( -6 * 4 ) 
y_4 = signal.sosfilt(lpf_4, h ) * gain( -6 * 5 ) 
y_5 = signal.sosfilt(lpf_5, h ) * gain( -6 * 6 ) 
y_6 = signal.sosfilt(lpf_6, h ) * gain( -6 * 7 ) 

x = y_0 + y_1 + y_2 + y_3 + y_4 + y_5 + y_6

X_0, Xf_0, Xdb_0 = fft( x_0, fs, sig_len)
X_1, Xf_1, Xdb_1 = fft( x_1, fs, sig_len)
X_2, Xf_2, Xdb_2 = fft( x_2, fs, sig_len)
X_3, Xf_3, Xdb_3 = fft( x_3, fs, sig_len)
X_4, Xf_4, Xdb_4 = fft( x_4, fs, sig_len)
X_5, Xf_5, Xdb_5 = fft( x_5, fs, sig_len)
X_6, Xf_6, Xdb_6 = fft( x_6, fs, sig_len)
X, Xf, Xdb = fft( x, fs, sig_len)
P, Pf, Pdb = fft( wav_pink, wav_fs, len(wav_pink))

plt.semilogx( Xf, Xdb )
plt.semilogx( Xf_0, Xdb_0 )
plt.semilogx( Xf_1, Xdb_1 )
plt.semilogx( Xf_2, Xdb_2 )
plt.semilogx( Xf_3, Xdb_3 )
plt.semilogx( Xf_4, Xdb_4 )
plt.semilogx( Xf_5, Xdb_5 )
plt.semilogx( Xf_6, Xdb_6 )
plt.semilogx( Pf, Pdb )
plt.ylim( -150, 10 )
plt.xlim( 1, int(fs / 2 ) )
plt.grid(which='both')
plt.show()




