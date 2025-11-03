import numpy as np
import matplotlib.pyplot as plt
import dsp

x = np.loadtxt('../pink.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )


plt.semilogx(Xf,Xdb)
plt.show()

