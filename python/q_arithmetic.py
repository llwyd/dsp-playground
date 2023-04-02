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
max_exp = 16

def convert_to_q(num, q) -> np.uint32:
    assert( q < max_exp )
    q_num = np.uint32(num * np.float32( 1 << q ) )
    print(f'float to Q{q} conversion {num} -> {bin(q_num)}')
    return q_num

def q_to_float(num, q):
    assert( q < max_exp )
    result = np.float32( np.float32(np.int32(num)) / np.float32( 1 << q ) )
    print(f'Q{q} to float conversion {bin(num)} -> {result}')
    return result

a = 0.666
a_q  = convert_to_q(a,15)
q_to_float(a_q,15)

print("")
a = -0.666
a_q  = convert_to_q(a,15)
q_to_float(a_q,15)

