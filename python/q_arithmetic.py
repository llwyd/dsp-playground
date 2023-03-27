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

def convert_to_q(num, e) -> np.uint32:
    assert( e < max_exp )
    q_num = num * np.power( 2, e )

    q_num = np.uint32(q_num)

    int_mask = 2**(max_exp - e) - 1
    q_int = np.uint16(int(num)) & int_mask
    q_int <<= e
    q_num += q_int
    print(f'float to Q{e} conversion {num} -> {bin(q_num)}')
    return q_num

def q_to_float(num, e):
    assert( e < max_exp )

    int_mask = 2**(max_exp - e) - 1
    int_part = np.float32(np.int16((num >> e)))
    mask = (2**e) - 1
    fract_part = num & mask

    fract = 0.0
    for i in range(e):
        shift = e - i
        bit = ( fract_part >> shift ) & 1
        fract += float(bit) * np.power(2.0, -i)

    result = float(int_part) + fract
    print(f'Q{e} to float conversion {bin(num)} -> {result}')

    return result

a = 0.666
a_q  = convert_to_q(a,15)
q_to_float(a_q,15)

print("")
a = -0.666
a_q  = convert_to_q(a,15)
q_to_float(a_q,15)

