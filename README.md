# Introduction
Modular multiplication is a fundamental and performance determining operation in various public-key cryptosystems. 
High-performance modular multipliers on FPGAs are commonly realized by several small-sized multipliers, an
adder tree for summing up the digit-products and a reduction circuit. While small-sized multipliers are available on pre-fabricated high-speed DSP slices, the adder tree and reduction circuit are implemented on standard logic. These latter operations represent the performance bottleneck to high-performance implementations. We report improved performance by regrouping digit-products on bit-level while incorporating the reduction for Mersenne primes. Our approach leads to very fast modular multipliers whose latency and throughput characteristics outperform all previous results. 

This tool can be used for generating a hardware description (VHDL) of high-performance modular multipliers for user chosen Mersenne primes from any small-sized multipliers.

The code will be online, once the paper is published.
