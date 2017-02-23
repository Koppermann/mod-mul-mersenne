"""File contains functions to generate the multiplier's hardware description."""

import math

def generate_vhdl(pp_list, exp_prime, m, n, x, y,):
    """Top-level function to generate VHDL code."""
    file_ptr = open(("vhdl/mod_mul.vhd"), 'w')
    write_lib(file_ptr)
    write_entity(file_ptr, exp_prime, m, n, x, y)
    write_architecture(file_ptr, pp_list, exp_prime)

def write_lib(file_ptr):
    """Write library and use instructions to VHDL file."""
    file_ptr.write("library ieee;\n")
    file_ptr.write("use ieee.std_logic_1164.all;\n")
    file_ptr.write("use ieee.numeric_std.all;\n\n")

def write_entity(file_ptr, exp_prime, m, n, x, y):
    """Declare entity in VHDL code."""
    file_ptr.write("entity mod_mul is\n")
    file_ptr.write("\t generic(\n")
    file_ptr.write("\t\t EXP_PRIME : integer := "+str(exp_prime)+";\n")
    file_ptr.write("\t\t M : integer := "+str(m)+";\n")
    file_ptr.write("\t\t N : integer := "+str(n)+";\n")
    file_ptr.write("\t\t Y : integer := "+str(y)+";\n")
    file_ptr.write("\t\t X : integer := "+str(x)+"\n")
    file_ptr.write("\t );\n")
    file_ptr.write("\t port(\n")
    file_ptr.write("\t\t clk: in std_ulogic;\n")
    file_ptr.write("\t\t a_i: in std_ulogic_vector(EXP_PRIME-1 downto 0);\n")
    file_ptr.write("\t\t b_i: in std_ulogic_vector(EXP_PRIME-1 downto 0);\n")
    file_ptr.write("\t\t c_o: out std_ulogic_vector(EXP_PRIME-1 downto 0)\n")
    file_ptr.write("\t );\n")
    file_ptr.write("end mod_mul;\n\n")

def write_architecture(file_ptr, pp_list, exp_prime):
    """Declare architecture in VHDL code."""
    file_ptr.write("architecture behavioral of mod_mul is\n\n")
    write_dsp_component(file_ptr)
    signal_list = write_signal_declaration(file_ptr, pp_list, len(pp_list))

    file_ptr.write("\t begin\n\n")

    write_generate_component(file_ptr)
    write_regroup_dp(file_ptr, pp_list, exp_prime)

    file_ptr.write("\t process begin\n")
    file_ptr.write("\t wait until rising_edge(clk);\n")
    write_adder_tree(file_ptr, signal_list, exp_prime, len(pp_list))
    file_ptr.write("\t end process;\n")
    file_ptr.write("end architecture behavioral;")

def write_adder_tree(file_ptr, signal_list, exp_prime, number_pp):
    """Describe adder tree including reduction in VHDL code."""
    for i in range(1, len(signal_list)):
        j = 0
        for pp in signal_list[i]:
            if j == len(signal_list[i-1])-1:
                file_ptr.write("\t\t"+pp+" <= std_ulogic_vector(resize(unsigned("+signal_list[i-1][j]+"), "+pp+"'length));\n")
            else:
                file_ptr.write("\t\t"+pp+" <= std_ulogic_vector(resize(unsigned("+signal_list[i-1][j]+"), "+pp+"'length) + resize(unsigned("+signal_list[i-1][j+1]+"), "+pp+"'length));\n")
            j += 2
    file_ptr.write("\t\t c_red <= std_ulogic_vector(resize(unsigned("+pp+"(EXP_PRIME+"+str(len(signal_list)-2)+" downto EXP_PRIME)), c_red'length) + resize(unsigned("+pp+"(EXP_PRIME-1 downto 0)), c_red'length));\n")
    file_ptr.write("\t\t c_o <= std_ulogic_vector(resize(unsigned(c_red""(EXP_PRIME downto EXP_PRIME)), c_o'length) + resize(unsigned(c_red(EXP_PRIME-1 downto 0)), c_o'length));\n\n")

def write_dsp_component(file_ptr):
    """Declare component in VHDL code."""
    file_ptr.write("\t component dsp_mul is\n")
    file_ptr.write("\t\t port(\n")
    file_ptr.write("\t\t\t clk: in std_ulogic;\n")
    file_ptr.write("\t\t\t a_i: in std_ulogic_vector(M-1 downto 0);\n")
    file_ptr.write("\t\t\t b_i: in std_ulogic_vector(N-1 downto 0);\n")
    file_ptr.write("\t\t\t p_o: out std_ulogic_vector(M+N-1 downto 0)\n")
    file_ptr.write("\t\t );\n")
    file_ptr.write("\t end component;\n\n")

