import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def fft(x,fs,fft_len):
    F = np.fft.fft(x,fft_len,norm='ortho')
    F = np.abs(F)
    F = norm(F)
    Ff = (fs/2)*np.linspace(0,1,int(fft_len/2))
    Fdb = 20*np.log10(F[:int(len(F)/2)]);
    
    return F, Ff, Fdb

def norm( n ):
    return n/np.max(np.abs(n))

def coeff_calc( k, alpha, a ):
    return ( k - 1 - ( alpha / 2 ) ) * ( a / k )

fs = 48000
order = 1
sig_len = 8192 * 8
alpha = 1

a = np.zeros( 5 )

a[0] = 1
a[1] = coeff_calc( 1, alpha, a[0] )
a[2] = coeff_calc( 2, alpha, a[1] )
a[3] = coeff_calc( 3, alpha, a[2] )
a[4] = coeff_calc( 4, alpha, a[3] )

print(a)


