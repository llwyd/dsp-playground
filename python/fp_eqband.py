import dsp
import fp_dsp as fp
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import q_arithmetic as qmath

class QBand():
    def gain_raw(self):
        return np.power(10, self.gain / 20)
    def __init__(self,lower_cutoff, upper_cutoff,fs,q,gain_db):
        self.order = 1
        self.fs = fs
        self.gain = gain_db
        self.filter2 = None 
        if lower_cutoff == 0.0:
            self.filter = signal.butter(self.order,upper_cutoff,'lowpass',fs=fs,output='sos')
        elif int(np.round(upper_cutoff)) == int(int(fs)/2):
            self.filter = signal.butter(self.order,lower_cutoff,'highpass',fs=fs,output='sos')
        else:
            self.filter = signal.butter(self.order,upper_cutoff,'lowpass',fs=fs,output='sos')
            self.filter2 = signal.butter(self.order,lower_cutoff,'highpass',fs=fs,output='sos')
       
        self.q = q
        self.sos = self.filter
        if self.filter2 is not None:
            self.sos = np.append(self.sos,self.filter2,axis=0)
        
        self.sos_q = qmath.to_q32(self.sos,self.q)
        self.gain_q = qmath.to_q32(self.gain_raw(),self.q) 
        print(f'EQBand: {lower_cutoff} <-> {upper_cutoff} g: {self.gain_raw()} ({self.gain}dB) fs:{self.fs}')

order = 1
fs = 48000
gain = 0.0 #db
cutoff = 1e3
sig_len = fs
q = 30

h = signal.unit_impulse(sig_len)
h_q = qmath.to_q32(h, q)
band = QBand(2000,fs/2,fs,q,-10)
ir = signal.sosfilt(band.sos,h)
ir_q = fp.sosfilt_rt(band.sos_q, h_q, band.gain_q, q)

ir_f32 = qmath.to_float32(ir_q,q)
_, Ff,Fdb = dsp.fft(ir,fs,sig_len)
_, Qf,Qdb = dsp.fft(ir_f32,fs,sig_len)

plt.semilogx(Ff,Fdb)
plt.semilogx(Qf,Qdb)
plt.xlim(1,fs/2)
plt.ylim(-30,10)
plt.show()

