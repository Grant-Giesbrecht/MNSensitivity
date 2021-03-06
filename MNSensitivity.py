from enum import Enum
import copy

class Network:

    def __init__(self, circ:list, Z_s:complex, Z_l:complex, freq:float):

        self.circ = circ
        self.Z_s = Z_s
        self.Z_l = Z_l
        self.freq = freq
        self.V_in = 1

    def __str__(self):
        out = f"Zs: {self.Z_s} ohms, Zl: {self.Z_l} ohms, freq: {self.freq} Hz, V_in: {self.V_in} V\n"
        for c in self.circ:
            a = c[0]
            b = c[1]
            out = out + f"\t{a},\t {b}\n"
        return out

    def __repr__(self):
        return self.__str__()


class Passive(Enum):
    """ Defines an enumerated type for specifying if a given component is
    a resistor, capacitor, or inductor.
    """

    R = 1
    C = 2
    L = 3

class Values:
    """ Defines a set of R, L, C to describe a component and it's parasitics
    """

    def __init__(self, R:float, L:float, C:float):

        self.R = R
        self.L = L
        self.C = C

class Component:
    """ Defines a component which can be a resistor, capacitor or inductor. A matching
    network in this program is comprised solely of these elements.

        | |       L            __________
    ----| |---_/\/\/\/\/\__----|________|---        <-- Capacitor Model
     C  | |                          R

                    _____| |______
                   |    C| |     |
    _/\/\/\/\/\_---|   _______   |----              <----- Resistor Model
          L        |--|_______|--|
                        R

        __________| |_________________
       |        C | |                 |
       |               _________      |             <---- Inductor Model
    ___|__/\/\/\/\____|    R    |_____|____
               L      |_________|
    """

    def __init__(self, init_str:str):

        self.val = Values(0, 0, 0)
        self.type = None
        self.name = "Unnamed Component"

        self.read_vals(init_str)

    def __str__(self):

        return f"{self.name}({self.type}) = R:{self.val.R}, C:{self.val.C}, L:{self.val.L}"

    def __repr__(self):
        return self.__str__()

    def read_vals(self, init_str:str):
        """ Reads values from an initialization string and stores them in the
        component class.

        Format:
        -------
        <name> <type (options=C, L, R)> <parameter (option=C, L, R)>
         <param_value (in SI units)> ... repeat param value expressions as
         desired ...

        unspecified parameters are set to zero

        Example:
        --------
        "C1 C L 1e-10 R .1 C 1e-6" Creates a component "C1" of type "C" with
        L=1e-10 H, R = .1 Ohms, C=1e-6 F.

        """

        words = init_str.split()

        if len(words) < 4:
            print("ERROR: Too few words in initialization stirng. requires at minimum 4.")
            self.name = "Unnamed Component"
            return None

        #Set name
        self.name = words[0]

        if words[1].upper() == "C":
            self.type = Passive.C
        elif words[1].upper() == "L":
            self.type = Passive.L
        elif words[1].upper() == "R":
            self.type = Passive.R

        #Loop through words and interpret values
        w = 2
        while w+1 < len(words):

            if words[w].upper() == "C":
                try:
                    self.val.C = float(words[w+1])
                except:
                    failed_word = words[w+1]
                    print(f"Failed to convert {failed_word} to float")
                    return None
            elif words[w].upper() == "L":
                try:
                    self.val.L = float(words[w+1])
                except:
                    failed_word = words[w+1]
                    print(f"Failed to convert {failed_word} to float")
                    return None
            elif words[w].upper() == "R":
                try:
                    self.val.R = float(words[w+1])
                except:
                    failed_word = words[w+1]
                    print(f"Failed to convert {failed_word} to float")
                    return None

            w += 2

    def Z(self, freq:float):

        if self.type == Passive.C:

            if self.Z_C(freq) == None:
                print(f"WARNING: Capacitor {self.name} has 0 capacitance. Will behave like R or L.")
                return self.Z_L(freq) + self.val.R
            else:
                return self.val.R + self.Z_L(freq) + self.Z_C(freq)

        elif self.type == Passive.L:

            if self.Z_C(freq) == None:
                return self.Z_L(freq) + self.val.R
            else:
                return self.pall(self.Z_L(freq) + self.val.R, self.Z_C(freq))
        elif self.type == Passive.R:

            if self.Z_C(freq) == None:
                return self.Z_L(freq) + self.val.R
            else:
                return self.Z_L(freq) + self.pall(self.val.R, self.Z_C(freq))

        else:
            print(f"ERROR: component {self.name} does not have a valid type {self.type}.")
            return None

    def Z_C(self, f:float):
        """ Calculates the impedance of a capacitor """

        if self.val.C == 0 or f == 0:
            return None

        return complex(0, -1)/(2*3.14159*f*self.val.C)

    def Z_L(self, f:float):
        """ Calculates the impedance of a capacitor """
        return complex(0, 1)*(2*3.14159*f*self.val.L)

    def pall(self, Z1:complex, Z2:complex):
        """ Calculates the impedance of two parallel elements """
        return Z1*Z2/(Z1+Z2)

    def str(self):

        out = ""
        if self.type == Passive.R:
            out = out + "RES-["
        if self.type == Passive.L:
            out = out + "IND-["
        if self.type == Passive.C:
            out = out + "CAP-["

        return out + str(f"R={self.val.R}, L={self.val.L}, C={self.val.C}]")


