import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy import stats


class EQBand():
    def __init__(self,f,fs,q,filter_type):
        self.gain_db = 0.0
        self.A = np.sqrt(10**(self.gain_db/20))

        w = 2 * np.pi * (f/fs)    
        alpha = np.sin(w) / (2 * q)
        self.sos = np.zeros(6)
        if filter_type == "LPF":
           b0 = (1 - np.cos(w)) / 2
           b1 = 1 - np.cos(w)
           b2 = (1 - np.cos(w)) / 2
           a0 = 1 + alpha
           a1 = -2 * np.cos(w)
           a2 = 1 - alpha
        elif filter_type == "HPF":
           b0 = (1 + np.cos(w)) / 2
           b1 = -(1 + np.cos(w))
           b2 = (1 + np.cos(w)) / 2
           a0 = 1 + alpha
           a1 = -2 * np.cos(w)
           a2 = 1 - alpha
        elif filter_type == "BPF":
           b0 = alpha
           b1 = 0.0
           b2 = -alpha
           a0 = 1 + alpha
           a1 = -2 * np.cos(w)
           a2 = 1 - alpha
        elif filter_type == "PT":
           b0 = 1.0
           b1 = 0.0
           b2 = 0.0
           a0 = 1.0
           a1 = 0.0
           a2 = 0.0
        else:
            assert False

        self.sos = [b0,b1,b2,a0,a1,a2]
        self.sos /= a0
        assert self.sos[3] == 1.0
