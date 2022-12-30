import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
from scipy.io import wavfile
import dsp



def update_gain_0(val):
    print(axband[0].val)
    lpf[0].update_gain(axband[0].val)
    Y_plot.set_ydata( lpf[0].FFTdb )

def update_plot():
    pass

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

Y_plot, = ax.semilogx( lpf[0].FFTf, lpf[0].FFTdb )
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
axband[1].on_changed(update_gain_0)
axband[2].on_changed(update_gain_0)
axband[3].on_changed(update_gain_0)
axband[4].on_changed(update_gain_0)

plt.show()
