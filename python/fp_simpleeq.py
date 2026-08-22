import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
import dsp
import fp_dsp as fp
from scipy.io.wavfile import read,write
import q_arithmetic as qmath
num_bands = 4
fs = 48000
sig_len = fs 
order = 1
q = 30

freqs = dsp.calculate_bands(4,fs)
eq_bands = []
for i in range(len(freqs) - 1):
    eq_bands.append(fp.QBand(freqs[i],freqs[i+1],fs,q,0.0))

fig, ax = plt.subplots(figsize=(8,6))

axcolor = 'lightgoldenrodyellow'
plt.subplots_adjust(bottom=0.35)
plt.hlines(-3,0,fs/2)
plt.hlines(0,0,fs/2,color='red')
plt.xlim(20,fs/2)
plt.ylim(-30,5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')


ideal_db, ideal_f = dsp.generate_decade_line( 15, 100000 )
ax.semilogx(ideal_f, ideal_db )

h = signal.unit_impulse(sig_len)
h_q = qmath.to_q32(h,q)
H, Hf, Hdb = dsp.fft(h, fs, sig_len)    
ly, = ax.semilogx(Hf,Hdb)

f = []
Fdb = []
Ff = []
F = []
axfreq = []
slider = []
y = np.zeros(sig_len)
x_pos = 0.2
x_inc = 0.05
y_pos = 0.01
y_inc = 0.0

def update():
    z = np.zeros(sig_len,dtype=np.int32)
    h = signal.unit_impulse(sig_len)
    h_q = qmath.to_q32(h,q)
    
    for i in range(0, num_bands):
        ir = fp.sosfilt_rt(eq_bands[i].sos_q,h_q,eq_bands[i].gain_q,q)
        z += ir
    return qmath.to_float32(z,q)

def update_graph(val):
    for i in range(0, num_bands):
        eq_bands[i].set_gain(slider[i].val)

    y = update()
    Y,Yf,Ydb = dsp.fft(y,fs,sig_len)
    
    ly.set_ydata(Ydb)

for i in range(0, num_bands):
    h = signal.unit_impulse(sig_len)
    h_q = qmath.to_q32(h,q)
    mq = fp.sosfilt_rt(eq_bands[i].sos_q,
                       h_q,
                       eq_bands[i].gain_q,
                       q)
    m = qmath.to_float32(mq,q)
    y += m
    M, Mf,Mdb = dsp.fft(m, fs, sig_len)    
    f.append(m)
    F.append(M)
    Fdb.append(Mdb)
    Ff.append(Mf)
    
    ax.semilogx(Mf,Mdb)
    init_gain = eq_bands[i].gain
    axfreq.append(plt.axes([x_pos, y_pos, 0.03, 0.25], facecolor=axcolor))
    slider.append(Slider(axfreq[i], 'Band', -100, 10, valinit=init_gain, valstep=0.1, orientation='vertical'))
    slider[i].on_changed(update_graph)
    x_pos += x_inc
    y_pos += y_inc

Y, Yf,Ydb = dsp.fft(y, fs, sig_len)    
ly.set_ydata(Ydb)

plt.show()

