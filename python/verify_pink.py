import numpy as np
import matplotlib.pyplot as plt
import dsp

x = np.loadtxt('../pink0.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )

Ydb = np.zeros(len(Xdb))

Ydb = np.add(Ydb,Xdb)

x = np.loadtxt('../pink1.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )
Ydb = np.add(Ydb,Xdb)

x = np.loadtxt('../pink2.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )
Ydb = np.add(Ydb,Xdb)


x = np.loadtxt('../pink3.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )
Ydb = np.add(Ydb,Xdb)

x = np.loadtxt('../pink4.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )
Ydb = np.add(Ydb,Xdb)

x = np.loadtxt('../pink5.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )
Ydb = np.add(Ydb,Xdb)

x = np.loadtxt('../pink6.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )
Ydb = np.add(Ydb,Xdb)

x = np.loadtxt('../pink7.txt')
x = dsp.norm(x)
X, Xf, Xdb = dsp.fft(x, 48000, len(x),norm='ortho' )
Ydb = np.add(Ydb,Xdb)

Zdb = Ydb / 8

plt.semilogx(Xf,Zdb)
plt.show()

