from MNSensitivity import *
import numpy as np
import matplotlib.pyplot as plot

circ = load_circuit("low_pass.mc")
print_circuit(circ)

Z_s = 50
Z_l = complex(20, 30)
freq = 500e6

net = Network(circ, Z_s, Z_l, freq)

n = 300
fs = np.logspace(6, 10, n)
sens = []
f_mhz = [f/1e6 for f in fs]

spec_L1L = get_spectrum_norm(net, "L1 L", fs)
spec_C1C = get_spectrum_norm(net, "C1 C", fs)
spec_Rs1 = get_spectrum_norm(net, "Z_s", fs)

fig = plot.figure()
ax = fig.add_subplot(111)
ax.semilogx(f_mhz, spec_L1L, label='L1 1% variation')
ax.semilogx(f_mhz, spec_C1C, label='C1 1% variation')
ax.semilogx(f_mhz, spec_Rs1, label='Rs 1% variation')
ax.grid(True)
ax.legend()


ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("$d \\tau$")
ax.set_title("Variation of $\\tau$ with 1% changes to L1, C1, and Rs")
ax.semilogx([500, 500], [min(spec_Rs1), max(spec_C1C)], linestyle='--', linewidth=1, color=(.1, .1, .1))

fig2 = plot.figure()
ax1_2 = fig2.add_subplot(131)
ax2_2 = fig2.add_subplot(132)
ax3_2 = fig2.add_subplot(133)
ax1_2.semilogx(f_mhz, spec_L1L)
ax2_2.semilogx(f_mhz, spec_C1C)
# ax2_2.semilogx(f_mhz, spec_L1Cnbig)
ax3_2.semilogx(f_mhz, spec_Rs1)
ax1_2.grid(True)
ax2_2.grid(True)
ax3_2.grid(True)

ax1_2.semilogx([500, 500], [min(spec_L1L), max(spec_L1L)], linestyle='--', linewidth=1, color=(.1, .1, .1))
ax2_2.semilogx([500, 500], [min(spec_C1C), max(spec_C1C)], linestyle='--', linewidth=1, color=(.1, .1, .1))
ax3_2.semilogx([500, 500], [min(spec_Rs1), max(spec_Rs1)], linestyle='--', linewidth=1, color=(.1, .1, .1))

ax1_2.set_xlabel("Frequency (MHz)")
ax1_2.set_ylabel("$d \\tau$")
ax2_2.set_xlabel("Frequency (MHz)")
ax2_2.set_ylabel("$d \\tau$")
ax3_2.set_xlabel("Frequency (MHz)")
ax3_2.set_ylabel("$d \\tau$")

ax1_2.set_title("Variation of $\\tau$ with\n 1% change to L1")
ax2_2.set_title("Variation of $\\tau$ with\n 1% change to C1")
ax3_2.set_title("Variation of $\\tau$ with\n 1% change to Rs")

##############################################################

fig3 = plot.figure()
fig4 = plot.figure()
fig5 = plot.figure()
ax3 = fig3.add_subplot(111)
ax4 = fig4.add_subplot(111)
ax5 = fig5.add_subplot(111)
ax3.semilogx(f_mhz, spec_L1L)
ax4.semilogx(f_mhz, spec_C1C)
ax5.semilogx(f_mhz, spec_Rs1)
ax3.grid(True)
ax4.grid(True)
ax5.grid(True)

ax3.semilogx([500, 500], [min(spec_L1L), max(spec_L1L)], linestyle='--', linewidth=1, color=(.1, .1, .1))
ax4.semilogx([500, 500], [min(spec_C1C), max(spec_C1C)], linestyle='--', linewidth=1, color=(.1, .1, .1))
ax5.semilogx([500, 500], [min(spec_Rs1), max(spec_Rs1)], linestyle='--', linewidth=1, color=(.1, .1, .1))

ax3.set_xlabel("Frequency (MHz)")
ax3.set_ylabel("$d \\tau$")
ax4.set_xlabel("Frequency (MHz)")
ax4.set_ylabel("$d \\tau$")
ax5.set_xlabel("Frequency (MHz)")
ax5.set_ylabel("$d \\tau$")

ax3.set_title("Variation of $\\tau$ with\n 1% change to L1")
ax4.set_title("Variation of $\\tau$ with\n 1% change to C1")
ax5.set_title("Variation of $\\tau$ with\n 1% change to Rs")

plot.show()

plot.show()
