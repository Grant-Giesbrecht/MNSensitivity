from MNSensitivity import *
import numpy as np
import matplotlib.pyplot as plot

circ = load_circuit("low_pass.mc")
print_circuit(circ)

Z_s = 50
Z_l = complex(20, 30)
freq = 500e6

net = Network(circ, Z_s, Z_l, freq)

s_L1_a = abs(sensitivity(net, "L1 L", .05e-9, True)[0])
s_L1_b = abs(sensitivity(net, "L1 L", .1e-9, True)[0])
s_L1_c = abs(sensitivity(net, "L1 L", .2e-9, True)[0])
s_C1_a = abs(sens_percent(net, "L1 L", .05/8.9+1)[0])
s_C1_b = abs(sens_percent(net, "L1 L", .1/8.9+1)[0])
s_C1_c = abs(sens_percent(net, "L1 L", .2/8.9+1)[0])
# s_C1_a = abs(sens_percent(net, "C1 C", 1.005)[0])
# s_C1_b = abs(sens_percent(net, "C1 C", 1.01)[0])
# s_C1_c = abs(sens_percent(net, "C1 C", 1.02)[0])

print(s_L1_a)
print(s_L1_b)
print(s_L1_c)
print("")
print(s_C1_a)
print(s_C1_b)
print(s_C1_c)

n = 300
fs = np.logspace(6, 10, n)
sens = []
f_mhz = []
for f in fs:
    net.freq = f
    s = sensitivity(net, "L1 L", .1e-9, True)
    s_new = abs(s[0]/1e9) # units: 1/nH
    sens.append(s_new)
    f_mhz.append(f/1e6)

fig = plot.figure()
ax1 = fig.add_subplot(111)
ax1.semilogx(f_mhz, sens)
ax1.grid(True)

ax1.set_xlabel("Frequency (MHz)")
ax1.set_ylabel("Sensitivity (1/nH)")
ax1.set_title("Sensitivity to L1 vs Frequency for Simple Network")
plot.show()
# print(f"\n\tZout at 1 kHz = {Z_out(circ, 1e3, complex(50, 0) )}")
#
# print(f"\n\tP_load (1V) (Zs=50R, Zl=10R) at 1 kHz = {P_load(10, Z_out(circ, 1e3, complex(50, 0) ), 1 )}")
# print(f"\n\tP_load (1V) (Zs=50R, Zl=10R) at 1 kHz = {P_net(net)}")
