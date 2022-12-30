import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
from scipy.io import wavfile
import dsp



def update_gain_0(val):
    print(axband[0].val)
    lpf[0].update_gain(axband[0].val)
    B0_plot.set_ydata( lpf[0].FFTdb )
    new_y = update_filter(lpf)
    update_graph(new_y)

def update_gain_1(val):
    print(axband[1].val)
    lpf[1].update_gain(axband[1].val)
    B1_plot.set_ydata( lpf[1].FFTdb )
    new_y = update_filter(lpf)
    update_graph(new_y)

def update_gain_2(val):
    print(axband[2].val)
    lpf[2].update_gain(axband[2].val)
    B2_plot.set_ydata( lpf[2].FFTdb )
    new_y = update_filter(lpf)
    update_graph(new_y)

def update_gain_3(val):
    print(axband[3].val)
    lpf[3].update_gain(axband[3].val)
    B3_plot.set_ydata( lpf[3].FFTdb )
    new_y = update_filter(lpf)
    update_graph(new_y)

def update_gain_4(val):
    print(axband[4].val)
    lpf[4].update_gain(axband[4].val)
    B4_plot.set_ydata( lpf[4].FFTdb )
    new_y = update_filter(lpf)
    update_graph(new_y)

def update_plot():
    pass

def update_filter(lpf):
    y = np.zeros(sig_len)
    total_gain = 1
    for i in range( len(lpf ) ):
        y = y + lpf[i].ir
        total_gain += lpf[i].gain
    y = y * dsp.gain( total_gain)
    return y

def update_graph(y):
    _, Yf, Ydb = dsp.fft( y, fs, sig_len)
    Y_plot.set_ydata( Ydb )

def stringify( val ):
    return str(val) + " Hz "

fs = 48000
sig_len = 8192 * 8

bands = [1, 10, 100, 1000, 10000]
ideal_db, ideal_f = dsp.generate_decade_line( 20, 100000 )
lpf = []
for cutoff in bands:
    lpf.append( dsp.SinglePoleLPF( 1, cutoff, 1, fs, sig_len ) )


fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.35)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')
axcolor = 'lightgoldenrodyellow'

y = update_filter(lpf)
Y, Yf, Ydb = dsp.fft( y, fs, sig_len)

Y_plot, = ax.semilogx( Yf, Ydb )
B0_plot, = ax.semilogx( lpf[0].FFTf, lpf[0].FFTdb )
B1_plot, = ax.semilogx( lpf[1].FFTf, lpf[1].FFTdb )
B2_plot, = ax.semilogx( lpf[2].FFTf, lpf[2].FFTdb )
B3_plot, = ax.semilogx( lpf[3].FFTf, lpf[3].FFTdb )
B4_plot, = ax.semilogx( lpf[4].FFTf, lpf[4].FFTdb )
ideal, = ax.semilogx(ideal_f, ideal_db )


axcolor = 'lightgoldenrodyellow'
axfreq = []
axband = []

slider_height = 0.2
slider_width = 0.03
slider_pos_x = 0.2
slider_pos_y = 0.035
slider_pos_x_inc = 0.035

for i in range(len(bands)):
    axfreq.append(fig.add_axes([slider_pos_x, slider_pos_y, slider_width, slider_height], facecolor=axcolor))
    axband.append( Slider(axfreq[i],stringify(bands[i]), -50, 20, valinit=1,valstep=1,orientation = "vertical" ) )
    slider_pos_x += slider_pos_x_inc

axband[0].on_changed(update_gain_0)
axband[1].on_changed(update_gain_1)
axband[2].on_changed(update_gain_2)
axband[3].on_changed(update_gain_3)
axband[4].on_changed(update_gain_4)

plt.show()
