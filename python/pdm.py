import numpy as np
import matplotlib.pyplot as plt

fs = 100
f = 1
t = np.linspace(0,fs - 1, fs)
x = np.sin(2 * np.pi * f * t/fs)

v_ref = 1.0
y = np.zeros(fs)
integrator = 0
comparator = 0
output = 0
dac_1_bit = [-v_ref,v_ref]

for i in range(fs):
    err = x[i] - output
    integrator += err
    if integrator > 0:
        comparator = 1
    else:
        comparator = 0
    y[i] = comparator
    output = dac_1_bit[comparator]

plt.plot((x + 1) / 2)
plt.step(t,y)
plt.show()
