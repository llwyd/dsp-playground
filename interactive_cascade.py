import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
from scipy.io import wavfile
import dsp

fs = 48000
sig_len = 8192

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.35)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')
axcolor = 'lightgoldenrodyellow'

axcolor = 'lightgoldenrodyellow'
axfreq = []
axband = []

axfreq.append(fig.add_axes([0.2, 0.035, 0.03, 0.20], facecolor=axcolor))
axband.append( Slider(axfreq[0],'1 Hz', -50, 20, valinit=1,valstep=1,orientation = "vertical" ) )

plt.show()
