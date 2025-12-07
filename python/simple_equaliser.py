import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
import dsp

def calculate_bands(bands, fs):
    step = (np.log(fs/2) - np.log(20)) / (bands)
    cutoff = np.zeros(bands)
    cutoff[0] = np.exp(step)*20

    for i in range(1,bands):
        cutoff[i] = np.exp(step) * cutoff[i-1]
    cutoff = np.pad(cutoff,(1,0),'constant',constant_values=0) 

    return cutoff


num_bands = 3
fs = 48000
sig_len = fs 
order = 1
axcolor = 'lightgoldenrodyellow'
fig, ax = plt.subplots(figsize=(8,6))

plt.subplots_adjust(bottom=0.35)
plt.hlines(-3,0,fs/2)
plt.xlim(20,fs/2)
plt.ylim(-30,5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')


ideal_db, ideal_f = dsp.generate_decade_line( 15, 100000 )
ax.semilogx(ideal_f, ideal_db )

freqs = [0.0,1000.0,10000.0, fs/2]
eq_bands = []
for i in range(0,num_bands):
    eq_bands.append(dsp.EQButterBand(freqs[i],freqs[i+1],fs,order))

h = signal.unit_impulse(sig_len)
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
    z = np.zeros(sig_len)
    
    for i in range(0, num_bands):
        h = signal.unit_impulse(sig_len)
        gain = np.power(10, eq_bands[i].gain / 20)
        lpf = signal.sosfilt(eq_bands[i].lpf, h) 
        hpf = signal.sosfilt(eq_bands[i].hpf, lpf)
        hpf *= gain
        
        z += hpf

    return z

def update_graph(val):
    for i in range(0, num_bands):
        eq_bands[i].gain = slider[i].val

    y = update()
    Y,Yf,Ydb = dsp.fft(y,fs,sig_len)
    
    ly.set_ydata(Ydb)

for i in range(0, num_bands):
    lpf = signal.sosfilt(eq_bands[i].lpf,h)
    m = signal.sosfilt(eq_bands[i].hpf,lpf)
    gain = np.power(10, eq_bands[i].gain / 20)
    m *= gain 
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