def print_circuit(circ:list):
    """ Prints the components in a Circuit List (format is 1D array of tuples,
    the first element contains a Component object, the 2nd a SER/PAL string)
    """

    for t in circ:

        try:
            orientation = t[1]
            comp = t[0]
            print(f"{orientation}: {comp.str()}")
        except:
            print("ERROR")

def load_circuit(filename:str):
    """ Reads a MNSensitivity cicuit file (.mc) and returns a Circuit list
    (format is 1D array of tuples, the first element contains a Component
    object, the 2nd a SER/PAL string).

    Format of the .mc file is:
        * each line contains a Component object init string (See Component class
          doc string to see format) after an orientation string (SER or PAL,
          specifies if the component is series or parallel to ground).
        * Comments can be specified by '#'
        * Blank lines are skipped
        * Components with earliest line number is assumed closest to source,
          last line number closest to load, and progressively inbetween.
    """

    circuit = []

    lnum = 0

    #Open file...
    with open(filename) as file:

        #For each line...
        while True:

            #Read line...
            line = file.readline()
            lnum += 1;
            if not line:
                break;

            #Break into tokens...
            words = line.split()

            if len(words) == 0:
                continue

            #Skip comments
            if words[0] == "#" or words[0][0] == '#':
                continue

            if len(words) < 5:
                print(f"ERROR: Fewer than 5 words on line {lnum}.")
                print(words)
                return []

            try:
                idx = line.find(" ")
                new_comp = Component(line[idx+1:])
            except:
                print(f"Failed to interpret component string on line {lnum}.")
                return []


            if words[0].upper() == "SER":
                circuit.append( (new_comp, "SER") )
            elif words[0].upper() == "PAL":
                circuit.append( (new_comp, "PAL") )
            else:
                unrectok = words[0]
                print(f"ERROR: Unrecognized orientation token '{unrectok}' on line {lnum}. Acceptable tokens are 'SER' and 'PAL'.")
                return []

    return circuit

def pall(Z1:complex, Z2:complex):
    """ Calculates the impedance of two parallel elements """
    return Z1*Z2/(Z1+Z2)

def Z_out(circuit:list, freq:float, Zsource:complex):
    """ Takes a circuit list (see load_circuit for format info) and frequency
    and calculates the equivilient output impedance of the network.
    """

    Zout = Zsource
    last_comp_name = None

    for t in circuit:

        #Verifies that the circuit element is valid
        try:
            #Read component
            comp = t[0]
            comp.Z_L(1) #Will fail if not a component class

            #Read orientation
            orientation = t[1]
            if orientation.upper() != "SER" and orientation.upper() != "PAL":
                print(f"ERROR: Invalid orientation '{orientation}' in circuit. Element: '{comp.name}'")
                return None
        except Exception as e:
            print(f"ERROR: Invalid circuit element. {str(e)}")
            try:
                print(f"\tError occured with component: {comp.name}")
            except:
                if last_comp_name == None:
                    print("\tError occured with first component.")
                else:
                    print(f"\tError occured because missing component object. Last valid component object: {last_comp_name}")

            return None

        #Save component name in case error occurs later and need to identify where
        last_comp_name = comp.name

        #If next element is parallel
        if orientation == "PAL":
            Zout = pall(Zout, comp.Z(freq))
        elif orientation == "SER":
            Zout = Zout + comp.Z(freq)

    return Zout

def P_load(Z_l:complex, Z_s:complex, Vin:float=1):

    return Vin**2 * Z_l.real/(Z_l+Z_s)**2

def P_net(network):

    return P_load(network.Z_l, Z_out(network.circ, network.freq, network.Z_s), network.V_in)

def tau_net(network):
    Z_net = Z_out(network.circ, network.freq, network.Z_s)
    return (4*network.Z_l*Z_net)/(network.Z_l**2 + 2*network.Z_l*Z_net + Z_net**2)

