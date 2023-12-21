from migen import *


class SimpleShiftRegister(Module):
    """Base implementation of a simple shift-right register.

    At every clock cycle, the input data ('i') will be written in (shifted in) in the next clock cycle, while the output data will be read out (shifted out) in the next clock cycle. 

    The inner shift register (`sr`) has the size of (input width + data width). This register contains a buffer, which allows storing a new data value while shifting out the current data. At all times, `sr` needs to store exactly 1 whole data and all bits of the data to be shifted out.
    """
    def __init__(self, data_width, input_width, output_width):
        assert data_width >= input_width
        assert data_width >= output_width

        self.i = Signal(input_width)
        self.o = Signal(output_width)

        self._sr       = sr       = Signal(input_width + data_width)
        self._counter  = counter  = (Signal(max=input_width) if input_width>1
                                     else Signal())

        self.sync += [
            If(counter == 0,
                sr.eq(Cat(sr[1:output_width], self.i))
            ).Else(
                sr[:-1].eq(sr[1:])
            ),
            If(counter == input_width - 1,
                counter.eq(0)
            ).Else(
                counter.eq(counter + 1)
            )
        ]
        self.comb += self.o.eq(sr[0:output_width])


class SimpleShiftRegister_ParallelToSerial(SimpleShiftRegister):
    """A parallel-to-serial shift-right register.

    All bits of the new value are shifted in only right before all current bits are shifted out.
    """
    def __init__(self, data_width=8):
        super().__init__(data_width=data_width, input_width=data_width, output_width=1)


class SimpleShiftRegister_SerialToParallel(SimpleShiftRegister):
    """A serial-to-parallel shift-right register.

    Shifting out all bits of the current value is immediately followed byshifting in the first bit of the new value.
    """
    def __init__(self, data_width=8):
        super().__init__(data_width=data_width, input_width=1, output_width=data_width)
        self.o_valid = Signal()

        o_counter = Signal(max=data_width)

        self.sync += [
            If(o_counter == data_width - 1,
                o_counter.eq(0)
            ).Else(
                o_counter.eq(o_counter + 1)
            )
        ]
        self.comb += self.o_valid.eq(o_counter == 0)


