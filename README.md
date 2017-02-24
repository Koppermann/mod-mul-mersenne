# Introduction
Modular multiplication is a fundamental and performance determining operation in various public-key cryptosystems. 
High-performance modular multipliers on FPGAs are commonly realized by several small-sized multipliers, an
adder tree for summing up the digit-products and a reduction circuit. While small-sized multipliers are available on pre-fabricated high-speed DSP slices, the adder tree and reduction circuit are implemented on standard logic. These latter operations represent the performance bottleneck to high-performance implementations. We report improved performance by regrouping digit-products on bit-level while incorporating the reduction for Mersenne primes. Our approach leads to very fast modular multipliers whose latency and throughput characteristics outperform all previous results. 

This tool can be used for generating a hardware description (VHDL) of high-performance modular multipliers for user chosen Mersenne primes from any small-sized multipliers.

The details and results can found in the paper "Automatic Generation of High-Performance Modular Multipliers for Arbitrary Mersenne Primes on FPGAs
", which has been accepted at [HOST'17](http://www.hostsymposium.org/accepted-list.php).

# How to Run
Before running this tool, make sure to have Python3 and pip3 installed. Then run:
```shell
git clone https://github.com/Fraunhofer-AISEC/mod-mul-mersenne.git
cd mod-mul-mersenne
sudo pip3 install .
```
In order to generate the modular multiplier, you need to change directory to example/ and run the script example.py, which will prompt the user for the Mersenne prime and the widths of the DSP input operands m*n. 
```shell
cd example
./example.py
```
After you input the parameters, the vhdl code (*mod_mul.vhd*) including testbench (*mod_mul_tb.vhd*) and testvectors (*tv_a.txt*, *tv_b.txt*, *tv_c.txt*) can be found in the vhdl/ folder.

**Note**: If you want to simulate or synthesize a modular multiplier using other than DSP48E1 dsp slices, you need to add your own VHDL hardware description of the respective DSP primitive (*dsp_mul.vhd*). 

# Performance Results
The following table shows the performance results of modular multipliers for different Mersenne primes synthesized on a Zynq-7020 and a Zynq-7045: 

| FPGA      | Mers. Prime | Mult. Width | Cycles | Freq. [MHz] | TP [GBit/s] | Time [ns] | #DSP | #LUTs | #Slices | #Regs |
|-----------|-------------|-------------|--------|-------------|-------------|-----------|------|-------|---------|-------|
| Zynq-7020 |      2^61-1 | 72*68       |      7 |         250 |       15.25 |     28.00 |   12 |   430 |     158 |   634 |
| Zynq-7020 |      2^89-1 | 96*102      |      7 |      198.85 |       17.70 |     35.20 |   24 |   889 |     333 |  1239 |
| Zynq-7020 |     2^107-1 | 120*119     |      7 |      171.78 |       18.38 |     40.75 |   35 |  1315 |     439 |  1697 |
| Zynq-7020 |     2^127-1 | 144*136     |      7 |      156.00 |       19.81 |     44.87 |   48 |  1821 |     547 |  2169 |
| Zynq-7045 |      2^61-1 | 72*68       |      7 |      454.55 |       27.73 |      15.4 |   12 |   422 |     157 |   650 |
| Zynq-7045 |      2^89-1 | 96*102      |      7 |      377.36 |       33.59 |     18.55 |   24 |   889 |     306 |  1239 |
| Zynq-7045 |     2^107-1 | 120*119     |      7 |      333.33 |       35.67 |     21.00 |   35 |  1315 |     428 |  1697 |
| Zynq-7045 |     2^127-1 | 144*136     |      7 |      307.69 |       39.08 |     22.75 |   48 |  1821 |     543 |  2169 |
| Zynq-7045 |     2^521-1 | 528*527     |      9 |      106.38 |       55.42 |     84.60 |  682 | 27484 |    7527 | 29853 |
