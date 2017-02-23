#!/usr/bin/python3
"""File that can be used for multiplier generation."""

import mod_mul_mersenne

def main():
    """Example function that demonstrates the multiplier generation."""
    # user input/output
    exp_prime = int(input("Enter exponent 'p' for Mersenne prime 2^p-1: p = "))
    dsp_mul_width_a = int(input("Enter 'm' for m*n-bit DSP multiplier: m = "))
    dsp_mul_width_b = int(input("Enter 'n' for m*n-bit DSP multiplier: n = "))

    # compute optimized adder tree
    m, n, x, y = mod_mul_mersenne.op_decomp(exp_prime, dsp_mul_width_a, dsp_mul_width_b)
    dp_list = mod_mul_mersenne.digit_product_generation(m, n, x, y)
    bit_list = mod_mul_mersenne.bit_slice_generation(dp_list, exp_prime)
    pp_list = mod_mul_mersenne.partial_product_generation(bit_list, exp_prime)

    mod_mul_mersenne.print_partial_products(pp_list)

    # generate VHDL code
    mod_mul_mersenne.generate_vhdl(pp_list, exp_prime, m, n, x, y)
    mod_mul_mersenne.generate_vhdl_tb(pp_list, exp_prime)
    mod_mul_mersenne.generate_test_set(exp_prime)

    print("VHDL code successfully generated.")

if __name__ == "__main__":
    main()
