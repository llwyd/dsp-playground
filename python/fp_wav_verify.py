import fp_dsp as fp
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import q_arithmetic as qmath
from scipy.io.wavfile import read,write
import dsp

fs, data = read('test.wav')

assert fs == 48000
q = 30
data_f32 = qmath.to_float32(data,q)
H, Hf, Hdb = dsp.fft(data_f32, fs, len(data))
ideal_db, ideal_f = dsp.generate_decade_line( 15, 100000 )
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(data)
plt.subplot(2,1,2)
plt.semilogx(Hf,Hdb)
plt.semilogx(ideal_f,ideal_db)
plt.xlim(20,fs/2)
plt.ylim(-30,5)
plt.show()
