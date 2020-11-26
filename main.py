from MNSensitivity import *

circ = load_circuit("simple.mc")
print_circuit(circ)

Z_s = 50
Z_l = 10
freq = 1e3

net = Network(circ, Z_s, Z_l, freq)

print(f"\n\tZout at 1 kHz = {Z_out(circ, 1e3, complex(50, 0) )}")

print(f"\n\tP_load (1V) (Zs=50R, Zl=10R) at 1 kHz = {P_load(10, Z_out(circ, 1e3, complex(50, 0) ), 1 )}")
print(f"\n\tP_load (1V) (Zs=50R, Zl=10R) at 1 kHz = {P_net(net)}")