def write_signal_declaration(file_ptr, pp_list, number_pp):
    """Declare all signals in VHDL code."""
    file_ptr.write("\t signal a_s: std_ulogic_vector((M*X)-1 downto 0);\n")
    file_ptr.write("\t signal b_s: std_ulogic_vector((N*Y)-1 downto 0);\n")
    file_ptr.write("\t signal c_red: std_ulogic_vector(EXP_PRIME downto 0);\n")
    file_ptr.write("\t type a_array is array (0 to X-1) of std_ulogic_vector(M-1 downto 0);\n")
    file_ptr.write("\t type b_array is array (0 to Y-1) of std_ulogic_vector(N-1 downto 0);\n")
    file_ptr.write("\t signal digit_a_s: a_array;\n")
    file_ptr.write("\t signal digit_b_s: b_array;\n")
    file_ptr.write("\t type ab_element is array (0 to Y-1) of std_ulogic_vector(M+N-1 downto 0);\n")
    file_ptr.write("\t type ab_array is array (0 to X-1) of ab_element;\n")
    file_ptr.write("\t signal ab: ab_array;\n\n")
    number_pp = len(pp_list)
    adder_tree_depth = math.ceil(math.log(number_pp, 2))
    signal_list = [[] for i in range(adder_tree_depth+1)]
    file_ptr.write("\t signal ")
    for i in range(0, number_pp):
        signal_list[0].append("pp"+str(i))
        if i == number_pp-1:
            file_ptr.write("pp"+str(i))
        else:
            file_ptr.write("pp"+str(i)+", ")
    file_ptr.write(": std_ulogic_vector(EXP_PRIME-1 downto 0);\n")
    for i in range(adder_tree_depth):
        file_ptr.write("\t signal ")
        for j in range(0, len(signal_list[i]), 2):
            if j == len(signal_list[i])-2:
                file_ptr.write(signal_list[i][j]+signal_list[i][j+1])
                file_ptr.write(": std_ulogic_vector(EXP_PRIME+"+str(i)+" downto 0);\n")
                signal_list[i+1].append(signal_list[i][j]+signal_list[i][j+1])
            elif j == len(signal_list[i])-1:
                file_ptr.write(signal_list[i][j]+"x")
                file_ptr.write(": std_ulogic_vector(EXP_PRIME+"+str(i)+" downto 0);\n")
                signal_list[i+1].append(signal_list[i][j]+"x")
            else:
                file_ptr.write(signal_list[i][j]+signal_list[i][j+1]+", ")
                signal_list[i+1].append(signal_list[i][j]+signal_list[i][j+1])
    file_ptr.write("\n")
    return signal_list

def write_generate_component(file_ptr):
    """Write generate statements in VHDL code."""
    file_ptr.write("\t a_s <= std_ulogic_vector(resize(unsigned(a_i), a_s'length));\n")
    file_ptr.write("\t b_s <= std_ulogic_vector(resize(unsigned(b_i), b_s'length));\n\n")
    file_ptr.write("\t GEN_INPUT_A: for i in 0 to X-1 generate\n")
    file_ptr.write("\t\t digit_a_s(i) <= a_s((M*(i+1)-1) downto M*i);\n")
    file_ptr.write("\t end generate;\n\n")
    file_ptr.write("\t GEN_INPUT_B: for i in 0 to Y-1 generate\n")
    file_ptr.write("\t\t digit_b_s(i) <= b_s((n*(i+1)-1) downto n*i);\n")
    file_ptr.write("\t end generate;\n\n")
    file_ptr.write("\t GEN_DSP_I: for i in 0 to X-1 generate\n")
    file_ptr.write("\t\t GEN_DSP_J: for j in 0 to Y-1 generate\n")
    file_ptr.write("\t\t\t M1: DSP_MUL\n")
    file_ptr.write("\t\t\t port map (\n")
    file_ptr.write("\t\t\t\t clk => clk,\n")
    file_ptr.write("\t\t\t\t p_o => ab(i)(j),\n")
    file_ptr.write("\t\t\t\t a_i => digit_a_s(i),\n")
    file_ptr.write("\t\t\t\t b_i => digit_b_s(j)\n")
    file_ptr.write("\t\t\t );\n")
    file_ptr.write("\t\t end generate GEN_DSP_J;\n")
    file_ptr.write("\t end generate GEN_DSP_I;\n\n")

def write_regroup_dp(file_ptr, pp_list, exp_prime):
    """Perform digit-product regrouping."""
    for i in range(len(pp_list)):
        file_ptr.write("\t pp"+str(i)+" <= ")
        for j in range(exp_prime-1, -1, -1):
            success = 0
            for bit in pp_list[i].bit_list:
                if bit.absolute == j:
                    success = 1
                    file_ptr.write("ab("+str(bit.identifier[0])+")("+str(bit.identifier[1])+")("+str(bit.relative)+")")
            if success == 0:
                file_ptr.write("'0'")
            if j != 0:
                file_ptr.write(" & ")
        file_ptr.write(";\n")