def flipping_test(dut, init_value):
    assert init_value <= 0b11111111

    is_p2s = isinstance(dut, SimpleShiftRegister_ParallelToSerial)
    is_s2p = isinstance(dut, SimpleShiftRegister_SerialToParallel)

    init_value_flipped = ~init_value & 0b11111111
    data = [0 for _ in range(8)]    # reset value
    data_old = [(init_value >> i) & 1 for i in range(8)]
    data_new = [(init_value_flipped >> i) & 1 for i in range(8)]
    # For serial-in test: store the "next bit" index
    next_ind = 1

    # Assume t is a timer with a reset of 0
    for t in range(26):
        # Assign the init_value to input when t=4, flip the bits when t=16, and flip them back to the original value when t=21
        if t in (3, 20):
            data = data_old[:]
        if t == 15:
            data = data_new[:]
        # For parallel-in: 
        # - Assign input with all data bits as input all the time
        if is_p2s:
            for ind in range(8):
                yield dut.i[ind].eq(data[ind])
        # For serial-in: 
        # - Enable input all the time
        # - Move the next bit of the up-to-date data into the input
        elif is_s2p:
            yield dut.i.eq(data[next_ind])
        # Print the output for each cycle
        if is_p2s:
            print("t={:>2} : i == {}{}{}{}{}{}{}{}, o == {}"
                .format(t, 
                    (yield dut.i[7]), (yield dut.i[6]), (yield dut.i[5]), 
                    (yield dut.i[4]), (yield dut.i[3]), (yield dut.i[2]), 
                    (yield dut.i[1]), (yield dut.i[0]), 
                    (yield dut.o)),
                ("[input = {:08b}]".format(init_value) if t == 4 else 
                "[output = {:08b}]".format(0) if t == 8 else
                "[output = {:08b}, and input = {:08b}]".format(init_value, init_value_flipped) if t == 16 else
                "[input = {:08b}]".format(init_value) if t == 21 else
                "[output = {:08b}]".format(init_value_flipped) if t == 24 else
                "[reset, input = {:08b}]".format(0) if t == 0 else ""))
        elif is_s2p:
            print("t={:>2} : i == {}, o(valid={}) == {}{}{}{}{}{}{}{}"
                .format(t, (yield dut.i), (yield dut.o_valid), 
                    (yield dut.o[7]), (yield dut.o[6]), (yield dut.o[5]), 
                    (yield dut.o[4]), (yield dut.o[3]), (yield dut.o[2]), 
                    (yield dut.o[1]), (yield dut.o[0])),
                ("[input = {:04b}....]".format(init_value >> 4) if t == 4 else 
                "[valid output]" if t == 8 else
                "[valid output, and input = ...{:05b}]".format(init_value_flipped & 0b11111) if t == 16 else
                "[input = {:03b}....]".format(init_value >> 5) if t == 21 else 
                "[valid output]" if t == 24 else
                "[reset, input = {:08b}]".format(0) if t == 0 else ""))
        # When 1<=t<=4:
        # - For serial-out: output (bit 0 to 3) should correspond to the reset data value (i.e. 0x00)
        # - For serial-in: output is invalid; bit 3 is the newest bit (of the reset value) shifted in
        if t in range(1, 5):
            if is_p2s:
                assert (yield dut.o) == 0
            elif is_s2p:
                assert not (yield dut.o_valid)
        # When 5<=t<=8:
        # - For serial-out: although the first value has been inputted at t=6, the output (bit 4 to 7) should still correspond to the reset value, since it hasn't been fully shifted out
        # - For serial-in:
        #   - When t=5: the initial value gets assigned as input starting at t=5, so bit 4 from the first value has been shifted in
        #   - When 6<=t=7: bits 5 and 6 from the first value has been shifted in
        #   - When t=8: bit 7 has been shifted in so output is valid and should correspond to: bits 0 to 3 of the reset value (0b000), and bits 4 to 7 of the first value
        if t in range(5, 9):
            if is_p2s:
                assert (yield dut.o) == 0
            elif is_s2p:
                assert (not (yield dut.o_valid)) != (t == 8)
                if (yield dut.o_valid):
                    for i in range(0, 4):
                        assert (yield dut.o[i]) == 0
                    for i in range(4, 7):
                        assert (yield dut.o[i]) == data_old[i]
        # When 9<=t<=16:
        # - For serial-out: output should correspond to the first data value
        # - For serial-in: 
        #   - When 9<=t=15: bits 0 and 6 from the first value has been shifted in
        #   - When t=16: bit 7 has been shifted in so output is valid and should correspond to the first data value
        if t in range(9, 17):
            if is_p2s:
                assert (yield dut.o) == data_old[t-9]
            elif is_s2p:
                assert (not (yield dut.o_valid)) != (t == 16)
                if (yield dut.o_valid):
                    for i in range(0, 7):
                        assert (yield dut.o[i]) == data_old[i]
        # When 17<=t<=21:
        # - For serial-out: output (bit 0 to 4) should correspond to the second data value
        # - For serial-in: output is invalid; bit 4 is the newest bit shifted in
        if t in range(17, 22):
            if is_p2s:
                assert (yield dut.o) == data_new[t-17]
            elif is_s2p:
                assert not (yield dut.o_valid)
        # When 22<=t<=24:
        # - For serial-out: although the first value has been inputted at t=22, the output (bit 5 to 7) should still correspond to the second data value, since it hasn't been fully shifted out
        # - For serial-in:
        #   - When t=22: new value gets flipped back to the original one starting at t=22, so bit 5 from the original value has been shifted in
        #   - When t=23: bit 6 from the original value has been shifted in
        #   - When t=24: bit 7 has been shifted in so output is valid and should correspond to: bits 0 to 4 of the second value, and bits 5 to 7 of the first value
        if t in range(22, 25):
            if is_p2s:
                assert (yield dut.o) == data_new[t-22+5]
            elif is_s2p:
                assert (not (yield dut.o_valid)) != (t == 24)
                if (yield dut.o_valid):
                    for i in range(0, 5):
                        assert (yield dut.o[i]) == data_new[i]
                    for i in range(5, 7):
                        assert (yield dut.o[i]) == data_old[i]
        # When t = 25:
        # - For serial-out: output (bit 0) should correspond to the first value
        # - For serial-in: output is invalid
        if t == 25:
            if is_p2s:
                assert (yield dut.o) == data_old[t-25]
            elif is_s2p:
                assert not (yield dut.o_valid)
        yield
        # For serial-in: always update the "next bit" index
        next_ind = (next_ind + 1) % 8


if __name__ == "__main__":
    print("\n** Parallel-in, Serial-out SR Test **")
    dut = SimpleShiftRegister_ParallelToSerial()
    run_simulation(dut, flipping_test(dut, 0b10101010), vcd_name="sr1_p2s.vcd")
    print("\n** Serial-in, Parallel-out SR Test **")
    dut = SimpleShiftRegister_SerialToParallel()
    run_simulation(dut, flipping_test(dut, 0b01010101), vcd_name="sr1_s2p.vcd")
