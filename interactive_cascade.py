import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
from scipy.io import wavfile
import dsp

def update_filter(freq):
    y = np.zeros(sig_len)
    total_gain = 0
    for i in range( len(freq) ):
        y = y + freq[i].lpf.ir
        total_gain += dsp.gain( freq[i].lpf.gain )
    raw_gain = -20*np.log10(total_gain)
    y = y * dsp.gain(raw_gain)
    return y

def update_graph(y):
    _, Yf, Ydb = dsp.fft( y, fs, sig_len)
    Y_plot.set_ydata( Ydb )

    cascade_slope = dsp.get_fslope( Yf, Ydb )
    ideal_slope = dsp.get_fslope( ideal_f, ideal_db )

    cascade_slope_text.set_text(f'Filter gradient: {cascade_slope:.3f}')
    ideal_slope_text.set_text(f' Ideal gradient: {ideal_slope:.3f}')

def stringify( val ):
    return str(val) + " Hz "

class SliderControl:
    def __init__( self, height, width, pos_x, pos_y ):
        self.height = height
        self.width = width
        self.x = pos_x
        self.y = pos_y

class FilterControl:
    def gain_changed( self, val ):
        self.lpf.update_gain(self.slider.val)
        self.plot.set_ydata( self.lpf.FFTdb )
        new_y = update_filter(freqband)
        update_graph(new_y)
    def freq_changed( self, val ):
        self.lpf.update_freq(self.fslider.val)
        self.plot.set_ydata( self.lpf.FFTdb )
        new_y = update_filter(freqband)
        update_graph(new_y)
    def __init__( self, fig, ax, filter_order, fc, fs, gain, samples, slider_config, fslider_config, axcolor ):
        self.lpf = dsp.SinglePoleLPF( filter_order, fc, gain, fs, samples )
        self.plot,  = ax.semilogx( self.lpf.FFTf, self.lpf.FFTdb )
        self.slider_ax = fig.add_axes([slider_config.x, slider_config.y, slider_config.width, slider_config.height], facecolor=axcolor)
        self.slider = Slider(self.slider_ax,stringify(fc), -50, 20, valinit=0,valstep=1,orientation = "vertical" )
        self.slider.on_changed(self.gain_changed)
        
        self.fslider_ax = fig.add_axes([fslider_config.x, fslider_config.y, fslider_config.width, fslider_config.height], facecolor=axcolor)
        self.fslider = Slider(self.fslider_ax,stringify(fc), 1, int(fs/2), valinit=fc,valstep=1,orientation = "horizontal" )
        self.fslider.on_changed(self.freq_changed)

fs = 48000
sig_len = 8192 * 8

axcolor = 'lightgoldenrodyellow'
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.35)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')
ax.set_xlim([1,fs/2])
ax.set_ylim([-50,5])

bands = [1, 10, 100, 1000, 10000]
ideal_db, ideal_f = dsp.generate_decade_line( 0, 100000 )
freqband = []

config = SliderControl(0.2, 0.03, 0.2, 0.035)
freq_config = SliderControl( 0.03, 0.2, 0.5, 0.175 )

slider_pos_x_inc = 0.035
for cutoff in bands:
    freqband.append( FilterControl(fig, ax, 1, cutoff, fs, 0, sig_len, config, freq_config, axcolor) )
    config.x += slider_pos_x_inc
    freq_config.y -= slider_pos_x_inc

y = update_filter(freqband)
Y, Yf, Ydb = dsp.fft( y, fs, sig_len)

Y_plot, = ax.semilogx( Yf, Ydb )
ideal, = ax.semilogx(ideal_f, ideal_db )

cascade_slope = dsp.get_fslope( Yf, Ydb )
ideal_slope = dsp.get_fslope( ideal_f, ideal_db )

cascade_slope_text =ax.text(1000,0,f'Filter gradient: {cascade_slope:.3f}')
ideal_slope_text =ax.text(1000,4,f' Ideal gradient: {ideal_slope:.3f}')

axcolor = 'lightgoldenrodyellow'

plt.show()
