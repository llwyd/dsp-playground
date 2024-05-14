import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
from scipy.io import wavfile
import dsp

y_gain = 0

def update_filter(freq):
    y = np.zeros(sig_len)
    total_gain = 0
    for i in range( len(freq) ):
        y = y + freq[i].lpf.ir
        total_gain += dsp.gain( freq[i].lpf.gain )
    raw_gain = -20*np.log10(total_gain)
    y = y * dsp.gain(raw_gain)
    y = y * dsp.gain(y_gain)
    return y

def update_overall_gain(val):
    global y_gain
    y_gain = val
    new_y = update_filter(freqband)
    update_graph(new_y)

def update_graph(y):
    _, Yf, Ydb = dsp.fft( y, fs, sig_len)
    Y_plot.set_ydata( Ydb )

    cascade_slope = dsp.get_fslope( Yf, Ydb )
    ideal_slope = dsp.get_fslope( ideal_f, ideal_db )

    cascade_slope_text.set_text(f'Filter gradient: {cascade_slope:.6f}')
    ideal_slope_text.set_text(f'Ideal gradient: {ideal_slope:.6f}')

def stringify( val ):
    return str(val) + " Hz "

class SliderControl:
    def __init__( self, height, width, pos_x, pos_y ):
        self.height = height
        self.width = width
        self.x = pos_x
        self.y = pos_y

class FilterControl:
    def update(self):
        new_freq = np.power(10, self.fslider.val)
        self.lpf.update_freq(new_freq)
        new_gain = (-10 * np.log10(new_freq)) + 3
        new_gain_raw = np.power(10,new_gain/20)
        self.lpf.update_gain(new_gain)
        self.plot.set_ydata( self.lpf.FFTdb )
        new_y = update_filter(freqband)
        update_graph(new_y)
    def freq_changed( self, val ):
        new_freq = np.power(10, self.fslider.val)
        self.lpf.update_freq(new_freq)
        new_gain = (-10 * np.log10(new_freq)) + 3
        new_gain_raw = np.power(10,new_gain/20)
        self.lpf.update_gain(new_gain)
        self.plot.set_ydata( self.lpf.FFTdb )
        new_y = update_filter(freqband)
        update_graph(new_y)
    def __init__( self, fig, ax, filter_order, fc, fs, gain, samples, fslider_config, axcolor ):
        self.lpf = dsp.SinglePoleLPF( filter_order, fc, gain, fs, samples )
        self.plot,  = ax.semilogx( self.lpf.FFTf, self.lpf.FFTdb )

        self.fslider_ax = fig.add_axes([fslider_config.x, fslider_config.y, fslider_config.width, fslider_config.height], facecolor=axcolor)
        self.fslider = Slider(self.fslider_ax,stringify(fc), np.log10(1), np.log10(fs/2), valinit=np.log10(fc),valstep=0.001,orientation = "horizontal" )
        self.fslider.on_changed(self.freq_changed)

fs = 44100
num_filters = 4
num_decades = int(np.ceil(np.log10(fs/2)))
print(f'Decades: {num_decades}')
print(f'     FS: {fs} Hz')
print(f'Filters: {num_filters}')
sig_len = fs

axcolor = 'lightgoldenrodyellow'
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.35)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')
ax.set_xlim([1,fs/2])
ax.set_ylim([-50,5])
ax.grid(which='both')



#bands = [1, 10, 100, 1000, 10000]
bands = [1,10,100,1000,10000]
freqband = []
freq_config = SliderControl( 0.03, 0.7, 0.2, 0.175 )
slider_pos_y_inc = 0.035

gain_config = SliderControl(0.2, 0.03, 0.05, 0.035)
slider_ax = fig.add_axes([gain_config.x, gain_config.y, gain_config.width, gain_config.height], facecolor=axcolor)
slider = Slider(slider_ax,"Gain", -50, 20, valinit=0,valstep=0.1,orientation = "vertical" )
slider.on_changed(update_overall_gain)

for cutoff in bands:
    freqband.append( FilterControl(fig, ax, 1, cutoff, fs, 0, sig_len, freq_config, axcolor) )
    freq_config.y -= slider_pos_y_inc

y = update_filter(freqband)
Y, Yf, Ydb = dsp.fft( y, fs, sig_len)


Y_plot, = ax.semilogx( Yf, Ydb )
ideal_db, ideal_f = dsp.generate_decade_line( 0, 100000 )
ideal, = ax.semilogx(ideal_f, ideal_db )

cascade_slope = dsp.get_fslope( Yf, Ydb )
ideal_slope = dsp.get_fslope( ideal_f, ideal_db )

cascade_slope_text =ax.text(100,0,f'Filter gradient: {cascade_slope:.6f}')
ideal_slope_text =ax.text(100,4,f'Ideal gradient: {ideal_slope:.6f}')

axcolor = 'lightgoldenrodyellow'

for freq in freqband:
    freq.update()

plt.show()
