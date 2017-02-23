"""File defines top-level functions."""

import math
from .classes import DigitProduct
from .classes import PartialProduct

def op_decomp(exp_prime, dsp_mul_width_a, dsp_mul_width_b):
    """Perform operand decomposition."""
    # determine whether A and B are decomposed by m or n respectively
    x = math.ceil(exp_prime/float(dsp_mul_width_a))
    y = math.ceil(exp_prime/float(dsp_mul_width_b))
    m, n = dsp_mul_width_a, dsp_mul_width_b
    # operand A shall consist of fewer digits than operand B
    if x > y:
        x, y = y, x
        m, n = n, m
    print("Required DSP slices =", x*y)
    print("Multiplier Width =", x*m, "*", y*n)
    print("m, n =", str(m)+str(", ")+str(n))
    print("x, y =", str(x)+str(", ")+str(y))
    return (m, n, x, y)

def digit_product_generation(m, n, x, y):
    """Generate digit-products."""
    dp_list = []
    for j in range(0, y):
        for i in range(0, x):
            lsb = i*m+j*n
            msb = lsb+m+n-1
            identifier = (i, j)
            dp_list.append(DigitProduct(identifier, lsb, msb))
    return dp_list

def bit_slice_generation(dp_list, exp_prime):
    """Slice digit-products."""
    sliced_list = []
    for dp in dp_list:
        sliced_list += dp.slice_block()
    sliced_list = remove_unused_bits(sliced_list, exp_prime)
    sliced_list = shift_bits(sliced_list, exp_prime)
    return sliced_list

def remove_unused_bits(bit_list, limit):
    """Remove bits that have greater bit position that limit."""
    reduced_list = []
    for bit in bit_list:
        if bit.absolute <= ((2*limit)-1):
            reduced_list.append(bit)
    return reduced_list

def shift_bits(bit_list, limit):
    """Shift bits to the right that have greater bit position that limit."""
    shifted_list = []
    for bit in bit_list:
        bit.shift(limit)
        shifted_list.append(bit)
    return shifted_list

def partial_product_generation(bit_list, exp_prime):
    """Generate partial-products."""
    pp_list = []
    while bit_list:
        pp = PartialProduct(exp_prime)
        tmp_bit_list = []
        for bit in bit_list:
            check = pp.add_bit(bit)
            if check is False:
                tmp_bit_list.append(bit)
        bit_list = tmp_bit_list
        pp_list.append(pp)
    return pp_list

def print_partial_products(pp_list):
    """Print partial-product utilization."""
    cycles = math.ceil(math.log2(len(pp_list)))+3 #3 = 1*mul+2*red
    print("Required cycles = ", cycles)
    print("************************ PARTIAL-PRODUCTS ************************")
    for i, bit in enumerate(pp_list):
        bit.print_line(i)
    print("******************************************************************")
