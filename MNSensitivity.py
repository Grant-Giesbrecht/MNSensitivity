from enum import Enum

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
            return self.val.R + self.Z_L(freq) + self.Z_C(freq)
        elif self.type == Passive.L:
            return self.pall(self.Z_L(freq) + self.val.R, self.Z_C(freq))
        elif self.type == Passive.R:
            return self.Z_L(freq) + self.pall(self.val.R, self.Z_C(freq))
        else:
            print(f"ERROR: component {self.name} does not have a valid type {self.type}.")
            return None

    def Z_C(self, f:float):
        """ Calculates the impedance of a capacitor """
        return complex(0, 1)/(2*3.14159*f*self.val.C)

    def Z_L(self, f:float):
        """ Calculates the impedance of a capacitor """
        return complex(0, 1)*(2*3.14159*f*self.val.L)

    def pall(self, Z1:complex, z2:complex):
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

    for t in circ:

        try:
            orientation = t[1]
            comp = t[0]
            print(f"{orientation}: {comp.str()}")
        except:
            print("ERROR")

def load_circuit(filename:str):

    circuit = []

    lnum = 0

    #Open file...
    with open(filename) as file:

        #For each line...
        while True:

            #Read line...
            line = file.readline()
            lnum += 0;
            if not line:
                break;

            #Break into tokens...
            words = line.split()
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
