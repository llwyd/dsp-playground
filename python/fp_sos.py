import dsp
import fp_dsp as fp
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import q_arithmetic as qmath

def sos(x,filt):
    assert filt[3] == 1.0
    s1 = 0
    s2 = 0
    y = np.zeros(len(x))
    for i in range(len(x)):
        y[i] = (x[i] * filt[0]) + s1
        s1 = s2 + (x[i] * filt[1]) - (filt[4] * y[i])
        s2 = (x[i] * filt[2]) - (filt[5] * y[i])

    return y

def sos_q(x,filt,q):
    s1 = np.int32(0)
    s2 = np.int32(0)
    y = np.zeros(len(x), dtype=np.int32)
    for i in range(len(x)):
        y[i] = qmath.mul32(x[i],filt[0],q) + s1
        s1 = s2 + qmath.mul32(x[i],filt[1],q) - qmath.mul32(filt[4],y[i],q)
        s2 = qmath.mul32(x[i],filt[2],q) - qmath.mul32(filt[5],y[i],q)

    return y

order = 1
fs = 48000
gain = 0.0 #db
cutoff = 1e3
sig_len = 4096
q = 30

h = signal.unit_impulse(sig_len)
h_q = qmath.to_q32(h, q)
lpf = signal.butter(order,cutoff,'lowpass',fs=fs,output='sos')
lpf_q = qmath.to_q32(lpf[0],q)

ir = signal.sosfilt( lpf, h )

ir2 = sos(h,lpf[0])
ir_q = fp.sosfilt(h_q,lpf_q,q)
ir3 = qmath.to_float32(ir_q,q)

_, Ff,Fdb = dsp.fft(ir,fs,sig_len)
_, F2f,F2db = dsp.fft(ir2,fs,sig_len)
_, F3f,F3db = dsp.fft(ir3,fs,sig_len)

plt.semilogx(Ff,Fdb)
plt.semilogx(F2f,F2db)
plt.semilogx(F3f,F3db)
plt.xlim(1,fs/2)
plt.ylim(-30,10)
plt.show()

