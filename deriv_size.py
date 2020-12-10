from MNSensitivity import *
import numpy as np
import matplotlib.pyplot as plot
from matplotlib import rc

plot.rcParams["font.family"] = "Times New Roman"
plot.rcParams.update({'font.size': 18})

plot.rcParams['mathtext.fontset'] = 'custom'
plot.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
plot.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
plot.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'

circ = load_circuit("low_pass.mc")
print_circuit(circ)

Z_s = 50
Z_l = complex(20, 30)
freq = 500e6

net = Network(circ, Z_s, Z_l, freq)

n = 300
fs = np.logspace(6, 10, n)
f_mhz = [f/1e6 for f in fs]

sens = get_spectrum_pcnt(net, "L1 L", fs, 1)
sens_p1 = get_spectrum_pcnt(net, "L1 L", fs, .02)
sens_10p = get_spectrum_pcnt(net, "L1 L", fs, 50)

# fig = plot.figure()
# ax1 = fig.add_subplot(111)
# ax1.semilogx(f_mhz, sens)
# ax1.grid(True)
#
# ax1.set_xlabel("Frequency (MHz)")
# ax1.set_ylabel("Sensitivity (1/nH)")
# ax1.set_title("Sensitivity to L1 vs Frequency for Simple Network")

fig2 = plot.figure(figsize=(8, 6))
ax2 = fig2.add_subplot(111)
ax2.semilogx(f_mhz, sens, linestyle='--', color=(0, 0, .8), label='dL = 1% L1')
ax2.semilogx(f_mhz, sens_p1, linestyle='-.', color=(.8, 0, 0), label='dL = 0.02% L1')
ax2.semilogx(f_mhz, sens_10p, linestyle=':', color=(.4, .4, .4), label='dL = 50% L1')
ax2.semilogx([500, 500], [min(sens_10p), max(sens_10p)], linestyle='--', linewidth=1.5, color=(.1, .1, .1))
ax2.grid(True)
ax2.legend()

ax2.set_xlabel("Frequency (MHz)")
ax2.set_ylabel("|Sensitivity| (1/nH)")
ax2.set_title("Comparison of Calculated Sensitivity\n with Variation in d$\Delta$ size.")
plot.show()
