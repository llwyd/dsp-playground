import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy import stats
import random
import dsp
from tqdm import trange
import noise
from enum import Enum

int_type = np.uint32
max_exp = 32

def convert_to_q(num, q, dbg_output = False) -> np.int32:
    assert( q < max_exp )
    q_num = np.int32(num * np.float32( 1 << q ) )
    
    if dbg_output:
        print(f'float to Q{q} conversion {num} -> {bin(q_num)}')
    
    return q_num

def q_to_float(num, q, dbg_output = False) -> np.float32:
    assert( q < max_exp )
    result = np.float32( np.float32(np.int32(num)) / np.float32( 1 << q ) )
    
    if dbg_output:
        print(f'Q{q} to float conversion {bin(num)} -> {result}')
    
    return result



if __name__ == "__main__":
    q = 31
    a = 0.666
    a_q  = convert_to_q(a,q)
    q_to_float(a_q,q)

    print("")
    a = -0.666
    a_q  = convert_to_q(a,q)
    q_to_float(a_q,q)


    num_samples = 4096
    fs = 48000
    f = 50
    t = np.linspace(0,num_samples - 1, num_samples)
    x = np.sin( 2 * np.pi * f * t / fs ) * 0.9999999

    y = convert_to_q(x,q)
    plt.plot(y)
    plt.show()



