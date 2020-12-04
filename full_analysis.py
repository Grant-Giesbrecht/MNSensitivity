from MNSensitivity import *
import numpy as np
import matplotlib.pyplot as plot

circ = load_circuit("low_pass.mc")
print_circuit(circ)

Z_s = 50
Z_l = complex(20, 30)
freq = 500e6

net = Network(circ, Z_s, Z_l, freq)

s_l1 = sens_pcnt(net, "L1 L")
s_c1 = sens_pcnt(net, "C1 C")
s_zs = sens_pcnt(net, "Z_s")

print(f"Sensitivity with Respect to L1: {s_l1}")
print(f"Sensitivity with Respect to C1: {s_c1}")
print(f"Sensitivity with Respect to Z_s: {s_zs}")

n = 300
fs = np.logspace(6, 10, n)
sens = []
f_mhz = [f/1e6 for f in fs]

spec_L1L = get_spectrum_pcnt(net, "L1 L", fs)
spec_C1C = get_spectrum_pcnt(net, "C1 C", fs)
spec_ZS = get_spectrum_pcnt(net, "Z_s", fs)

fig = plot.figure()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
ax1.semilogx(f_mhz, spec_L1L)
ax2.semilogx(f_mhz, spec_C1C)
ax3.semilogx(f_mhz, spec_ZS)
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

ax1.set_xlabel("Frequency (MHz)")
ax1.set_ylabel("Sensitivity (1/H)")
ax2.set_xlabel("Frequency (MHz)")
ax2.set_ylabel("Sensitivity (1/F)")
ax3.set_xlabel("Frequency (MHz)")
ax3.set_ylabel("Sensitivity (1/Ohm)")
ax1.set_title("Sensitivity to L1")
ax2.set_title("Sensitivity to C1")
ax3.set_title("Sensitivity to Zs")
plot.show()
