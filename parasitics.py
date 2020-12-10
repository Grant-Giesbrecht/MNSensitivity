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
spec_L1Ca = get_spectrum_val(net, "L1 C", fs, .1e-12)
spec_L1Cb = get_spectrum_val(net, "L1 C", fs, 1e-12)
spec_L1Ra = get_spectrum_val(net, "L1 R", fs, .1)
spec_L1Rb = get_spectrum_val(net, "L1 R", fs, 1)

spec_L1Ln = get_spectrum_norm(net, "L1 L", fs)
spec_L1Cn = get_spectrum_norm(net, "L1 C", fs, abs_val=.1e-12)
spec_L1Cnbig = get_spectrum_norm(net, "L1 C", fs, abs_val=1e-12)
spec_L1Rn = get_spectrum_norm(net, "L1 R", fs, abs_val=1)

# fig = plot.figure()
# ax1 = fig.add_subplot(131)
# ax2 = fig.add_subplot(132)
# ax3 = fig.add_subplot(133)
# ax1.semilogx(f_mhz, spec_L1L)
# ax2.semilogx(f_mhz, spec_L1Ca)
# ax2.semilogx(f_mhz, spec_L1Cb)
# ax3.semilogx(f_mhz, spec_L1Ra)
# ax3.semilogx(f_mhz, spec_L1Rb)
# ax1.grid(True)
# ax2.grid(True)
# ax3.grid(True)
#
# ax1.set_xlabel("Frequency (MHz)")
# ax1.set_ylabel("Sensitivity (1/H)")
# ax2.set_xlabel("Frequency (MHz)")
# ax2.set_ylabel("Sensitivity (1/F)")
# ax3.set_xlabel("Frequency (MHz)")
# ax3.set_ylabel("Sensitivity (1/Ohm)")
# ax1.set_title("Sensitivity to L1")
# ax2.set_title("Sensitivity to C1")
# ax3.set_title("Sensitivity to Zs")
#
# fig2 = plot.figure()
# ax1_2 = fig2.add_subplot(131)
# ax2_2 = fig2.add_subplot(132)
# ax3_2 = fig2.add_subplot(133)
# ax1_2.semilogx(f_mhz, spec_L1Ln)
# ax2_2.semilogx(f_mhz, spec_L1Cn)
# # ax2_2.semilogx(f_mhz, spec_L1Cnbig)
# ax3_2.semilogx(f_mhz, spec_L1Rn)
# ax1_2.grid(True)
# ax2_2.grid(True)
# ax3_2.grid(True)
#
# ax1_2.semilogx([500, 500], [min(spec_L1Ln), max(spec_L1Ln)], linestyle='--', linewidth=1, color=(.1, .1, .1))
# ax2_2.semilogx([500, 500], [min(spec_L1Ln), max(spec_L1Cn)], linestyle='--', linewidth=1, color=(.1, .1, .1))
# ax3_2.semilogx([500, 500], [min(spec_L1Ln), max(spec_L1Rn)], linestyle='--', linewidth=1, color=(.1, .1, .1))
#
# ax1_2.set_xlabel("Frequency (MHz)")
# ax1_2.set_ylabel("$d \\tau$")
# ax2_2.set_xlabel("Frequency (MHz)")
# ax2_2.set_ylabel("$d \\tau$")
# ax3_2.set_xlabel("Frequency (MHz)")
# ax3_2.set_ylabel("$d \\tau$")
# ax1_2.set_title("Variation of $\\tau$ with\n 1% change to L1")
# ax2_2.set_title("Variation of $\\tau$ with\n 0.1pF parastic C added to L1")
# ax3_2.set_title("Variation of $\\tau$ with\n 1 ohm parastic R added to L1")





fig3 = plot.figure(figsize=(8, 6))
ax3 = fig3.add_subplot(111)
# ax3.semilogx(f_mhz, spec_L1Ln, label='1% Variation to Inductance')
# ax3.semilogx(f_mhz, spec_L1Cn, label='$C_{parasitic}$ = 0.1 pF')
# ax3.semilogx(f_mhz, spec_L1Rn, label='$R_{parasitic}$ = 1 $\\Omega$')
ax3.semilogx(f_mhz, spec_L1Ln, label='1% Variation to Inductance', color=(0, 0, .8))
ax3.semilogx(f_mhz, spec_L1Cn, label='$C_{parasitic}$ = 0.1 pF', color=(.8, 0, 0))
ax3.semilogx(f_mhz, spec_L1Rn, label='$R_{parasitic}$ = 1 $\\Omega$', color=(.4, .4, .4))

# ax2.semilogx(f_mhz, sens, linestyle='--', color=(0, 0, .6), label='Variation = 1%')
# ax2.semilogx(f_mhz, sens_p1, linestyle='-.', color=(.6, 0, 0), label='Variation = .02%')
# ax2.semilogx(f_mhz, sens_10p, linestyle=':', color=(.3, .3, .3), label='Variation = 50%')

ax3.grid(True)
ax3.grid(True)
ax3.grid(True)

ax3.semilogx([500, 500], [min(spec_L1Ln), max(spec_L1Ln)], linestyle='--', linewidth=1, color=(.1, .1, .1))

ax3.set_xlabel("Frequency (MHz)")
ax3.set_ylabel("$|d \\tau|$")
ax3.set_title("Comparison of Tolerance and Parasitic Effects in L1 on $\\tau$")
ax3.legend()

plot.show()
