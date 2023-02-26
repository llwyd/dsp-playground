import numpy as np
import random

class NoiseGenerator():
    def Update(self):
        self.prev_value = self.value
        self.value = (random.random() * 2) - 1

    def __init__(self):
        self.value = 0
        self.prev_value = 0

def xorshift(x):
    assert x > 0
    x = np.uint32(x)
    x ^= x << np.uint32(13);
    x ^= x >> np.uint32(17);
    x ^= x << np.uint32(5);
    return np.uint32(x)

class U32BitNoiseGenerator():
    def Update(self):
        self.prev_value = np.uint32(self.value)
        self.value = np.uint32(xorshift(self.value))
    def __init__(self,seed=np.uint32(0x12345678)):
        assert seed > 0
        self.value = np.uint32(xorshift(seed))
        self.prev_value = 0
