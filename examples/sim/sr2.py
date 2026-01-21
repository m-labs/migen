from migen import *


class ShiftRegisterWithEnableStrobes(Module):
    """Base implementation of a shift-right register with enable strobes.

    The input enable (`ie`) strobe controls whether or not the input data will be shifted in at the next clock cycle. If the buffer has been filled, the new data value will replace the last value currently residing in the register.

    The output enable (`oe`) strobe controls whether or not the output data will be shifted out at the next clock cycle. Thus, the output is valid 1 clock cycle after `oe` is asserted.

    The inner shift register (`sr`) has the size of (input width + data width). This register contains a buffer, which allows storing a new data value while shifting out the current data. At all times, `sr` needs to store exactly 1 whole data and all bits of the data to be shifted out.
    """
    def __init__(self, data_width, input_width, output_width):
        assert data_width >= input_width
        assert data_width >= output_width

        self.i = Signal(input_width)
        self.ie = Signal()
        self.o = Signal(output_width)
        self.oe = Signal()

        self._sr       = sr       = Signal(input_width + data_width)
        self._counter  = counter  = Signal(max=data_width+1, reset=input_width)
        self._mask     = mask     = Signal(data_width)
        init_oe = Signal()

        self.comb += mask.eq((1 << (data_width - counter)) - 1)

        self.sync += [
            sr.eq(
                Mux(self.ie, 
                    self.i << (data_width - counter), 
                    (sr >> self.oe) & ~mask)
                | ((sr >> self.oe) & mask)
            ),
            If(self.oe,
                init_oe.eq(1),
                If((init_oe) & (counter < input_width),
                    counter.eq(counter + 1)
                ).Else(
                    counter.eq(1)
                )
            )
        ]
        self.comb += self.o.eq(sr[:output_width])


class ShiftRegisterWithEnableStrobes_ParallelToSerial(ShiftRegisterWithEnableStrobes):
    """A parallel-to-serial shift-right register with a buffer.

    When input enable is high, in the next clock cycle the new value of all bits are stored in the buffer. The data to be shifted out (or being shifted out) will not be replaced with the new data.

    When output enable is high, in the next clock cycle each bit of the value in the buffer is shifted out, LSB first. The serial output is valid 1 clock cycle after `oe` is high. There is no padding between data or irrelevant bit at the output as long as `oe` is asserted.
    """
    def __init__(self, data_width=8):
        super().__init__(data_width=data_width, input_width=data_width, output_width=1)


class ShiftRegisterWithEnableStrobes_SerialToParallel(ShiftRegisterWithEnableStrobes):
    """A serial-to-parallel shift-right register with a buffer.

    When input enable is high, in the next clock cycle the LSB of the new value will stored in the buffer. The data to be shifted out (or being shifted out) will not be replaced with the new data.

    When output enable is high, in the next clock cycle each bit of the value in the buffer is shifted out, LSB first. The parallel output begins to be populated 1 clock cycle after `oe` is high, but the whole data has been shifted out only in the same clock cycle as the output valid (`o_valid`) strobe becomes high.
    """
    def __init__(self, data_width=8):
        super().__init__(data_width=data_width, input_width=1, output_width=data_width)
        self.o_valid = Signal()

        oe_counter = Signal(max=data_width, reset=0)
        oe_d       = Signal()

        self.sync += [
            If(self.oe,
                If(oe_counter == 0, oe_counter.eq(data_width - 1))
                .Else(oe_counter.eq(oe_counter - 1))
            ),
            oe_d.eq(self.oe)
        ]
        self.comb += self.o_valid.eq((oe_counter == 0) & ~(~oe_d & self.ie))


