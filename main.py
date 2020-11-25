from MNSensitivity import *

circ = load_circuit("simple.mc")
print_circuit(circ)

print(f"\n\tZout at 1 kHz = {Z_out(circ, 1e3, complex(50, 0) )}")