def sens_percent(network, param:str, val):
    """
    val: multiplier (2 -> +100%, 1 -> no change, etc)
    """


    if type(val) != float and type(val) != float and type(val) != int:
        print("ERROR: Value must be float, complex or int type.")
        return None

    net = copy.deepcopy(network)

    if param.upper() == "FREQ":
        net.freq *= val
        dv = net.freq*abs(val-1)
    elif param.upper() == "Z_L":
        net.Z_l *= val
        dv = net.Z_l*abs(val-1)
    elif param.upper() == "Z_S":
        net.Z_s *= val
        dv = net.Z_s*abs(val-1)
    elif param.upper() == "VIN":
        net.V_in *= val
        dv = net.V_in*abs(val-1)
    else:
        words = param.split()
        if len(words) < 2:
            print("ERROR: Invalid parameter. Fewer than two words.")
            return None
        element_name = words[0]
        val_name = words[1]

        element = None
        for t in net.circ:
            if t[0].name.upper() == element_name.upper():
                element = t[0]

        if element == None:
            print("ERROR: Element not found.")
            return None

        if val_name.upper() == "C":
            element.val.C *= val
            dv = element.val.C*abs(val-1)
        elif val_name.upper() == "L":
            element.val.L *= val
            dv = element.val.L*abs(val-1)
        elif val_name.upper() == "R":
            element.val.R *= val
            dv = element.val.R*abs(val-1)
        else:
            print(f"ERROR: Invalid element parameter '{val_name}'.")
            return None

    t0 = tau_net(network)
    t1 = tau_net(net)
    dT = t1-t0
    dTdV = dT/dv
    print(f"dv = {dv} val={val}")
    return (dTdV, dT, t0, t1)

def sens_pcnt(network, param:str, val=1):
    """
    Same as sens_percent() except val is in percent-100
    ie. val=1 -> multiplier of 1.01, val=0 -> multiplier 1, val 50 -> multiplier 1.5

    has abbreviated return
    """

    return abs(sens_percent(network, param, 1+val/100.0)[0])

def sens_percent(network, param:str, val):
    """
    val: multiplier (2 -> +100%, 1 -> no change, etc)
    """


    if type(val) != float and type(val) != float and type(val) != int:
        print("ERROR: Value must be float, complex or int type.")
        return None

    if param.upper() == "FREQ":
        dv = network.freq*abs(val-1)
    elif param.upper() == "Z_L":
        dv = network.Z_l*abs(val-1)
    elif param.upper() == "Z_S":
        dv = network.Z_s*abs(val-1)
    elif param.upper() == "VIN":
        dv = network.V_in*abs(val-1)
    else:
        words = param.split()
        if len(words) < 2:
            print("ERROR: Invalid parameter. Fewer than two words.")
            return None
        element_name = words[0]
        val_name = words[1]

        element = None
        for t in network.circ:
            if t[0].name.upper() == element_name.upper():
                element = t[0]

        if element == None:
            print("ERROR: Element not found.")
            return None

        if val_name.upper() == "C":
            dv = element.val.C*abs(val-1)
        elif val_name.upper() == "L":
            dv = element.val.L*abs(val-1)
        elif val_name.upper() == "R":
            dv = element.val.R*abs(val-1)


    return sensitivity(network, param, dv, True)

def sensitivity(network, param:str, val, use_tau=False):

    if type(val) != float and type(val) != float and type(val) != int:
        print("ERROR: Value must be float, complex or int type.")
        return None

    net = copy.deepcopy(network)

    if param.upper() == "FREQ":
        net.freq += val
    elif param.upper() == "Z_L":
        net.Z_l += val
    elif param.upper() == "Z_S":
        net.Z_s += val
    elif param.upper() == "VIN":
        net.V_in += val
    else:
        words = param.split()
        if len(words) < 2:
            print("ERROR: Invalid parameter. Fewer than two words.")
            return None
        element_name = words[0]
        val_name = words[1]

        element = None
        for t in net.circ:
            if t[0].name.upper() == element_name.upper():
                element = t[0]

        if element == None:
            print("ERROR: Element not found.")
            return None

        if val_name.upper() == "C":
            element.val.C += val
        elif val_name.upper() == "L":
            element.val.L += val
        elif val_name.upper() == "R":
            element.val.R += val
        else:
            print(f"ERROR: Invalid element parameter '{val_name}'.")
            return None

    if use_tau:
        t0 = tau_net(network)
        t1 = tau_net(net)
        dT = t1-t0
        dTdV = dT/val
        return (dTdV, dT, t0, t1)

    P0 = P_net(network)
    P1 = P_net(net)

    dP = P1-P0

    dPdV = dP/val

    return (dPdV, dP, P0, P1)

def get_spectrum_pcnt(network, param, fs, val=1):

    f_orig = network.freq

    sens = []

    for f in fs:
        network.freq = f
        sens.append(sens_pcnt(network, param, val))

    network.freq = f_orig

    return sens

def get_spectrum_val(network, param, fs, val):

    f_orig = network.freq

    sens = []

    for f in fs:
        network.freq = f
        sens.append(abs(sensitivity(network, param, val, True)[0]))
        # sens.append(sens_pcnt(network, param, val))

    network.freq = f_orig

    return sens

def get_spectrum_norm(network, param, fs, val=1, abs_val=None):

    f_orig = network.freq

    sens = []

    for f in fs:
        network.freq = f
        if abs_val is not None:
            sens.append(abs(sensitivity(network, param, abs_val, use_tau=True)[1]))
        else:
            sens.append(abs(sens_percent(network, param, 1+val/100.0)[1]))

    network.freq = f_orig

    return sens
