"""File contains functions to generate the multiplier's hardware description."""

import os
import math

def generate_vhdl_tb(pp_list, exp_prime):
    """Top-level function to generate VHDL code."""
    file_ptr = open(("vhdl/mod_mul_tb.vhd"), 'w')
    cycles = math.ceil(math.log2(len(pp_list)))+3
    write_lib(file_ptr)
    write_entity(file_ptr, exp_prime)
    write_architecture(file_ptr, cycles)

def write_lib(file_ptr):
    """Write library and use instructions to VHDL file."""
    file_ptr.write("Library ieee;\n")
    file_ptr.write("use ieee.std_logic_1164.all;\n")
    file_ptr.write("use ieee.numeric_std.all;\n")
    file_ptr.write("use ieee.std_logic_textio.all;\n")
    file_ptr.write("use std.textio.all;\n\n")

def write_entity(file_ptr, exp_prime):
    """Declare entity in VHDL code."""
    ceil_byte_exp_prime = exp_prime
    rem = (exp_prime)%8
    if rem != 0:
        ceil_byte_exp_prime = exp_prime+(8-exp_prime%8)
    file_ptr.write("entity mod_mul_tb is\n")
    file_ptr.write("\t generic(\n")
    file_ptr.write("\t\t TB_WIDTH : integer := "+str(exp_prime)+";\n")
    file_ptr.write("\t\t TV_WIDTH : integer := "+str(ceil_byte_exp_prime)+"\n")
    file_ptr.write("\t );\n")
    file_ptr.write("end mod_mul_tb;\n\n")

def write_component(file_ptr):
    """Declare component in VHDL code."""
    file_ptr.write("\t component mod_mul is\n")
    file_ptr.write("\t\t port(\n")
    file_ptr.write("\t\t\t clk: in std_ulogic;\n")
    file_ptr.write("\t\t\t a_i: in std_ulogic_vector(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t\t\t b_i: in std_ulogic_vector(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t\t\t c_o: out std_ulogic_vector(TB_WIDTH-1 downto 0)\n")
    file_ptr.write("\t\t );\n")
    file_ptr.write("\t end component;\n\n")

def write_architecture(file_ptr, cycles):
    """Declare component in VHDL code."""
    cwd = os.getcwd()
    file_ptr.write("architecture behavioral of mod_mul_tb is\n\n")
    write_component(file_ptr)
    file_ptr.write("\t signal a: std_ulogic_vector(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t signal b: std_ulogic_vector(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t signal c: std_ulogic_vector(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t signal result_test: std_ulogic_vector(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t signal clk: std_ulogic := '0';\n\n")
    file_ptr.write("\t file file_a: text open read_mode is \""+str(cwd)+"/vhdl/tv_a.txt\";\n")
    file_ptr.write("\t file file_b: text open read_mode is \""+str(cwd)+"/vhdl/tv_b.txt\";\n")
    file_ptr.write("\t file file_c: text open read_mode is \""+str(cwd)+"/vhdl/tv_c.txt\";\n\n")
    file_ptr.write("\t type test_array is array (1000-1 downto 0) of std_ulogic_vector(TV_WIDTH-1 downto 0);\n")
    file_ptr.write("\t signal a_v: test_array;\n")
    file_ptr.write("\t signal b_v: test_array;\n")
    file_ptr.write("\t signal result_v: test_array;\n\n")
    file_ptr.write("\t begin\n")
    file_ptr.write("\t clk <= not clk after 5 ns;\n\n")
    file_ptr.write("\t readf_testvectors: process\n")
    file_ptr.write("\t\t variable rdline: line;\n")
    file_ptr.write("\t\t variable a_var, b_var: std_ulogic_vector(TV_WIDTH-1 downto 0);\n")
    file_ptr.write("\t\t variable c_var: std_ulogic_vector((TV_WIDTH-1) downto 0);\n")
    file_ptr.write("\t\t begin\n")
    file_ptr.write("\t\t\t for i in 0 to 1000-1 loop\n")
    file_ptr.write("\t\t\t\t -- read key\n")
    file_ptr.write("\t\t\t\t readline(file_a, rdline);\n")
    file_ptr.write("\t\t\t\t hread(rdline, a_var);\n")
    file_ptr.write("\t\t\t\t a_v(i) <= a_var;\n")
    file_ptr.write("\t\t\t\t -- read plain\n")
    file_ptr.write("\t\t\t\t readline(file_b, rdline);\n")
    file_ptr.write("\t\t\t\t hread(rdline, b_var);\n")
    file_ptr.write("\t\t\t\t b_v(i) <= b_var;\n")
    file_ptr.write("\t\t\t\t -- read cipher\n")
    file_ptr.write("\t\t\t\t readline(file_c, rdline);\n")
    file_ptr.write("\t\t\t\t hread(rdline, c_var);\n")
    file_ptr.write("\t\t\t\t result_v(i) <= c_var;\n")
    file_ptr.write("\t\t\t end loop;\n")
    file_ptr.write("\t\t wait;\n")
    file_ptr.write("\t end process readf_testvectors;\n\n")
    file_ptr.write("\t stim_results: process\n")
    file_ptr.write("\t\t begin\n")
    file_ptr.write("\t\t wait for 100ns;\n")
    file_ptr.write("\t\t for i in 0 to 1000-1 loop\n")
    file_ptr.write("\t\t\t a <= a_v(i)(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t\t\t b <= b_v(i)(TB_WIDTH-1 downto 0);\n")
    file_ptr.write("\t\t\t result_test <= result_v(i)(TB_WIDTH-1 downto 0);\n")
    for i in range(cycles+1):
        file_ptr.write("\t\t\t wait until rising_edge(clk);\n")
    file_ptr.write("\t\t\t assert (c = result_test) report \"wrong result!\" severity failure;\n")
    file_ptr.write("\t\t end loop;\n")
    file_ptr.write("\t\t report \"SUCCESS: all modular multiplications successfully calculated!\";\n")
    file_ptr.write("\t\t wait;\n")
    file_ptr.write("\t end process stim_results;\n\n")

    file_ptr.write("\t DUT: mod_mul port map(\n")
    file_ptr.write("\t\t clk => clk,\n")
    file_ptr.write("\t\t a_i => a(TB_WIDTH-1 downto 0),\n")
    file_ptr.write("\t\t b_i => b(TB_WIDTH-1 downto 0),\n")
    file_ptr.write("\t\t c_o => c(TB_WIDTH-1 downto 0)\n")
    file_ptr.write("\t );\n\n")

    file_ptr.write("\t end architecture behavioral;\n")
