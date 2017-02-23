"""File holds the three classes Bit, DigitProduct, and PartialProduct."""

class Bit:
    """Class Bit represents a single bit of a digit-product."""

    def __init__(self, identifier, absolute, relative):
        self.identifier = identifier
        self.absolute = absolute
        self.relative = relative

    def shift(self, x_bits):
        """Shift bit in its absolute position by x_bits."""
        self.absolute %= x_bits

    def print_info(self):
        """Print class info."""
        print("identifier =", self.identifier)
        print("absolute =", self.absolute)
        print("relative =", self.relative)


class DigitProduct():
    """Class DigitProduct represents a DSP multiplier i.e. digit-product."""

    def __init__(self, identifier, lsb, msb):
        self.identifier = identifier
        self.lsb = lsb
        self.msb = msb

    def slice_block(self):
        """Slice digit-product in single bits."""
        bit_list = []
        for i in range(0, self.msb-self.lsb+1):
            bit_list.append(Bit(self.identifier, self.lsb+i, i))
        return bit_list

    def print_info(self):
        """Print class info."""
        print("identifier =", self.identifier)
        print(self.msb, "downto", self.lsb)


class PartialProduct:
    """Class PartialProduct represents a partial-product that can hold an
    undefined amount of class Bit instances."""

    def __init__(self, exp_prime):
        self.bit_list = []
        self.exp_prime = exp_prime

    def add_bit(self, new_bit):
        """Add bit to current partial-product."""
        for current_bit in self.bit_list:
            if current_bit.absolute == new_bit.absolute:
                return False
        self.bit_list.append(new_bit)
        return True

    def print_info(self):
        """Print class info of all bits contained in this partial-product."""
        for current_bit in self.bit_list:
            current_bit.print_info()

    def print_line(self, line_number):
        """Print partial-product indicating whether bit positions are taken."""
        print("PP%#02d"% line_number, end="  ")
        for i in range(0, self.exp_prime):
            success = 0
            for current_bit in self.bit_list:
                if current_bit.absolute == i:
                    success = 1
            if success == 1:
                print("o", end="")
            else:
                print("x", end="")
        print("")