def flipping_test(dut, init_value):
    assert init_value <= 0b11111111

    is_p2s = isinstance(dut, ShiftRegisterWithEnableStrobes_ParallelToSerial)
    is_s2p = isinstance(dut, ShiftRegisterWithEnableStrobes_SerialToParallel)

    init_value_flipped = ~init_value & 0b11111111
    data = [(init_value >> i) & 1 for i in range(8)]
    data_old = data[:]
    # For serial-in test: store the "next bit" index
    next_ind = 0

    # Assume t is a timer with a reset of 0
    for t in range(26):
        # Enable output when t in [1,6], [9,10], [11,15] or [19, 21]
        if t in (
            *[i for i in range(0, 6)], *[i for i in range(8, 15)], 
            *[i for i in range(18, 21)]):
            yield dut.oe.eq(1)
        else:
            yield dut.oe.eq(0)
        # Flip the bits when t=5
        if t == 4:
            data = [(init_value_flipped >> i) & 1 for i in range(8)]
        # For parallel-in: 
        # - Enable input when t=1 or 5
        # - Assign input with all data bits as input all the time
        # - After t=5, input remains unchanged while input is disabled
        if is_p2s:
            if t in (0, 4):
                yield dut.ie.eq(1)
            else:
                yield dut.ie.eq(0)
            for ind in range(8):
                yield dut.i[ind].eq(data[ind])
        # For serial-in: 
        # - Enable input all the time
        # - Move the next bit of the up-to-date data into the input; stop moving in only when output is disabled
        elif is_s2p:
            yield dut.ie.eq(1)
            yield dut.i.eq(data[next_ind])
        # Print the output for each cycle
        if is_p2s:
            print("t={:>2} : i(e={}) == {}{}{}{}{}{}{}{}, o(e={}) == {}"
                .format(t, (yield dut.ie),
                    (yield dut.i[7]), (yield dut.i[6]), (yield dut.i[5]), 
                    (yield dut.i[4]), (yield dut.i[3]), (yield dut.i[2]), 
                    (yield dut.i[1]), (yield dut.i[0]), 
                    (yield dut.oe), (yield dut.o)),
                ("[input = {:08b}]".format(init_value) if t == 1 else 
                "[input = {:08b}]".format(init_value_flipped) if t == 5 else 
                "[output = {:08b}]".format(init_value) if t == 11 else
                "[output = {:08b}]".format(init_value_flipped) if t == 22 else
                "[begin ie=0]" if t == 6 else
                "[reset]" if t == 0 else ""))
        elif is_s2p:
            print("t={:>2} : i(e={}) == {}, o(e={}, valid={}) == {}{}{}{}{}{}{}{}"
                .format(t, (yield dut.ie), (yield dut.i),
                    (yield dut.oe), (yield dut.o_valid), 
                    (yield dut.o[7]), (yield dut.o[6]), (yield dut.o[5]), 
                    (yield dut.o[4]), (yield dut.o[3]), (yield dut.o[2]), 
                    (yield dut.o[1]), (yield dut.o[0])),
                ("[input = ....{:04b}]".format(init_value & 0b1111) if t == 1 else 
                "[input = {:04b}....]".format(init_value_flipped >> 4) if t == 5 else 
                "[valid output]" if t in (11, 22) else
                "[continue >> data while oe=0]" if t == 21 else
                "[reset]" if t == 0 else ""))
        # When 2<=t<=5:
        # - For serial-out: output (bit 0 to 3) should correspond to the first data value
        # - For serial-in: input is incomplete (bit 3 is the newest bit shifted in)
        if t in range(2, 5):
            if is_p2s:
                assert (yield dut.o) == data_old[t-2]
            elif is_s2p:
                assert not (yield dut.o_valid)
        # When 6<=t<=7:
        # - For serial-out: although the second value has been inputted at t=6, the output (bit 4 to 5) should still correspond to the first data value, since it hasn't been fully shifted out
        # - For serial-in: while input is incomplete:
        #   - When t=6: original value becomes flipped starting at t=5, so bit 4 from the new value has been shifted in
        #   - When t=7: bit 5 from the new value has been shifted in
        if t in range(6, 8):
            if is_p2s:
                assert (yield dut.o) == data_old[t-6]
            elif is_s2p:
                assert not (yield dut.o_valid)
        # When 8<=t<=9:
        # - For serial-out: since output is disabled, output should be kept as if t=7 (i.e. equal to bit 5)
        # - For serial-in: while the input remains incomplete, since input enable is kept high while no data gets shifted out, bit 5 of the incomplete input gets replaced with the input value shifted in from 1 clock cycle before (i.e. 0 and 0 from t=7 to 8)
        if t in range(8, 10):
            if is_p2s:
                assert (yield dut.o) == data_old[5]
            elif is_s2p:
                assert not (yield dut.o_valid)
        # When 10<=t<=11:
        # - For serial-out: output (bit 6 to 7) should correspond to the first data value, since it hasn't been fully shifted out
        # - For serial-in:
        #   - When t=10, input is incomplete (only shifted in bit 6)
        #   - When t=11, input is complete, output should correspond to: bits 0 to 3 of the first value, and bits 4 to 7 of the second value
        if t in range(10, 12):
            if is_p2s:
                assert (yield dut.o) == data_old[t-10 + 6]
            elif is_s2p:
                assert (not (yield dut.o_valid)) != (t == 11)
                if (yield dut.o_valid):
                    for i in range(0, 4):
                        assert (yield dut.o[i]) == data_old[i]
                    for i in range(4, 7):
                        assert (yield dut.o[i]) == data[i]
        # When 12<=t<=16:
        # - For serial-out: output (bit 0 to 4) should correspond to the second data value (flipped from the first value)
        # - For serial-in: input is incomplete (bit 4 is the newest bit shifted in)
        if t in range(12, 17):
            if is_p2s:
                assert (yield dut.o) == data[t-12]
            elif is_s2p:
                assert not (yield dut.o_valid)
        # When 17<=t<=19:
        # - For serial-out: since output is disabled, output should be kept as if t=16 (i.e. equal to bit 4)
        # - For serial-in: while the input remains incomplete, since input enable is kept high while no data gets shifted out, bit 4 of the incomplete input gets replaced with the input value shifted in from 1 clock cycle before (i.e. 0); this value is kept until output enable becomes high again at t=9
        if t in range(17, 20):
            if is_p2s:
                assert (yield dut.o) == data[4]
            elif is_s2p:
                assert not (yield dut.o_valid)
        # When 20<=t<=22:
        # - For serial-out: output (bit 5 to 7) should correspond to the second data value, since it hasn't been fully shifted out
        # - For serial-in: 
        #   - When 20<=t=21, input is incomplete (only shifted in bits 5 to 6)
        #   - When t=22, input is complete, all output bits should correspond to the second value
        if t in range(20, 23):
            if is_p2s:
                assert (yield dut.o) == data[t-20 + 5]
            elif is_s2p:
                assert (not (yield dut.o_valid)) != (t == 22)
                if (yield dut.o_valid):
                    for i in range(0, 7):
                        assert (yield dut.o[i]) == data[i]
        # When t >= 23:
        # - For serial-out: since no data is inputed, the output should be 0
        # - For serial-in: 
        #   - Since input enable is high while output has been disabled, the input value from 1 clock cycle before will keep replacing bit 7 (the MSB of the data shifted out)
        #   - Thus, the output is no longer valid.
        if t >= 23:
            if is_p2s:
                assert (yield dut.o) == 0
            elif is_s2p:
                assert not (yield dut.o_valid)
        yield
        # For serial-in: always update the "next bit" index unless output is to be disabled in the next clock cycle, or when t>=21
        if t in (
            *[i for i in range(0, 5)], *[i for i in range(7, 14)], 
            *[i for i in range(17, 20)], *[i for i in range(20, 26)]):
            next_ind = (next_ind + 1) % 8


if __name__ == "__main__":
    print("\n** Parallel-in, Serial-out SR Test **")
    dut = ShiftRegisterWithEnableStrobes_ParallelToSerial()
    run_simulation(dut, flipping_test(dut, 0b10101010), vcd_name="sr2_p2s.vcd")
    print("\n** Serial-in, Parallel-out SR Test **")
    dut = ShiftRegisterWithEnableStrobes_SerialToParallel()
    run_simulation(dut, flipping_test(dut, 0b01010101), vcd_name="sr2_s2p.vcd")
