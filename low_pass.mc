################################################################################
# This describes a simple L-C matching network                                 #
#                                                                              #
# Each line describes one element. Follows format:                             #
#                                                                              #
#   <orientation {SER, PAL}>  <element_name>  <element type {L,C,R}>           #
#      <parameter {L,C,R}> <parameter_value> ...                               #
#                                                                              #
# Up to three parameter-value pairs can be provided on one line. Unspecificed  #
# parameters will be assumed to equal 0.                                       #
#                                                                              #
#   Ex: "PAL R1 R L 100e-12 R 100" describes a parallel resistor called 'R1'   #
#       with a value of 100 ohms, a parasitic inductance of 100 pH, and no     #
#       parasitic capacitance.                                                 #
#                                                                              #
################################################################################

SER L1 L L 8.9e-9
PAL C1 C C 10.1e-12
