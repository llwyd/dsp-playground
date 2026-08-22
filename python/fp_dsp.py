import dsp
import numpy as np
import q_arithmetic as qmath
from scipy import signal
max_q = 32

class QNum():
    def float_to_q(self):
        num_q = np.int32(self.num_f * np.float32(1 << self.q))
        return num_q
    def __init__( self, num, q, dbg_output = False ):
        assert q < max_q
        self.q = q
        self.num_f = np.float32(num)
        self.num_q = self.float_to_q()
    
        if dbg_output:
            print(f'float to Q{q} conversion {self.num_f} -> {hex(self.num_q)}')

def sosfilt(biquad,x,gain,q):
    assert q < max_q
    s1 = np.int32(0)
    s2 = np.int32(0)
    y = np.zeros(len(x), dtype=np.int32)
    
    for filt in biquad:
        for i in range(len(x)):
            y[i] = qmath.mul32(x[i],filt[0],q) + s1
            s1 = s2 + qmath.mul32(x[i],filt[1],q) - qmath.mul32(filt[4],y[i],q)
            s2 = qmath.mul32(x[i],filt[2],q) - qmath.mul32(filt[5],y[i],q)
        x = np.copy(y)
    for i in range(len(y)):
        y[i] = qmath.mul32(y[i], gain, q)
    return y

# Real time / sample by sample for real time dsp
def sosfilt_rt(biquad,z,gain,q):
    assert q < max_q
    num_biquads = len(biquad)
    s1 = np.zeros(num_biquads, dtype = np.int32)
    s2 = np.zeros(num_biquads, dtype = np.int32)
    y = np.zeros(len(z), dtype=np.int32)
    #x = z.copy()
    x = z
    for i in range(len(z)):
        for j, filt in enumerate(biquad):
            y[i] = qmath.mul32(x[i],filt[0],q) + s1[j]
            s1[j] = s2[j] + qmath.mul32(x[i],filt[1],q) - qmath.mul32(filt[4],y[i],q)
            s2[j] = qmath.mul32(x[i],filt[2],q) - qmath.mul32(filt[5],y[i],q)
            x[i] = y[i]
        
        y[i] = qmath.mul32(y[i], gain, q)
    
    return y

class QBand():
    def gain_raw(self):
        return np.power(10, self.gain / 20)
    def set_gain(self,gain_db):
        self.gain = gain_db
        self.gain_q = qmath.to_q32(self.gain_raw(),self.q) 

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

