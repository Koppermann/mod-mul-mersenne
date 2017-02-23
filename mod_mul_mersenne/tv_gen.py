"""This file contains a function to generate the test vectors for the modular multiplier."""

import random

def generate_test_set(exp_prime):
    """Function to generate test vectors. """
    ceil_byte_exp_prime = exp_prime
    rem = (exp_prime)%8
    if rem != 0:
        ceil_byte_exp_prime = exp_prime+(8-exp_prime%8)
    nmb_bytes = int(ceil_byte_exp_prime/8)

    file_ptr_a = open(("vhdl/tv_a.txt"), 'w')
    file_ptr_b = open(("vhdl/tv_b.txt"), 'w')
    file_ptr_c = open(("vhdl/tv_c.txt"), 'w')

    # corner cases
    for x in range(2, 10):
        a = (2**exp_prime)-x
        a_hex = hex(a)[2:].zfill(int(ceil_byte_exp_prime/4))
        b = (2**exp_prime)-x
        b_hex = hex(b)[2:].zfill(int(ceil_byte_exp_prime/4))
        file_ptr_a.write(str(a_hex)+"\n")
        file_ptr_b.write(str(b_hex)+"\n")
        c = (a*b)%((2**exp_prime)-1)
        c = hex(c)[2:].zfill(int(nmb_bytes*2))
        file_ptr_c.write(str(c)+"\n")

    for x in range(0, 999):
        a = random.getrandbits(exp_prime)
        a_hex = hex(a)[2:].zfill(int(ceil_byte_exp_prime/4))
        b = random.getrandbits(exp_prime)
        b_hex = hex(b)[2:].zfill(int(ceil_byte_exp_prime/4))
        file_ptr_a.write(str(a_hex)+"\n")
        file_ptr_b.write(str(b_hex)+"\n")
        c = (a*b)%((2**exp_prime)-1)
        c = hex(c)[2:].zfill(int(nmb_bytes*2))
        file_ptr_c.write(str(c)+"\n")
