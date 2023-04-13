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

def float_to_q16bit(num, q, dbg_output = False) -> np.int16:
    assert( q < 16 )
    q_num = np.int16(num * np.float32( 1 << q ) )
    
    if dbg_output:
        print(f'float to Q{q} conversion {num} -> {bin(q_num)}')
    
    return q_num

def q16bit_to_float(num, q, dbg_output = False) -> np.float32:
    assert( q < max_exp )
    result = np.float32( np.float32(np.int16(num)) / np.float32( 1 << q ) )
    
    if dbg_output:
        print(f'Q{q} to float conversion {bin(num)} -> {result}')
    
    return result

def mul16(a,b,q):
    assert( q < 16 )

    temp = ( np.int32(a) * np.int32(b) ) >> q

    return np.int16( temp & 0xFFFF )


if __name__ == "__main__":

    fs = 44100
    omega = 2*np.pi*(1/fs)
    omega_q = float_to_q16bit(omega,15,True)


